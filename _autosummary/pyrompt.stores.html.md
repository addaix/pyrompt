# pyrompt.stores

Storage layer for pyrompt using dol abstractions.

Provides clean Mapping/MutableMapping interfaces to filesystem storage.

### Functions

| [`get_default_base_path`](#pyrompt.stores.get_default_base_path)()                          | Get platform-appropriate base path for pyrompt data.      |
|---------------------------------------------------------------------------------------------------|-----------------------------------------------------------|
| [`mk_collection_path`](#pyrompt.stores.mk_collection_path)(collection_name[, base_path]) | Get the path for a collection.                            |
| [`mk_collection_stores`](#pyrompt.stores.mk_collection_stores)(collection_name[, ...])     | Create all stores for a collection.                       |
| [`mk_metadata_store`](#pyrompt.stores.mk_metadata_store)(rootdir[, for_type])           | Create a JSON metadata store.                             |
| [`mk_prompt_store`](#pyrompt.stores.mk_prompt_store)(rootdir[, extension])            | Create a file store for prompts with clean interface.     |
| [`mk_template_store`](#pyrompt.stores.mk_template_store)(rootdir[, extensions])         | Create a template store that handles multiple extensions. |

### pyrompt.stores.get_default_base_path()

Get platform-appropriate base path for pyrompt data.

* **Returns:**
  %LOCALAPPDATA%/pyrompt
  - macOS/Linux: ~/.local/share/pyrompt
* **Return type:**
  [`str`](https://docs.python.org/3/builtins/stdtypes.html#str)

### pyrompt.stores.mk_collection_path(collection_name, base_path=None)

Get the path for a collection.

* **Parameters:**
  * **collection_name** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Name of the collection
  * **base_path** ([`Optional`](https://docs.python.org/3/library/typing.html#typing.Optional)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str)]) – Optional base path (uses default if None)
* **Return type:**
  [`Path`](https://docs.python.org/3/library/pathlib.html#pathlib.Path)
* **Returns:**
  Path object for the collection directory

### pyrompt.stores.mk_collection_stores(collection_name, base_path=None, create_metadata=False)

Create all stores for a collection.

* **Parameters:**
  * **collection_name** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Name of the collection
  * **base_path** ([`Optional`](https://docs.python.org/3/library/typing.html#typing.Optional)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str)]) – Optional base path
  * **create_metadata** ([`bool`](https://docs.python.org/3/builtins/functions.html#bool)) – Whether to create metadata stores
* **Returns:**
  ‘prompts’, ‘templates’, and optionally ‘prompt_meta’, ‘template_meta’
* **Return type:**
  [`dict`](https://docs.python.org/3/builtins/stdtypes.html#dict)

### pyrompt.stores.mk_metadata_store(rootdir, for_type='prompts')

Create a JSON metadata store.

* **Parameters:**
  * **rootdir** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Directory to store metadata
  * **for_type** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Type of metadata (just for documentation)
* **Returns:**
  MutableMapping[str, dict] with JSON file storage

### Example

```pycon
>>> store = mk_metadata_store('/tmp/meta')
>>> store['greeting'] = {'author': 'thor', 'version': '1.0'}
>>> meta = store['greeting']
```

### pyrompt.stores.mk_prompt_store(rootdir, extension='txt')

Create a file store for prompts with clean interface.

- Keys don’t show extension
- Values are strings (not bytes)
- Supports tab completion

* **Parameters:**
  * **rootdir** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Directory to store prompts
  * **extension** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – File extension (without dot)
* **Returns:**
  MutableMapping[str, str] with file-backed storage

### Example

```pycon
>>> store = mk_prompt_store('/tmp/prompts')
>>> store['greeting'] = "Hello, {name}!"
>>> print(store['greeting'])
Hello, {name}!
```

### pyrompt.stores.mk_template_store(rootdir, extensions=None)

Create a template store that handles multiple extensions.

Keeps the extension in the key so we can detect template engine.

* **Parameters:**
  * **rootdir** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Directory to store templates
  * **extensions** ([`Optional`](https://docs.python.org/3/library/typing.html#typing.Optional)[[`list`](https://docs.python.org/3/builtins/stdtypes.html#list)]) – List of extensions to support (with dots)
    Defaults to [‘.txt’, ‘.jinja2’, ‘.j2’, ‘.jinja’, ‘.mustache’, ‘.hbs’]
* **Returns:**
  MutableMapping[str, str] with file-backed storage

### Example

```pycon
>>> store = mk_template_store('/tmp/templates')
>>> store['greeting.jinja2'] = "Hello {{ name }}!"
>>> store['simple.txt'] = "Hello {name}!"
```
