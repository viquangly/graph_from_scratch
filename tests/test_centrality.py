
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

    for k, v in centrality.items():
        if normalize:
            assert v == pytest.approx(expected[k])
        else:
            assert v == expected[k]


@pytest.mark.parametrize(
    'normalize,expected',
    [
        (
            False,
            {
                'out': {'a': 2, 'b': 2, 'c': 1, 'd': 0, 'e': 1, 'f': 1, 'g': 1, 'z': 0},
                'in': {'a': 0, 'b': 1, 'c': 1, 'd': 3, 'e': 1, 'f': 1, 'g': 1, 'z': 0}
            }
        ),
        (
            True,
            {
                'out': {'a': 2 / 7, 'b': 2 / 7, 'c': 1 / 7, 'd': 0, 'e': 1 / 7, 'f': 1 / 7, 'g': 1 / 7, 'z': 0},
                'in': {'a': 0, 'b': 1 / 7, 'c': 1 / 7, 'd': 3 / 7, 'e': 1 / 7, 'f': 1 / 7, 'g': 1 / 7, 'z': 0}
            }
        ),
    ]
)
def test_directed_degree_centrality(normalize, expected):
    graph = ds.weighted_path_graph(True)
    centrality = ct.degree_centrality(graph, normalize)
    for direction in centrality.keys():
        expected_ = expected[direction]
        actual_ = centrality[direction]
        extra_nodes = set(expected_).symmetric_difference(set(actual_))
        assert not extra_nodes

        for k, v in actual_.items():
            if normalize:
                assert v == pytest.approx(expected_[k])
            else:
                assert v == expected_[k]
