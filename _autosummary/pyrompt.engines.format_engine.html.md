# pyrompt.engines.format_engine

Python format string template engine.

Supports standard Python format strings with {placeholder} syntax.
Provides extended syntax for defaults: {name:default_value}

### Classes

| [`FormatEngine`](#pyrompt.engines.format_engine.FormatEngine)()   | Python format string engine.   |
|-------------------------------------------------------------------|--------------------------------|

### *class* pyrompt.engines.format_engine.FormatEngine

Bases: [`TemplateEngine`](pyrompt.engines.html.md#pyrompt.engines.TemplateEngine)

Python format string engine.

Syntax: {name} or {name:format_spec}
Extended: {name:default_value} for simple defaults (when not a format spec)

### Examples

```pycon
>>> engine = FormatEngine()
>>> engine.render("Hello {name}!", name="Alice")
'Hello Alice!'
>>> info = engine.parse_template("Hello {name}, you are {age} years old!")
>>> info['placeholders']
['name', 'age']
```

#### detect(content)

Detect format strings by single braces.

* **Parameters:**
  **content** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Template content
* **Return type:**
  [`bool`](https://docs.python.org/3/builtins/functions.html#bool)
* **Returns:**
  True if content appears to use Python format syntax

#### parse_template(template_str)

Extract placeholders from format string.

Uses string.Formatter to parse the template.

* **Parameters:**
  **template_str** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Template content
* **Return type:**
  [`dict`](https://docs.python.org/3/builtins/stdtypes.html#dict)
* **Returns:**
  dict with ‘placeholders’, ‘defaults’, ‘metadata’

#### render(template_str, \*\*kwargs)

Render using str.format().

* **Parameters:**
  * **template_str** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Template content
  * **\*\*kwargs** – Values to inject
* **Return type:**
  [`str`](https://docs.python.org/3/builtins/stdtypes.html#str)
* **Returns:**
  Rendered string
