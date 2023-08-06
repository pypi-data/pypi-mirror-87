from functools import partial
from typing import Callable, Optional, TYPE_CHECKING

from sqlalchemy.orm import Mapper

from .container import ApiPointer
from .identity import ApiIdentity
from ..exc import ApiIdentityError, ApiPointerError

if TYPE_CHECKING:
    # preventing cross import
    from .registry import ApiPointerRegistry

__all__ = [
    'api_pointer_factory',
    'api_pointer_from_identity',
]


def api_pointer_factory(
    registry: 'ApiPointerRegistry'
) -> Callable[[str], ApiPointer]:
    """API pointer factory."""
    # noinspection PyTypeChecker
    return partial(api_pointer_from_identity, registry)


def api_pointer_from_identity(
    registry: 'ApiPointerRegistry',
    identity_str: str,
) -> ApiPointer:
    """Getting API pointer from it`s string identity."""
    if identity_str in registry:
        # This identity has been walked ealier throught model relation
        # cascade, so, this model is in registry already.
        return registry[identity_str]

    identity = ApiIdentity(identity_str)
    return _walk_on_identity(registry, identity)


def _walk_on_identity(
    registry: 'ApiPointerRegistry',
    identity: ApiIdentity,
    till_index: int = 1,
    parent: Optional[ApiPointer] = None,
) -> ApiPointer:
    """Identity relation cascade walking."""

    api_pointer = _get_api_pointer(
        registry,
        identity,
        till_index,
        parent=parent
    )

    if parent is not None:
        parent.add_child(api_pointer)

    if till_index == len(identity):
        # Index of slice is last index, identity has no relation childs.
        return api_pointer

    return _walk_on_identity(
        registry, identity, till_index=till_index+1, parent=api_pointer
    )


def _get_api_pointer(
    registry: 'ApiPointerRegistry',
    identity: ApiIdentity,
    till_index: int,
    parent: Optional[ApiPointer] = None,
) -> ApiPointer:
    """API pointer getter."""
    sub_identity = identity.slice(stop=till_index)
    identity_str = str(sub_identity)

    if identity_str in registry:
        return registry[identity_str]

    sa_cls = registry.sa_cls if (
        parent is None
    ) else parent.sa_relationship.mapper.class_

    mapper = registry.sa_mappers[sa_cls]  # type: Mapper

    identity_ending = sub_identity.last

    # Checking if identity represents column.
    if identity_ending in mapper.columns:
        sa_column = mapper.columns[identity_ending]

        if len(identity) > till_index:
            raise ApiIdentityError('Identity, that represents column, '
                                   'must not have any childs.')

    else:
        sa_column = None

    # Checking if identity represents relationship.
    if sa_column is None and identity_ending in mapper.relationships:
        sa_relationship = mapper.relationships[identity_ending]

    else:
        sa_relationship = None

    if sa_column is None and sa_relationship is None:
        # First part of identity is neigther column, nor relationship.
        raise ApiPointerError('%r is neigther columns nor relationship. '
                              % identity_ending)

    api_pointer = ApiPointer(
        sub_identity,
        sa_cls,
        sa_column,
        sa_relationship,
        parent=parent,
    )

    registry[identity_str] = api_pointer

    return api_pointer
