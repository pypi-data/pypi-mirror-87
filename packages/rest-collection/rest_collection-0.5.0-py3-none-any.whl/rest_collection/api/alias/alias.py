from abc import abstractmethod
from itertools import count
from typing import Dict, Iterator, Mapping, overload

from ..pointer import ApiPointer

__all__ = [
    'AbstractAliasMap',
    'NumericAliasMap',
    'TablenameAliasMap',
]


class AbstractAliasMap(Mapping[str, str]):
    __slots__ = '_data',

    def __init__(self):
        self._data = {}  # type: Dict[str, str]

    @overload
    def __getitem__(self, key: ApiPointer) -> str: ...

    @overload
    def __getitem__(self, key: str) -> str: ...

    def __getitem__(self, key):
        if isinstance(key, ApiPointer):
            return self._get_alias(key)

        if isinstance(key, str):
            return self._data[key]

        raise KeyError(key)

    def _get_alias(self, api_pointer: ApiPointer) -> str:
        if api_pointer.sa_relationship is not None:
            key = str(api_pointer.identity)

        else:
            # For column api pointers we need to obtain table identity only,
            # excluding column part of identity.
            key = str(api_pointer.identity.slice(stop=-1))

        if key in self._data:
            alias = self._data[key]

        else:
            alias = self._generate_alias(api_pointer)
            self._data[key] = alias

        return alias

    @abstractmethod
    def _generate_alias(self, api_pointer: ApiPointer) -> str: ...

    def __len__(self) -> int:
        return len(self._data)

    def __iter__(self) -> Iterator[str]:
        return iter(self._data)


class NumericAliasMap(AbstractAliasMap):
    __slots__ = '_counter', '_prefix'

    def __init__(self, start: int = 0, prefix: str = '_'):
        super().__init__()
        self._counter = count(start=start)
        self._prefix = prefix

    def _generate_alias(self, api_pointer: ApiPointer) -> str:
        return '{}{:0>2}'.format(
            self._prefix,
            next(self._counter),
        )


class TablenameAliasMap(AbstractAliasMap):

    def _generate_alias(self, api_pointer: ApiPointer) -> str:
        if api_pointer.sa_relationship is not None:
            return api_pointer.sa_relationship.target.name
        return api_pointer.sa_cls.__table__.name
