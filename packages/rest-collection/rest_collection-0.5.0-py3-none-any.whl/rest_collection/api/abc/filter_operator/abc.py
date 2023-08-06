from abc import ABCMeta, abstractmethod
from collections import namedtuple
from typing import Any, Callable, Dict, Iterator, Mapping, Optional, Tuple, Type
from weakref import ref

from sqlalchemy import Column
from sqlalchemy.sql.elements import BinaryExpression

from rest_collection.typing import ApiOperatorType
from .deserializer import api_operator_deserializer, \
    api_operator_set_deserializer
from ...exc import ApiFilterOperatorError

__all__ = [
    'AbstractApiOperatorRegistry',
    'AbstractApiOperator',
    'AbstractApiSimpleOperator',
    'AbstractApiSetOperator',
]


_SplitedArguments = namedtuple('SplitedArguments', ('args', 'kwargs'))
_DeserializerType = Callable[..., Any]


class _ApiOperatorMeta(ABCMeta):
    """
    Api operator metaclass.
    """

    # We use metaclass attribute as map, shared between all instances of all
    # classes.
    _deserializer_map = {
        None: api_operator_deserializer,
    }  # type: Dict[Optional[Type], _DeserializerType]

    def __init__(cls, name: str, bases: Tuple, namespace: Dict) -> None:
        super().__init__(name, bases, namespace)
        cls._deserializer = None  # type: Optional[_DeserializerType]

    def set_deserializer(cls,
                         deserializer: _DeserializerType,
                         default: bool = False,
                         descent: bool = False) -> None:
        if not descent and not default:
            # Individual deserializer works within class.
            cls._deserializer = deserializer
            return

        # Reseting individual deserializer, if it was set earlier.
        cls._deserializer = None
        deserializer_map = cls.__class__._deserializer_map

        if descent:
            # Class tree available deserializer.
            deserializer_map[cls] = deserializer
            return

        if cls in deserializer_map:
            # noinspection PyTypeChecker
            del deserializer_map[cls]

        # Default deserializer for all classes.
        deserializer_map[None] = deserializer

    @property
    def deserializer(cls) -> _DeserializerType:
        if cls._deserializer is not None:
            # Class has individual deserializer.
            return cls._deserializer

        mro = cls.__mro__
        deserializer_map = cls.__class__._deserializer_map

        for mro_cls in mro:
            if mro_cls in deserializer_map:
                # There is deserializer in shared deserializer map,
                # that suites over inheritance hierarchy.
                return deserializer_map[mro_cls]

        # Default deserializer for all classes.
        return deserializer_map[None]


class AbstractApiOperator(metaclass=_ApiOperatorMeta):
    """
    Abstract API operator class.
    """
    __slots__ = '_registry_ref', '_key'

    def __init__(self,
                 key: str,
                 operator_registry: 'AbstractApiOperatorRegistry') -> None:
        self._registry_ref = ref(operator_registry)
        self._key = key

    @property
    def registry(self) -> Optional['AbstractApiOperatorRegistry']:
        return self._registry_ref()

    @property
    def key(self) -> str:
        return self._key

    name = key

    @abstractmethod
    def _deserialize(self,
                     column_type: Type,
                     raw_value: Any,
                     *args,
                     **kwargs) -> Any:
        """Deserialization of raw value."""

    @staticmethod
    def _get_deserialize_result(*args, **kwargs) -> _SplitedArguments:
        return _SplitedArguments(args, kwargs)

    def deserialize(self,
                    column_type: Type,
                    raw_value,
                    *args,
                    **kwargs) -> _SplitedArguments:
        try:
            result = self._deserialize(column_type, raw_value, *args, **kwargs)

        except Exception as err:
            raise ApiFilterOperatorError(
                'Unable to parse operator %r value %r.' % (self._key, raw_value)
            ) from err

        if isinstance(result, _SplitedArguments):
            return result

        if isinstance(result, Mapping):
            return _SplitedArguments((), result)

        if isinstance(result, tuple):
            # "2-place tuple" case from tuple of dict is not taken into account.
            return _SplitedArguments(result, {})

        return _SplitedArguments((result,), {})

    @property
    @abstractmethod
    def operator(self) -> ApiOperatorType: ...

    def __call__(self, sa_column: Column, raw_value: Any) -> BinaryExpression:
        result = self.deserialize(sa_column.type.python_type, raw_value)
        return self.operator(sa_column, *result.args, **result.kwargs)

    @classmethod
    def register(
        cls,
        key: str,
        operator_registry: 'AbstractApiOperatorRegistry'
    ) -> 'AbstractApiOperator':
        if key in operator_registry and isinstance(
            operator_registry[key], cls
        ):
            # Different operators must be declared with different classes.
            # Otherwise, if operator was changed in new inheritor class,
            # it will not be added to operator registry. It is because there
            # is no checking of operator modification in current condition.
            return operator_registry[key]

        item = cls(key, operator_registry)
        operator_registry.register(item.key, item)
        return item

    def __repr__(self) -> str:
        return '<%s key=%s operator=%s>' % (
            self.__class__.__name__,
            self._key,
            self.operator.__name__
        )


class AbstractApiSimpleOperator(AbstractApiOperator):
    """Abstract simple API operator with default deserializer."""
    __slots__ = ()

    @property
    @abstractmethod
    def operator(self) -> ApiOperatorType: ...

    def _deserialize(self,
                     column_type: Type,
                     raw_value: Any,
                     *args,
                     **kwargs) -> _SplitedArguments:
        deserializer = self.__class__.deserializer
        # noinspection PyCallingNonCallable
        return self._get_deserialize_result(
            deserializer(column_type, raw_value)
        )


class AbstractApiSetOperator(AbstractApiSimpleOperator):
    """Abstract simple API operator for data collectons (sets)."""
    __slots__ = ()

    @property
    @abstractmethod
    def operator(self) -> ApiOperatorType: ...


# AbstrastApiSetOperator is registering for inheritors tree.
AbstractApiSetOperator.set_deserializer(
    api_operator_set_deserializer, descent=True
)


class AbstractApiOperatorRegistry(Mapping[str, AbstractApiOperator]):
    """
    Abstract API operator registry container.
    """
    __slots__ = '_data', '__weakref__'

    def __init__(self) -> None:
        self._data = {}  # type: Dict[str, AbstractApiOperator]

    def __getitem__(self, key: str) -> AbstractApiOperator:
        return self._data[key]

    def __len__(self) -> int:
        return len(self._data)

    def __iter__(self) -> Iterator[str]:
        return iter(self._data)

    def register(self, key: str, operator: AbstractApiOperator) -> None:
        assert isinstance(key, str), 'Key must be a string.'
        assert isinstance(
            operator, AbstractApiOperator
        ), 'Operator must be an object of type %r.' % \
            AbstractApiOperator.__name__
        self._data[key] = operator

    def __call__(self,
                 key: str,
                 sa_column: Column,
                 raw_value: Any) -> BinaryExpression:
        assert isinstance(sa_column, Column), \
            'Column must be an object of type sqlalchemy.Column.'
        return self._data[key](sa_column, raw_value)
