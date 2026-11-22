"""SemanticIndex with a fake `oa` module: deterministic embeddings, no network, no paid calls."""

import sys
import types

import pytest

np = pytest.importorskip("numpy")  # optional dependency

VECS = {
    "python expert": [1.0, 0.0, 0.0],
    "python tutor": [0.95, 0.05, 0.0],
    "chef": [0.0, 1.0, 0.0],
    "pandas help": [0.9, 0.0, 0.1],
}


def _fake_embeddings(x, model=None):
    if isinstance(x, str):
        return VECS[x]
    return [VECS[t] for t in x]


@pytest.fixture
def index_cls(monkeypatch):
    oa = types.ModuleType("oa")
    oa.embeddings = _fake_embeddings
    monkeypatch.setitem(sys.modules, "oa", oa)
    monkeypatch.setitem(sys.modules, "oa.batch_embeddings", None)  # force the fallback path
    from pyrompt.search import SemanticIndex

    return SemanticIndex


class _Coll(dict):
    meta = None


def _coll():
    c = _Coll({k: k for k in ["python expert", "python tutor", "chef"]})
    c.meta = {
        "python expert": {"lang": "py", "tags": ["code", "expert"]},
        "python tutor": {"lang": "py", "tags": ["teach"]},
        "chef": {"lang": "none", "tags": ["food"]},
    }
    return c


def test_search_ranks_by_cosine(index_cls):
    idx = index_cls(_coll())
    res = idx.search("pandas help", top_k=2)
    assert [k for k, _ in res] == ["python expert", "python tutor"]
    assert res[0][1] > res[1][1] > 0
    assert idx.search("pandas help", top_k=1) == res[:1]


def test_empty_collection_searches_to_nothing(index_cls):
    assert index_cls({}).search("pandas help") == []


def test_add_remove_rebuild(index_cls):
    c = _coll()
    idx = index_cls(c)
    c["pandas help"] = "pandas help"
    idx.add("pandas help")
    assert "pandas help" in [k for k, _ in idx.search("python expert", top_k=10)]
    idx.remove("chef")
    idx.remove("never-there")  # silently ignored
    assert "chef" not in [k for k, _ in idx.search("python expert", top_k=10)]
    idx.rebuild()
    assert "chef" in [k for k, _ in idx.search("python expert", top_k=10)]


def test_filters_use_collection_meta(index_cls):
    idx = index_cls(_coll())
    keys = lambda r: [k for k, _ in r]
    assert keys(idx.search("python expert", top_k=5, filters={"lang": "py"})) == [
        "python expert", "python tutor",
    ]
    assert keys(idx.search("python expert", top_k=5, filters={"tags": ["teach", "food"]})) == [
        "python tutor", "chef",
    ]
    assert keys(idx.search("python expert", top_k=5, filters={"tags": "code"})) == []
    assert keys(idx.search("python expert", top_k=5, filters={"missing": 1})) == []


def test_matches_filters_edge_cases(index_cls):
    plain = index_cls({"chef": "chef"})
    assert plain._matches_filters("chef", {"a": 1}) is True  # no meta attribute
    c = _coll()
    idx = index_cls(c)
    assert idx._matches_filters("not-in-meta", {"lang": "py"}) is False
    assert idx._matches_filters("python expert", {"tags": ["code"]}) is True
    assert idx._matches_filters("python expert", {"lang": ["py", "js"]}) is True
    assert idx._matches_filters("chef", {"lang": ["py", "js"]}) is False


def test_diversity_drops_near_duplicates(index_cls):
    c = _coll()
    idx = index_cls(c)
    full = [k for k, _ in idx.search("python expert", top_k=5)]
    assert full[:2] == ["python expert", "python tutor"]
    diverse = [k for k, _ in idx.search("python expert", top_k=5, diversity_threshold=0.9)]
    assert diverse == ["python expert", "chef"]
    assert idx._diversify_results([], 0.5) == []


def test_cluster_groups_similar_items(index_cls):
    pytest.importorskip("sklearn")  # optional dependency
    idx = index_cls(_coll())
    clusters = idx.cluster(n_clusters=2)
    groups = sorted(sorted(v) for v in clusters.values())
    assert groups == [["chef"], ["python expert", "python tutor"]]
    assert index_cls({}).cluster() == {}


def test_missing_oa_gives_a_helpful_error(monkeypatch):
    monkeypatch.setitem(sys.modules, "oa", None)
    from pyrompt.search import SemanticIndex

    with pytest.raises(ImportError, match="oa required"):
        SemanticIndex({"a": "a"})
