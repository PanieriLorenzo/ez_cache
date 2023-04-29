"""An ABC for access to a file backend"""
from abc import abstractmethod
from pathlib import Path
from filelock import FileLock
from typing import Any


class FileBackend:
    @abstractmethod
    def _init_file(self):
        """Initialize the file with an empty dictionary."""

    @abstractmethod
    def _read(self) -> dict[Any, Any]:
        """Read the full dictionary from the file."""

    @abstractmethod
    def _write(self, d: dict[Any, Any]):
        """Write the full dictionary to the file"""

    # INTERNALS AHEAD, don't touch!
    #
    # the following methods are implemented in terms of the
    # abstract methods. Don't mess with these!

    def __init__(self, file_path: Path):
        self.file_path = file_path
        self.__file_lock = FileLock(file_path.parent / (f"{file_path.name}.lock"))
        self.file_lock_timeout_s = 60

    def read(self) -> dict[Any, Any]:
        """Atomically read the dictionary from the file"""
        self.__acquire_lock()
        self.__ensure_initialized()
        d = self._read()
        self.__release_lock()
        return d

    def write(self, d: dict[Any, Any]):
        """Atomically write the dictionary to the file"""
        self.__acquire_lock()
        self._write(d)
        self.__release_lock()

    def start_transaction(self) -> dict[Any, Any]:
        """Acquire lock and read dictionary without releasing lock"""
        self.__acquire_lock()
        self.__ensure_initialized()
        return self._read()

    def commit_transaction(self, d: dict[Any, Any]):
        """Write dictionary to file, then release lock. Raises IOError if lock
        was not already acquired."""
        if not self.__file_lock.is_locked:
            raise PermissionError("Cannot commit to file that isn't locked")
        self._write(d)
        self.__release_lock()

    def __acquire_lock(self):
        self.__file_lock.acquire(timeout=self.file_lock_timeout_s)

    def __release_lock(self):
        self.__file_lock.release()

    def __ensure_initialized(self):
        """Idempotent initialization. If the file is not present, create it, if
        it exists, don't do anything."""
        if not self.file_path.is_file():
            self._init_file()
