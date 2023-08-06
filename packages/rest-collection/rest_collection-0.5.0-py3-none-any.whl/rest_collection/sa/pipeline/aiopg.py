from contextlib import suppress

from sqlalchemy.ext.declarative import DeclarativeMeta

from rest_collection.api import ApiPointerRegistry, ApiRequest
from ..container import PipelineResult
from ..grouper import SqlalchemyGrouper

__all__ = [

]


with suppress(ImportError):
    from aiopg.sa import Engine
    from ..selector import AiopgSqlalchemySelector

    __all__.append('aiopg_select_and_group')

    async def aiopg_select_and_group(query_string: str,
                                     sa_cls: DeclarativeMeta,
                                     sa_engine: Engine) -> PipelineResult:
        """Pipeline for selecting and grouping of data, based on aiopg."""
        api_request = ApiRequest(
            query_string, ApiPointerRegistry(sa_cls)
        )

        selector = AiopgSqlalchemySelector.from_api_request(
            sa_engine, api_request
        )

        data = SqlalchemyGrouper.from_select_collection(
            selector.select_collection
        ).group(await selector.select())

        return PipelineResult(data, await selector.count())
