from .container import ApiOperatorRegistry
from ..operator import ApiBetweenOperator, ApiContainsOperator, \
    ApiEndsWithOperator, ApiEqualOperator, \
    ApiGreaterOrEqualOperator, ApiGreaterThanOperator, \
    ApiIContainsOperator, ApiIEndsWithOperator, \
    ApiIStartsWithOperator, ApiInOperator, ApiIsOperator, \
    ApiLessOrEqualOperator, ApiLessThanOperator, \
    ApiNotContainsOperator, ApiNotEndsWithOperator, \
    ApiNotEqualOperator, ApiNotIContainsOperator, \
    ApiNotIEndsWithOperator, ApiNotIStartsWithOperator, \
    ApiNotInOperator, ApiNotIsOperator, ApiNotStartsWithOperator, \
    ApiStartsWithOperator

__all__ = [
    'API_OPERATOR_REGISTRY',
]


API_OPERATOR_REGISTRY = ApiOperatorRegistry()


# "Equal" operator.
ApiEqualOperator.register('eq', API_OPERATOR_REGISTRY)

# "Not equal" operator.
ApiNotEqualOperator.register('ne', API_OPERATOR_REGISTRY)

# "Greater" operator.
ApiGreaterThanOperator.register('gt', API_OPERATOR_REGISTRY)

# "Greater or equal" operator.
ApiGreaterOrEqualOperator.register('ge', API_OPERATOR_REGISTRY)

# "Less" operator.
ApiLessThanOperator.register('lt', API_OPERATOR_REGISTRY)

# "Less or equal" operator.
ApiLessOrEqualOperator.register('le', API_OPERATOR_REGISTRY)

# "Starts with" operator.
ApiStartsWithOperator.register('sw', API_OPERATOR_REGISTRY)

# "Starts with" operator with case ignoring.
ApiIStartsWithOperator.register('isw', API_OPERATOR_REGISTRY)

# "Not starts with" operator.
ApiNotStartsWithOperator.register('nsw', API_OPERATOR_REGISTRY)

# "Not starts with" operator with case ignoring.
ApiNotIStartsWithOperator.register('nis', API_OPERATOR_REGISTRY)

# "Ends with" operator.
ApiEndsWithOperator.register('ew', API_OPERATOR_REGISTRY)

# "Ends with" operator with case ignoring.
ApiIEndsWithOperator.register('iew', API_OPERATOR_REGISTRY)

# "Not ends with" operator.
ApiNotEndsWithOperator.register('new', API_OPERATOR_REGISTRY)

# "Not ends with" operator with case ignoring.
ApiNotIEndsWithOperator.register('nie', API_OPERATOR_REGISTRY)

# "Contains" operator.
ApiContainsOperator.register('ct', API_OPERATOR_REGISTRY)

# "Contains" operator with case ignoring.
ApiIContainsOperator.register('ict', API_OPERATOR_REGISTRY)

# "Not contains" operator.
ApiNotContainsOperator.register('nc', API_OPERATOR_REGISTRY)

# "Not contains" operator with case ignoring.
ApiNotIContainsOperator.register('nic', API_OPERATOR_REGISTRY)

# "In" operator.
ApiInOperator.register('in', API_OPERATOR_REGISTRY)

# "Not in" operator.
ApiNotInOperator.register('nn', API_OPERATOR_REGISTRY)

# "Is" operator.
ApiIsOperator.register('is', API_OPERATOR_REGISTRY)

# "Not is" operator.
ApiNotIsOperator.register('ns', API_OPERATOR_REGISTRY)

# "Between" operator.
ApiBetweenOperator.register('bw', API_OPERATOR_REGISTRY)
