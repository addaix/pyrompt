# pyrompt.search

Semantic search for prompts and templates using embeddings.

Provides similarity-based search over collections.

### Functions

| [`default_embeddings`](#pyrompt.search.default_embeddings)()   | The embedding function used when none is passed: `oa.embeddings`, else `aix.embeddings`.   |
|-------------------------------------------------------------------------|--------------------------------------------------------------------------------------------|

### Classes

| [`SemanticIndex`](#pyrompt.search.SemanticIndex)(collection, \*[, auto_update, ...])   | Semantic search index for prompts/templates.   |
|------------------------------------------------------------------------------------------------------|------------------------------------------------|

### *class* pyrompt.search.SemanticIndex(collection, , auto_update=False, embedding_model='text-embedding-3-small', batch_size=100, embeddings=None)

Bases: [`object`](https://docs.python.org/3/builtins/functions.html#object)

Semantic search index for prompts/templates.

Embeds through `embeddings` (a keyword seam; by default `oa.embeddings`, else
`aix.embeddings`) to create vector representations, then supports similarity search.

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

### pyrompt.search.default_embeddings()

The embedding function used when none is passed: `oa.embeddings`, else `aix.embeddings`.

Both take `(text_or_texts, model=...)` and return a vector, or one vector per text.
Raises `ImportError` naming both when neither is installed.

* **Return type:**
  [`Callable`](https://docs.python.org/3/library/typing.html#typing.Callable)
