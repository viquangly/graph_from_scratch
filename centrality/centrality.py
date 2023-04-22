
from typing import Dict, Hashable, Union

from graph_cls import GraphTypeHint
from graph_typing import Numeric


CentralityDict = Dict[Hashable, Numeric]


def degree_centrality(graph: GraphTypeHint, normalize: bool = True) -> Union[CentralityDict, Dict[str, CentralityDict]]:
    """
    Calculate the degree centrality of nodes in the graph

    :param graph: undirected or directed graph

    :param normalize: bool; Default is True.  If True, centrality is normalized.

    :return: If graph is undirected, return a dict keyed by node and its corresponding centrality.
    If graph is directed, return a nested dict with keys 'in' and 'out' representing the direction along with their
    corresponding centrality dict.
    """
    max_possible_degrees = len(graph) - 1
    denominator = max_possible_degrees if normalize else 1

    nodes = graph.nodes
    in_degree_dict = dict.fromkeys(nodes, 0)
    out_degree_dict = dict.fromkeys(nodes, 0)

    for out, in_ in graph.edges:
        in_degree_dict[in_] += (1 / denominator)
        out_degree_dict[out] += (1 / denominator)

    if not graph.is_directed:
        return in_degree_dict
    else:
        return {
            'in': in_degree_dict,
            'out': out_degree_dict
        }
