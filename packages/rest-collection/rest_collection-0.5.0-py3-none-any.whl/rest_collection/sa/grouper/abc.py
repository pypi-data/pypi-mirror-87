from abc import ABCMeta, abstractmethod
from collections import OrderedDict, defaultdict
from typing import DefaultDict, Dict, Mapping, MutableMapping, Sequence, Tuple

__all__ = [
    'AbstractGrouper'
]


class AbstractGrouper(metaclass=ABCMeta):
    __slots__ = ()

    def group(self, data: Sequence[Sequence]) -> Dict[str, Tuple[Dict, ...]]:
        grouped = defaultdict(
            OrderedDict
        )  # type: DefaultDict[str, OrderedDict]

        for row in data:
            self.group_row(row, grouped)

        return {
            k: tuple(v.values()) for k, v in grouped.items()
        }

    __call__ = group

    @abstractmethod
    def group_row(
        self,
        row: Sequence,
        grouped: Mapping[str, MutableMapping[Tuple, Dict]],
    ) -> None: ...
