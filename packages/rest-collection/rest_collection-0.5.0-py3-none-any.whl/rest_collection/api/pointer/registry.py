from typing import Callable, Iterator, MutableMapping

from sqlalchemy.ext.declarative import DeclarativeMeta

from .container import ApiPointer
from .factory import api_pointer_factory
from .sa_mapper import SaMapperRegistry

__all__ = [
    'ApiPointerRegistry'
]


class ApiPointerRegistry(MutableMapping[str, ApiPointer]):
    """
    API Pointer registry.
    """
    __slots__ = '_pointers', '_sa_mappers', '_sa_cls', '_factory'

    def __init__(
        self,
        sa_cls: DeclarativeMeta,
        factory: Callable[
            ['ApiPointerRegistry'],
            Callable[[str], ApiPointer],
        ] = api_pointer_factory,
    ):
        self._pointers = {}  # type: MutableMapping[str, ApiPointer]
        self._sa_mappers = SaMapperRegistry()
        self._sa_cls = sa_cls
        self._factory = factory(self)

    @property
    def sa_mappers(self) -> SaMapperRegistry:
        return self._sa_mappers

    @property
    def sa_cls(self) -> DeclarativeMeta:
        return self._sa_cls

    @property
    def factory(self) -> Callable[[str], ApiPointer]:
        return self._factory

    def __getitem__(self, key: str) -> ApiPointer:
        if key not in self._pointers:
            # Key adding is implemented inside factory, because key (
            # identity) can contains more than one model (API pointer). So,
            # identities can be added during walking throught the
            # relationship cascade.
            self._factory(key)
        return self._pointers[key]

    def __contains__(self, key: str) -> bool:
        return key in self._pointers

    def __len__(self) -> int:
        return len(self._pointers)

    def __setitem__(self, key: str, value: ApiPointer) -> None:
        self._pointers[key] = value

    def __delitem__(self, key: str) -> None:
        del self._pointers[key]

    def __iter__(self) -> Iterator[str]:
        return iter(self._pointers)

    def __repr__(self) -> str:
        return '<%s keys=%s>' % (
            self.__class__.__name__,
            ', '.join(sorted(self._pointers))
        )
