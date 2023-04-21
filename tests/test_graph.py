

import pytest

from tests import datasets as ds


@pytest.mark.parametrize('is_directed', [False, True])
def test_add_node(is_directed):
    graph = ds.empty_graph(is_directed)
    graph.add_node('a')
    assert 'a' in graph
    assert graph.order == 1
    assert graph.size == 0


@pytest.mark.parametrize('is_directed', [False, True])
def test_add_duplicate_nodes(is_directed):
    graph = ds.empty_graph(is_directed)
    graph.add_nodes_from(list('aaaaa'))
    assert graph.order == 1
    assert graph.size == 0


@pytest.mark.parametrize('is_directed', [False, True])
def test_add_nodes_from(is_directed):
    graph = ds.empty_graph(is_directed)
    graph.add_nodes_from(list('ab'))
    assert 'a' in graph
    assert 'b' in graph
    assert graph.order == 2
    assert graph.size == 0


@pytest.mark.parametrize(
    'is_directed,expected_edges',
    [
        (False, {('a', 'b'), ('b', 'a')}),
        (True, {('a', 'b')})
    ]
)
def test_add_edge(is_directed, expected_edges):
    graph = ds.empty_graph(is_directed)
    graph.add_edge('a', 'b')
    assert 'a' in graph
    assert 'b' in graph
    assert not graph.edges.symmetric_difference(expected_edges)
    assert graph.order == 2
    assert graph.size == 1


@pytest.mark.parametrize(
    'is_directed,n_edges,expected_c_to_a',
    [(False, 6, True), (True, 3, False)]
)
def test_add_edges_from(is_directed, n_edges, expected_c_to_a):
    graph = ds.empty_graph(is_directed)
    graph.add_edges_from([('a', 'b'), ('a', 'c'), ('b', 'd')])
    assert all([x in graph for x in list('abcd')])
    assert graph.order == 4
    assert graph.size == 3
    assert len(graph.edge_weights.keys()) == n_edges
    assert graph.path_exists('a', 'c')
    assert graph.path_exists('c', 'a') == expected_c_to_a


@pytest.mark.parametrize('is_directed', [False, True])
def test_add_duplicate_edges(is_directed):
    graph = ds.empty_graph(is_directed)
    graph.add_edges_from([('a', 'b'), ('a', 'b'), ('a', 'b')])
    assert graph.order == 2
    assert graph.size == 1


@pytest.mark.parametrize(
    'graph,expected', [(ds.empty_graph(), 0), (ds.path_graph(), 9)]
)
def test_size(graph, expected):
    assert graph.size == expected


@pytest.mark.parametrize(
    'graph,expected',
    [
        (ds.empty_graph(False), 0), (ds.path_graph(False), 10),
        (ds.empty_graph(True), 0), (ds.path_graph(True), 10)
    ]
)
def test_order(graph, expected):
    assert graph.order == expected


@pytest.mark.parametrize(
    'u,v,expected',
    [
        ('a', 'e', True), ('a', 'd', True), ('d', 'e', True),
        ('g', 'i', True),
        ('a', 'g', False), ('b', 'h', False)
    ]
)
def test_path_exists(u, v, expected):
    graph = ds.path_graph()
    assert graph.path_exists(u, v) == expected
    assert graph.path_exists(v, u) == expected


def test_remove_edge():
    graph = ds.path_graph()
    original_size = graph.size

    graph.remove_edge('c', 'd')
    graph.remove_edge('h', 'i')

    assert graph.size == (original_size - 2)
    assert not graph.path_exists('a', 'd')
    assert not graph.path_exists('d', 'e')
    assert not graph.path_exists('g', 'i')
    assert not graph.path_exists('i', 'h')
    assert graph.path_exists('j', 'i')
    assert (('c', 'd') not in graph.edges) and (('d', 'c') not in graph.edges)
    assert (('h', 'i') not in graph.edges) and (('i', 'h') not in graph.edges)


def test_remove_edges_from():
    graph = ds.path_graph()
    original_size = graph.size

    graph.remove_edges_from([('c', 'd'), ('h', 'i')])
    assert graph.size == (original_size - 2)
    assert not graph.path_exists('a', 'd')
    assert not graph.path_exists('d', 'e')
    assert not graph.path_exists('g', 'i')
    assert not graph.path_exists('i', 'h')
    assert graph.path_exists('j', 'i')
    assert (('c', 'd') not in graph.edges) and (('d', 'c') not in graph.edges)
    assert (('h', 'i') not in graph.edges) and (('i', 'h') not in graph.edges)


def test_remove_node():
    graph = ds.path_graph()
    c_neighbors = graph.get_neighbors('c')
    original_order = graph.order
    original_size = graph.size
    graph.remove_node('c')
    assert 'c' not in graph.nodes
    assert graph.order == (original_order - 1)
    assert graph.size == (original_size - 3)
    edges_after_removal = graph.edges
    for neighbor in c_neighbors:
        assert ('c', neighbor) not in edges_after_removal
        assert (neighbor, 'c') not in edges_after_removal
    assert not graph.path_exists('b', 'd')
    assert not graph.path_exists('d', 'b')
