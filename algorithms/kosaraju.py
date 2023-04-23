
from typing import Generator

from algorithms.search import dfs
import graph_cls as gc


def kosaraju(graph: gc.DiGraph) -> Generator:
    """
    Perform Kosaraju's algorithm for finding Strongly Connected Components in a directed graph

    :param graph: a directed graph

    :return: generator of SCCs
    """
    if not graph.is_directed:
        raise TypeError('graph should be directed')

    reversed_graph = gc.to_reversed(graph)
    nodes = graph.nodes
    nodes_visited = set()

    while nodes:
        node = nodes.pop()
        dfs_traversal = set(dfs(graph, node))
        dfs_traversal.add(node)

        reversed_dfs_traversal = set(dfs(reversed_graph, node))
        reversed_dfs_traversal.add(node)

        scc = dfs_traversal.intersection(reversed_dfs_traversal)
        nodes_visited.update(scc)
        nodes -= nodes_visited
        yield scc
