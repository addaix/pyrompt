# pyrompt.base

Core collection classes for prompts and templates.

Provides PromptCollection and TemplateCollection with MutableMapping interfaces.

### Classes

| [`PromptCollection`](#pyrompt.base.PromptCollection)(collection_name, \*[, ...])   | Collection of prompts with MutableMapping interface.   |
|-------------------------------------------------------------------------------------------------|--------------------------------------------------------|
| [`TemplateCollection`](#pyrompt.base.TemplateCollection)(collection_name, \*[, ...]) | Collection of templates with multi-engine support.     |

### *class* pyrompt.base.PromptCollection(collection_name, , base_path=None, with_metadata=False, store_factory=None)

Bases: [`MutableMapping`](https://docs.python.org/3/library/collections.abc.html#collections.abc.MutableMapping)

Collection of prompts with MutableMapping interface.

Backed by file storage via dol, with optional metadata.

### Examples

```pycon
>>> import tempfile
>>> prompts = PromptCollection('my_project', base_path=tempfile.mkdtemp())
>>> prompts['system'] = "You are a helpful assistant."
>>> print(prompts['system'])
You are a helpful assistant.
>>> len(prompts)
1
```

### *class* pyrompt.base.TemplateCollection(collection_name, , base_path=None, with_metadata=False, default_engine='format')

Bases: [`MutableMapping`](https://docs.python.org/3/library/collections.abc.html#collections.abc.MutableMapping)

Collection of templates with multi-engine support.

Automatically detects template engine based on file extension
or content. Provides rendering capabilities.

### Examples

```pycon
>>> import tempfile
>>> templates = TemplateCollection('my_project', base_path=tempfile.mkdtemp())
>>> templates['greeting.txt'] = "Hello {name}!"
>>> templates.render('greeting.txt', name='Alice')
'Hello Alice!'
>>> # With Jinja2 (if installed)
>>> templates['greeting.jinja2'] = "Hello {{ name }}!"
>>> templates.render('greeting.jinja2', name='Bob')
'Hello Bob!'
```

#### create_prompt_functions(keys=None, \*\*common_kwargs)

Create an `aix.PromptFuncs` collection from templates (one function per key).

LLM generation routes through `aix` (lazy import).

* **Parameters:**
  * **keys** ([`Optional`](https://docs.python.org/3/library/typing.html#typing.Optional)[[`List`](https://docs.python.org/3/library/typing.html#typing.List)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str)]]) – Template keys to include (None = all)
  * **\*\*common_kwargs** – Common kwargs for all prompt functions (e.g. ‘model’)
* **Returns:**
  `aix.PromptFuncs` object with a function for each template

### Example

```pycon
>>> import tempfile
>>> from pyrompt import TemplateCollection
>>> tc = TemplateCollection('demo', base_path=tempfile.mkdtemp())
>>> tc['greeting.txt'] = "Greet {name}"
>>> funcs = tc.create_prompt_functions()
>>> funcs['greeting.txt'](name='Alice')
'Hello Alice!'
```

#### parse(key)

Parse a template to extract structure.

Returns dict with placeholders, defaults, metadata.

* **Parameters:**
  **key** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Template key
* **Return type:**
  [`dict`](https://docs.python.org/3/builtins/stdtypes.html#dict)
* **Returns:**
  Dict with ‘placeholders’, ‘defaults’, ‘metadata’

### Example

```pycon
>>> import tempfile
>>> templates = TemplateCollection('demo', base_path=tempfile.mkdtemp())
>>> templates['greeting.txt'] = "Hello {name}!"
>>> info = templates.parse('greeting.txt')
>>> info['placeholders']
['name']
```

#### render(key, \*\*kwargs)

Render a template with provided values.

* **Parameters:**
  * **key** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Template key
  * **\*\*kwargs** – Values to inject
* **Return type:**
  [`str`](https://docs.python.org/3/builtins/stdtypes.html#str)
* **Returns:**
  Rendered template string

### Example

```pycon
>>> import tempfile
>>> templates = TemplateCollection('demo', base_path=tempfile.mkdtemp())
>>> templates['greeting.txt'] = "Hello {name}!"
>>> templates.render('greeting.txt', name='Alice')
'Hello Alice!'
```

#### to_prompt_function(key, \*\*prompt_func_kwargs)

Convert template to an AI-enabled function using `aix.prompt_func`.

LLM generation is routed through `aix` (the multi-provider facade) so the
model/provider is switchable. `aix` is imported lazily, only when called.

* **Parameters:**
  * **key** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Template key
  * **\*\*prompt_func_kwargs** – Additional kwargs for `aix.prompt_func`
    (e.g., ‘model’, ‘temperature’, ‘name’)
* **Returns:**
  Callable function that invokes the LLM with the rendered template

### Example

```pycon
>>> import tempfile
>>> from pyrompt import TemplateCollection
>>> tc = TemplateCollection('demo', base_path=tempfile.mkdtemp())
>>> tc['explain.txt'] = "Explain {concept} in simple terms."
>>> explain = tc.to_prompt_function('explain.txt')
>>> explain(concept="quantum computing")
'Quantum computing is ...'
```

#### to_prompt_json_function(key, json_schema, \*\*prompt_func_kwargs)

Convert template to a JSON-returning AI function.

Uses `aix.prompt_func(output_schema=dict)`: aix requests JSON and parses it
robustly (tolerating fenced output), returning a parsed dict. `json_schema` is
accepted for API compatibility; aix does best-effort JSON rather than strict
JSON-Schema enforcement. LLM generation routes through `aix` (lazy import).

* **Parameters:**
  * **key** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Template key
  * **json_schema** ([`dict`](https://docs.python.org/3/builtins/stdtypes.html#dict)) – Desired JSON schema (kept for API compatibility)
  * **\*\*prompt_func_kwargs** – Additional kwargs for `aix.prompt_func`
* **Returns:**
  Function that returns a parsed JSON dict

### Example

```pycon
>>> import tempfile
>>> from pyrompt import TemplateCollection
>>> tc = TemplateCollection('demo', base_path=tempfile.mkdtemp())
>>> tc['extract.txt'] = "Extract people from: {text}"
>>> extract = tc.to_prompt_json_function('extract.txt', {})
>>> extract(text="Alice met Bob")
{'people': ['Alice', 'Bob']}
```
