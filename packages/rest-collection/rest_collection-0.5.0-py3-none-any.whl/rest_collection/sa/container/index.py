from typing import Iterator, Tuple, Sequence

from sqlalchemy import Table, Column

__all__ = [
    'TableIndices',
]


class _ItemGetter(object):
    """Реализация operator.itemgetter, возвращающая только кортежи."""
    def __init__(self, *items: int) -> None:
        self._items = items

    def __call__(self, data: Sequence) -> Tuple:
        return tuple(map(lambda item: data[item], self._items))


class TableIndices(object):
    """Определяющий индексы колонок таблиц контейнер."""
    __slots__ = '_table',

    def __init__(self, sa_table: Table) -> None:
        self._table = sa_table

    def _iter_columns(self, offset: int) -> Iterator[Column]:
        return enumerate(self._table.columns, start=offset)

    def get_indices(self, offset: int = 0) -> Tuple[int, ...]:
        return tuple(i for i, _ in self._iter_columns(offset=offset))

    def get_primary_indices(self, offset: int = 0) -> Tuple[int, ...]:
        return tuple(
            i for i, column in self._iter_columns(offset=offset)
            if column.primary_key is True
        )

    def primary_getter(self, offset: int = 0) -> _ItemGetter:
        return _ItemGetter(*self.get_primary_indices(offset=offset))

    def getter(self, offset: int = 0) -> _ItemGetter:
        return _ItemGetter(*self.get_indices(offset=offset))
