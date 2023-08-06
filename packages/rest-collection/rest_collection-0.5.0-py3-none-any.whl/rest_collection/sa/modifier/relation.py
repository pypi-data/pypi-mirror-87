from sqlalchemy.sql import Select

from rest_collection.api import AbstractApiRelationRequestContext
from .abc import AbstractSaQueryModifier

__all__ = [
    'SaQueryRelationModifier',
]


class SaQueryRelationModifier(
    AbstractSaQueryModifier[AbstractApiRelationRequestContext]
):
    __slots__ = ()

    def fill_join_map(self) -> None:
        if self:
            for api_pointer, innerjoin in \
                    self.data.relation_pointers.items():

                self.join_map.add_pointer(
                    api_pointer,
                    innerjoin=innerjoin,
                    strict_outerjoin=not innerjoin
                )

    def modify(self, sa_query: Select) -> Select:
        join_map = self.join_map

        if not join_map:
            return sa_query

        return sa_query.select_from(join_map.join_clause.clause)
