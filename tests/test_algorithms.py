
import pytest

from algorithms.djikstra import djikstra
from algorithms.floyd_warshall import floyd_warshall
from algorithms.kosaraju import kosaraju
from algorithms.bellman_ford import bellman_ford
import graph_cls as gc
import datasets as ds
import paths.shortest_path as sp


def test_djisktra():
    graph = ds.weighted_path_graph()
    distance_dict, prev_dict = djikstra(graph, 'a')
    shortest_path, distance = sp._shortest_path(distance_dict, prev_dict, 'a', 'd')
    assert shortest_path == list('abefgd')
    assert distance == 5


def test_floyd_warshall():
    graph = ds.weighted_path_graph()
    distance_dict, prev_dict = floyd_warshall(graph)
    shortest_path, distance = sp._shortest_path(distance_dict, prev_dict, 'a', 'd')
    assert shortest_path == list('abefgd')
    assert distance == 5


def test_bellman_ford():
    graph = ds.weighted_path_graph()
    distance_dict, prev_dict = bellman_ford(graph, 'a')
    shortest_path, distance = sp._shortest_path(distance_dict, prev_dict, 'a', 'd')
    assert shortest_path == list('abefgd')
    assert distance == 5


@pytest.mark.parametrize(
    'graph,expected',
    [
        (ds.connected_component_graph(), {('a', 'b', 'c'), ('d', 'e'), ('f', 'g', 'h'), ('i',)}),
        (gc.to_directed(ds.weighted_path_graph(False)), {tuple('abcdefg'), ('z',)}),
        (ds.weighted_path_graph(True), {('a',), ('b',), ('c',), ('d',), ('e',), ('f',), ('g',), ('z',)})
    ]
)
def test_kosaraju(graph, expected):
    scc = {tuple(sorted(x)) for x in kosaraju(graph)}
    assert not scc.symmetric_difference(expected)
