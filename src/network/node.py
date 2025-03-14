# -*- coding: utf-8 -*-
"""Node module"""

__copyright__ = "Copyright (c) 2025 HSLU PREN Team 2, FS25. All rights reserved."

from dataclasses import dataclass
from enum import StrEnum


class NodeType(StrEnum):
    """Node type enumeration"""

    START = "start"
    END = "end"
    NORMAL = "normal"


class NodeLabel(StrEnum):
    """Node label enumeration"""

    START = "START"
    W = "W"
    X = "X"
    Y = "Y"
    Z = "Z"
    A = "A"
    B = "B"
    C = "C"

    UNDEFINED = "<UNDEFINED>"


@dataclass
class Node:
    """Node of a graph"""

    x: float
    y: float
    label: NodeLabel = NodeLabel.UNDEFINED
    node_type: NodeType = NodeType.NORMAL
    disabled: bool = False
    visited: bool = False

    def __str__(self) -> str:
        return f"Node({self.label})"

    def __repr__(self) -> str:
        return str(self)

    def __eq__(self, value: object) -> bool:
        if not isinstance(value, Node):
            return False
        return self.label == value.label

    def __hash__(self) -> int:
        return hash(self.label)
