# pyrompt.engines.jinja2_engine

Jinja2 template engine.

Provides rich templating with conditionals, loops, and filters.

### Classes

| [`Jinja2Engine`](#pyrompt.engines.jinja2_engine.Jinja2Engine)()   | Jinja2 template engine.   |
|-------------------------------------------------------------------|---------------------------|

### *class* pyrompt.engines.jinja2_engine.Jinja2Engine

Bases: [`TemplateEngine`](pyrompt.engines.html.md#pyrompt.engines.TemplateEngine)

Jinja2 template engine.

Syntax: {{ variable }}, {% if %}, {% for %}, etc.
Supports filters: {{ name|default(‘friend’) }}

### Examples

```pycon
>>> # Requires jinja2 installed
>>> engine = Jinja2Engine()
>>> template = "Hello {{ name|default('friend') }}!"
>>> engine.render(template, name="Alice")
'Hello Alice!'
>>> engine.render(template)
'Hello friend!'
```

#### detect(content)

Detect Jinja2 by {{ }} and {% %}.

* **Parameters:**
  **content** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Template content
* **Return type:**
  [`bool`](https://docs.python.org/3/builtins/functions.html#bool)
* **Returns:**
  True if content appears to use Jinja2 syntax

#### parse_template(template_str)

Parse Jinja2 template to extract variables.

Uses Jinja2’s meta.find_undeclared_variables().

* **Parameters:**
  **template_str** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Template content
* **Return type:**
  [`dict`](https://docs.python.org/3/builtins/stdtypes.html#dict)
* **Returns:**
  dict with ‘placeholders’, ‘defaults’, ‘metadata’

#### render(template_str, \*\*kwargs)

Render Jinja2 template.

* **Parameters:**
  * **template_str** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Template content
  * **\*\*kwargs** – Values to inject
* **Return type:**
  [`str`](https://docs.python.org/3/builtins/stdtypes.html#str)
* **Returns:**
  Rendered string
* **Raises:**
  **jinja2.TemplateError** – If template has errors
