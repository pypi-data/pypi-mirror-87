from datetime import datetime, time, timedelta
from functools import partial, singledispatch, update_wrapper
from json import loads
from typing import Any, Callable, FrozenSet, Optional, Type

from dateutil.parser import parse

__all__ = [
    'api_operator_deserializer',
    'api_operator_set_deserializer',
]


def _singledispatch(fn: Callable[..., Any]) -> Any:
    """
    Decorator for "single dispatch function", that define handler by first
    argument, but not by type of first argument (because first argument
    declares type itself already).
    """
    singledispatched_fn = singledispatch(fn)

    def wrapper(*args, **kwargs):
        return singledispatched_fn.dispatch(args[0])(*args, **kwargs)

    return update_wrapper(wrapper, singledispatched_fn)


def _value_or_none(value: Any, callback: Callable[[Any], Any]) -> Any:
    if value is None:
        return
    return callback(value)


@_singledispatch
def api_operator_deserializer(column_type: Type, raw_value: Any) -> Any:
    value = loads(raw_value)
    return _value_or_none(value, column_type)


@api_operator_deserializer.register(str)
def _str_deserializer(_, raw_value: Any) -> Optional[str]:
    value = str(raw_value)
    # null is a reserved word for NULL type.
    return value if value.lower() != 'null' else None


@api_operator_deserializer.register(time)
def _time_deserializer(_, raw_value: Any) -> time:
    # time parsing function
    value = parse(raw_value)
    return time(hour=value.hour, minute=value.minute, second=value.second)


@api_operator_deserializer.register(datetime)
def _datetime_deserializer(_, raw_value: Any) -> datetime:
    # date parsing function
    return parse(raw_value)


@api_operator_deserializer.register(timedelta)
def _timedelta_deserializer(_, raw_value: Any) -> timedelta:
    # time interval parsing function
    value = int(raw_value)
    return timedelta(milliseconds=value)


def _deserialize_set(fn: Callable[[Any], Any],
                     raw_value: Any) -> FrozenSet[Any]:
    return frozenset(map(fn, loads(raw_value)))


@_singledispatch
def api_operator_set_deserializer(column_type: Type,
                                  raw_value: Any) -> FrozenSet[Any]:
    return _deserialize_set(column_type, raw_value)


@api_operator_set_deserializer.register(str)
def _str_set_deserializer(_, raw_value: Any) -> FrozenSet[Optional[str]]:
    # string parsing function for sets.
    return _deserialize_set(
        partial(_str_deserializer, None), raw_value
    )


@api_operator_set_deserializer.register(time)
def _time_set_deserializer(_, raw_value: Any) -> FrozenSet[time]:
    # string parsing function for sets.
    return _deserialize_set(
        partial(_time_deserializer, None), raw_value
    )


@api_operator_set_deserializer.register(datetime)
def _datetime_set_deserializer(_, raw_value: Any) -> FrozenSet[datetime]:
    # date parsing function for sets.
    return _deserialize_set(
        partial(_datetime_deserializer, None), raw_value
    )


@api_operator_set_deserializer.register(timedelta)
def _timedelta_set_deserializer(_, raw_value: Any) -> FrozenSet[timedelta]:
    # time interval parsing function for sets.
    return _deserialize_set(
        partial(_timedelta_deserializer, None), raw_value
    )
