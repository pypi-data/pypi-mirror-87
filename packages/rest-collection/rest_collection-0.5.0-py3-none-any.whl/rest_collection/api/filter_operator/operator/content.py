from collections import namedtuple
from functools import partial
from operator import methodcaller
from typing import Any

from sqlalchemy import Column, String, cast, literal, not_
from sqlalchemy.sql.elements import BinaryExpression

from rest_collection.typing import ApiOperatorType
from ...abc import AbstractApiSimpleOperator

__all__ = [
    'ApiStartsWithOperator',
    'ApiNotStartsWithOperator',
    'ApiIStartsWithOperator',
    'ApiNotIStartsWithOperator',
    'ApiEndsWithOperator',
    'ApiNotEndsWithOperator',
    'ApiIEndsWithOperator',
    'ApiNotIEndsWithOperator',
    'ApiContainsOperator',
    'ApiNotContainsOperator',
    'ApiIContainsOperator',
    'ApiNotIContainsOperator',
]


_LikeRule = namedtuple('_LikeRule', ('method', 'value_getter'))

_LIKE_RULE_MAP = {
    'startswith': _LikeRule('like', lambda x: literal(x) + '%'),
    'istartswith': _LikeRule('ilike', lambda x: literal(x) + '%'),
    'endswith': _LikeRule('like', lambda x: '%' + literal(x)),
    'iendswith': _LikeRule('ilike', lambda x: '%' + literal(x)),
    'contains': _LikeRule('like', lambda x: '%' + literal(x) + '%'),
    'icontains': _LikeRule('ilike', lambda x: '%' + literal(x) + '%'),
}


def _make_like_expression(like_rule_label: str,
                          column: Column,
                          value: Any) -> BinaryExpression:
    """
    Making filter like or ilike expression.

    :param like_rule_label: Key of ``_LIKE_RULE_MAP``.
    :param column: Sqlalchemy column.
    :param value: Value of filter.
    """
    like_rule = _LIKE_RULE_MAP[like_rule_label]

    if column.type.python_type is not str:
        column = cast(column, String)

    return methodcaller(
        like_rule.method, like_rule.value_getter(str(value))
    )(column)


_startswith = partial(
    _make_like_expression, 'startswith'
)  # type: ApiOperatorType


class ApiStartsWithOperator(AbstractApiSimpleOperator):
    __slots__ = ()

    @property
    def operator(self) -> ApiOperatorType:
        return _startswith


class ApiNotStartsWithOperator(AbstractApiSimpleOperator):
    __slots__ = ()

    @property
    def operator(self) -> ApiOperatorType:
        return lambda a, b: not_(_startswith(a, b))


_istartswith = partial(
    _make_like_expression, 'istartswith'
)  # type: ApiOperatorType


class ApiIStartsWithOperator(AbstractApiSimpleOperator):
    __slots__ = ()

    @property
    def operator(self) -> ApiOperatorType:
        return _istartswith


class ApiNotIStartsWithOperator(AbstractApiSimpleOperator):
    __slots__ = ()

    @property
    def operator(self) -> ApiOperatorType:
        return lambda a, b: not_(_istartswith(a, b))


_endswith = partial(
    _make_like_expression, 'endswith'
)  # type: ApiOperatorType


class ApiEndsWithOperator(AbstractApiSimpleOperator):
    __slots__ = ()

    @property
    def operator(self) -> ApiOperatorType:
        return _endswith


class ApiNotEndsWithOperator(AbstractApiSimpleOperator):
    __slots__ = ()

    @property
    def operator(self) -> ApiOperatorType:
        return lambda a, b: not_(_endswith(a, b))


_iendswith = partial(
    _make_like_expression, 'iendswith'
)  # type: ApiOperatorType


class ApiIEndsWithOperator(AbstractApiSimpleOperator):
    __slots__ = ()

    @property
    def operator(self) -> ApiOperatorType:
        return _iendswith


class ApiNotIEndsWithOperator(AbstractApiSimpleOperator):
    __slots__ = ()

    @property
    def operator(self) -> ApiOperatorType:
        return lambda a, b: not_(_iendswith(a, b))


_contains = partial(
    _make_like_expression, 'contains'
)  # type: ApiOperatorType


class ApiContainsOperator(AbstractApiSimpleOperator):
    __slots__ = ()

    @property
    def operator(self) -> ApiOperatorType:
        return _contains


class ApiNotContainsOperator(AbstractApiSimpleOperator):
    __slots__ = ()

    @property
    def operator(self) -> ApiOperatorType:
        return lambda a, b: not_(_contains(a, b))


_icontains = partial(
    _make_like_expression, 'icontains'
)  # type: ApiOperatorType


class ApiIContainsOperator(AbstractApiSimpleOperator):
    __slots__ = ()

    @property
    def operator(self) -> ApiOperatorType:
        return _icontains


class ApiNotIContainsOperator(AbstractApiSimpleOperator):
    __slots__ = ()

    @property
    def operator(self) -> ApiOperatorType:
        return lambda a, b: not_(_icontains(a, b))
