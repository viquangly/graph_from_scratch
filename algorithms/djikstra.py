
from typing import Dict, Set, Hashable, Tuple

import graph_typing as gt

from exceptions import NodeNotInGraphException
from graph_cls import GraphTypeHint


def _get_next_node_smallest_distance(
        distance_dict: Dict, visited_nodes: Set
) -> Tuple[Hashable, gt.Numeric]:
    """
    Helper function to get the next unvisited node with the smallest distance from source.

    :param distance_dict: dict keyed by nodes and distances from the source node as values

    :param visited_nodes: set of nodes already visited

    :return: 2-element tuple of the next node and its corresponding distance from source.
    """
    min_distance = float('inf')
    min_node = None

    for node, distance in distance_dict.items():
        if node in visited_nodes:
            continue
        if distance < min_distance:
            min_distance = distance
            min_node = node

    return min_node, min_distance


def djikstra(graph: GraphTypeHint, u: Hashable) -> Tuple[Dict, Dict]:
    """
    Perform Djikstra's Algorithm for Shortest Path

    :param graph: Graph or DiGraph object

    :param u: hashable object; the source node

    :return: 2 element tuple.  1st element is a dict keyed by the source-node / target-node tuple and values of the
    distance to the source node.  2nd element is a dict keyed by the source-node / target-node tuple and its
    previous node in the shortest path.
    """
    if u not in graph.nodes:
        raise NodeNotInGraphException(u)

    unvisited_nodes = graph.nodes
    visited_nodes = set()

    distance_dict = dict.fromkeys(unvisited_nodes, float('inf'))
    distance_dict[u] = 0

    prev_dict = dict.fromkeys(unvisited_nodes, None)
    curr_node = u
    neighbors = graph.get_neighbors(curr_node)

    while neighbors:
        for neighbor in neighbors:
            curr_distance = graph.get_edge_weight(curr_node, neighbor) + distance_dict[curr_node]
            min_distance = distance_dict[neighbor]
            if curr_distance < min_distance:
                distance_dict[neighbor] = curr_distance
                prev_dict[neighbor] = curr_node
        visited_nodes.add(curr_node)
        curr_node, _distance = _get_next_node_smallest_distance(distance_dict, visited_nodes)
        if (curr_node is None) or (_distance == float('inf')):
            break
        neighbors = graph.get_neighbors(curr_node) - visited_nodes

    distance_dict = {
        (u, node): distance for node, distance in distance_dict.items()
        if (distance < float('inf')) and (node != u)
    }
    prev_dict = {(u, node): prev for node, prev in prev_dict.items() if prev is not None}

    return distance_dict, prev_dict
