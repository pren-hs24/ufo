# -*- coding: utf-8 -*-
"""
Utility base class for Nodes in order to make the code\n
more understandable, better structured and easier to\n
adapt and fix.\n
"""

__copyright__ = "Copyright (c) 2025 HSLU PREN Team 2, FS25. All rights reserved."


from enum import Enum


class RealNodeState(Enum):
    """RealNode state enumeration"""

    UNKNOWN = 0
    FREE = 1
    BLOCKED = 2


class RealNodeLabel(Enum):
    """RealNode label enumeration"""

    START = 0
    A = 1
    B = 2
    C = 3
    W = 4
    X = 5
    Y = 6
    Z = 7


class RealNode:
    """Node measured in reality"""

    REAL_RADIUS: int = 30  # expected radius of a Node on the Graph in mm

    pos_x: int
    pos_y: int
    label: RealNodeLabel
    state: RealNodeState

    # [Constructor] with the values for physical nodes
    # - label     = (str) the label by which it is identified
    # - posX      = (int) horizontal position of the node in mm
    # - posY      = (int) vertical position of the node in mm
    # (center (0,0) is left upper corner)
    def __init__(self, label: RealNodeLabel, pos_x: int, pos_y: int):
        self.label = label
        self.state = RealNodeState.UNKNOWN
        self.pos_x = pos_x
        self.pos_y = pos_y

    def __str__(self) -> str:
        return f"Node: {self.label.name}({self.pos_x}mm,{self.pos_y}mm) -> {self.state.name}"

    def __eq__(self, other: object) -> bool:
        if isinstance(other, RealNode):
            return (
                self.label == other.label
                and self.pos_x == other.pos_x
                and self.pos_y == other.pos_y
            )
        if isinstance(other, str):
            return self.label.name == other
        return False

    @property
    def get_label(self) -> str:
        """get the name of the label asigned to this node"""
        return self.label.name

    def set_label(self, label: RealNodeLabel) -> None:
        """change the label of the node to what you need it to be"""
        self.label = label

    @property
    def get_pos_x(self) -> int:
        """get the real width value of the location"""
        return self.pos_x

    def set_pos_x(self, pos_x: int) -> None:
        """change the real width value of the location"""
        self.pos_x = pos_x

    @property
    def get_pos_y(self) -> int:
        """get the real height value of the location"""
        return self.pos_y

    def set_pos_y(self, pos_y: int) -> None:
        """change the real height value of the location"""
        self.pos_y = pos_y

    @property
    def get_coordinates(self) -> tuple[int, int]:
        """get the location of the node"""
        return (self.pos_x, self.pos_y)

    def change_position(self, pos_x: int, pos_y: int) -> None:
        """change the location entirely"""
        self.set_pos_x(pos_x)
        self.set_pos_y(pos_y)

    @classmethod
    def get_real_radius(cls) -> int:
        """get the radius of a node"""
        return RealNode.REAL_RADIUS

    def is_available(self) -> None:
        """let the system know that this node is usable"""
        self._change_state(RealNodeState.FREE)

    def is_blocked(self) -> None:
        """let the system know that this node can **not** be used"""
        self._change_state(RealNodeState.BLOCKED)

    def _change_state(self, new_state: RealNodeState) -> None:
        self.state = new_state
