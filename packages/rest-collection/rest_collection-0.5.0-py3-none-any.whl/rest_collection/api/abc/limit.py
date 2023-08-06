from abc import abstractmethod
from typing import Any, Optional

from .request import AbstractApiRequest, AbstractApiRequestContext

__all__ = [
    'AbstractApiLimitRequestContext'
]


class AbstractApiLimitRequestContext(AbstractApiRequestContext):

    __slots__ = '_start', '_stop'

    def __init__(self, request: AbstractApiRequest) -> None:
        self._start = None
        self._stop = None
        super().__init__(request)

    @abstractmethod
    def _initialize(self) -> None: ...

    def __repr__(self) -> str:
        return '<%s (start=%s, stop=%s)' % (
            self.__class__.__name__, self._start, self._stop
        )

    @property
    def start(self) -> int:
        return self._start or 0

    @property
    def stop(self) -> Optional[int]:
        return self._stop

    @property
    def limit(self) -> Optional[int]:
        if isinstance(self._stop, int):
            return self._stop - self.start

    def __len__(self) -> Optional[int]:
        return self.limit

    def __eq__(self, other: Any) -> bool:
        return (
            isinstance(other, self.__class__) and
            self._start == other.start and
            self._stop == other.stop
        )

    def __bool__(self) -> bool:
        return bool(self._start or self._stop)
