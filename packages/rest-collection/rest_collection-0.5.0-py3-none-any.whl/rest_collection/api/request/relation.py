from rest_collection.container import Aliases
from ..abc import AbstractApiRelationRequestContext
from ..exc import ApiError, ApiRelationError
from ..param import ApiContextParamBlocks, ApiContextParamSchema, \
    ApiContextParamSchemaNode, ApiParam
from ..utils import as_bool

__all__ = [
    'ApiRelationRequestContext',
]


def _normalize_strict(url_param: ApiParam) -> bool:
    return as_bool(url_param.value)


class ApiRelationRequestContext(AbstractApiRelationRequestContext):
    __slots__ = ()

    _url_param_schema = ApiContextParamSchema(
        ApiContextParamSchemaNode(Aliases('with', 'include')),
        ApiContextParamSchemaNode(
            Aliases('with_strict', 'include_strict'),
            normalizer=_normalize_strict,
            block_default=True
        )
    )

    def _initialize(self) -> None:
        # Let`s filter only "relation" context request parameters.
        url_param_schema = self.__class__._url_param_schema

        relation_param_blocks = ApiContextParamBlocks(
            self.request, url_param_schema
        )

        for relation_url_param, strict_url_param in relation_param_blocks:

            try:
                relation_url_pointer = self.pointer_registry[
                    relation_url_param.value
                ]
            except ApiError as err:
                raise ApiRelationError(
                    'Invalid identity of related model was defined.'
                ) from err

            if relation_url_pointer.sa_relationship is None:
                raise ApiRelationError(
                    'Related model can not be a column.'
                )

            self._relation_pointers[relation_url_pointer] = \
                strict_url_param.value
