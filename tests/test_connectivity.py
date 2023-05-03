
import pytest

import connectivity.connectivity as conn
import datasets as ds
import graph_cls as gc


@pytest.mark.parametrize(
    'graph,expected',
    [
        (ds.weighted_path_graph(), False),
        (gc.to_undirected(ds.connected_component_graph()), True),
    ]
)
def test_connectivity(graph, expected):
    assert conn.is_connected(graph) == expected
