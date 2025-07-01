# -*- coding: utf-8 -*-
"""
# VisualNode Module:
Utility base class for Nodes in order to make the code\n
more understandable, better structured and easier to\n
adapt and fix.\n
"""

__copyright__ = "Copyright (c) 2025 HSLU PREN Team 2, FS25. All rights reserved."

from math import sqrt
from typing import Self


class VisualNode:
    """VisualNode containing all the information about an object in an image."""

    pos_x: int
    pos_y: int
    width: int
    height: int
    label: str

    # [Constructor] with the values for the visual representation
    # of nodes in an image
    # - label     = (str) the label by which it is identified
    # - width     = (int) horizontal position of the node in px
    # - height    = (int) vertical position of the node in px
    # (center (0,0) is left upper corner)
    def __init__(self, label: str, point: tuple[int, int], width: int, height: int):
        self.label = label
        self.pos_x = point[0]
        self.pos_y = point[1]
        self.width = width
        self.height = height

    @classmethod
    def position_only(cls, label: str, point: tuple[int, int]) -> "VisualNode":
        """a simplyfied constructor for the busy amoung us"""
        return cls(label, point, 1, 1)

    def __str__(self) -> str:
        return f"VisualNode: {self.label}({self.width}px,{self.height}px)"

    def __eq__(self, other: object) -> bool:
        if isinstance(other, str):
            return self.label == other
        if isinstance(other, VisualNode):
            return (
                self.label == other.label
                and self.width == other.width
                and self.height == other.height
            )
        return False

    @property
    def get_label(self) -> str:
        """get the name of the label asigned to this node"""
        return self.label

    @property
    def get_pos_x(self) -> int:
        """get the width value of the upper left corner"""
        return self.pos_x

    @property
    def get_pos_y(self) -> int:
        """get the height values of the upper left corner"""
        return self.pos_y

    @property
    def get_width(self) -> int:
        """get the width of the rectangle in the image"""
        return self.width

    @property
    def get_height(self) -> int:
        """get the height of the rectangle in the image"""
        return self.height

    @property
    def get_coordinates(self) -> tuple[int, int]:
        """get the upper left corner"""
        return (self.pos_x, self.pos_y)

    @property
    def get_dimensions(self) -> tuple[int, int]:
        """get the width and height of this rectangle"""
        return (self.width, self.height)

    def get_distance(self, other: Self) -> float:
        """Compute the distance between this and an other ``VisualNode``."""
        return sqrt(
            (self.get_pos_x - other.get_pos_x) ** 2
            + (self.get_pos_y - other.get_pos_y) ** 2
        )
