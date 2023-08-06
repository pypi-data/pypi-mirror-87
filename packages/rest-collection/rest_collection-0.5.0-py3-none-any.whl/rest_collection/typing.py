from typing import Callable, TypeVar, Union

from sqlalchemy import Column, Table
from sqlalchemy.sql import Alias
from sqlalchemy.sql.elements import BinaryExpression

__all__ = [
    'ApiOperatorType',
    'SelectableElementType',
    'SaEngineType',
    'ApiContextType',
]

ApiOperatorType = Callable[..., BinaryExpression]
SelectableElementType = Union[Table, Alias, Column]

SaEngineType = TypeVar('SaEngineType')
ApiContextType = TypeVar('ApiContextType')
