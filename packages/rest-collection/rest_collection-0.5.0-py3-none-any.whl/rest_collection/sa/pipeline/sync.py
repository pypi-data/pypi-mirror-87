from sqlalchemy.engine import Engine
from sqlalchemy.ext.declarative import DeclarativeMeta

from rest_collection.api import ApiPointerRegistry, ApiRequest
from ..container import PipelineResult
from ..grouper import SqlalchemyGrouper
from ..selector import SqlalchemySelector

__all__ = [
    'select_and_group',
]


def select_and_group(query_string: str,
                     sa_cls: DeclarativeMeta,
                     sa_engine: Engine) -> PipelineResult:
    """Pipeline for sync selecting and grouping of data."""
    api_request = ApiRequest(
        query_string, ApiPointerRegistry(sa_cls)
    )

    selector = SqlalchemySelector.from_api_request(sa_engine, api_request)

    data = SqlalchemyGrouper.from_select_collection(
        selector.select_collection
    ).group(selector.select())

    return PipelineResult(data, selector.count())
