from contextlib import closing
from typing import List, Optional

from sqlalchemy import func, select
from sqlalchemy.engine import Engine, RowProxy

from .abc import AbstractSqlalchemySelector
from .mixin import SqlalchemySelectorMixin

__all__ = [
    'SqlalchemySelector',
]


class SqlalchemySelector(SqlalchemySelectorMixin,
                         AbstractSqlalchemySelector[Engine]):
    """Sync selector."""
    __slots__ = ()

    def select(self, *args, **kwargs) -> List[RowProxy]:
        sa_query = self.get_query()

        with closing(self._sa_engine.connect()) as conn:
            return conn.execute(sa_query).fetchall()

    def count(self, *args, **kwargs) -> Optional[int]:
        sa_query = self.get_query(for_counting=True)
        sa_query = select([func.count()]).select_from(sa_query.alias())

        with closing(self._sa_engine.connect()) as conn:
            return conn.execute(sa_query).scalar()
