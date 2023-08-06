from typing import Any, Callable, Dict, Iterator, Mapping, Optional, Tuple

from rest_collection.container import Aliases
from .container import ApiParam

__all__ = [
    'ApiContextParamSchemaNode',
    'ApiContextParamSchema',
]


class ApiContextParamSchemaNode(object):
    """API params schema node."""
    __slots__ = 'aliases', '_normalizer', 'block_default'

    def __init__(self,
                 aliases: Aliases,
                 normalizer: Optional[Callable[[ApiParam], Any]] = None,
                 block_default: Optional[bool] = None):
        assert normalizer is None or callable(normalizer)
        assert isinstance(aliases, Aliases)

        self.aliases = aliases
        self._normalizer = normalizer
        self.block_default = block_default

    @property
    def main(self) -> str:
        return self.aliases.main

    name = main

    def normalize(self, url_param: ApiParam) -> None:
        if self._normalizer is not None:
            url_param.value = self._normalizer(url_param)

        url_param.name = self.aliases.map.get(url_param.name, url_param.name)


class ApiContextParamSchema(Mapping[str, ApiContextParamSchemaNode]):
    """API params schema (defined allowed params)."""
    __slots__ = '_map', '_nodes'

    def __init__(self,
                 node: ApiContextParamSchemaNode,
                 *nodes: ApiContextParamSchemaNode) -> None:
        nodes = (node, *nodes)

        assert all(map(
            lambda x: isinstance(x, ApiContextParamSchemaNode), nodes
        ))
        self._map = {}  # type: Dict[str, ApiContextParamSchemaNode]

        for node in nodes:
            for alias in node.aliases:
                self._map[alias] = node

        self._nodes = nodes

    def __iter__(self) -> Iterator[str]:
        return iter(self._map)

    def __getitem__(self, key: str) -> ApiContextParamSchemaNode:
        return self._map[key]

    def __len__(self) -> int:
        return len(self._map)

    def main_for(self, key: str) -> str:
        return self._map[key].main

    def normalize(self, url_param: ApiParam) -> None:
        self._map[url_param.name].normalize(url_param)

    def __repr__(self) -> str:
        return '<%s data=%s>' % (
            self.__class__.__name__, repr(self._map)
        )

    @property
    def first_node(self) -> ApiContextParamSchemaNode:
        return self._nodes[0]

    @property
    def nodes(self) -> Tuple[ApiContextParamSchemaNode, ...]:
        return self._nodes
