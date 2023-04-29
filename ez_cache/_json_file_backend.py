"""Access to JSON file as a dictionary"""
from ez_cache._file_backend import FileBackend
from typing import Any
from pathlib import Path
import json
import jsonpickle


class JSONFileBackend(FileBackend):
    def __init__(self, file_path: Path):
        super().__init__(file_path)

    def _init_file(self):
        with open(self.file_path, "w") as f:
            f.write(jsonpickle.dumps({}, keys=True))

    def _read(self) -> dict[Any, Any]:
        with open(self.file_path) as f:
            return jsonpickle.loads(f.read(), keys=True)

    def _write(self, d: dict[Any, Any]):
        with open(self.file_path, "w") as f:
            f.write(jsonpickle.dumps(d, keys=True))
