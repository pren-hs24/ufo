# -*- coding: utf-8 -*-
"""Node module"""

__copyright__ = "Copyright (c) 2025 HSLU PREN Team 2, FS25. All rights reserved."

from typing import Callable
from .edge import Edge
from .node import Node, NodeType, NodeLabel


class Network:
    """Network of nodes and edges"""

    def __init__(self) -> None:
        self._edges: set[Edge] = set()

    def add_edge(self, edge: Edge) -> None:
        """Add an edge to the network"""
        self._edges.add(edge)

    @property
    def edges(self) -> set[Edge]:
        """Get all edges of the network"""
        return self._edges

    @property
    def nodes(self) -> set[Node]:
        """Get all nodes of the network"""
        nodes: set[Node] = set()
        for edge in self._edges:
            nodes.add(edge.nodes[0])
            nodes.add(edge.nodes[1])
        return nodes

    @property
    def start(self) -> Node:
        """Get the start node of the network"""
        for node in self.nodes:
            if node.node_type == NodeType.START:
                return node
        raise ValueError("Start node not found")

    @property
    def end(self) -> set[Node]:
        """Get all end nodes of the network"""
        return {node for node in self.nodes if node.node_type == NodeType.END}

    def get_edge(self, node1: Node, node2: Node) -> Edge:
        """Get an edge between two nodes"""
        for edge in self._edges:
            if node1 in edge.nodes and node2 in edge.nodes:
                return edge
        raise ValueError("Edge not found")

    def get_node_by_label(self, node: NodeLabel) -> Node:
        """Get a node by label"""
        return next(n for n in self.nodes if n.label == node)

    def get_edge_by_label(self, node1: NodeLabel, node2: NodeLabel) -> Edge:
        """Get an edge between two nodes by label"""
        return self.get_edge(
            self.get_node_by_label(node1), self.get_node_by_label(node2)
        )

    def __str__(self) -> str:
        return f"Network({len(self._edges)} edges, {len(self.nodes)} nodes)"

    def __repr__(self) -> str:
        return str(self)


type NetworkProvider = Callable[[], Network]
