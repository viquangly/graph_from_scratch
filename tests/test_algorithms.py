
from algorithms.djikstra import djikstra
from algorithms.floyd_warshall import floyd_warshall
import paths.shortest_path as sp
import datasets as ds


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
