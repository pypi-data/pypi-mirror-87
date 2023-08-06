from sqlalchemy.sql import Select

from rest_collection.api import AbstractApiFilterRequestContext
from .abc import AbstractSaQueryModifier

__all__ = [
    'SaQueryFilterModifier',
]


class SaQueryFilterModifier(
    AbstractSaQueryModifier[AbstractApiFilterRequestContext]
):
    __slots__ = ()

    def fill_join_map(self) -> None:
        if not self:
            return

        for api_pointer in self.data.pointers:
            self.join_map.add_pointer(api_pointer)

    def modify(self, sa_query: Select, *args, **kwargs) -> Select:
        if not self:
            return sa_query

        return sa_query.where(
            self.data.compile(self.join_map.aliased_table_map)
        )
