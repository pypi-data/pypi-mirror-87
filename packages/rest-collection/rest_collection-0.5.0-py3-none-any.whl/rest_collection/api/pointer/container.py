from abc import ABCMeta
from typing import Any, FrozenSet, Optional, Set, Tuple
from weakref import WeakSet, ref

from sqlalchemy import Column
from sqlalchemy.ext.declarative import DeclarativeMeta
from sqlalchemy.orm import RelationshipProperty

from .identity import ApiIdentity
from ..exc import ApiTypeError

__all__ = [
    'ApiPointer'
]


def _make_ref_or_none(value):
    if value is None:
        return
    return ref(value)


def _resolve_ref_or_none(ref_):
    if ref_ is None:
        return
    # noinspection PyCallingNonCallable
    return ref_()


class ApiPointer(object, metaclass=ABCMeta):
    """
    API pointer container, that associates string identity of ORM model and
    ORM model itself.
    """
    __slots__ = (
        '_identity',
        '_sa_column',
        '_sa_relationship',
        '_sa_cls',
        '_parent_ref',
        '_childs_refs',
        '__weakref__',
    )

    def __init__(self,
                 identity: ApiIdentity,
                 sa_cls: DeclarativeMeta,
                 sa_column: Optional[Column],
                 sa_relationship: Optional[RelationshipProperty],
                 parent: Optional['ApiPointer'] = None,
                 childs: Optional[Set['ApiPointer']] = None) -> None:
        self._identity = identity
        self._sa_column = sa_column
        self._sa_relationship = sa_relationship
        self._sa_cls = sa_cls
        self._parent_ref = _make_ref_or_none(parent)
        self._childs_refs = WeakSet(childs)

    def __repr__(self) -> str:
        return '<ApiPointer (identity=%s)>' % self._identity

    @property
    def identity(self) -> ApiIdentity:
        return self._identity

    @property
    def sa_column(self) -> Optional[Column]:
        return self._sa_column

    @property
    def sa_relationship(self) -> Optional[RelationshipProperty]:
        return self._sa_relationship

    @property
    def sa_cls(self) -> DeclarativeMeta:
        return self._sa_cls

    @property
    def parents(self) -> Tuple['ApiPointer', ...]:
        """Parent pointers chain (ordered from top parents to self parent)."""
        parent = self.parent

        if parent is None:
            return ()

        return parent.parents + (parent, )

    @property
    def parent(self) -> Optional['ApiPointer']:
        """Parent pointer."""
        return _resolve_ref_or_none(self._parent_ref)

    @property
    def childs(self) -> FrozenSet['ApiPointer']:
        """Child pointers."""
        return frozenset(self._childs_refs)

    def add_child(self, api_pointer: 'ApiPointer') -> None:
        self._childs_refs.add(api_pointer)

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, self.__class__):
            raise ApiTypeError(
                'Comparison with object of %r allowed.' %
                self.__class__.__name__
            )
        return self._identity == other.identity

    def __hash__(self) -> int:
        return hash(self._identity)
