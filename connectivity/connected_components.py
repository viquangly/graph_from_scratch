
from typing import List, Set, Hashable
import warnings

import graph_cls as gc
from algorithms.search import bfs


def connected_components(graph: gc.GraphTypeHint) -> List[Set[Hashable]]:
    """
    Find connected components for an undirected graph, or weakly connected components for directed graphs.

    :param graph: directed or undirected graph

    :return: List of sets representing connected components
    """
    if graph.is_directed:
        warnings.warn('This function will only find weakly connected components for directed graphs.')
        graph = gc.to_undirected(graph, suppress_warning=True)

    nodes = graph.nodes
    components = []
    while nodes:
        curr_node = nodes.pop()
        component = set(bfs(graph, curr_node))
        component.add(curr_node)
        components.append(component)
        nodes -= component
    return components
