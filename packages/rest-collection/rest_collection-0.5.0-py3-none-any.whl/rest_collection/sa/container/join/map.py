from itertools import chain, takewhile
from operator import attrgetter
from typing import Callable, Iterator, Mapping, Set, Tuple
from weakref import WeakKeyDictionary, WeakSet

from sqlalchemy import join, outerjoin
from sqlalchemy.sql import Join

from rest_collection.api import AliasedTableMap, ApiPointer
from .clause import JoinClause

__all__ = [
    'JoinMap',
]


class JoinMap(Mapping[ApiPointer, Callable[..., Join]]):
    """
    Карта стыковки таблиц
    """

    __slots__ = (
        '_data',
        '__weakref__',
        '_strict_outerjoin',
        '_aliased_table_map',
    )

    def __init__(self, aliased_table_map: AliasedTableMap) -> None:
        self._data = WeakKeyDictionary()  # type: WeakKeyDictionary
        self._strict_outerjoin = WeakSet()  # type: WeakSet
        self._aliased_table_map = aliased_table_map

    def __len__(self) -> int:
        return len(self._data)

    def __getitem__(self, key: ApiPointer) -> Callable[..., Join]:
        value = self._data[key]
        if value:
            return join
        return outerjoin

    @property
    def aliased_table_map(self) -> AliasedTableMap:
        return self._aliased_table_map

    @property
    def roots(self) -> Set[ApiPointer]:
        return {pointer for pointer in self._data if pointer.parent is None}

    def _walk_pointer(
        self,
        api_pointer: ApiPointer,
    ) -> Iterator[ApiPointer]:
        yield api_pointer

        for child in sorted(
            api_pointer.childs, key=attrgetter('identity')
        ):
            if child not in self._data:
                continue

            yield from self._walk_pointer(child)

    def __iter__(self) -> Iterator[ApiPointer]:
        return iter(chain.from_iterable(map(
            self._walk_pointer,
            sorted(self.roots, key=attrgetter('identity')),
        )))

    def _process_existing_item(
        self,
        api_pointer: ApiPointer,
        innerjoin: bool,
        strict_outerjoin: bool,
    ) -> None:

        if not innerjoin and not strict_outerjoin:
            # Если нет требования обязательной стыковки по outerjoin,
            # то бессмысленно что-либо делать с существующими данными,
            # так как innerjoin мы не переписываем в более мягкое условие
            # outerjoin
            return

        self._data[api_pointer] = innerjoin

        if innerjoin:
            self._data.update(dict.fromkeys(api_pointer.parents, True))
            return

        self._strict_outerjoin.add(api_pointer)
        for child in api_pointer.childs:
            if child in self._data:
                self._strict_outerjoin.add(child)
                self._data[child] = False

    def _process_existing_parents(
        self,
        parents: Tuple[ApiPointer, ...],
        innerjoin: bool,
    ) -> Tuple[bool, bool]:

        existing_parent_in_strict_outerjoin = (
            parents[-1] in self._strict_outerjoin
        )

        # Если потомок стыкуется по innerjoin, то родители также должны быть
        # пристыкованы по innerjoin, исключая случай, когда ближайший
        # родитель из карты стыкуется по outerjoin.
        innerjoin = innerjoin and not existing_parent_in_strict_outerjoin

        if innerjoin:
            self._data.update(dict.fromkeys(parents, True))

        return innerjoin, existing_parent_in_strict_outerjoin

    def _process_new_parents(
        self,
        parents: Tuple[ApiPointer, ...],
        innerjoin: bool,
        existing_parent_in_strict_outerjoin: bool,
    ) -> None:

        self._data.update(dict.fromkeys(parents, innerjoin))

        if existing_parent_in_strict_outerjoin:
            self._strict_outerjoin.union(frozenset(parents))

    def add_pointer(
        self,
        api_pointer: ApiPointer,
        innerjoin: bool = False,
        strict_outerjoin: bool = False
    ) -> None:
        """
        Добавление указателя в карту стыковки таблиц.

        :param api_pointer: Указатель
        :param innerjoin: Определение типа стыковки
        :param strict_outerjoin: Форсирование нестрогой стыковки (
        по-умолчанию в приоритете строгая).

        Сущестует 5 случаев при добавлении указателя:
            - Указатель существует в карте и он должен быть выбран строго с
            помощью outerjoin
            - Указатель существует в карте
            - Указатель и его родители не существуют в карте
            - Один из родителей указателя существует в карте и он не обязан
            быть выбран с помощью outerjoin
            - Один из родителей указателя существует в карте и он обязан
            быть выбран с помощью outerjoin

        :return:
        """
        assert isinstance(api_pointer, ApiPointer), \
            'В качестве ключа ожидается экземпляр "%s".' % \
            ApiPointer.__name__
        assert isinstance(innerjoin, bool), \
            'Ожидаются только bool значения.'
        assert isinstance(strict_outerjoin, bool), \
            'Ожидаются только bool значения.'

        if api_pointer.sa_column is not None:
            # Колонки не могут участвовать в условии стыковки, преобразуем в
            # отношение.
            api_pointer = api_pointer.parent

        if api_pointer is None:
            # Была передана колонка корневой модели, игнорируем.
            return

        if api_pointer in self._strict_outerjoin:
            # Указатель уже отмечен как strict_outerjoin, изменять нечего.
            return

        if strict_outerjoin:
            # Форсируем устновку innerjoin в False (если вдруг он указан).
            innerjoin = False

        if api_pointer in self._data:
            self._process_existing_item(
                api_pointer, innerjoin, strict_outerjoin
            )
            return

        parents = api_pointer.parents

        # Собираем родителей, которые присутствуют в карте.
        parents_in_map = tuple(takewhile(
            lambda x: x in self._data, api_pointer.parents
        ))
        existing_parent_in_strict_outerjoin = False

        if parents_in_map:
            # Обработка существующих в карте родителей указателя.
            (
                innerjoin, existing_parent_in_strict_outerjoin
            ) = self._process_existing_parents(
                parents_in_map, innerjoin
            )

        # Собираем родителей, которых нет в карте.
        new_parents = parents[len(parents_in_map):]

        if new_parents:
            # Обрабатываем вновь добавляемых родителей указателя.
            self._process_new_parents(
                parents[len(parents_in_map):],
                innerjoin,
                existing_parent_in_strict_outerjoin
            )

        if strict_outerjoin or existing_parent_in_strict_outerjoin:
            # Добавляем указатель в список ограниченных условием стыковки
            # outerjoin.
            self._strict_outerjoin.add(api_pointer)

        # Добавляем в карту сам указатель
        self._data[api_pointer] = innerjoin

    @property
    def join_clause(self) -> JoinClause:
        join_clause = JoinClause(self._aliased_table_map)

        for api_pointer, join_fn in self.items():
            join_clause.apply(
                api_pointer,
                join_fn,
            )

        return join_clause
