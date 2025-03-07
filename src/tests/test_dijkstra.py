# -*- coding: utf-8 -*-
"""dijkstra pathfinder tests"""

__copyright__ = "Copyright (c) 2025 HSLU PREN Team 2, FS25. All rights reserved."


from common.competition import create_network
from network.node import NodeLabel
from pathfinder.dijkstra import DijkstraPathfinder


def test_unmodified() -> None:
    """
    Test the Dijkstra pathfinder with an unmodified network
    """
    network = create_network()
    pathfinder = DijkstraPathfinder()
    b = next(x for x in network.end if x.label == NodeLabel.B)

    path = pathfinder.find_path(network, b)

    assert path[0].label == NodeLabel.START
    assert path[1].label == NodeLabel.X
    assert path[2].label == NodeLabel.Y
    assert path[3].label == NodeLabel.B


def test_disabled_node() -> None:
    """
    Test the Dijkstra pathfinder with node X disabled
    """
    network = create_network()
    pathfinder = DijkstraPathfinder()
    b = next(x for x in network.end if x.label == NodeLabel.B)

    network.get_node_by_label(NodeLabel.X).disabled = True
    path = pathfinder.find_path(network, b)

    assert path[0].label == NodeLabel.START
    assert path[1].label == NodeLabel.Z
    assert path[2].label == NodeLabel.Y
    assert path[3].label == NodeLabel.B


def test_disabled_edge() -> None:
    """
    Test the Dijkstra pathfinder with edge X -> Y disabled
    """
    network = create_network()
    pathfinder = DijkstraPathfinder()
    b = next(x for x in network.end if x.label == NodeLabel.B)

    network.get_edge_by_label(NodeLabel.X, NodeLabel.Y).disabled = True
    path = pathfinder.find_path(network, b)

    assert path[0].label == NodeLabel.START
    assert path[1].label == NodeLabel.X
    assert path[2].label == NodeLabel.A
    assert path[3].label == NodeLabel.B


def test_obstructed_edge() -> None:
    """
    Test the Dijkstra pathfinder with edge X -> Y disabled and edge X -> A obstructed
    """
    network = create_network()
    pathfinder = DijkstraPathfinder()
    b = next(x for x in network.end if x.label == NodeLabel.B)

    network.get_edge_by_label(NodeLabel.X, NodeLabel.Y).disabled = True
    network.get_edge_by_label(NodeLabel.X, NodeLabel.A).obstructed = True
    path = pathfinder.find_path(network, b)

    assert path[0].label == NodeLabel.START
    assert path[1].label == NodeLabel.Z
    assert path[2].label == NodeLabel.Y
    assert path[3].label == NodeLabel.B


def test_complex() -> None:
    """
    Test the Dijkstra pathfinder with edge X -> A obstructed, edge X -> Y and node Z disabled
    """
    network = create_network()
    pathfinder = DijkstraPathfinder()
    b = next(x for x in network.end if x.label == NodeLabel.B)

    network.get_edge_by_label(NodeLabel.X, NodeLabel.Y).disabled = True
    network.get_edge_by_label(NodeLabel.X, NodeLabel.A).obstructed = True
    network.get_node_by_label(NodeLabel.Z).disabled = True
    path = pathfinder.find_path(network, b)

    assert path[0].label == NodeLabel.START
    assert path[1].label == NodeLabel.W
    assert path[2].label == NodeLabel.A
    assert path[3].label == NodeLabel.B
