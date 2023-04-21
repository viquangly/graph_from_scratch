
from graph_cls import Graph, DiGraph, GraphTypeHint


def empty_graph(is_directed: bool = False) -> GraphTypeHint:
    return DiGraph() if is_directed else Graph()


def path_graph(is_directed: bool = False) -> GraphTypeHint:
    edges = [
        ('a', 'b'), ('b', 'c'), ('c', 'd'),
        ('b', 'e'), ('c', 'f'), ('a', 'f'),
        ('g', 'h'), ('h', 'i'), ('i', 'j')
    ]
    graph_type = DiGraph if is_directed else Graph
    return graph_type(edges=edges)


def weighted_path_graph(is_directed: bool = False) -> GraphTypeHint:
    edges = [
        ('a', 'b', 1), ('b', 'c', 10), ('c', 'd', 10),
        ('b', 'e', 1), ('e', 'f', 1), ('f', 'g', 1),
        ('g', 'd', 1)
    ]
    graph_type = DiGraph if is_directed else Graph
    return graph_type(nodes=['z'], edges=edges)
