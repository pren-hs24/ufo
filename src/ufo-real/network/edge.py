# -*- coding: utf-8 -*-
"""Edge module"""

__copyright__ = "Copyright (c) 2025 HSLU PREN Team 2, FS25. All rights reserved."

from common.constants import CLEAR_OBSTACLE_PENALTY_WEIGHT
from .node import Node


class Edge:
    """Edge of a graph"""

    disabled: bool = False
    obstructed: bool = False
    visited: bool = False

    def __init__(self, *nodes: Node) -> None:
        self.nodes = nodes

    @property
    def distance(self) -> float:
        """Get the distance between the two nodes"""
        a = self.nodes[0]
        b = self.nodes[1]
        return float(((a.x - b.x) ** 2 + (a.y - b.y) ** 2) ** 0.5)

    @property
    def weight(self) -> float:
        """Get the weight of the edge"""
        if self.disabled or any(node.disabled for node in self.nodes):
            return float("inf")
        if self.obstructed:
            return self.distance + CLEAR_OBSTACLE_PENALTY_WEIGHT
        return self.distance

    def __str__(self) -> str:
        return f"Edge({self.nodes[0].label} -> {self.nodes[1].label})"

    def __repr__(self) -> str:
        return str(self)

    def __eq__(self, value: object) -> bool:
        if not isinstance(value, Edge):
            return False
        return set(self.nodes) == set(value.nodes)

    def __hash__(self) -> int:
        return hash(self.nodes)
