# pyrompt.mall

Collection of collections - a “mall” of prompt/template stores.

Provides nested access: mall[‘collection_name’][‘prompt_key’]

### Classes

| [`PromptMall`](#pyrompt.mall.PromptMall)(workspace_name, \*[, base_path, ...])   | Collection of collections - a "mall" of stores.   |
|-----------------------------------------------------------------------------------------------------|---------------------------------------------------|

### *class* pyrompt.mall.PromptMall(workspace_name, , base_path=None, collection_names=None, with_metadata=False)

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
