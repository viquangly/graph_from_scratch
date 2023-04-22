
from typing import Dict, Hashable

from graph_cls import Graph, DiGraph
from graph_typing import Numeric


def degree_centrality(graph: Graph, normalize: bool = True) -> Dict[Hashable, Numeric]:
    """
    Calculate the degree centrality of the nodes in an undirected graph.

    :param graph: an undirected graph

    :param normalize: bool.  Default is True.  If True, centrality is normalized.

    :return: dict keyed by node and its corresponding centrality
    """
    if graph.is_directed:
        raise TypeError('graph must be an undirected graph')

    max_possible_degrees = len(graph) - 1
    denominator = max_possible_degrees if normalize else 1
    degree_dict = {node: (len(neighbors) / denominator) for node, neighbors in graph.g.items()}
    return degree_dict


def directed_degree_centrality(graph: DiGraph, in_degree: bool, normalize: bool = True) -> Dict[Hashable, Numeric]:
    """
    Calculate the degree centrality of the nodes in a directed graph.

    :param graph: a directed graph

    :param in_degree: bool; if True, calculate the in-degree centrality, otherwise out-degree centrality

    :param normalize: bool.  Default is True.  If True, centrality is normalized.

    :return: dict keyed by node and its corresponding centrality
    """
    if not graph.is_directed:
        raise TypeError('graph must be a directed graph')

    direction_index = int(in_degree)
    counter = dict.fromkeys(graph.nodes, 0)
    max_possible_degrees = len(graph) - 1
    denominator = max_possible_degrees if normalize else 1
    for edge in graph.edges:
        node = edge[direction_index]
        counter[node] += (1 / denominator)
    return counter
