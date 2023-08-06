from abc import abstractmethod
from typing import Generic, Optional
from weakref import ref

from sqlalchemy.sql import Select

from rest_collection.typing import ApiContextType
from ..container import JoinMap

__all__ = [
    'AbstractSaQueryModifier',
]


class AbstractSaQueryModifier(Generic[ApiContextType]):
    """
    Модификатор запроса
    """
    __slots__ = '_data_ref', '_join_map_ref'

    def __init__(self,
                 api_context: ApiContextType,
                 join_map: JoinMap) -> None:
        self._data_ref = ref(api_context)
        self._join_map_ref = ref(join_map)

    @property
    def data(self) -> Optional[ApiContextType]:
        return self._data_ref()

    @property
    def join_map(self) -> JoinMap:
        return self._join_map_ref()

    @abstractmethod
    def fill_join_map(self) -> None: ...

    @abstractmethod
    def modify(self, sa_query: Select) -> Select: ...

    def __call__(self, *args, **kwargs) -> Select:
        return self.modify(*args, **kwargs)

    def __bool__(self) -> bool:
        return bool(self.data)
