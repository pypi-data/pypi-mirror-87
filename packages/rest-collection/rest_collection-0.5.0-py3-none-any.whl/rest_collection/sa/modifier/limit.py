from sqlalchemy.sql import Select

from rest_collection.api import AbstractApiLimitRequestContext
from .abc import AbstractSaQueryModifier

__all__ = [
    'SaQueryLimitModifier',
]


class SaQueryLimitModifier(
    AbstractSaQueryModifier[AbstractApiLimitRequestContext]
):
    __slots__ = ()

    def fill_join_map(self) -> None: ...

    def modify(self, sa_query: Select, *args, **kwargs) -> Select:
        if not self:
            return sa_query

        data = self.data

        start = data.start
        stop = data.stop
        limit = data.limit

        if start:
            sa_query = sa_query.offset(start)

        if stop:
            sa_query = sa_query.limit(limit)

        return sa_query
