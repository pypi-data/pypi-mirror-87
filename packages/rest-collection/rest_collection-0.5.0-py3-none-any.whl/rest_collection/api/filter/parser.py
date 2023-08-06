from typing import List, Optional, TYPE_CHECKING, Union

from pyparsing import CaselessLiteral, CharsNotIn, Combine, Literal, OneOrMore, \
    ParseException, ParserElement, StringEnd, Suppress, White, ZeroOrMore, \
    nestedExpr

from .expression import ApiFilterExpression, ApiFilterExpressionGroup
from ..exc import ApiFilterError
from ..pointer import ApiPointerRegistry

if TYPE_CHECKING:
    from ..abc import AbstractApiOperatorRegistry


__all__ = [
    'ApiFilterParser',
]

_OPENER = '{'
_CLOSER = '}'

_OPERATOR_EXPRESSION = CaselessLiteral('and') | CaselessLiteral('or')

_ESCAPE_CLOSER_EXCLUSION_EXPRESSION = (
    StringEnd() | (ZeroOrMore(White()) + _OPERATOR_EXPRESSION)
)

# Expressions for escaping curly brackets support.
# If we have escape symbol, we have to escape itself too.
_ESCAPE_EXPRESSION = (
    # JSON-encoded escaped opener
    Combine(Suppress('\\') + Literal('\\') + Literal(_OPENER)) |
    # JSON-encoded escaped closer
    Combine(
        Suppress('\\') + Literal('\\') + Literal(_CLOSER) +
        ~_ESCAPE_CLOSER_EXCLUSION_EXPRESSION
    ) |
    # Escaped opener
    Combine(Suppress('\\') + Literal(_OPENER)) |
    # Escaped closer
    Combine(
        Suppress('\\') + Literal(_CLOSER) + ~_ESCAPE_CLOSER_EXCLUSION_EXPRESSION
    ) |
    # Escaped escape symbol
    Combine(Suppress('\\') + Literal('\\'))
)

# Filter value valid word. Stolen from ``pyparsing.nestedExpr`` content
# definition.
_FILTER_WORD_EXPRESSION = Combine(
    OneOrMore(
        ~Literal(_OPENER) +
        ~Literal(_CLOSER) +
        (
            _ESCAPE_EXPRESSION |
            CharsNotIn(ParserElement.DEFAULT_WHITE_CHARS, exact=1)
        )
    )
).setParseAction(lambda t: t[0].strip())


_FILTER_EXPRESSION = (
    _FILTER_WORD_EXPRESSION +  # Column
    _FILTER_WORD_EXPRESSION +  # Operator
    OneOrMore(  # Value
        _FILTER_WORD_EXPRESSION
    ).setParseAction(' '.join)
)

_FILTER_PARSER = nestedExpr(
    _OPENER,
    _CLOSER,
    content=_FILTER_EXPRESSION | _OPERATOR_EXPRESSION,
)


def _unwrap_parenthesis(pyparsing_list: List) -> List:
    """
    Getting of the brackets content, that was obtained by library parsing.
    One more brackets can be the content of the brackets, in this case, we omit
    nested brackets.
    """
    if len(pyparsing_list) == 1 and isinstance(pyparsing_list[0], list):
        return _unwrap_parenthesis(pyparsing_list[0])
    return pyparsing_list


def _has_nested_list(pyparsing_list: List) -> bool:
    """
    Checking for the nested list. If nested list exists, it means, that there
    is additional filter expression inside current.
    """
    return any(map(lambda item: isinstance(item, list), pyparsing_list))


def _get_plain_list(pyparsing_list: List) -> Optional[List]:
    """Getting plain list, without nested structures."""
    pyparsing_list = _unwrap_parenthesis(pyparsing_list)

    if not _has_nested_list(pyparsing_list):
        return pyparsing_list


def _split_list_by(pyparsing_list: List, splitter: str) -> List:
    """
    Spliting parsed list into smaller lists, devided by splitter.
    """
    result = []
    sub_result = []

    for item in _unwrap_parenthesis(pyparsing_list):
        if not isinstance(item, str) or item != splitter:
            sub_result.append(item)
            continue

        result.append(sub_result[:])
        sub_result = []

    result.append(sub_result[:])

    return list(map(_unwrap_parenthesis, result))


class ApiFilterParser(object):
    __slots__ = '_pointer_registry', '_operator_registry'

    def __init__(self,
                 pointer_registry: ApiPointerRegistry,
                 operator_registry: 'AbstractApiOperatorRegistry') -> None:
        self._pointer_registry = pointer_registry
        self._operator_registry = operator_registry

    @property
    def pointer_registry(self) -> ApiPointerRegistry:
        return self._pointer_registry

    @property
    def operator_registry(self) -> 'AbstractApiOperatorRegistry':
        return self._operator_registry

    def _parse_expression(self,
                          pyparsing_list: List) -> ApiFilterExpression:
        return ApiFilterExpression.from_list(
            pyparsing_list,
            self.pointer_registry,
            operator_registry=self.operator_registry
        )

    def _parse_and_group(self, pyparsing_list: List) -> Optional[
        Union[ApiFilterExpressionGroup, ApiFilterExpression]
    ]:
        """
        Group and expression parsing, that connected together with AND.
        """
        and_chunks = _split_list_by(pyparsing_list, 'and')
        if not and_chunks:
            return

        expression_list = _get_plain_list(and_chunks)

        if expression_list:
            return self._parse_expression(expression_list)

        return ApiFilterExpressionGroup.create_or_unwrap(*filter(
            None, map(self._parse_or_group, and_chunks)
        )) or None

    def _parse_or_group(self, pyparsing_list: List) -> Optional[
        Union[ApiFilterExpressionGroup, ApiFilterExpression]
    ]:
        """
        Group and expression parsing, that connected together with OR.
        """
        or_chunks = _split_list_by(pyparsing_list, 'or')
        if not or_chunks:
            return

        expression_list = _get_plain_list(or_chunks)

        if expression_list:
            return self._parse_expression(expression_list)

        return ApiFilterExpressionGroup.create_or_unwrap(*filter(
            None, map(self._parse_and_group, or_chunks)
        ), conjunction=False) or None

    def parse(self, filter_str: str) -> Optional[ApiFilterExpressionGroup]:
        """
        API filter string parser.
        """
        if filter_str is None:
            return

        try:
            result = _FILTER_PARSER.parseString('{%s}' % filter_str).asList()

        except ParseException as err:
            raise ApiFilterError(
                'Incorrect filter %r value.' % filter_str
            ) from err

        if not result:
            return

        # Parsed list splitting begins from OR operand in order to combining
        # all of same-level AND operands in certain groups. It repeats
        # database and language priority of AND operand over OR operand.
        expression = self._parse_or_group(result)

        if expression is not None:
            return ApiFilterExpressionGroup.create_or_unwrap(expression)

    __call__ = parse
