from collections import namedtuple


__all__ = [
    'PipelineResult',
]


PipelineResult = namedtuple('PipelineResult', ('data', 'count'))
