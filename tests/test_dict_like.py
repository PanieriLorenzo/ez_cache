from src.ez_cache._dict_like import DictLike
from typing import Any, Iterable
from dataclasses import dataclass
import pytest


class ExampleDict(DictLike):
    data: dict[Any, Any]

    def __init__(self, d: dict):
        super().__init__()
        self.data = d

    def _get(self, key: Any) -> Any:
        return self.data[key]

    def _set(self, key: Any, value: Any):
        self.data[key] = value

    def _delete(self, key: Any):
        del self.data[key]

    def _keys(self) -> Iterable[Any]:
        return iter(self.data.keys())


def test_get():
    d = ExampleDict({"foo": 1})
    assert d.get("foo") == 1


def test_set():
    d = ExampleDict({})
    d.set("foo", 1)
    assert d.data["foo"] == 1


def test_delete():
    d = ExampleDict({"foo": 1})
    d.delete("foo")
    with pytest.raises(KeyError):
        foo = d.data["foo"]  # noqa: F841


def test_keys():
    d = ExampleDict({"foo": 1, "bar": 2})
    keys = d.keys()
    assert list(keys) == ["foo", "bar"]


def test_contains():
    d = ExampleDict({"foo": 1, "bar": 2})
    assert d.contains("foo")
    assert d.contains("bar")
    assert not d.contains("baz")


def test_clear():
    d = ExampleDict({"foo": 1, "bar": 2})
    assert len(d.data) == 2
    d.clear()
    assert len(d.data) == 0


def test___contains__():
    d = ExampleDict({"foo": 1, "bar": 2})
    assert "foo" in d
    assert "bar" in d
    assert "baz" not in d


def test___delitem__():
    d = ExampleDict({"foo": 1})
    del d["foo"]
    with pytest.raises(KeyError):
        foo = d.data["foo"]  # noqa: F841


def test___getitem__():
    d = ExampleDict({"foo": 1})
    assert d["foo"] == 1


def test___setitem__():
    d = ExampleDict({})
    d["foo"] = 1
    assert d.data["foo"] == 1
