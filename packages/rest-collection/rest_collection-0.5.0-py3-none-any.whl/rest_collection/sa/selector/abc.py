from abc import abstractmethod
from typing import Any, Generic, List, Optional, Tuple

from sqlalchemy.sql import Select

from rest_collection.api import AbstractAliasMap, AbstractApiRequest, \
    AliasedTableMap, NumericAliasMap
from rest_collection.typing import SaEngineType
from ..container import JoinMap, SelectCollection
from ..modifier import AbstractSaQueryModifier

__all__ = [
    'AbstractSqlalchemySelector',
    'AbstractAsyncSqlalchemySelector',
]


class _AbstractSqlalchemySelector(Generic[SaEngineType]):
    """
    Base abstract selector.
    """
    __slots__ = (
        '_sa_engine',
        '_select_collection',
        '_modifiers',
        '_join_map',
    )

    def __new__(cls, *args, **kwargs):
        if cls is _AbstractSqlalchemySelector:
            # this class can not be initialized
            raise RuntimeError()

        return super().__new__(cls, *args, **kwargs)

    def __init__(self,
                 sa_engine: SaEngineType,
                 join_map: JoinMap,
                 modifiers: Tuple[AbstractSaQueryModifier, ...],
                 select_collection: SelectCollection) -> None:
        self._sa_engine = sa_engine
        self._join_map = join_map
        self._modifiers = modifiers
        self._select_collection = select_collection

    @property
    def select_collection(self) -> SelectCollection:
        return self._select_collection

    @abstractmethod
    def get_query(self, for_counting: bool = False) -> Select: ...

    @staticmethod
    @abstractmethod
    def _get_modifiers(
        join_map: JoinMap,
        api_request: AbstractApiRequest,
    ) -> Tuple[AbstractSaQueryModifier, ...]: ...

    @classmethod
    def from_api_request(cls,
                         sa_engine: SaEngineType,
                         api_request: AbstractApiRequest,
                         alias_map: Optional[AbstractAliasMap] = None):
        if alias_map is None:
            alias_map = NumericAliasMap()

        aliased_table_map = AliasedTableMap(alias_map)
        join_map = JoinMap(aliased_table_map)
        modifiers = cls._get_modifiers(join_map, api_request)

        for modifier in modifiers:
            modifier.fill_join_map()

        select_collection = SelectCollection.from_join_map(
            api_request.root_sa_cls.__table__,
            join_map,
        )
        return cls(sa_engine,
                   join_map,
                   modifiers,
                   select_collection)


class AbstractSqlalchemySelector(
    _AbstractSqlalchemySelector[SaEngineType]
):
    """
    Abstract sync selector.
    """
    __slots__ = ()

    @abstractmethod
    def select(self, *args, **kwargs) -> List[Any]: ...

    @abstractmethod
    def count(self, *args, **kwargs) -> Optional[int]: ...

    def __call__(self, *args, **kwargs) -> List[Any]:
        return self.select(*args, **kwargs)


class AbstractAsyncSqlalchemySelector(
    _AbstractSqlalchemySelector[SaEngineType]
):
    """
    Abstract async selector.
    """
    __slots__ = ()

    @abstractmethod
    async def select(self, *args, **kwargs) -> List[Any]: ...

    @abstractmethod
    async def count(self, *args, **kwargs) -> Optional[int]: ...

    async def __call__(self, *args, **kwargs) -> List[Any]:
        return await self.select(*args, **kwargs)
