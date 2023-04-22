
from collections import deque
from typing import Generator, Hashable

from graph_cls import GraphTypeHint


def _search(graph: GraphTypeHint, source: Hashable, breadth_first: bool) -> Generator:
    """
    Helper function to perform breadth / depth first search

    :param graph: directed or undirected graph

    :param source: hashable object; the source node

    :param breadth_first: bool; if True, perform bfs else dfs

    :return: generator
    """
    queue = deque(graph.get_neighbors(source))
    visited_nodes = {source}
    while queue:
        curr_node = queue.popleft()
        if curr_node in visited_nodes:
            continue
        yield curr_node
        visited_nodes.add(curr_node)
        neighbors = graph.get_neighbors(curr_node) - visited_nodes

        if breadth_first:
            queue.extend(neighbors)
        else:
            queue.extendleft(neighbors)


def dfs(graph: GraphTypeHint, source: Hashable) -> Generator:
    """
    Depth first search algorithm

    :param graph: directed or undirected graph

    :param source: hashable object; the source node

    :return: generator
    """
    return _search(graph, source, False)


def bfs(graph: GraphTypeHint, source: Hashable) -> Generator:
    """
    Breadth first search algorithm

    :param graph: directed or undirected graph

    :param source: hashable object; the source node

    :return: generator
    """
    return _search(graph, source, True)
