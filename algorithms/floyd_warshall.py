
from collections import defaultdict

from typing import Tuple, Dict
from graph_cls import GraphTypeHint


def floyd_warshall(graph: GraphTypeHint) -> Tuple[Dict, Dict]:
    distance_dict = defaultdict(lambda: float('inf'))
    prev_dict = defaultdict(lambda: None)

    nodes = graph.nodes

    for edge, weight in graph.edge_weights.items():
        u, v = edge
        distance_dict[edge] = weight
        prev_dict[edge] = u

    for node in nodes:
        distance_dict[(node, node)] = 0
        prev_dict[(node, node)] = node

    for intermediary in nodes:
        for source in nodes:
            for target in nodes:
                prev_distance = distance_dict[(source, target)]
                curr_distance = distance_dict[(source, intermediary)] + distance_dict[(intermediary, target)]
                if prev_distance > curr_distance:
                    distance_dict[(source, target)] = curr_distance
                    prev_dict[(source, target)] = prev_dict[(intermediary, target)]

    distance_dict = {edge: distance for edge, distance in distance_dict.items() if distance < float('inf')}
    prev_dict = {edge: prev for edge, prev in prev_dict.items() if (prev is not None) and (edge[0] != edge[1])}

    return distance_dict, prev_dict
