'''
Template parser preprocessor for Foliant.
'''

import pkgutil
import yaml
import urllib

from . import engines
from importlib import import_module

from foliant.meta.generate import load_meta, get_meta_for_chapter
from foliant.preprocessors.utils.combined_options import (Options,
                                                          CombinedOptions,
                                                          validate_in)
from foliant.preprocessors.utils.preprocessor_ext import (BasePreprocessorExt,
                                                          allow_fail)


OptionValue = int or float or bool or str


def get_engines():
    '''
    Get dictionary with available template engines.
    Key - engine name, value - engine class
    '''
    result = {}
    for importer, modname, ispkg in pkgutil.iter_modules(engines.__path__):
        module = import_module(f'foliant.preprocessors.templateparser.engines.{modname}')
        if hasattr(module, 'TemplateEngine'):
            result[modname] = module.TemplateEngine
    return result


class Preprocessor(BasePreprocessorExt):
    defaults = {
        'engine_params': {}
    }
    engines = get_engines()
    tags = ('template', *engines.keys())
    tag_params = ('engine',
                  'context',
                  'ext_context',
                  'engine_params')  # all other params will be redirected to template

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.logger = self.logger.getChild('templateparser')

        self.logger.debug(f'Preprocessor inited: {self.__dict__}')

    def load_external_context(self, path: str, options) -> dict:
        '''
        Load context for template from a yaml-file.
        `path` may be a path to yaml-file relative to current markdown-file or
        a link to file on remote server
        '''
        if path.startswith('http'):
            filename = self.working_dir / f'template_context'
            self.logger.debug(f'Downloading context from {path} ({filename})')
            try:
                urllib.request.urlretrieve(path, filename)
            except (urllib.error.URLError, urllib.error.HTTPError) as e:
                self._warning(f'Cannot retrieve external context over url {path}.',
                              error=e)
                return {}
        else:
            filename = self.current_filepath.parent / options['ext_context']
            if not filename.exists():
                self._warning(f'External context file {path} not found')
                return {}
        result = yaml.load(open(filename, encoding="utf8"), yaml.Loader)
        if isinstance(result, dict):
            return result
        else:
            return {'context': result}

    @allow_fail('Failed to render template.')
    def process_template_tag(self, block) -> str:
        """
        Function for processing tag. Send the contents to the corresponging
        template engine along with parameters from tag and config, and
        <content_file> path. Replace the tag with output from the engine.
        """
        tag_options = Options(self.get_options(block.group('options')),
                              validators={'engine': validate_in(self.engines.keys())})
        options = CombinedOptions({'config': self.options,
                                   'tag': tag_options},
                                  priority='tag')

        tag = block.group('tag')
        if tag == 'template':  # if "template" tag is used — engine must be specified
            if 'engine' not in options:
                self._warning('Engine must be specified in the <template> tag. Skipping.',
                              self.get_tag_context(block))
                return block.group(0)
            engine = self.engines[options['engine']]
        else:
            engine = self.engines[tag]

        current_pos = block.start()
        chapter = get_meta_for_chapter(self.current_filepath)
        section = chapter.get_section_by_offset(current_pos)
        _foliant_vars = {
            'meta': section.data,
            'meta_object': self.meta,
            'config': self.config,
            'target': self.context['target'],
            'backend': self.context['backend'],
            'project_path': self.context['project_path']
        }

        context = {}

        # external context is loaded first, it has lowest priority
        if 'ext_context' in options:
            context.update(self.load_external_context(options['ext_context'], options))

        # all unrecognized params are redirected to template engine params
        context.update({p: options[p] for p in options if p not in self.tag_params})

        # add options from "context" param
        context.update(options.get('context', {}))

        template = engine(block.group('body'),
                          context,
                          options.get('engine_params', {}),
                          self.current_filepath,
                          _foliant_vars)
        return template.build()

    def apply(self):
        self.meta = load_meta(self.config.get('chapters', []))
        self._process_tags_for_all_files(self.process_template_tag)

        self.logger.info('Preprocessor applied')
