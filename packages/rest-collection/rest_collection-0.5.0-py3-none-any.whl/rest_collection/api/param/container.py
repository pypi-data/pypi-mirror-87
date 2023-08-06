from typing import Any, Iterable, Iterator, Tuple

__all__ = [
    'ApiParam',
]


class ApiParam(Iterable[Any]):
    """Representation of API param."""
    __slots__ = 'name', 'value'

    def __init__(self, name: str, value: Any) -> None:
        self.name = name.lower().strip()
        self.value = value

    @property
    def key(self) -> str:
        return self.name

    @key.setter
    def key(self, value: str) -> None:
        self.name = value

    def __iter__(self) -> Iterator[Any]:
        yield self.name
        yield self.value

    def __repr__(self) -> str:
        return '<%s name=%s value=%s>' % (
            self.__class__.__name__,
            repr(self.name),
            repr(self.value)
        )

    @classmethod
    def from_tuple(cls, tuple_: Tuple[str, Any]) -> 'ApiParam':
        return cls(*tuple_)
