

__all__ = [
    'ApiError',
    'ApiTypeError',
    'ApiValueError',
    'ApiPointerError',
    'ApiIdentityError',
    'ApiPointerExistsError',
    'ApiOrderByError',
    'ApiLimitError',
    'ApiRelationError',
    'ApiFilterError',
    'ApiFilterExpressionError',
    'ApiFilterOperatorError',
]


class ApiError(Exception):
    """Root api error."""


class ApiTypeError(ApiError, TypeError):
    """Type api error."""


class ApiValueError(ApiError, ValueError):
    """Value api error."""


class ApiPointerError(ApiError):
    """Pointer to model api error."""


class ApiIdentityError(ApiPointerError):
    """Pointer to model identity api error."""


class ApiPointerExistsError(ApiPointerError):
    pass


class ApiOrderByError(ApiError):
    """API "order_by" request context error."""


class ApiLimitError(ApiError):
    """API "limit" request context error."""


class ApiRelationError(ApiError):
    """API "relation" request context error."""


class ApiFilterError(ApiError):
    """API "filter" request context error."""


class ApiFilterExpressionError(ApiFilterError):
    """API filter expression parsing error."""


class ApiFilterOperatorError(ApiFilterExpressionError):
    """API filter operator parsing error."""
