from .filter import ApiFilterRequestContext
from .limit import ApiLimitRequestContext
from .order_by import ApiOrderByRequestContext
from .relation import ApiRelationRequestContext
from ..abc import AbstractApiRequest
from ..pointer import ApiPointerRegistry

__all__ = [
    'ApiRequest',
]


class ApiRequest(AbstractApiRequest):
    """API request."""
    __slots__ = '_relation', '_order_by', '_limit', '_filter'

    order_by_cls = ApiOrderByRequestContext
    limit_cls = ApiLimitRequestContext
    relation_cls = ApiRelationRequestContext
    filter_cls = ApiFilterRequestContext

    def __init__(self,
                 query_str: str,
                 url_pointer_registry: ApiPointerRegistry) -> None:
        super().__init__(query_str, url_pointer_registry)
        self._relation = self.__class__.relation_cls(self)
        self._order_by = self.__class__.order_by_cls(self)
        self._limit = self.__class__.limit_cls(self)
        self._filter = self.__class__.filter_cls(self)

    @property
    def order_by(self) -> ApiOrderByRequestContext:
        return self._order_by

    @property
    def limit(self) -> ApiLimitRequestContext:
        return self._limit

    @property
    def relation(self) -> ApiRelationRequestContext:
        return self._relation

    @property
    def filter(self) -> ApiFilterRequestContext:
        return self._filter
