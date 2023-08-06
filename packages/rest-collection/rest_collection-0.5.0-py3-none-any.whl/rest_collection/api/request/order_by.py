from typing import Any

from rest_collection.container import Aliases
from ..abc import AbstractApiOrderByRequestContext
from ..exc import ApiOrderByError
from ..order_by import ApiOrderByDirection
from ..param import ApiContextParamBlocks, ApiContextParamSchema, \
    ApiContextParamSchemaNode, ApiParam
from ..utils import as_bool

__all__ = [
    'ApiOrderByRequestContext',
]


_NORMALIZE_ASC_MAP = {
    'asc': as_bool,
    'desc': lambda value: not as_bool(value),
    'sort': as_bool,
}


def _normalize_asc(url_param: ApiParam) -> Any:
    normalizer = _NORMALIZE_ASC_MAP[url_param.name]
    return normalizer(url_param.value)


class ApiOrderByRequestContext(AbstractApiOrderByRequestContext):
    """
    API order by request context.
    """
    __slots__ = ()

    _url_param_schema = ApiContextParamSchema(
        ApiContextParamSchemaNode(Aliases('order_by', 'sort_by')),
        ApiContextParamSchemaNode(
            Aliases('asc', 'desc', 'sort'),
            normalizer=_normalize_asc,
            block_default=True
        )
    )

    def _initialize(self) -> None:
        # Let`s filter only "order_by" context request parameters.
        url_param_schema = self.__class__._url_param_schema

        order_by_param_blocks = ApiContextParamBlocks(
            self.request, url_param_schema
        )

        for order_by_url_param, asc_url_param in order_by_param_blocks:
            order_by = self.pointer_registry[order_by_url_param.value]

            if order_by in self._data:
                # Omit identities, that already handled.
                continue

            if order_by.sa_column is None:
                raise ApiOrderByError(
                    'Identities of columns only are allowed for sorting '
                    'purposes. Relationship %r is not sortable.' %
                    order_by.identity
                )

            self._data[order_by] = ApiOrderByDirection(
                order_by.sa_column, asc_url_param.value
            )
