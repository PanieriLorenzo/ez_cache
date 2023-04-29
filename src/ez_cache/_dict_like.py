"""An ABC for dictionary-like access.

Do not check for KeyErrors those are handled automatically.
Do not implement thread safety, that is handled automatically,
if you add another layer you risk deadlocking.
"""

from abc import ABC, abstractmethod
from typing import Any, Iterable
from threading import Lock


class DictLike(ABC):
    @abstractmethod
    def _get(self, key: Any) -> Any:
        pass

    @abstractmethod
    def _set(self, key: Any, value: Any):
        pass

    @abstractmethod
    def _delete(self, key: Any):
        pass

    @abstractmethod
    def _keys(self) -> Iterable[Any]:
        pass

    # INTERNALS AHEAD, don't touch!
    #
    # the following methods are implemented in terms of the
    # abstract methods. Don't mess with these!

    def __init__(self):
        self.__lock = Lock()

    def set(self, key: Any, value: Any):
        with self.__lock:
            self._set(key, value)

    def get(self, key: Any) -> Any:
        with self.__lock:
            self.__check_key(key)
            return self._get(key)

    def delete(self, key: Any):
        with self.__lock:
            self.__check_key(key)
            self._delete(key)

    def contains(self, key: Any) -> bool:
        with self.__lock:
            return key in self._keys()

    def clear(self):
        with self.__lock:
            # must collect into list to avoid modifying iterator
            for key in list(self._keys()):
                self._delete(key)

    def keys(self) -> Iterable[Any]:
        with self.__lock:
            return self._keys()

    def __check_key(self, key: Any):
        if key not in self._keys():
            raise KeyError

    def __contains__(self, key: Any) -> bool:
        return self.contains(key)

    def __delitem__(self, key: Any):
        self.delete(key)

    def __getitem__(self, key: Any) -> Any:
        return self.get(key)

    def __setitem__(self, key: Any, value: Any):
        self.set(key, value)
