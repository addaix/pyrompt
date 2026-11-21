# pyrompt.engines

Template engine plugin system for pyrompt.

Provides extensible template engine support with auto-detection.

### Functions

| [`register_engine`](#pyrompt.engines.register_engine)(engine)             | Register a template engine.                |
|--------------------------------------------------------------------------------------|--------------------------------------------|
| [`get_engine`](#pyrompt.engines.get_engine)(name)                    | Get engine by name.                        |
| [`get_engine_by_extension`](#pyrompt.engines.get_engine_by_extension)(extension)  | Get engine that handles a given extension. |
| [`detect_engine`](#pyrompt.engines.detect_engine)(content[, extension]) | Detect appropriate engine for content.     |
| [`list_engines`](#pyrompt.engines.list_engines)()                      | List all registered engine names.          |

### Classes

| [`TemplateEngine`](#pyrompt.engines.TemplateEngine)()   | Abstract base class for template engines.   |
|---------------------------------------------------------------------|---------------------------------------------|

### *class* pyrompt.engines.TemplateEngine

Bases: [`ABC`](https://docs.python.org/3/library/abc.html#abc.ABC)

Abstract base class for template engines.

Template engines parse and render templates with different syntaxes.
They must provide:

- name: Unique identifier (e.g., ‘format’, ‘jinja2’)
- extensions: List of file extensions (e.g., [‘.jinja2’, ‘.j2’])
- parse_template: Extract placeholders and defaults
- render: Render template with values
- detect: Optionally detect if content uses this engine

#### detect(content)

Detect if content uses this engine based on syntax.

Used when extension doesn’t clearly indicate engine.
Override to provide content-based detection.

* **Parameters:**
  **content** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Template content
* **Return type:**
  [`bool`](https://docs.python.org/3/builtins/functions.html#bool)
* **Returns:**
  True if content appears to use this engine

#### *abstractmethod* parse_template(template_str)

Parse template to extract structure.

* **Parameters:**
  **template_str** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Template content
* **Returns:**
  - ‘placeholders’: list of parameter names
  - ’defaults’: dict of default values
  - ’metadata’: any engine-specific info
* **Return type:**
  [`dict`](https://docs.python.org/3/builtins/stdtypes.html#dict)

#### *abstractmethod* render(template_str, \*\*kwargs)

Render template with provided values.

* **Parameters:**
  * **template_str** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Template content
  * **\*\*kwargs** – Values to inject
* **Return type:**
  [`str`](https://docs.python.org/3/builtins/stdtypes.html#str)
* **Returns:**
  Rendered string

### pyrompt.engines.detect_engine(content, extension=None)

Detect appropriate engine for content.

Priority:

1. Extension match (if provided)
2. Content-based detection
3. Default (format)

* **Parameters:**
  * **content** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Template content
  * **extension** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Optional file extension
* **Return type:**
  [`TemplateEngine`](#pyrompt.engines.TemplateEngine)
* **Returns:**
  TemplateEngine instance (never None, falls back to ‘format’)

### pyrompt.engines.get_engine(name)

Get engine by name.

* **Parameters:**
  **name** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Engine name (e.g., ‘format’, ‘jinja2’)
* **Return type:**
  [`Optional`](https://docs.python.org/3/library/typing.html#typing.Optional)[[`TemplateEngine`](#pyrompt.engines.TemplateEngine)]
* **Returns:**
  TemplateEngine instance or None if not found

### pyrompt.engines.get_engine_by_extension(extension)

Get engine that handles a given extension.

* **Parameters:**
  **extension** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – File extension (e.g., ‘.jinja2’)
* **Return type:**
  [`Optional`](https://docs.python.org/3/library/typing.html#typing.Optional)[[`TemplateEngine`](#pyrompt.engines.TemplateEngine)]
* **Returns:**
  TemplateEngine instance or None if not found

### pyrompt.engines.list_engines()

List all registered engine names.

* **Return type:**
  [`List`](https://docs.python.org/3/library/typing.html#typing.List)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str)]
* **Returns:**
  List of engine names

### pyrompt.engines.register_engine(engine)

Register a template engine.

* **Parameters:**
  **engine** ([`TemplateEngine`](#pyrompt.engines.TemplateEngine)) – TemplateEngine instance to register

### Modules

| [`format_engine`](pyrompt.engines.format_engine.html.md#module-pyrompt.engines.format_engine)     | Python format string template engine.   |
|---------------------------------------------------------------------------------------------------------|-----------------------------------------|
| [`jinja2_engine`](pyrompt.engines.jinja2_engine.html.md#module-pyrompt.engines.jinja2_engine)     | Jinja2 template engine.                 |
| [`mustache_engine`](pyrompt.engines.mustache_engine.html.md#module-pyrompt.engines.mustache_engine) | Mustache template engine.               |
