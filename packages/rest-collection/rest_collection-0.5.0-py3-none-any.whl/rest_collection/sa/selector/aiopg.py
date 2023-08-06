from contextlib import suppress
from typing import List, Optional

from sqlalchemy import func, select

from .abc import AbstractAsyncSqlalchemySelector
from .mixin import SqlalchemySelectorMixin

__all__ = [

]


with suppress(ImportError):
    # We don`t know was aiopg installed or not.
    # So, we suppress ImportError if not.
    from aiopg.sa import Engine
    from aiopg.sa.result import RowProxy

    __all__.append('AiopgSqlalchemySelector')

    class AiopgSqlalchemySelector(SqlalchemySelectorMixin,
                                  AbstractAsyncSqlalchemySelector[Engine]):
        """Async aiopg-based selector."""
        __slots__ = ()

        async def select(self, *args, **kwargs) -> List[RowProxy]:
            sa_query = self.get_query()

            async with self._sa_engine.acquire() as conn:
                result_proxy = await conn.execute(sa_query)
                return await result_proxy.fetchall()

        async def count(self, *args, **kwargs) -> Optional[int]:
            sa_query = self.get_query(for_counting=True)
            sa_query = select([func.count()]).select_from(sa_query.alias())

            async with self._sa_engine.acquire() as conn:
                result_proxy = await conn.execute(sa_query)
                return await result_proxy.scalar()
