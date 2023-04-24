
from __future__ import annotations

from copy import deepcopy
from typing import Hashable, Optional, Set, Union
import warnings

import graph_typing as gt
from exceptions import NodeNotInGraphException


def to_directed(graph: Graph) -> DiGraph:
    """
    Convert an undirected graph to a directed graph

    :param graph: an undirected graph

    :return: directed graph
    """
    if graph.is_directed:
        raise TypeError('graph must be an undirected graph')

    out_graph = DiGraph(nodes=graph.nodes)
    for edge, weight in graph.edge_weights.items():
        u, v = edge
        out_graph.add_edge(u, v, weight)
    return out_graph


def to_undirected(graph: DiGraph, suppress_warning: bool = False) -> Graph:
    """
    Convert a directed graph to undirected graph.  Note: If edge u-v has different weight than edge v-u
    in the directed graph, weight of one edge will be overwritten by the other during the conversion to undirected
    graph.

    :param graph: directed graph

    :param suppress_warning: bool; default is False.  If True, raise warning if edge u-v has different weight that
    edge v-u, as the prior weight will be overwritten by new weight in undirected graph

    :return: undirected graph
    """
    if not graph.is_directed:
        raise TypeError('graph must be directed graph')

    out_graph = Graph(nodes=graph.nodes)
    for edge, weight in graph.edge_weights.items():
        u, v = edge
        reverse_edge = (v, u)
        if reverse_edge in out_graph.edge_weights:
            reverse_edge_weight = out_graph.edge_weights[(v, u)]
            if (reverse_edge_weight != weight) and not suppress_warning:
                warnings.warn(f'{u=}-{v=} with {weight=} will overwrite {v=}-{u=} weight={reverse_edge_weight}')
        out_graph.add_edge(u, v, weight)
    return out_graph


def to_reversed(graph: DiGraph) -> DiGraph:
    """
    Create a directed graph with the direction of edges reversed.

    :param graph: directed graph

    :return: directed graph with direction reversed
    """
    if not graph.is_directed:
        raise TypeError('graph must be directed')
    out_graph = DiGraph(graph.nodes)
    for edge, weight in graph.edge_weights.items():
        u, v = edge
        out_graph.add_edge(v, u, weight)
    return out_graph


class DiGraph:
    """
    Class DiGraph for creating directed graphs.
    """
    def __init__(self, nodes: Optional[gt.NodeCollection] = None, edges: Optional[gt.EdgeCollection] = None):
        """
        Instantiate an object of class DiGraph

        :param nodes: optional; a collection of hashable objects representing nodes.  Default is None.

        :param edges: optional; a collection tuples.  Default is None.  Tuples should be 2 or 3 elements
        where the first 2 elements are hashable objects representing the source node and the target node.  The 3rd
        element is a numeric value representing the edge weight; defaults to edge weight of 1 if not supplied.
        """
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
    def is_directed(self) -> bool:
        return True

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

    @property
    def is_weighted(self) -> bool:
        return (min(self.edge_weights) == 1) and (max(self.edge_weights) == 1)

    def get_neighbors(self, node: Hashable) -> Set:
        """
        Get the neighbors of the node

        :param node: hashable object

        :return: set of neighboring nodes
        """
        return deepcopy(self[node])

    def add_node(self, node: Hashable) -> None:
        """
        Add a node to the graph in-place.

        :param node: hashable object

        :return: None
        """
        if node not in self:
            self.g[node] = set()

    def add_nodes_from(self, nodes: gt.NodeCollection) -> None:
        """
        Add a collection of nodes to the graph in-place.

        :param nodes: collection of hashable objects

        :return: None
        """
        for node in nodes:
            self.add_node(node)

    def add_edge(self, u: Hashable, v: Hashable, weight: gt.Numeric = 1) -> None:
        """
        Add an edge to the graph in-place.

        :param u: hashable object; the source node.

        :param v: hashable object; the target node.

        :param weight: numeric.  The edge weight.  Default is 1.

        :return: None
        """
        self.add_node(u)
        self.add_node(v)
        self[u].add(v)
        self.edge_weights[(u, v)] = weight

    def add_edges_from(self, edges: gt.EdgeCollection) -> None:
        """
        Add a collection of edges to the graph in-place.

        :param edges: collection of 2 or 3 element tuples.  Tuples should be 2 or 3 elements
        where the first 2 elements are hashable objects representing the source node and the target node.  The 3rd
        element is a numeric value representing the edge weight; defaults to edge weight of 1 if not supplied.

        :return: None
        """
        for edge in edges:
            self.add_edge(*edge)

    def remove_edge(self, u: Hashable, v: Hashable) -> None:
        """
        Remove the edge from the graph.

        :param u: hashable object; the source node

        :param v: hashable object; the target node

        :return: None
        """
        del self.edge_weights[(u, v)]
        self[u].remove(v)

    def remove_edges_from(self, edges: gt.EdgeCollection) -> None:
        """
        Remove the edges from the graph in-place.

        :param edges: collection of 2-element tuples.  Do not include the edge weights in the tuples.

        :return: None
        """
        for edge in set(edges):
            self.remove_edge(*edge)

    def remove_node(self, node: Hashable) -> None:
        """
        Remove the node from the graph in-place.  Note: All edges incident on the node are also removed.

        :param node: hashable object

        :return: None
        """
        neighbors = self.get_neighbors(node)
        for neighbor in neighbors:
            self.remove_edge(node, neighbor)
        del self.g[node]

    def remove_nodes_from(self, nodes: gt.NodeCollection) -> None:
        """
        Remove collection of nodes from the graph in-place.  Note: All edges incident on the nodes are also removed.

        :param nodes: collection of hashable objects

        :return: None
        """
        for node in set(nodes):
            self.remove_node(node)

    def path_exists(self, u: Hashable, v: Hashable) -> bool:
        """
        Check if path exists from u to v.

        :param u: hashable object; the source node.

        :param v: hashable object; the target node.

        :return: bool.  Return True if a path exists from u to v, else False.
        """
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
        """
        Get the edge weight for edge u-v.

        :param u: hashable object; the source node.

        :param v: hashable object; the target node.

        :return: numeric value; the edge weight
        """
        return self.edge_weights[(u, v)]


class Graph(DiGraph):
    """
    Class Graph for undirected graphs.
    """
    @property
    def size(self) -> int:
        # Divide by 2 because undirected
        return len(self.edge_weights) // 2

    def add_edge(self, u: Hashable, v: Hashable, weight: gt.Numeric = 1) -> None:
        """
        Add an edge to the graph in-place.  This method will create both u-v and v-u edges for undirected graph.

        :param u: hashable object

        :param v: hashable object

        :param weight: numeric.  The edge weight.  Default is 1.

        :return: None
        """
        super().add_edge(u, v, weight)
        super().add_edge(v, u, weight)

    def remove_edge(self, u: Hashable, v: Hashable) -> None:
        """
        Remove the edge from the graph.  Note: This method will remove both u-v and v-u edges for undirected graph.

        :param u: hashable object

        :param v: hashable object

        :return: None
        """
        super().remove_edge(u, v)
        super().remove_edge(v, u)

    @property
    def is_directed(self) -> bool:
        return False


GraphTypeHint = Union[Graph, DiGraph]
