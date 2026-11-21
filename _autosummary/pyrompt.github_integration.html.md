# pyrompt.github_integration

GitHub integration for sharing and discovering prompt collections.

Enables:

- Publishing collections to GitHub repositories
- Discovering public collections
- Syncing collections with GitHub

### Functions

| [`clone_collection`](#pyrompt.github_integration.clone_collection)(repo, local_path[, token])     | Clone a GitHub collection to local directory.      |
|--------------------------------------------------------------------------------------------------|----------------------------------------------------|
| [`discover_prompt_collections`](#pyrompt.github_integration.discover_prompt_collections)([search_term, ...]) | Discover public \*_pyrompt repositories on GitHub. |
| [`fork_collection`](#pyrompt.github_integration.fork_collection)(source, token[, organization])  | Fork a collection to your account or organization. |

### Classes

| [`GitHubPromptCollection`](#pyrompt.github_integration.GitHubPromptCollection)(repo, \*[, token, ...])   | Prompt collection backed by GitHub repository.   |
|---------------------------------------------------------------------------------------------------|--------------------------------------------------|

### *class* pyrompt.github_integration.GitHubPromptCollection(repo, , token=None, readonly=True, branch='main', local_cache=None, collection_type='prompts')

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

### pyrompt.github_integration.clone_collection(repo, local_path, token=None)

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

### pyrompt.github_integration.discover_prompt_collections(search_term=None, min_stars=0, language='Python', max_results=50)

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

### pyrompt.github_integration.fork_collection(source, token, organization=None)

Fork a collection to your account or organization.

* **Parameters:**
  * **source** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Source repo (user/repo_pyrompt)
  * **token** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – GitHub token with repo permissions
  * **organization** ([`Optional`](https://docs.python.org/3/library/typing.html#typing.Optional)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str)]) – Optional organization to fork to
* **Return type:**
  [`GitHubPromptCollection`](#pyrompt.github_integration.GitHubPromptCollection)
* **Returns:**
  GitHubPromptCollection for the new fork

### Example

```pycon
>>> forked = fork_collection(
...     'thorwhalen/awesome_prompts_pyrompt',
...     token='ghp_...'
... )
```
