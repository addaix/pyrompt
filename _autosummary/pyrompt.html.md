# pyrompt

pyrompt: Python Prompt Management

A flexible framework for managing, sharing, and searching prompts and prompt templates
with support for multiple templating languages and idiomatic Python interfaces.

Quick Start:

```pycon
>>> import tempfile
>>> from pyrompt import PromptCollection, TemplateCollection
>>> _base = tempfile.mkdtemp()
>>> prompts = PromptCollection('my_project', base_path=_base)
>>> templates = TemplateCollection('my_project', base_path=_base)
>>> prompts['system'] = "You are a helpful Python expert."
>>> templates['greeting.txt'] = "Hello, {name}!"
>>> print(templates.render('greeting.txt', name='Alice'))
Hello, Alice!
```

Main Components:

> - PromptCollection: Store and manage prompts
> - TemplateCollection: Store and manage templates with multi-engine support
> - PromptMall: Collection of collections
> - SemanticIndex: Semantic search over prompts
> - GitHubPromptCollection: GitHub-backed collections

### Functions

| [`register_engine`](#pyrompt.register_engine)(engine)                           | Register a template engine.                                |
|----------------------------------------------------------------------------------------------------|------------------------------------------------------------|
| [`get_engine`](#pyrompt.get_engine)(name)                                  | Get engine by name.                                        |
| [`list_engines`](#pyrompt.list_engines)()                                    | List all registered engine names.                          |
| [`detect_engine`](#pyrompt.detect_engine)(content[, extension])               | Detect appropriate engine for content.                     |
| [`discover_prompt_collections`](#pyrompt.discover_prompt_collections)([search_term, ...])   | Discover public \*_pyrompt repositories on GitHub.         |
| [`fork_collection`](#pyrompt.fork_collection)(source, token[, organization])    | Fork a collection to your account or organization.         |
| [`clone_collection`](#pyrompt.clone_collection)(repo, local_path[, token])       | Clone a GitHub collection to local directory.              |
| [`get_default_base_path`](#pyrompt.get_default_base_path)()                           | Get platform-appropriate base path for pyrompt data.       |
| [`quick_setup`](#pyrompt.quick_setup)(project_name[, with_templates, ...])  | Quick setup for a new pyrompt project.                     |
| [`import_from_dict`](#pyrompt.import_from_dict)(collection, prompts[, metadata]) | Import prompts from a dictionary.                          |
| [`export_to_dict`](#pyrompt.export_to_dict)(collection[, include_metadata])    | Export collection to a dictionary.                         |
| [`validate_template`](#pyrompt.validate_template)(template_str[, ...])            | Validate a template string.                                |
| [`merge_collections`](#pyrompt.merge_collections)(target, \*sources[, ...])       | Merge multiple collections into a target collection.       |
| [`list_available_engines`](#pyrompt.list_available_engines)()                          | List all available template engines with their details.    |
| [`render_template_file`](#pyrompt.render_template_file)(file_path[, output_path])    | Render a template file directly.                           |
| [`create_project_structure`](#pyrompt.create_project_structure)(project_name[, ...])     | Create a complete project structure for prompt management. |
| [`get_stats`](#pyrompt.get_stats)(collection)                             | Get statistics about a collection.                         |

### Classes

| [`PromptCollection`](#pyrompt.PromptCollection)(collection_name, \*[, ...])      | Collection of prompts with MutableMapping interface.   |
|----------------------------------------------------------------------------------------------------|--------------------------------------------------------|
| [`TemplateCollection`](#pyrompt.TemplateCollection)(collection_name, \*[, ...])    | Collection of templates with multi-engine support.     |
| [`PromptMall`](#pyrompt.PromptMall)(workspace_name, \*[, base_path, ...])  | Collection of collections - a "mall" of stores.        |
| [`TemplateEngine`](#pyrompt.TemplateEngine)()                                  | Abstract base class for template engines.              |
| [`SemanticIndex`](#pyrompt.SemanticIndex)(collection, \*[, auto_update, ...]) | Semantic search index for prompts/templates.           |
| [`GitHubPromptCollection`](#pyrompt.GitHubPromptCollection)(repo, \*[, token, ...])    | Prompt collection backed by GitHub repository.         |

### *class* pyrompt.GitHubPromptCollection(repo, , token=None, readonly=True, branch='main', local_cache=None, collection_type='prompts')

Bases: [`MutableMapping`](https://docs.python.org/3/library/collections.abc.html#collections.abc.MutableMapping)

Prompt collection backed by GitHub repository.

Repositories must end with ‘_pyrompt’ suffix for discovery.
Contains prompts/ and/or templates/ directories.

### Examples

```pycon
>>> # Publishing a collection
>>> gh = GitHubPromptCollection(
...     repo='username/my_prompts_pyrompt',
...     token='ghp_...',
...     readonly=False
... )
>>> gh['greeting'] = "Hello, {name}!"
>>> gh.sync()  # Commits and pushes to GitHub
```

#### sync(message='Update prompts via pyrompt')

Push local changes to GitHub.

* **Parameters:**
  **message** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Commit message
* **Raises:**
  [**PermissionError**](https://docs.python.org/3/builtins/exceptions.html#PermissionError) – If collection is readonly

### *class* pyrompt.PromptCollection(collection_name, , base_path=None, with_metadata=False, store_factory=None)

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

### *class* pyrompt.PromptMall(workspace_name, , base_path=None, collection_names=None, with_metadata=False)

Bases: [`Mapping`](https://docs.python.org/3/library/collections.abc.html#collections.abc.Mapping)

Collection of collections - a “mall” of stores.

Provides nested access: mall[‘collection_name’][‘prompt_key’]

### Examples

```pycon
>>> mall = PromptMall('my_workspace')
>>> mall['system']['python_expert'] = "You are a Python expert."
>>> mall['templates']['greeting'] = "Hello {name}!"
>>> list(mall.keys())
['system', 'templates']
>>> results = mall.search('python')
```

#### add_collection(name, collection_type='prompt')

Add a new collection to the mall.

* **Parameters:**
  * **name** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Collection name
  * **collection_type** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – ‘prompt’ or ‘template’

### Example

```pycon
>>> mall.add_collection('personas', 'prompt')
>>> mall['personas']['analyst'] = "You are a data analyst."
```

#### get_collection_type(name)

Get the type of a collection.

* **Parameters:**
  **name** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Collection name
* **Return type:**
  [`Optional`](https://docs.python.org/3/library/typing.html#typing.Optional)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str)]
* **Returns:**
  ‘prompt’, ‘template’, or None if not found

#### items()

Get (name, collection) pairs.

#### keys()

Get collection names.

#### remove_collection(name)

Remove a collection from the mall.

#### NOTE
This only removes it from the mall, not from disk.

* **Parameters:**
  **name** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Collection name

#### search(query, collections=None, \*\*search_kwargs)

Search across multiple collections.

* **Parameters:**
  * **query** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Search query
  * **collections** ([`Optional`](https://docs.python.org/3/library/typing.html#typing.Optional)[[`List`](https://docs.python.org/3/library/typing.html#typing.List)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str)]]) – Collection names to search (None = all)
  * **\*\*search_kwargs** – Additional args for SemanticIndex.search
* **Return type:**
  [`Dict`](https://docs.python.org/3/library/typing.html#typing.Dict)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str), [`List`](https://docs.python.org/3/library/typing.html#typing.List)[[`tuple`](https://docs.python.org/3/builtins/stdtypes.html#tuple)]]
* **Returns:**
  Dict mapping collection_name -> search results

### Example

```pycon
>>> results = mall.search('python expert', top_k=3)
>>> for coll_name, matches in results.items():
...     print(f"\n{coll_name}:")
...     for key, score in matches:
...         print(f"  {key}: {score:.3f}")
```

#### values()

Get collections.

### *class* pyrompt.SemanticIndex(collection, , auto_update=False, embedding_model='text-embedding-3-small', batch_size=100)

Bases: [`object`](https://docs.python.org/3/builtins/functions.html#object)

Semantic search index for prompts/templates.

Uses oa.embeddings to create vector representations,
then supports similarity search.

### Examples

```pycon
>>> from pyrompt import PromptCollection, SemanticIndex
>>> prompts = PromptCollection('my_project')
>>> prompts['python'] = "You are a Python expert."
>>> prompts['data'] = "You specialize in data analysis."
>>> index = SemanticIndex(prompts)
>>> results = index.search("help with pandas", top_k=2)
```

#### add(key)

Add single item to index.

* **Parameters:**
  **key** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Key of item to add

#### cluster(n_clusters=5)

Cluster prompts/templates into groups.

* **Parameters:**
  **n_clusters** ([`int`](https://docs.python.org/3/builtins/functions.html#int)) – Number of clusters
* **Returns:**
  Dict mapping cluster_id -> list of keys
* **Raises:**
  [**ImportError**](https://docs.python.org/3/builtins/exceptions.html#ImportError) – If scikit-learn not available

#### rebuild()

Rebuild entire index from current collection.

#### remove(key)

Remove item from index.

* **Parameters:**
  **key** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Key of item to remove

#### search(query, top_k=5, filters=None, diversity_threshold=None)

Search for similar prompts.

* **Parameters:**
  * **query** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Search query text
  * **top_k** ([`int`](https://docs.python.org/3/builtins/functions.html#int)) – Number of results to return
  * **filters** ([`Optional`](https://docs.python.org/3/library/typing.html#typing.Optional)[[`dict`](https://docs.python.org/3/builtins/stdtypes.html#dict)]) – Metadata filters (if collection has metadata)
  * **diversity_threshold** ([`Optional`](https://docs.python.org/3/library/typing.html#typing.Optional)[[`float`](https://docs.python.org/3/builtins/functions.html#float)]) – If set, exclude results too similar to each other
* **Return type:**
  [`List`](https://docs.python.org/3/library/typing.html#typing.List)[[`Tuple`](https://docs.python.org/3/library/typing.html#typing.Tuple)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str), [`float`](https://docs.python.org/3/builtins/functions.html#float)]]
* **Returns:**
  List of (key, similarity_score) tuples, sorted by score descending

### Example

```pycon
>>> results = index.search("help with data analysis", top_k=3)
>>> for key, score in results:
...     print(f"{key}: {score:.3f}")
```

### *class* pyrompt.TemplateCollection(collection_name, , base_path=None, with_metadata=False, default_engine='format')

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

### *class* pyrompt.TemplateEngine

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

### pyrompt.clone_collection(repo, local_path, token=None)

Clone a GitHub collection to local directory.

* **Parameters:**
  * **repo** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Repository name (user/repo_pyrompt)
  * **local_path** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Local directory path
  * **token** ([`Optional`](https://docs.python.org/3/library/typing.html#typing.Optional)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str)]) – Optional GitHub token

### Example

```pycon
>>> clone_collection(
...     'thorwhalen/awesome_prompts_pyrompt',
...     '/tmp/my_prompts'
... )
```

### pyrompt.create_project_structure(project_name, base_path=None, include_examples=True)

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

### pyrompt.detect_engine(content, extension=None)

Detect appropriate engine for content.

Priority:

1. Extension match (if provided)
2. Content-based detection
3. Default (format)

* **Parameters:**
  * **content** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Template content
  * **extension** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Optional file extension
* **Return type:**
  [`TemplateEngine`](pyrompt.engines.html.md#pyrompt.engines.TemplateEngine)
* **Returns:**
  TemplateEngine instance (never None, falls back to ‘format’)

### pyrompt.discover_prompt_collections(search_term=None, min_stars=0, language='Python', max_results=50)

Discover public \*_pyrompt repositories on GitHub.

* **Parameters:**
  * **search_term** ([`Optional`](https://docs.python.org/3/library/typing.html#typing.Optional)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str)]) – Search query (e.g., “python data”)
  * **min_stars** ([`int`](https://docs.python.org/3/builtins/functions.html#int)) – Minimum star count
  * **language** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Programming language filter
  * **max_results** ([`int`](https://docs.python.org/3/builtins/functions.html#int)) – Maximum number of results
* **Return type:**
  [`List`](https://docs.python.org/3/library/typing.html#typing.List)[[`dict`](https://docs.python.org/3/builtins/stdtypes.html#dict)]
* **Returns:**
  List of dicts with repo info (name, description, stars, url)

### Example

```pycon
>>> collections = discover_prompt_collections(
...     search_term='python',
...     min_stars=5
... )
>>> for repo in collections:
...     print(f"{repo['name']}: {repo['stars']} stars")
```

### pyrompt.export_to_dict(collection, include_metadata=True)

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

### pyrompt.fork_collection(source, token, organization=None)

Fork a collection to your account or organization.

* **Parameters:**
  * **source** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Source repo (user/repo_pyrompt)
  * **token** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – GitHub token with repo permissions
  * **organization** ([`Optional`](https://docs.python.org/3/library/typing.html#typing.Optional)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str)]) – Optional organization to fork to
* **Return type:**
  [`GitHubPromptCollection`](pyrompt.github_integration.html.md#pyrompt.github_integration.GitHubPromptCollection)
* **Returns:**
  GitHubPromptCollection for the new fork

### Example

```pycon
>>> forked = fork_collection(
...     'thorwhalen/awesome_prompts_pyrompt',
...     token='ghp_...'
... )
```

### pyrompt.get_default_base_path()

Get platform-appropriate base path for pyrompt data.

* **Returns:**
  %LOCALAPPDATA%/pyrompt
  - macOS/Linux: ~/.local/share/pyrompt
* **Return type:**
  [`str`](https://docs.python.org/3/builtins/stdtypes.html#str)

### pyrompt.get_engine(name)

Get engine by name.

* **Parameters:**
  **name** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Engine name (e.g., ‘format’, ‘jinja2’)
* **Return type:**
  [`Optional`](https://docs.python.org/3/library/typing.html#typing.Optional)[[`TemplateEngine`](pyrompt.engines.html.md#pyrompt.engines.TemplateEngine)]
* **Returns:**
  TemplateEngine instance or None if not found

### pyrompt.get_stats(collection)

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

### pyrompt.import_from_dict(collection, prompts, metadata=None)

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

### pyrompt.list_available_engines()

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

### pyrompt.list_engines()

List all registered engine names.

* **Return type:**
  [`List`](https://docs.python.org/3/library/typing.html#typing.List)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str)]
* **Returns:**
  List of engine names

### pyrompt.merge_collections(target, \*sources, conflict_strategy='skip')

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

### pyrompt.quick_setup(project_name, with_templates=True, with_metadata=False, base_path=None)

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

### pyrompt.register_engine(engine)

Register a template engine.

* **Parameters:**
  **engine** ([`TemplateEngine`](pyrompt.engines.html.md#pyrompt.engines.TemplateEngine)) – TemplateEngine instance to register

### pyrompt.render_template_file(file_path, output_path=None, \*\*kwargs)

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

### pyrompt.validate_template(template_str, engine_name='format', required_params=None)

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

### Modules

| [`base`](pyrompt.base.html.md#module-pyrompt.base)                             | Core collection classes for prompts and templates.                 |
|-------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------|
| [`cli`](pyrompt.cli.html.md#module-pyrompt.cli)                               | Command-line interface for pyrompt.                                |
| [`engines`](pyrompt.engines.html.md#module-pyrompt.engines)                       | Template engine plugin system for pyrompt.                         |
| [`github_integration`](pyrompt.github_integration.html.md#module-pyrompt.github_integration) | GitHub integration for sharing and discovering prompt collections. |
| [`mall`](pyrompt.mall.html.md#module-pyrompt.mall)                             | Collection of collections - a "mall" of prompt/template stores.    |
| [`search`](pyrompt.search.html.md#module-pyrompt.search)                         | Semantic search for prompts and templates using embeddings.        |
| [`stores`](pyrompt.stores.html.md#module-pyrompt.stores)                         | Storage layer for pyrompt using dol abstractions.                  |
| [`util`](pyrompt.util.html.md#module-pyrompt.util)                             | Utility functions and convenience helpers for pyrompt.             |
