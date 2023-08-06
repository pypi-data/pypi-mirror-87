from operator import methodcaller
from typing import Any, Callable, FrozenSet, List, Optional, Sequence, \
    TYPE_CHECKING, Union
from weakref import ref

from sqlalchemy import Column, and_, or_
from sqlalchemy.sql.elements import BinaryExpression, BooleanClauseList

from rest_collection.typing import ApiOperatorType
from ..alias import AliasedTableMap
from ..exc import ApiFilterExpressionError, ApiPointerError
from ..pointer import ApiPointer, ApiPointerRegistry

if TYPE_CHECKING:
    from ..abc import AbstractApiOperatorRegistry

__all__ = [
    'ApiFilterExpression',
    'ApiFilterExpressionGroup',
]


class ApiFilterExpression(object):
    """
    API filter expression.
    """
    __slots__ = '_pointer_ref', '_operator', '_value'

    def __init__(self,
                 pointer: ApiPointer,
                 operator: ApiOperatorType,
                 value: Any):
        self._pointer_ref = ref(pointer)
        self._operator = operator
        self._value = value

    @property
    def pointer(self) -> Optional[ApiPointer]:
        return self._pointer_ref()

    @property
    def sa_column(self) -> Column:
        return getattr(self.pointer, 'sa_column')

    @property
    def value(self) -> Any:
        return self._value

    @property
    def operator(self) -> ApiOperatorType:
        return self._operator

    def compile(self, aliased_table_map: AliasedTableMap) -> BinaryExpression:
        api_pointer = self.pointer

        if api_pointer.parent is None:
            column = self.sa_column

        else:
            aliased_table = aliased_table_map[self.pointer]
            column = aliased_table.columns[self.sa_column.key]

        return self._operator(
            column,
            self.value,
        )

    __call__ = compile

    @classmethod
    def from_string(
        cls,
        expression_string: str,
        pointer_registry: ApiPointerRegistry,
        operator_registry: 'AbstractApiOperatorRegistry',
    ) -> 'ApiFilterExpression':
        expression_string = expression_string.strip('() ')
        return cls.from_list(
            expression_string.split(' ', 2),
            pointer_registry,
            operator_registry,
        )

    @classmethod
    def from_list(
        cls,
        expression_list: List,
        pointer_registry: ApiPointerRegistry,
        operator_registry: 'AbstractApiOperatorRegistry',
    ) -> 'ApiFilterExpression':
        if not isinstance(expression_list, list) or len(expression_list) != 3:
            raise ApiFilterExpressionError(
                'Unable to parse expression list. '
                'It must contain column key, operator key and value itself.'
            )

        column_pointer_key, operator_key, value = expression_list

        try:
            column_pointer = pointer_registry[column_pointer_key]

        except ApiPointerError as err:
            raise ApiFilterExpressionError(
                'There is no model pointer with key %r.' %
                column_pointer_key
            ) from err

        if column_pointer.sa_column is None:
            raise ApiFilterExpressionError(
                'In filter expression list it is allowed to declare only '
                'column, but %r is a relationship.' % column_pointer_key
            )

        try:
            operator = operator_registry[operator_key]

        except KeyError as err:
            raise ApiFilterExpressionError(
                'There is not operator %r in operator registry list.'
                % operator_key
            ) from err

        return cls(column_pointer, operator, value)

    def __eq__(self, other: Any) -> bool:
        try:
            return (
                self.pointer == other.pointer and
                self._operator == other.operator and
                self._value == other.value
            )
        except AttributeError:
            return False

    def __repr__(self) -> str:
        return '<%s pointer=%s operator=%s value=%s>' % (
            self.__class__.__name__,
            repr(self.pointer),
            repr(self._operator),
            repr(self._value)
        )


_ExpressionType = Union[
    ApiFilterExpression,
    'ApiFilterExpressionGroup',
]


class ApiFilterExpressionGroup(Sequence[ApiFilterExpression]):
    """
    Api filter expression group, that are concatenated logically.
    """
    __slots__ = '_expressions', '_conjunction'

    def __init__(self,
                 *expressions: _ExpressionType,
                 conjunction: bool = True) -> None:
        self._conjunction = bool(conjunction)

        # ApiFilterExpression is not hashable, so current attribute is list,
        # not set.
        self._expressions = []  # type: List[_ExpressionType]
        self.join(*expressions)

    def __len__(self) -> int:
        return len(self._expressions)

    def __getitem__(self, index: int) -> _ExpressionType:
        return self._expressions[index]

    def join(self, *expressions: _ExpressionType) -> None:
        for expression in expressions:
            assert isinstance(expression, (
                ApiFilterExpression, ApiFilterExpressionGroup
            ))

            if expression not in self._expressions:
                self._expressions.append(expression)

    @property
    def expressions(self) -> List[_ExpressionType]:
        return self._expressions

    @property
    def conjunction(self) -> bool:
        return self._conjunction

    def __repr__(self) -> str:
        return '<%s conjunction="%s" expressions=%s>' % (
            self.__class__.__name__,
            self._conjunction and 'and' or 'or',
            repr(self._expressions)
        )

    def __eq__(self, other: Any) -> bool:
        try:
            return (
                self._conjunction == other.conjunction and
                self._expressions == other.expressions
            )
        except AttributeError:
            return False

    @property
    def sa_operator(self) -> Callable[...,  BooleanClauseList]:
        return self._conjunction and and_ or or_

    def compile(self, aliased_table_map: 'AliasedTableMap') -> Union[
        BooleanClauseList, BinaryExpression, None
    ]:
        expressions = self._expressions
        if len(expressions) == 0:
            return

        if len(expressions) == 1:
            # It is senselessly to apply operator on single expression.
            return self._expressions[0].compile(aliased_table_map)

        return self.sa_operator(*map(
            methodcaller('compile', aliased_table_map), self._expressions
        ))

    __call__ = compile

    @property
    def pointers(self) -> FrozenSet[ApiPointer]:

        def get_pointers():
            for expression in self._expressions:

                if isinstance(expression, self.__class__):
                    yield from expression.pointers
                    continue

                yield expression.pointer

        return frozenset(get_pointers())

    @classmethod
    def create_or_unwrap(
        cls,
        *expressions: _ExpressionType,
        conjunction: bool = True
    ) -> 'ApiFilterExpressionGroup':
        """Creation or returning filter expression group, if it declares
        singly."""
        if len(expressions) == 1 and isinstance(expressions[0], cls):
            return expressions[0]
        return cls(*expressions, conjunction=conjunction)
