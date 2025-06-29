# -*- coding: utf-8 -*-
"""
# Robot Module:
Utility base class for Nodes in order to make the code\n
more understandable, better structured and easier to\n
adapt and fix.\n
"""

__copyright__ = "Copyright (c) 2025 HSLU PREN Team 2, FS25. All rights reserved."

from math import atan2, degrees, sqrt


class Robot:
    """Class containing all the values about the Robot"""

    posX: int
    posY: int
    angle: float

    # [Constructor] with all the values for the robot
    # - posX      = (int) horizontal position of the robot in mm
    # - posY      = (int) vertical position of the robot in mm
    # (center (0,0) is left upper corner)
    # - angle     = (int) degree in which direction the camera is facing
    #               (0° to the right - East, 90° straight down - South,
    #               180° to the left - Weast, 270° straight up - North)
    def __init__(self, pos_x: int, pos_y: int, angle: float):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.angle = angle

    def __str__(self) -> str:
        return (
            "Robot:\n"
            + "------\n"
            + f"- Position:\t({self.posX}mm,{self.posY}mm)\n"
            + f"- Direction:\t{self.angle}°"
        )

    def __eq__(self, value) -> bool:
        if isinstance(value, Robot):
            return (
                self.pos_x == value.pos_x
                and self.pos_y == value.pos_y
                and self.angle == value.angle
            )
        else:
            return False

    @property
    def get_pos_x(self) -> int:
        """get the width value of the location the robot is at right now"""
        return self.pos_x

    def __set_pos_x(self, new_pos_x: int) -> None:
        self.pos_x = new_pos_x

    @property
    def get_pos_y(self) -> int:
        """get the height value of the location the robot is at right now"""
        return self.pos_y

    def __set_pos_y(self, new_pos_y: int) -> None:
        self.pos_y = new_pos_y

    @property
    def get_direction(self) -> float:
        """get the direction the robot is facing as an angle in degrees"""
        return self.angle

    def __set_direction(self, new_angle: float) -> None:
        self.angle = new_angle

    def change_position(self, coordinates: tuple[int, int]) -> None:
        """get the location of the robot entirely"""
        self.__set_pos_x(coordinates[0])
        self.__set_pos_y(coordinates[1])

    def turn_by(self, turn_angle: float) -> None:
        """
        Change the direction in which the robot is facing by\n
        ``turn_angle`` amount of degrees. Should be of type ``float``.
        """
        self.__set_direction(self.get_direction + turn_angle % 360.0)

    def turn_towards(self, coordinates: tuple[int, int]) -> None:
        """
        Set the robot's direction by inputting the new\n
        ``coordinates`` it should be facing.
        """
        self.__set_direction(self._compute_angle(coordinates))

    # Helper function to determine the distance and angle of
    # a point on the plane in comparison to the robot
    # - x       = (int) mm horizontel coordinate of the point
    # - y       = (int) mm vertical coordinate of the point
    # (The center (0,0) is the upper-left corner of the map,
    # going down or right from there increases the value)
    # - return  = (dDeg, dDis)
    # - dDeg    = (int) amount of ° to turn in order to be
    #             aligned between -180 and 180
    # - dDis    = (float) distance in mm towards the point
    def compute_distance_and_difference(
        self, coordinates: tuple[int, int]
    ) -> tuple[float, float]:
        """
        It computes the distance between the robot and the point\n
        with the given ``coordinates``, as well as the difference\n
        between the direction in which the robot is facing and\n
        the angle at which the point can be found.
        """
        # calculate difference in angles
        d_deg = (
            self._compute_angle(coordinates) - self.get_direction + 180.0
        ) % 360 - 180.0

        # calculate distance
        d_dis = self._compute_distance(coordinates)

        return (d_deg, d_dis)

    def _compute_angle(self, coordinates: tuple[int, int]) -> float:
        dx, dy = self._compute_deltas(coordinates)
        return degrees(atan2(dy, dx))

    def _compute_distance(self, coordinates: tuple[int, int]) -> float:
        dx, dy = self._compute_deltas(coordinates)
        return sqrt(dx**2 + dy**2)

    def _compute_deltas(self, coordinates: tuple[int, int]) -> tuple[int, int]:
        dx = coordinates[0] - self.get_pos_x
        dy = coordinates[1] - self.get_pos_y
        return (dx, dy)
