from abc import abstractmethod
from typing import Any, FrozenSet, Optional, Union

from sqlalchemy.sql.elements import BinaryExpression, BooleanClauseList

from .request import AbstractApiRequest, AbstractApiRequestContext
from ..alias import AliasedTableMap
from ..filter import ApiFilterExpressionGroup, ApiFilterParser
from ..pointer import ApiPointer

__all__ = [
    'AbstractApiFilterRequestContext',
]


class AbstractApiFilterRequestContext(AbstractApiRequestContext):

    __slots__ = '_data', '_parser'

    def __init__(self, request: AbstractApiRequest) -> None:
        self._data = None  # type: Optional[ApiFilterExpressionGroup]
        self._parser = ApiFilterParser(
            request.pointer_registry,
            request.operator_registry,
        )
        super().__init__(request)

    @property
    def data(self) -> Optional[ApiFilterExpressionGroup]:
        return self._data

    @property
    def pointers(self) -> Optional[FrozenSet[ApiPointer]]:
        if self:
            return self._data.pointers

    @abstractmethod
    def _initialize(self) -> None: ...

    def __repr__(self) -> str:
        return '<%s (data=%s)' % (
            self.__class__.__name__, repr(self._data)
        )

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, self.__class__) and other.data == self._data

    def __bool__(self) -> bool:
        return self._data is not None

    def compile(self, aliased_table_map: AliasedTableMap) -> Union[
        BooleanClauseList, BinaryExpression, None
    ]:
        if self:
            return self._data.compile(aliased_table_map)
