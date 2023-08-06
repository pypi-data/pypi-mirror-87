from itertools import zip_longest
from typing import Any, Generic, Iterator, Optional, Sequence, TYPE_CHECKING, \
    Tuple, TypeVar

from rest_collection.container import Chunked
from .container import ApiParam
from .schema import ApiContextParamSchema

if TYPE_CHECKING:
    from ..abc import AbstractApiRequest


__all__ = [
    'ApiContextParams',
    'ApiContextParamBlocks',
]


_ApiContextParamsDataType = TypeVar(
    '_ApiContextParamsDataType', bound=Tuple[Any, ...]
)


class _BaseApiContextParams(Generic[_ApiContextParamsDataType]):
    __slots__ = '_data', '_schema'

    def __init__(self,
                 request: 'AbstractApiRequest',
                 url_param_schema: ApiContextParamSchema) -> None:
        from ..abc import AbstractApiRequest
        assert isinstance(request, AbstractApiRequest)
        assert isinstance(url_param_schema, ApiContextParamSchema)

        self._schema = url_param_schema
        self._data = self._get_data(request)

    def _get_data(self,
                  request: 'AbstractApiRequest') -> _ApiContextParamsDataType:
        url_params = tuple(filter(
            lambda x: x.name in self._schema, request.params
        ))

        for url_param in url_params:
            self._schema.normalize(url_param)

        return url_params


class ApiContextParams(_BaseApiContextParams[Tuple[ApiParam, ...]],
                       Sequence[ApiParam]):
    """Representation of sequence of API params."""
    __slots__ = ()

    def __getitem__(self, index: int) -> ApiParam:
        return self._data[index]

    def __len__(self) -> int:
        return len(self._data)

    def _filter(self, param_name: str) -> Iterator[ApiParam]:
        return filter(lambda x: x.name == param_name, self._data)

    def get_only(self, param_name: str) -> Tuple[ApiParam, ...]:
        return tuple(self._filter(param_name))

    def get_first(self, param_name: str) -> Optional[ApiParam]:
        try:
            return next(self._filter(param_name))
        except StopIteration:
            pass


class ApiContextParamBlocks(
    _BaseApiContextParams[Tuple[Tuple[ApiParam, ...], ...]],
    Sequence
):
    """Representation of block of API params."""
    __slots__ = ()

    def _get_data(
        self,
        request: 'AbstractApiRequest'
    ) -> Tuple[Tuple[ApiParam, ...], ...]:
        url_params = super()._get_data(request)

        chunked_url_params = Chunked(
            lambda url_param: url_param.name == self._schema.first_node.name,
            url_params
        )

        return tuple(
            tuple(
                ApiParam(
                    node.name, node.block_default
                ) if url_param is None else url_param

                for url_param, node in zip_longest(
                    url_params_chunk, self._schema.nodes
                )
            ) for url_params_chunk in chunked_url_params
        )

    def __getitem__(self, index: int) -> Tuple[ApiParam, ...]:
        return self._data[index]

    def __len__(self) -> int:
        return len(self._data)
