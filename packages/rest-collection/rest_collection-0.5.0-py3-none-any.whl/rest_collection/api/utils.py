from typing import Any

__all__ = [
    'as_bool'
]

_FALSY_STR = {'0', 'false', 'no', 'down'}


def as_bool(value: Any) -> bool:
    if not isinstance(value, str):
        return bool(value)

    return value.lower().strip() not in _FALSY_STR
