
import graph_cls as gc
from algorithms.search import bfs


def is_connected(graph: gc.Graph) -> bool:
    """
    Check if an undirected graph is connected

    :param graph: an undirected graph

    :return: bool; True if graph is connected else False
    """
    if graph.is_directed:
        raise TypeError('graph must be undirected graph')

    nodes = graph.nodes
    source = nodes.pop()
    nodes_visited = set(bfs(graph, source))

    return not (nodes - nodes_visited)


def is_weakly_connected(graph: gc.DiGraph) -> bool:
    """
    Check if a directed graph is weakly connected

    :param graph: a directed graph

    :return: bool; True if graph is weakly connected else False
    """
    if not graph.is_directed:
        raise TypeError('graph must be directed graph')
    graph = gc.to_undirected(graph)
    return is_connected(graph)


def is_strongly_connected(graph: gc.DiGraph) -> bool:
    """
    Check if a directed graph is strongly connected

    :param graph: a directed graph

    :return: bool; True if graph is strongly connected else False
    """
    if not graph.is_directed:
        raise TypeError('graph must be directed graph')

    all_nodes = graph.nodes

    for node in graph.nodes:
        nodes_visited = set(bfs(graph, node))
        nodes_visited.add(node)
        unvisited_nodes = all_nodes - nodes_visited
        if unvisited_nodes:
            return False
    return True
