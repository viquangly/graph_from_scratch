
from collections import deque
from typing import Dict, Hashable, Tuple, List, Optional

from algorithms.djikstra import djikstra
from algorithms.floyd_warshall import floyd_warshall
from graph_typing import Numeric
from graph_cls import GraphTypeHint


def _shortest_path(distance_dict: Dict, prev_dict: Dict, u: Hashable, v: Hashable) -> Tuple[List, Numeric]:
    if (u, v) not in prev_dict:
        return [], float('inf')

    distance = distance_dict[(u, v)]
    path = deque()
    path.appendleft(v)
    while u != v:
        v = prev_dict[(u, v)]
        path.appendleft(v)
    return list(path), distance


def shortest_path(graph: GraphTypeHint, u: Optional[Hashable], v: Optional[Hashable]) -> Dict[Tuple, Tuple]:
    if (u is None) and (v is not None):
        raise ValueError('u cannot be None while v is not None')
    distance_dict, prev_dict = floyd_warshall(graph) if (u is None) and (v is None) else djikstra(graph, u)

    if (u is not None) and (v is not None):
        return {(u, v): _shortest_path(distance_dict, prev_dict, u, v)}
    else:
        return {edge: _shortest_path(distance_dict, prev_dict, *edge) for edge in distance_dict.keys()}
