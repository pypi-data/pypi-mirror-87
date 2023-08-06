from operator import eq, ge, gt, le, lt, ne

from rest_collection.typing import ApiOperatorType
from ...abc import AbstractApiSimpleOperator

__all__ = [
    'ApiEqualOperator',
    'ApiNotEqualOperator',
    'ApiGreaterThanOperator',
    'ApiGreaterOrEqualOperator',
    'ApiLessThanOperator',
    'ApiLessOrEqualOperator',
]


class ApiEqualOperator(AbstractApiSimpleOperator):
    __slots__ = ()

    @property
    def operator(self) -> ApiOperatorType:
        return eq


class ApiNotEqualOperator(AbstractApiSimpleOperator):
    __slots__ = ()

    @property
    def operator(self) -> ApiOperatorType:
        return ne


class ApiGreaterThanOperator(AbstractApiSimpleOperator):
    __slots__ = ()

    @property
    def operator(self) -> ApiOperatorType:
        return gt


class ApiGreaterOrEqualOperator(AbstractApiSimpleOperator):
    __slots__ = ()

    @property
    def operator(self) -> ApiOperatorType:
        return ge


class ApiLessThanOperator(AbstractApiSimpleOperator):
    __slots__ = ()

    @property
    def operator(self) -> ApiOperatorType:
        return lt


class ApiLessOrEqualOperator(AbstractApiSimpleOperator):
    __slots__ = ()

    @property
    def operator(self) -> ApiOperatorType:
        return le
