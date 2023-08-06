from abc import ABCMeta, abstractmethod
from typing import Any, Callable, Iterable, Iterator, Optional, Set, \
    TYPE_CHECKING, Tuple
from urllib.parse import parse_qsl
from weakref import ref

from sqlalchemy.ext.declarative import DeclarativeMeta

from .filter_operator import AbstractApiOperatorRegistry
from ..param import ApiParam
from ..pointer import ApiPointer, ApiPointerRegistry

if TYPE_CHECKING:
    from .filter import AbstractApiFilterRequestContext
    from .limit import AbstractApiLimitRequestContext
    from .order_by import AbstractApiOrderByRequestContext
    from .relation import AbstractApiRelationRequestContext


__all__ = [
    'AbstractApiRequestContext',
    'AbstractApiRequest',
]


class AbstractApiRequestContext(object, metaclass=ABCMeta):
    """
    Abstract API request context.
    """
    __slots__ = '_request_ref', '__weakref__'

    def __init__(self, request: 'AbstractApiRequest') -> None:
        super().__init__()
        self._request_ref = ref(request)
        self._initialize()

    @abstractmethod
    def _initialize(self) -> None: ...

    @property
    def request(self) -> Optional['AbstractApiRequest']:
        return self._request_ref()

    @property
    def pointer_registry(self) -> ApiPointerRegistry:
        return getattr(self.request, 'pointer_registry')


def _iter_values(values: Iterable) -> Iterator[Any]:
    """Values iteration."""
    for value in values:
        if isinstance(value, Iterable) and not isinstance(value, str):
            yield from iter(value)

        else:
            yield value


class AbstractApiRequest(metaclass=ABCMeta):
    """Abstract API request."""

    __slots__ = (
        '_pointer_registry',
        '_params',
        '_operator_registry',
        '__weakref__',
    )

    def __init__(
        self,
        query_str: str,
        api_pointer_registry: ApiPointerRegistry,
        api_operator_registry: Optional[
            'AbstractApiOperatorRegistry'
        ] = None
    ):
        if api_operator_registry is None:
            from ..filter_operator import API_OPERATOR_REGISTRY
            api_operator_registry = API_OPERATOR_REGISTRY

        self._pointer_registry = api_pointer_registry
        self._operator_registry = api_operator_registry
        self._params = tuple(map(ApiParam.from_tuple, parse_qsl(query_str)))

    @property
    def params(self) -> Tuple[ApiParam, ...]:
        """Request params."""
        return self._params

    @property
    def pointer_registry(self) -> ApiPointerRegistry:
        """API pointer registry."""
        return self._pointer_registry

    @property
    def pointer_factory(self) -> Callable[[str], ApiPointer]:
        """API pointer factory."""
        return self._pointer_registry.factory

    @property
    def operator_registry(self) -> 'AbstractApiOperatorRegistry':
        """Filter operator registry."""
        return self._operator_registry

    @property
    def root_sa_cls(self) -> DeclarativeMeta:
        return self._pointer_registry.sa_cls

    def filter_params(self, param_names: Set[str]) -> Tuple[ApiParam, ...]:
        """Request params filtering."""
        return tuple(filter(lambda x: x.name in param_names, self._params))

    @staticmethod
    def get_first_param(url_params: Iterable[ApiParam],
                        param_names: Set[str]) -> Optional[ApiParam]:
        try:
            return next(filter(
                lambda x: x.name in param_names, url_params
            )).value
        except (StopIteration, AttributeError):
            pass

    @property
    @abstractmethod
    def order_by(self) -> 'AbstractApiOrderByRequestContext': ...

    @property
    @abstractmethod
    def limit(self) -> 'AbstractApiLimitRequestContext': ...

    @property
    @abstractmethod
    def relation(self) -> 'AbstractApiRelationRequestContext': ...

    @property
    @abstractmethod
    def filter(self) -> 'AbstractApiFilterRequestContext': ...
