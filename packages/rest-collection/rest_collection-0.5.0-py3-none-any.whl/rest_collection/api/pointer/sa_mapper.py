from operator import attrgetter
from typing import Iterator, Mapping
from weakref import WeakKeyDictionary

from sqlalchemy import inspect
from sqlalchemy.ext.declarative import DeclarativeMeta
from sqlalchemy.orm import Mapper

__all__ = [
    'SaMapperRegistry',
]


class SaMapperRegistry(Mapping[DeclarativeMeta, Mapper]):
    """
    Sqlalchemy model mappers registry.
    """
    __slots__ = '_data', '__weakref__'

    def __init__(self):
        self._data = WeakKeyDictionary()

    def __getitem__(self, key: DeclarativeMeta) -> Mapper:
        if key not in self._data:
            self._data[key] = inspect(key)
        return self._data[key]

    def __len__(self) -> int:
        return len(self._data)

    def __iter__(self) -> Iterator[DeclarativeMeta]:
        return iter(self._data)

    def __repr__(self) -> str:
        return '<%s keys=%s>' % (
            self.__class__.__name__,
            ', '.join(sorted(map(
                attrgetter('__tablename__'), self._data.keys()
            )))
        )

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            raise TypeError('Comparison only with %r objects is allowed.' %
                            self.__class__.__name__)
        return frozenset(other) == frozenset(self)
