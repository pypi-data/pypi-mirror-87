from itertools import count
from operator import itemgetter
from typing import Any, Hashable, Iterator, MutableMapping
from weakref import WeakKeyDictionary, WeakValueDictionary

__all__ = [
    'WeakKeyOrderedDict',
]


class WeakKeyOrderedDict(MutableMapping[Hashable, Any]):

    __slots__ = '_data', '_keys', '_key_count'

    def __init__(self) -> None:
        self._key_count = count()
        self._keys = WeakValueDictionary()  # type: WeakValueDictionary
        self._data = WeakKeyDictionary()  # type: WeakKeyDictionary

    def __getitem__(self, key: Hashable) -> Any:
        return self._data[key]

    def __setitem__(self, key: Hashable, value: Any) -> None:
        key_key = next(self._key_count)
        self._keys[key_key] = key
        self._data[key] = value

    def __delitem__(self, key: Hashable) -> None:
        del self._data[key]

        key_key_to_delete = None

        for key_key, key_value in self._keys.items():
            if key_value == key:
                key_key_to_delete = key_key
                break

        if key_key_to_delete is not None:
            del self._keys[key_key_to_delete]

    def __iter__(self) -> Iterator[Hashable]:
        return iter(
            map(itemgetter(1), sorted(self._keys.items(), key=itemgetter(0)))
        )

    def __len__(self) -> int:
        return len(self._data)
