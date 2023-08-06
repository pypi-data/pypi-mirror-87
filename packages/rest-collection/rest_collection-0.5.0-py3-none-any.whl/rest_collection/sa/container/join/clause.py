from typing import Callable, Tuple, Union, overload
from weakref import WeakSet

from sqlalchemy import Table
from sqlalchemy.sql import Alias, Join
from sqlalchemy.sql.elements import AnnotatedColumnElement, BinaryExpression

from rest_collection.api import AliasedTableMap, ApiPointer

__all__ = [
    'JoinClause'
]


def _find_left_right(
    left_table: Table,
    join_expression: BinaryExpression
) -> Tuple[AnnotatedColumnElement, AnnotatedColumnElement]:
    left = join_expression.left
    right = join_expression.right

    if left.table == left_table:
        return left, right

    return right, left


class JoinClause(object):
    """Конструктор выражения join."""
    __slots__ = '_joined', '_clause', '_aliased_table_map'

    def __init__(self,
                 aliased_table_map: AliasedTableMap) -> None:
        # Набор таблиц, которые были пристыкованы.
        self._joined = WeakSet()  # type: WeakSet

        # Само выражение.
        self._clause = None

        self._aliased_table_map = aliased_table_map

    @overload
    def _add_joined(self, joined: Table) -> Table: ...

    @overload
    def _add_joined(self, joined: Alias) -> Alias: ...

    def _add_joined(self, joined):
        self._joined.add(joined)
        return joined

    def apply(
        self,
        api_pointer: ApiPointer,
        join_fn: Callable[..., Join],
    ) -> Union[Join, Table]:
        # Применение сущности отношения на уже составленное JOIN выражение
        sa_relationship = api_pointer.sa_relationship
        primaryjoin = sa_relationship.primaryjoin
        secondaryjoin = sa_relationship.secondaryjoin

        left_column, right_column = _find_left_right(
            api_pointer.sa_cls.__table__,
            primaryjoin,
        )

        if self._clause is None:
            # Expression is not initialized, we add root table without aliasing.
            self._clause = self._add_joined(left_column.table)

        if api_pointer.parent is not None:
            # If it is not root table related model, we need to obtain
            # aliased annotated column for left side of join.
            # For root table related models, we just take column from
            # primaryjoin, because, we don`t setting alias for root model.
            left_column = self._aliased_table_map[
                api_pointer.parent
            ].columns[left_column.key]

        if secondaryjoin is None:
            # If secondaryjoin is ``None``, we have plain joining, so we need
            # aliased table from map.
            right_table = self._aliased_table_map[api_pointer]

            if right_table in self._joined:
                return self._clause

            secondary_table = None

            # Getting aliased column.
            right_column = right_table.columns[right_column.key]

        else:
            secondary_table = self._aliased_table_map[api_pointer]

            if secondary_table in self._joined:
                return self._clause

            # If we have secondaryjoin, right table of primary join is a
            # relation table for many to many relationship. There is no
            # necessity for aliasing it (now).
            # todo: Detect if relation tables need aliasing too.
            right_table = right_column.table

        self._add_joined(right_table)

        self._clause = join_fn(
            self._clause,
            right_table,
            onclause=left_column == right_column,
        )

        if secondary_table is None:
            return self._clause

        secondary_left_column, secondary_right_column = _find_left_right(
            sa_relationship.target,
            secondaryjoin,
        )

        # With aliasing model there is a feature for many-to-many models. They
        # now can include twicely into statement now, because including via
        # many-to-many secondary join does not make alias for relation model,
        # and then, when it includes directly, in includes as one more model.
        self._clause = join_fn(
            self._clause,
            self._add_joined(secondary_table),
            onclause=secondary_table.columns[
                secondary_left_column.key
            ] == secondary_right_column,
        )
        return self._clause

    @property
    def clause(self) -> Union[Join, Table]:
        return self._clause

    def __repr__(self) -> str:
        return '<%s clause=%s>' % (self.__class__.__name__, repr(self._clause))
