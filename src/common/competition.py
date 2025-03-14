# -*- coding: utf-8 -*-
"""Competition module"""

__copyright__ = "Copyright (c) 2025 HSLU PREN Team 2, FS25. All rights reserved."


from network.edge import Edge
from network.node import Node, NodeLabel, NodeType
from network.network import Network


def create_network() -> Network:
    """Create a network for the competition"""
    start = Node(x=0, y=0, label=NodeLabel.START, node_type=NodeType.START)
    w = Node(x=2, y=1, label=NodeLabel.W)
    x = Node(x=0.5, y=1, label=NodeLabel.X)
    y = Node(x=0, y=2.5, label=NodeLabel.Y)
    z = Node(x=-2, y=1, label=NodeLabel.Z)
    a = Node(x=2, y=4, label=NodeLabel.A, node_type=NodeType.END)
    b = Node(x=0, y=5, label=NodeLabel.B, node_type=NodeType.END)
    c = Node(x=-2, y=4, label=NodeLabel.C, node_type=NodeType.END)

    network = Network()

    network.add_edge(Edge(start, w))
    network.add_edge(Edge(start, x))
    network.add_edge(Edge(start, z))
    network.add_edge(Edge(w, a))
    network.add_edge(Edge(w, x))
    network.add_edge(Edge(x, y))
    network.add_edge(Edge(x, z))
    network.add_edge(Edge(x, a))
    network.add_edge(Edge(y, a))
    network.add_edge(Edge(y, b))
    network.add_edge(Edge(y, c))
    network.add_edge(Edge(y, z))
    network.add_edge(Edge(z, c))
    network.add_edge(Edge(a, b))
    network.add_edge(Edge(b, c))

    return network
