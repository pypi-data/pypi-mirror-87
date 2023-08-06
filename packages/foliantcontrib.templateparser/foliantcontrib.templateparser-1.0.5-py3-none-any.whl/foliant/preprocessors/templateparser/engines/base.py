from pathlib import Path, PosixPath


class TemplateEngineBase:
    """Base class for template engines"""

    def __init__(self,
                 content: str,  # string with template body;
                 context: dict,  # dictionary with variables which should be redirected to template;
                 params: dict,  # dictionary with template engine params;
                 md_file: PosixPath or str,  # path to the md-file where the template occured.
                 foliant_vars: dict):  # dictionary with foliant variables like meta or target
        self._content = content
        self._context = context
        self._params = params
        self._md_file = Path(md_file)
        self._foliant_vars = foliant_vars

    def build(self):
        """Build template with engine and return resulting string"""
        raise NotImplementedError()
