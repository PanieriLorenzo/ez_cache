from src.ez_cache._file_backend import FileBackend
from typing import Any
from pathlib import Path
from tempfile import TemporaryDirectory
import json
import pytest


class ExampleBackend(FileBackend):
    def __init__(self, file_path: Path):
        super().__init__(file_path)

    def _init_file(self):
        with open(self.file_path, "w") as f:
            f.write(json.dumps({}))

    def _read(self) -> dict[Any, Any]:
        with open(self.file_path) as f:
            return json.loads(f.read())

    def _write(self, d: dict[Any, Any]):
        with open(self.file_path, "w") as f:
            f.write(json.dumps(d))


@pytest.fixture
def temp_backend():
    with TemporaryDirectory() as dir_:
        yield ExampleBackend(Path(dir_) / "file.json")


def test_read(temp_backend: ExampleBackend):
    d = temp_backend.read()
    assert isinstance(d, dict)


def test_write(temp_backend: ExampleBackend):
    d = {"foo": 42}
    temp_backend.write(d)
    with open(temp_backend.file_path) as f:
        assert json.loads(f.read()) == d


def test_transaction(temp_backend: ExampleBackend):
    d = temp_backend.start_transaction()
    d["foo"] = 42
    temp_backend.commit_transaction(d)
    with open(temp_backend.file_path) as f:
        assert json.loads(f.read()) == d
