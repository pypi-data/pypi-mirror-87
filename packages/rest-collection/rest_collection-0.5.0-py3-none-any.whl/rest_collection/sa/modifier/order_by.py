from sqlalchemy.sql import Select

from rest_collection.api import AbstractApiOrderByRequestContext
from .abc import AbstractSaQueryModifier

__all__ = [
    'SaQueryOrderByModifier',
]


class SaQueryOrderByModifier(
    AbstractSaQueryModifier[AbstractApiOrderByRequestContext]
):
    __slots__ = ()

    def fill_join_map(self) -> None:
        if not self:
            return

        for api_pointer in self.data:
            self.join_map.add_pointer(api_pointer)

    def modify(self, sa_query: Select, **kwargs) -> Select:
        if not self:
            return sa_query

        aliased_table_map = self.join_map.aliased_table_map
        return sa_query.order_by(*(
            direction.compile(api_pointer, aliased_table_map)
            for api_pointer, direction in self.data.items()
        ))
