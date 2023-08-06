from functools import total_ordering
from typing import Any, Optional, Sequence, Tuple

from ..exc import ApiIdentityError

__all__ = [
    'ApiIdentity',
]


@total_ordering
class ApiIdentity(Sequence[str]):
    """API string identity of model."""
    __slots__ = '_parts', '_str'

    def __init__(self,
                 identity: str,
                 parts: Optional[Tuple[str, ...]] = None) -> None:

        if not identity and not parts:
            raise ApiIdentityError('Identity can not be empty.')

        elif not isinstance(identity, str):
            raise ApiIdentityError('Identity must be a string.')

        # Validation of "parts" argument is not performing.
        # This argument was implemented only for simplier sub identity
        # initialization.
        self._parts = parts or tuple(identity.split('.'))
        self._str = identity

    @property
    def parts(self) -> Tuple[str, ...]:
        return self._parts

    @property
    def last(self) -> str:
        return self._parts[-1]

    @property
    def first(self) -> str:
        return self._parts[0]

    def __str__(self) -> str:
        return self._str

    def __eq__(self, other: Any) -> bool:
        return self._str == str(other)

    def __hash__(self) -> int:
        return hash(self._str)

    def __len__(self) -> int:
        return len(self._parts)

    def __getitem__(self, index: int) -> str:
        return self._parts[index]

    def slice(self, start: int = 0, stop: int = 1) -> 'ApiIdentity':
        if start == 0 and stop == len(self._parts):
            return self

        parts = self._parts[start:stop]
        identity = '.'.join(parts)
        return self.__class__(
            identity,
            parts=parts,
        )

    def __repr__(self) -> str:
        return '<%s str=%s>' % (self.__class__.__name__, self._str)

    def __gt__(self, other: Any) -> bool:
        return self._str > str(other)
