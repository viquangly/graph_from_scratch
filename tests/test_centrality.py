
import pytest

from tests import datasets as ds
from centrality import centrality as ct


@pytest.mark.parametrize(
    'normalize,expected',
    [
        (False, {'a': 2, 'b': 3, 'c': 2, 'd': 3, 'e': 2, 'f': 2, 'g': 2, 'z': 0}),
        (True, {'a': 2 / 7, 'b': 3 / 7, 'c': 2 / 7, 'd': 3 / 7, 'e': 2 / 7, 'f': 2 / 7, 'g': 2 / 7, 'z': 0})
    ]
)
def test_degree_centrality(normalize, expected):
    graph = ds.weighted_path_graph(False)
    centrality = ct.degree_centrality(graph, normalize)
    extra_nodes = set(expected).symmetric_difference(set(centrality))
    assert not extra_nodes
    acceptable_error = 1e-6 if normalize else 0
    for k, v in centrality.items():
        assert v == pytest.approx(expected[k], acceptable_error)


@pytest.mark.parametrize(
    'in_degree,normalize,expected',
    [
        (False, False, {'a': 2, 'b': 2, 'c': 1, 'd': 0, 'e': 1, 'f': 1, 'g': 1, 'z': 0}),
        (False, True, {'a': 2 / 7, 'b': 2 / 7, 'c': 1 / 7, 'd': 0, 'e': 1 / 7, 'f': 1 / 7, 'g': 1 / 7, 'z': 0}),
        (True, False, {'a': 0, 'b': 1, 'c': 1, 'd': 3, 'e': 1, 'f': 1, 'g': 1, 'z': 0}),
        (True, True, {'a': 0, 'b': 1 / 7, 'c': 1 / 7, 'd': 3 / 7, 'e': 1 / 7, 'f': 1 / 7, 'g': 1 / 7, 'z': 0})
    ]
)
def test_directed_degree_centrality(in_degree, normalize, expected):
    graph = ds.weighted_path_graph(True)
    centrality = ct.directed_degree_centrality(graph, in_degree, normalize)
    extra_nodes = set(expected).symmetric_difference(set(centrality))
    assert not extra_nodes
    acceptable_error = 1e-6 if normalize else 0
    for k, v in centrality.items():
        assert v == pytest.approx(expected[k], acceptable_error)
