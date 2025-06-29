# -*- coding: utf-8 -*-
"""Obstacle module"""

__copyright__ = "Copyright (c) 2025 HSLU PREN Team 2, FS25. All rights reserved."

# Utility base class for images of Obstacles. It is supposed
# to make the code more understandable and allow the image
# recognition to same all the objects it recorded.


class Obstacle:
    """data class to save values about obstacles"""

    LENGTH = 70  # length of the obstacle in mm
    DEPTH = 20  # depth of the obstacle in mm
    HEIGHT = 50  # hight of the obstacle in mm

    __counter: int = 1  # unique id for all obstacles

    x_min: int  # upper left corner x value in px
    y_min: int  # upper left corner y value in px
    x_max: int  # lower right corner x value in px
    y_max: int  # lower right corner y value in px
    id: int  # unique id in order to compare and identify

    # [Constructor] with the values for the visual corners
    # of the image of the obstacle
    # x_min = (int) # upper left corner x value in px
    # y_min = (int) # upper left corner y value in px
    # x_max = (int) # lower right corner x value in px
    # y_max = (int) # lower right corner y value in px
    def __init__(self, x_min: int, y_min: int, x_max: int, y_max: int):
        self.x_min = x_min
        self.y_min = y_min
        self.x_max = x_max
        self.y_max = y_max
        self.id = self.__counter

        self.__counter += 1

    def __str__(self) -> str:
        return f"Obstacle {self.id}: ({self.x_min},{self.y_min}),\
            ({self.x_max},{self.y_max})"

    def __eq__(self, other) -> bool:
        if isinstance(other, Obstacle):
            return (
                self.x_min == other.x_min
                and self.y_min == other.y_min
                and self.x_max == other.x_max
                and self.y_max == other.y_max
            )
        elif isinstance(other, str):
            return str(self.id) == other
        elif isinstance(other, int):
            return self.id == other
        else:
            raise ValueError("Incompatible type for comparison.")

    @property
    def get_upper_left(self) -> tuple[int, int]:
        """get the coordinates of the upper left corner"""
        return (self.x_min, self.y_min)

    @property
    def get_lower_right(self) -> tuple[int, int]:
        """get the coordinates of the lower right corner"""
        return (self.x_max, self.y_max)

    @property
    def get_id(self) -> str:
        """get the unique id of this obstacle"""
        return str(self.id)

    @classmethod
    def get_length(cls) -> int:
        """get the standard ``length`` of an obstacle"""
        return Obstacle.LENGTH

    @classmethod
    def get_depth(cls) -> int:
        """get the standard ``depth`` of an obstacle"""
        return Obstacle.DEPTH

    @classmethod
    def get_height(cls) -> int:
        """get the standard ``height`` of an obstacle"""
        return Obstacle.HEIGHT
