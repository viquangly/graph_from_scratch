
from typing import Hashable

from graph_typing import Edge


class NodeNotInGraphException(BaseException):

    def __init__(self, node: Hashable):
        super().__init__(f'Node {node} is not in graph')


class EdgeNotInGraphException(BaseException):

    def __init__(self, edge: Edge):
        super().__init__(f'Edge {edge} is not in graph')


class EmptyGraphException(BaseException):

    def __init__(self):
        super().__init__('Graph is empty')


class PathDoesNotExistException(BaseException):

    def __init__(self, u: Hashable, v: Hashable):
        super().__init__(f'Path does not exist between {u=} and {v=}')
