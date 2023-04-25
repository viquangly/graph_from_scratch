
from typing import Hashable, Tuple, Dict

from graph_cls import DiGraph


def bellman_ford(graph: DiGraph, u: Hashable) -> Tuple[Dict, Dict]:
    """
    Perform Bellman-Ford algorithm for shortest path.

    :param graph: Graph or DiGraph object

    :param u: hashable object; the source node

    :return: 2 element tuple.  1st element is a dict keyed by the source-node / target-node tuple and values of the
    distance to the source node.  2nd element is a dict keyed by the source-node / target-node tuple and its
    previous node in the shortest path.
    """
    source = u
    distance_dict = dict.fromkeys(graph.nodes, float('inf'))
    distance_dict[u] = 0
    prev_dict = dict.fromkeys(graph.nodes, None)

    for _ in range(graph.order - 1):
        for edge, weight in graph.edge_weights.items():
            u, v = edge
            if distance_dict[u] != float("Inf") and ((distance_dict[u] + weight) < distance_dict[v]):
                distance_dict[v] = distance_dict[u] + weight
                prev_dict[v] = u

    for edge, weight in graph.edge_weights.items():
        u, v = edge
        if distance_dict[u] != float("Inf") and distance_dict[u] + weight < distance_dict[v]:
            raise ValueError('graph contains negative cycles')

    distance_dict = {
        (source, node): distance for node, distance in distance_dict.items()
        if (distance < float('inf')) and (node != source)
    }
    prev_dict = {(source, node): prev for node, prev in prev_dict.items() if prev is not None}

    return distance_dict, prev_dict
