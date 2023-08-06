[![](https://img.shields.io/pypi/v/foliantcontrib.templateparser.svg)](https://pypi.org/project/foliantcontrib.templateparser/)  [![](https://img.shields.io/github/v/tag/foliant-docs/foliantcontrib.templateparser.svg?label=GitHub)](https://github.com/foliant-docs/foliantcontrib.templateparser)

# TemplateParser preprocessor for Foliant

Preprocessor which allows to use templates in Foliant source files. Preprocessor now supports only [Jinja2](http://jinja.pocoo.org/) templating engine, but more can be added easily.

## Installation

```bash
$ pip install foliantcontrib.templateparser
```

## Config

All params that are stated in foliant.yml are considered global params. All of them may be overriden in template tag options, which have higher priority.

```yaml
preprocessors:
    - templateparser:
        engine: jinja2
        engine_params:
            root: '/usr/src/app'
        context:
            param1: 1008
            param2: 'Kittens'
        ext_context: context.yml
        param3: 'Puppies'
```

`engine`
:   name of the template engine which will be used to process template. Supported engines right now: `jinja2`.

`engine_params`
:   dictionary with parameters which will be transfered to the template engine.

`context`
:   dictionary with variables which will be redirected to the template.

`ext_context`
:   path to YAML- or JSON-file with context dictionary. (relative to current md-file), or URL to such file on the remote server.

_All parameters with other names are also transfered to the template, as if they appeared inside the `context` dictionary. (`param3` in the above example)_

> Please note that even if this may seem convenient, it is preferred to include template variables in the `context` dictionary, as in future more reserved parameters may be added which may conflict with your stray variables.

If some variable names overlap among these methods to supply context, preprocessor uses this priority order:

1. Context dictionary.
2. Stray variables.
3. External context file.

## Usage

To use the template in a Markdown file just insert a tag of the template engine name, for example:

```html
This is ordinary markdown text.
<jinja2>
This is a Jinja2 template:
I can count to five!
{% for i in range(5) %}{{ i + 1 }}{% endfor %}
</jinja2>
```

After making a document with Foliant this will be transformed to:

```
This is ordinary markdown text.

This is a Jinja2 template:
I can count to five!
12345
```

You can also use a general `<template>` tag, but in this case you have to specify the engine you want to use in the `engine` parameter:

```html
This is ordinary markdown text.
<template engine="jinja2">
This is a Jinja2 template:
I can count to five!
{% for i in range(5) %}{{ i + 1 }}{% endfor %}
</template>
```

### Sending variables to template

To send a variable to template, add them into the `context` option. This option accepts `yaml` dictionary format.

```html
<jinja2 context="{'name': Andy, 'age': 8}">
Hi, my name is {{name}}!
I am {{ age }} years old.
{% for prev in range(age - 1, 0, -1) %}
The year before I was {{prev}} years old.
{% endfor %}
</jinja2>
```

Result:

```
Hi, my name is Andy!
I am 8 years old.

The year before I was 7 years old.

The year before I was 6 years old.

The year before I was 5 years old.

The year before I was 4 years old.

The year before I was 3 years old.

The year before I was 2 years old.

The year before I was 1 years old.
```

Also, you can supply a yaml-file with variables in an `ext_context` parameter:

```
<jinja2 ext_context="swagger.yaml">
Swagger file version: {{ swagger }}
Base path: {{ base_path }}
...
</jinja2>
```

### Built-in variables

There are some variables that are available in your template by default:

- `_foliant_context` — dictionary with all user-defined variables, from tag parameters, `context` or `ext_context` variables,
- `_foliant_vars` — dictionary with all variables mentioned below (in case of name collisions),
- `meta` — dictionary with current chapter's metadata, details in the next chapter,
- `meta_object` — project's meta object, details in the next chapter,
- `config` — Foliant project config,
- `target` — current target,
- `backend` — current backend.

### Integration with metadata

Templates support latest Foliant [metadata](https://foliant-docs.github.io/docs/cli/meta/) functionality. You can find the meta dictionary for current section under `meta` variable inside template:

```html
<meta status="ready" title="Custom Title" author="John"></meta>

<jinja2>
Document status: {{ meta.status }}

The document "{{ meta.title }}" is brought to you by {{ meta.author }}
</jinja2>
```

Result:

```html
Document status: ready

The document "Custom Title" is brought to you by John
```

You can also find the whole project's `Meta` object under `meta_object` variable inside template:

```html
<meta status="ready" title="Custom Title" author="John"></meta>

<jinja2>
List of chapters in this project:
{% for chapter in meta_object.chapters %}
* {{ chapter.name }}
{%- endfor %}
</jinja2>
```

Result:

```html
List of chapters in this project:

* index
* sub
* auth
```

### Extends and includes

Extends and includes work in templates. The path of the extending\\included file is relative to the Markdown file where the template lives.

In Jinja2 engine you can override the path of the included\\extended files with `root` engine_param. **Note that this param is relative to project root.**

### Pro tips

**Pro tip #1**

All context variables are also available in the `_foliant_context` dictionary. It may be handy if you don't know at design-time which key names are supplied in the external context file:

```
<jinja2 ext_context="customers.yml">
{% for name, data in _foliant_context.items() %}

# Customer {{ name }}

Purchase: {{ data['purchase'] }}
Order id: {{ data['order_id'] }}

{% endfor %}
</jinja2>
```

**Pro tip #2**

If your context file is inside private git repository, you can utilize the power of [Includes](https://foliant-docs.github.io/docs/preprocessors/includes/) preprocessor to retrieve it.

1. Create a file in your `src` dir, for example, `context.md` (`md` extension is obligatory, includes only process markdown files).
2. Add an includes tag:

**&lt;include repo_url="https://my_login:my_password@my.git.org/my_repo.git" path="path/to/file.yml"></include>**

3. And supply path to this file in your `ext_context` param:

```
<jinja2 ext_context="context.md">
```

**Pro tip #3**

If data inside your external context file is not a dictionary, it will be available inside template under `context` variable (or `_foliant_context['context']`).
