# -*- coding: utf-8 -*-
"""Competition module"""

__copyright__ = "Copyright (c) 2025 HSLU PREN Team 2, FS25. All rights reserved."


from network.edge import Edge
from network.node import Node, NodeLabel, NodeType
from network.network import Network


def create_network() -> Network:
    """Create a network for the competition"""
    start = Node(NodeType.START, NodeLabel.START, x=0, y=0)
    w = Node(NodeType.NORMAL, NodeLabel.W, x=2, y=1)
    x = Node(NodeType.NORMAL, NodeLabel.X, x=0.5, y=1)
    y = Node(NodeType.NORMAL, NodeLabel.Y, x=0, y=2.5)
    z = Node(NodeType.NORMAL, NodeLabel.Z, x=-2, y=1)
    a = Node(NodeType.END, NodeLabel.A, x=2, y=4)
    b = Node(NodeType.END, NodeLabel.B, x=0, y=5)
    c = Node(NodeType.END, NodeLabel.C, x=-2, y=4)

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
