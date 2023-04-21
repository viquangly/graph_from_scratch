
from __future__ import annotations

from copy import deepcopy
from typing import Hashable, Optional, Set, Union

import graph_typing as gt
from exceptions import NodeNotInGraphException


class DiGraph:

    def __init__(self, nodes: Optional[gt.NodeCollection] = None, edges: Optional[gt.EdgeCollection] = None):
        self.g = {}
        self.edge_weights = {}

        if nodes is not None:
            self.add_nodes_from(nodes)

        if edges is not None:
            self.add_edges_from(edges)

    def __contains__(self, node: Hashable) -> bool:
        return node in self.g

    def __getitem__(self, node: Hashable) -> Set:
        self._assert_node_exists(node)
        return self.g[node]

    def __len__(self):
        return len(self.g)

    def _assert_node_exists(self, node: Hashable) -> None:
        if node not in self:
            raise NodeNotInGraphException(node)

    @property
    def size(self) -> int:
        return len(self.edge_weights)

    @property
    def order(self) -> int:
        return len(self)

    @property
    def nodes(self) -> Set:
        return set(self.g.keys())

    @property
    def edges(self) -> Set:
        return set(self.edge_weights.keys())

    @property
    def is_empty(self) -> bool:
        return bool(self)

    def get_neighbors(self, node: Hashable) -> Set:
        return deepcopy(self[node])

    def add_node(self, node: Hashable) -> None:
        if node not in self:
            self.g[node] = set()

    def add_nodes_from(self, nodes: gt.NodeCollection) -> None:
        for node in nodes:
            self.add_node(node)

    def add_edge(self, u: Hashable, v: Hashable, weight: gt.Numeric = 1) -> None:
        if weight <= 0:
            raise ValueError('weight must be > 0')
        self.add_node(u)
        self.add_node(v)
        self[u].add(v)
        self.edge_weights[(u, v)] = weight

    def add_edges_from(self, edges: gt.EdgeCollection) -> None:
        for edge in edges:
            self.add_edge(*edge)

    def remove_edge(self, u: Hashable, v: Hashable) -> None:
        del self.edge_weights[(u, v)]
        self[u].remove(v)

    def remove_edges_from(self, edges: gt.EdgeCollection) -> None:
        for edge in set(edges):
            self.remove_edge(*edge)

    def remove_node(self, node: Hashable) -> None:
        neighbors = self.get_neighbors(node)
        for neighbor in neighbors:
            self.remove_edge(node, neighbor)
        del self.g[node]

    def remove_nodes_from(self, nodes: gt.NodeCollection) -> None:
        for node in set(nodes):
            self.remove_node(node)

    def path_exists(self, u: Hashable, v: Hashable) -> bool:
        self._assert_node_exists(u)
        self._assert_node_exists(v)

        visited_nodes = set()
        neighbors = self.get_neighbors(u)
        while neighbors:
            if v in neighbors:
                return True
            visited_nodes.update(neighbors)
            new_neighbors = set()
            for neighbor in neighbors:
                new_neighbors |= self.get_neighbors(neighbor)
            neighbors.update(new_neighbors)
            neighbors -= visited_nodes
        return False

    def get_edge_weight(self, u: Hashable, v: Hashable) -> gt.Numeric:
        return self.edge_weights[(u, v)]


class Graph(DiGraph):

    @property
    def size(self) -> int:
        # Divide by 2 because undirected
        return len(self.edge_weights) // 2

    def add_edge(self, u: Hashable, v: Hashable, weight: gt.Numeric = 1) -> None:
        super().add_edge(u, v, weight)
        super().add_edge(v, u, weight)

    def remove_edge(self, u: Hashable, v: Hashable) -> None:
        super().remove_edge(u, v)
        super().remove_edge(v, u)


GraphTypeHint = Union[Graph, DiGraph]
