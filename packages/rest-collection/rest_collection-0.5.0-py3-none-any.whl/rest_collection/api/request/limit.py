from rest_collection.container import Aliases
from ..abc import AbstractApiLimitRequestContext
from ..exc import ApiLimitError
from ..param import ApiContextParamSchema, ApiContextParamSchemaNode, \
    ApiContextParams, ApiParam

__all__ = [
    'ApiLimitRequestContext'
]


def _normalize_limit(url_param: ApiParam) -> int:
    try:
        return abs(int(url_param.value))

    except (TypeError, ValueError) as err:
        raise ApiLimitError(
            'Only non-negative numbers must be used as limit params.'
        ) from err


class ApiLimitRequestContext(AbstractApiLimitRequestContext):
    __slots__ = ()

    _url_param_schema = ApiContextParamSchema(
        ApiContextParamSchemaNode(Aliases('start'), _normalize_limit),
        ApiContextParamSchemaNode(Aliases('stop'), _normalize_limit)
    )

    def _initialize(self) -> None:
        # Let`s filter only "limit" context request parameters.
        url_param_schema = self.__class__._url_param_schema
        context_url_params = ApiContextParams(self.request, url_param_schema)

        start_url_param = context_url_params.get_first(
            url_param_schema.main_for('start')
        )
        stop_url_param = context_url_params.get_first(
            url_param_schema.main_for('stop')
        )

        if start_url_param is not None:
            self._start = start_url_param.value

        if stop_url_param is not None:
            self._stop = stop_url_param.value

        limit = self.limit
        if limit and limit < 0:
            raise ApiLimitError('Stop limit position must be '
                                'greater, than start limit '
                                'position.')
