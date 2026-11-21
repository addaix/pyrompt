# pyrompt.engines.mustache_engine

Mustache template engine.

Logic-less templates with sections and partials.

### Classes

| [`MustacheEngine`](#pyrompt.engines.mustache_engine.MustacheEngine)()   | Mustache template engine.   |
|---------------------------------------------------------------------|-----------------------------|

### *class* pyrompt.engines.mustache_engine.MustacheEngine

Bases: [`TemplateEngine`](pyrompt.engines.html.md#pyrompt.engines.TemplateEngine)

Mustache template engine.

Syntax: {{variable}}, {{#section}}, {{^inverted}}, {{!comment}}
Logic-less templating for cross-platform compatibility.

### Examples

```pycon
>>> # Requires pystache installed
>>> engine = MustacheEngine()
>>> template = "Hello {{name}}!"
>>> engine.render(template, name="Alice")
'Hello Alice!'
>>> template = "{{#premium}}Thank you!{{/premium}}"
>>> engine.render(template, premium=True)
'Thank you!'
```

#### detect(content)

Detect Mustache by {{var}} without spaces.

Distinguishes from Jinja2 by lack of spaces: {{var}} vs {{ var }}.

* **Parameters:**
  **content** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Template content
* **Return type:**
  [`bool`](https://docs.python.org/3/builtins/functions.html#bool)
* **Returns:**
  True if content appears to use Mustache syntax

#### parse_template(template_str)

Parse Mustache template for variables.

Extracts variable names from {{var}} and {{#section}} tags.

* **Parameters:**
  **template_str** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Template content
* **Return type:**
  [`dict`](https://docs.python.org/3/builtins/stdtypes.html#dict)
* **Returns:**
  dict with ‘placeholders’, ‘defaults’, ‘metadata’

#### render(template_str, \*\*kwargs)

Render Mustache template.

* **Parameters:**
  * **template_str** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Template content
  * **\*\*kwargs** – Values to inject
* **Return type:**
  [`str`](https://docs.python.org/3/builtins/stdtypes.html#str)
* **Returns:**
  Rendered string
