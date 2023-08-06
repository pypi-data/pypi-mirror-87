from typing import Dict, Iterator, Mapping
from weakref import WeakKeyDictionary

from sqlalchemy.sql import Alias

from .alias import AbstractAliasMap
from ..pointer import ApiPointer

__all__ = [
    'AliasedTableMap',
]


class AliasedTableMap(Mapping[ApiPointer, Alias]):
    __slots__ = '_alias_map', '_data', '_aliases'

    def __init__(self, alias_map: AbstractAliasMap):
        self._data = WeakKeyDictionary()
        self._aliases = {}  # type: Dict[str, Alias]
        self._alias_map = alias_map

    def __getitem__(self, key: ApiPointer) -> Alias:
        if key in self._data:
            return self._data[key]

        alias = self._alias_map[key]

        if alias in self._aliases:
            aliased_table = self._aliases[alias]

        else:
            if key.sa_relationship is not None:
                aliased_table = key.sa_relationship.target.alias(alias)

            else:
                aliased_table = key.sa_cls.__table__.alias(alias)

            self._aliases[alias] = aliased_table

        self._data[key] = aliased_table
        return aliased_table

    def __len__(self) -> int:
        return len(self._data)

    def __iter__(self) -> Iterator[ApiPointer]:
        return iter(self._data)

    @property
    def alias_map(self) -> AbstractAliasMap:
        return self._alias_map

