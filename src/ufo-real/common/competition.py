# -*- coding: utf-8 -*-
"""Competition module"""

__copyright__ = "Copyright (c) 2025 HSLU PREN Team 2, FS25. All rights reserved."


from typing import Any
import json
from os import path
from pyaddict import JDict

from network.edge import Edge
from network.node import Node, NodeLabel, NodeType
from network.network import Network


DYNAMIC_NETWORK_FILE = "dynamic_network.json"


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


def update_dynamic_network(config: dict[str, Any]) -> None:
    """Update the dynamic network for the competition"""

    with open(DYNAMIC_NETWORK_FILE, "w+", encoding="utf8") as file:
        json.dump(config, file)


def create_dynamic_network() -> Network:
    """Create a dynamic network for the competition"""
    if not path.exists(DYNAMIC_NETWORK_FILE):
        return create_network()

    with open(DYNAMIC_NETWORK_FILE, "r", encoding="utf8") as file:
        config = JDict(json.load(file)).chain()

    start = Node(
        x=config.assertGet("START.x", float),
        y=config.assertGet("START.y", float),
        label=NodeLabel.START,
        node_type=NodeType.START,
    )
    w = Node(
        x=config.assertGet("W.x", float),
        y=config.assertGet("W.y", float),
        label=NodeLabel.W,
    )
    x = Node(
        x=config.assertGet("X.x", float),
        y=config.assertGet("X.y", float),
        label=NodeLabel.X,
    )
    y = Node(
        x=config.assertGet("Y.x", float),
        y=config.assertGet("Y.y", float),
        label=NodeLabel.Y,
    )
    z = Node(
        x=config.assertGet("Z.x", float),
        y=config.assertGet("Z.y", float),
        label=NodeLabel.Z,
    )
    a = Node(
        x=config.assertGet("A.x", float),
        y=config.assertGet("A.y", float),
        label=NodeLabel.A,
        node_type=NodeType.END,
    )
    b = Node(
        x=config.assertGet("B.x", float),
        y=config.assertGet("B.y", float),
        label=NodeLabel.B,
        node_type=NodeType.END,
    )
    c = Node(
        x=config.assertGet("C.x", float),
        y=config.assertGet("C.y", float),
        label=NodeLabel.C,
        node_type=NodeType.END,
    )

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
