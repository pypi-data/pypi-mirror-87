from typing import Any, Type

from ujson import loads

from rest_collection.typing import ApiOperatorType
from ...abc import AbstractApiOperator, AbstractApiSetOperator, \
    AbstractApiSimpleOperator

__all__ = [
    'ApiInOperator',
    'ApiNotInOperator',
    'ApiIsOperator',
    'ApiNotIsOperator',
    'ApiBetweenOperator',
]


class ApiInOperator(AbstractApiSetOperator):
    __slots__ = ()

    @property
    def operator(self) -> ApiOperatorType:
        return lambda a, b: a.in_(b)


class ApiNotInOperator(AbstractApiSetOperator):
    __slots__ = ()

    @property
    def operator(self) -> ApiOperatorType:
        return lambda a, b: a.notin_(b)


class ApiIsOperator(AbstractApiSimpleOperator):
    __slots__ = ()

    @property
    def operator(self) -> ApiOperatorType:
        return lambda a, b: a.is_(b)


class ApiNotIsOperator(AbstractApiSimpleOperator):
    __slots__ = ()

    @property
    def operator(self) -> ApiOperatorType:
        return lambda a, b: a.isnot(b)


class ApiBetweenOperator(AbstractApiOperator):
    __slots__ = ()

    @property
    def operator(self) -> ApiOperatorType:
        return lambda a, b, c: a.between(b, c)

    def _deserialize(self,
                     column_type: Type,
                     raw_value: Any,
                     *args,
                     **kwargs) -> Any:
        right, left = loads(raw_value)
        deserializer = self.__class__.deserializer
        # noinspection PyCallingNonCallable
        return self._get_deserialize_result(
            deserializer(column_type, right), deserializer(column_type, left)
        )
