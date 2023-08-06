from typing import Any, Callable, Iterable, Iterator, Sequence, Tuple

__all__ = [
    'Chunk',
    'Chunked',
]


class Chunk(Iterable[Any]):
    __slots__ = '_data', '_condition', '_condition_fulfilled'

    def __init__(self,
                 condition: Callable[[Any], Any],
                 data: Sequence[Any]) -> None:
        self._data = data
        self._condition = condition
        self._condition_fulfilled = False

    def __iter__(self) -> Iterator[Any]:
        for item in self._data:

            result = self._condition(item)

            if self._condition_fulfilled:
                if result:
                    break

                yield item

            if result:
                self._condition_fulfilled = True
                yield item


class Chunked(Iterator):
    __slots__ = '_data', '_condition', '_index'

    def __init__(self,
                 condition: Callable[[Any], Any],
                 data: Sequence[Any]) -> None:
        self._data = tuple(data)
        self._condition = condition
        self._index = 0

    def __next__(self) -> Tuple[Any, ...]:
        chunk = tuple(Chunk(self._condition, self._data[self._index:]))

        if not chunk:
            raise StopIteration()

        self._index += len(chunk)
        return chunk
