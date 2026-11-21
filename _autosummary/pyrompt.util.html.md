# pyrompt.util

Utility functions and convenience helpers for pyrompt.

### Functions

| [`quick_setup`](#pyrompt.util.quick_setup)(project_name[, with_templates, ...])   | Quick setup for a new pyrompt project.                     |
|-----------------------------------------------------------------------------------------------------|------------------------------------------------------------|
| [`import_from_dict`](#pyrompt.util.import_from_dict)(collection, prompts[, metadata])  | Import prompts from a dictionary.                          |
| [`export_to_dict`](#pyrompt.util.export_to_dict)(collection[, include_metadata])     | Export collection to a dictionary.                         |
| [`validate_template`](#pyrompt.util.validate_template)(template_str[, ...])             | Validate a template string.                                |
| [`merge_collections`](#pyrompt.util.merge_collections)(target, \*sources[, ...])        | Merge multiple collections into a target collection.       |
| [`list_available_engines`](#pyrompt.util.list_available_engines)()                           | List all available template engines with their details.    |
| [`render_template_file`](#pyrompt.util.render_template_file)(file_path[, output_path])     | Render a template file directly.                           |
| [`create_project_structure`](#pyrompt.util.create_project_structure)(project_name[, ...])      | Create a complete project structure for prompt management. |
| [`get_stats`](#pyrompt.util.get_stats)(collection)                              | Get statistics about a collection.                         |

### pyrompt.util.create_project_structure(project_name, base_path=None, include_examples=True)

Create a complete project structure for prompt management.

Creates directories and example files for a new pyrompt project.

* **Parameters:**
  * **project_name** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Name of the project
  * **base_path** ([`Optional`](https://docs.python.org/3/library/typing.html#typing.Optional)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str)]) – Optional base path
  * **include_examples** ([`bool`](https://docs.python.org/3/builtins/functions.html#bool)) – Whether to include example prompts
* **Return type:**
  [`str`](https://docs.python.org/3/builtins/stdtypes.html#str)
* **Returns:**
  Path to created project directory

### Example

```pycon
>>> path = create_project_structure('my_ai_app')
>>> print(f"Project created at: {path}")
```

### pyrompt.util.export_to_dict(collection, include_metadata=True)

Export collection to a dictionary.

* **Parameters:**
  * **collection** – PromptCollection or TemplateCollection
  * **include_metadata** ([`bool`](https://docs.python.org/3/builtins/functions.html#bool)) – Whether to include metadata
* **Return type:**
  [`Dict`](https://docs.python.org/3/library/typing.html#typing.Dict)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str), [`Any`](https://docs.python.org/3/library/typing.html#typing.Any)]
* **Returns:**
  Dict with ‘prompts’ and optionally ‘metadata’ keys

### Example

```pycon
>>> import tempfile
>>> from pyrompt import PromptCollection
>>> prompts = PromptCollection('my_project', base_path=tempfile.mkdtemp())
>>> prompts['system'] = 'You are helpful.'
>>> export_to_dict(prompts, include_metadata=False)
{'prompts': {'system': 'You are helpful.'}}
```

### pyrompt.util.get_stats(collection)

Get statistics about a collection.

* **Parameters:**
  **collection** – PromptCollection or TemplateCollection
* **Return type:**
  [`Dict`](https://docs.python.org/3/library/typing.html#typing.Dict)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str), [`Any`](https://docs.python.org/3/library/typing.html#typing.Any)]
* **Returns:**
  Dict with statistics

### Example

```pycon
>>> import tempfile
>>> from pyrompt import PromptCollection
>>> prompts = PromptCollection('my_project', base_path=tempfile.mkdtemp())
>>> get_stats(prompts)['total_prompts']
0
```

### pyrompt.util.import_from_dict(collection, prompts, metadata=None)

Import prompts from a dictionary.

* **Parameters:**
  * **collection** – PromptCollection or TemplateCollection
  * **prompts** ([`Dict`](https://docs.python.org/3/library/typing.html#typing.Dict)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str), [`str`](https://docs.python.org/3/builtins/stdtypes.html#str)]) – Dict mapping keys to prompt/template strings
  * **metadata** ([`Optional`](https://docs.python.org/3/library/typing.html#typing.Optional)[[`Dict`](https://docs.python.org/3/library/typing.html#typing.Dict)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str), [`dict`](https://docs.python.org/3/builtins/stdtypes.html#dict)]]) – Optional dict mapping keys to metadata dicts

### Example

```pycon
>>> import tempfile
>>> from pyrompt import PromptCollection
>>> prompts = PromptCollection('my_project', base_path=tempfile.mkdtemp())
>>> import_from_dict(prompts, {'system': 'You are helpful.', 'user': 'Hello!'})
>>> sorted(prompts)
['system', 'user']
```

### pyrompt.util.list_available_engines()

List all available template engines with their details.

* **Return type:**
  [`Dict`](https://docs.python.org/3/library/typing.html#typing.Dict)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str), [`Dict`](https://docs.python.org/3/library/typing.html#typing.Dict)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str), [`Any`](https://docs.python.org/3/library/typing.html#typing.Any)]]
* **Returns:**
  Dict mapping engine name to info dict

### Example

```pycon
>>> engines = list_available_engines()
>>> print(engines['format']['extensions'])
['.txt', '']
```

### pyrompt.util.merge_collections(target, \*sources, conflict_strategy='skip')

Merge multiple collections into a target collection.

* **Parameters:**
  * **target** – Target collection to merge into
  * **\*sources** – Source collections to merge from
  * **conflict_strategy** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – How to handle conflicts (‘skip’, ‘overwrite’, ‘error’)

### Example

```pycon
>>> import tempfile
>>> from pyrompt import PromptCollection
>>> base = tempfile.mkdtemp()
>>> target = PromptCollection('merged', base_path=base)
>>> source1 = PromptCollection('source1', base_path=base)
>>> source1['a'] = 'A'
>>> merge_collections(target, source1, conflict_strategy='skip')
>>> sorted(target)
['a']
```

### pyrompt.util.quick_setup(project_name, with_templates=True, with_metadata=False, base_path=None)

Quick setup for a new pyrompt project.

Creates both prompt and template collections with sensible defaults.

* **Parameters:**
  * **project_name** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Name of the project
  * **with_templates** ([`bool`](https://docs.python.org/3/builtins/functions.html#bool)) – Whether to create a template collection
  * **with_metadata** ([`bool`](https://docs.python.org/3/builtins/functions.html#bool)) – Whether to enable metadata
  * **base_path** ([`Optional`](https://docs.python.org/3/library/typing.html#typing.Optional)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str)]) – Optional base path
* **Return type:**
  [`Dict`](https://docs.python.org/3/library/typing.html#typing.Dict)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str), [`Any`](https://docs.python.org/3/library/typing.html#typing.Any)]
* **Returns:**
  Dict with ‘prompts’ and optionally ‘templates’ keys

### Example

```pycon
>>> import tempfile
>>> collections = quick_setup('my_ai_project', base_path=tempfile.mkdtemp())
>>> collections['prompts']['system'] = "You are a helpful assistant."
>>> collections['templates']['greeting.txt'] = "Hello {name}!"
>>> sorted(collections)
['prompts', 'templates']
```

### pyrompt.util.render_template_file(file_path, output_path=None, \*\*kwargs)

Render a template file directly.

* **Parameters:**
  * **file_path** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Path to template file
  * **output_path** ([`Optional`](https://docs.python.org/3/library/typing.html#typing.Optional)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str)]) – Optional path to save rendered output
  * **\*\*kwargs** – Template parameters
* **Return type:**
  [`str`](https://docs.python.org/3/builtins/stdtypes.html#str)
* **Returns:**
  Rendered string

### Example

```pycon
>>> result = render_template_file(
...     'templates/greeting.txt',
...     name='Alice'
... )
```

### pyrompt.util.validate_template(template_str, engine_name='format', required_params=None)

Validate a template string.

* **Parameters:**
  * **template_str** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Template content
  * **engine_name** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Engine to use (‘format’, ‘jinja2’, ‘mustache’)
  * **required_params** ([`Optional`](https://docs.python.org/3/library/typing.html#typing.Optional)[[`List`](https://docs.python.org/3/library/typing.html#typing.List)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str)]]) – Optional list of required parameter names
* **Return type:**
  [`Dict`](https://docs.python.org/3/library/typing.html#typing.Dict)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str), [`Any`](https://docs.python.org/3/library/typing.html#typing.Any)]
* **Returns:**
  Dict with ‘valid’, ‘errors’, ‘warnings’, ‘placeholders’

### Example

```pycon
>>> result = validate_template("Hello {name}!", required_params=['name'])
>>> assert result['valid']
>>> result = validate_template("Hello {name}!", required_params=['name', 'age'])
>>> assert not result['valid']
```
