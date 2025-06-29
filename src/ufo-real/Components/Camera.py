# -*- coding: utf-8 -*-
"""
Camera module:\n
Utility base class for the camera and all the specs it has.\n
Primarily heps to make the code more understandable, better\n
structured and easier to adapt and fix.\n
"""

__copyright__ = "Copyright (c) 2025 HSLU PREN Team 2, FS25. All rights reserved."

#

import numpy as np

from .obstacle import Obstacle
from .pylon import Pylon
from .real_node import RealNode
from .visual_node import VisualNode


class Camera:
    """the camera and all its predefined settings"""

    image_width: int  # width of the image
    image_height: int  # height of the image
    elevation: int
    angle: int
    hfov: int
    vfov: int
    ratio: tuple[int, int]

    # [Constructor] with all the base values for the camera
    # - width     = (int) pixels an camera image has in width
    # - height    = (int) pixels an camera image has in height
    # - elevation = (int) mm the camera is off the floor
    # - angle     = (int) degrees to which the camera is angled
    #               downwards (90° straight ahead, 80° slightly
    #               down, 56° optimal)
    # - fov       = (int) degrees the camera field of view captures
    def __init__(self, width: int, height: int, elevation: int, angle: int, fov: int):
        self.image_width = width
        self.image_height = height
        self.elevation = elevation
        self.angle = angle
        self.hfov = fov  # horizontal field of view

        temp = self.image_width / self.image_height
        if np.abs(temp - 1.77) <= 0.01:
            self.ratio = (16, 9)
        elif np.abs(temp - 1.6) <= 0.01:
            self.ratio = (16, 10)
        elif np.abs(temp - 1.33) <= 0.01:
            self.ratio = (4, 3)
        elif np.abs(temp - 1) <= 0.01:
            self.ratio = (1, 1)
        else:
            raise SystemError("Unknown ratio")

        self.vfov = int(
            np.abs(self.hfov * self.image_height / self.image_width)
        )  # vertical field of view

    # simplified constructor
    @classmethod
    def from_image(cls, width: int, height: int):
        """get a camara without knowing all the attributes"""
        return cls(width, height, 55, 56, 70)

    # default camera settings constructor
    @classmethod
    def from_default(cls):
        """get a camara while knowing only the dimensions of the image"""
        return cls.from_image(2560, 1440)

    def __str__(self) -> str:
        return (
            "Camera specs:\n"
            + "-------------\n"
            + f"- Image:\t({self.image_width}X{self.image_height})\n"
            + f"- Ratio:\t{self.ratio[0]}:{self.ratio[1]}\n"
            + f"- Elevation:\t{self.elevation}mm\n"
            + f"- Angle:\t{self.angle}°\n"
            + f"- HFOV:\t\t{self.hfov}°\n"
            + f"- VFOV:\t\t{self.vfov}°"
        )

    def __eq__(self, value) -> bool:
        if isinstance(value, Camera):
            return (
                self.image_width == value.image_width
                and self.image_height == value.image_height
                and self.elevation == value.elevation
                and self.angle == value.angle
                and self.hfov == value.hfov
                and self.vfov == value.vfov
                and self.ratio[0] == value.ratio[0]
                and self.ratio[1] == value.ratio[1]
            )
        else:
            return False

    @property
    def get_width(self) -> int:
        """get the width of the image"""
        return self.image_width

    @property
    def get_height(self) -> int:
        """get the height of the image"""
        return self.image_height

    @property
    def get_elevation(self) -> int:
        """get the height at which the camera is mounted"""
        return self.elevation

    @property
    def get_angle(self) -> int:
        """get the direction the camera is facing as an angle in degrees"""
        return self.angle

    @property
    def get_hfov(self) -> int:
        """get the angle of the horizontal field of view"""
        return self.hfov

    @property
    def get_vfov(self) -> int:
        """get the angle of the vertical field of view"""
        return self.vfov

    @property
    def get_ratio(self) -> float:
        """get the the image ratio"""
        return np.abs(self.ratio[0] / self.ratio[1])

    def compute_image_position(self, angle: float, distance: float) -> tuple[int, int]:
        """
        Computes where in the image an object should be draw depending\n
        on the angle the camera needs to turn around to have it in its\n
        center and the distance between the camera and the object.\n
        - ``angle``     = (``int``) degrees to the camera\n
        (+ = to the right, - = to the left)\n
        - ``distance``  = (``float``) distance in mm between the object and the camera\n
        - return    = (``int``, ``int``) px width and height where the center should be\n
        """
        # type check
        if not isinstance(angle, float) or not isinstance(distance, float):
            raise ImportError("TypeError has occured in image rendering.")

        x = int(
            np.round((self.image_width / 2) + (angle * (self.image_width / self.hfov)))
        )

        temp = 0.0
        if distance == 0:
            if self.elevation >= 0:
                temp = 90.0
            else:
                temp = -90.0
        else:
            temp = np.degrees(np.arctan(self.elevation / distance))

        beta = 90.0 - temp
        beta_diff = beta - (self.angle - (self.vfov / 2))
        y = int(
            np.round(self.image_height - (beta_diff / self.vfov * self.image_height))
        )

        return (x, y)

    def _compute_pylon_distance(self, pylon: Pylon) -> float:
        """
        Computes the distance to a pylon based on its height the camera stats.
        - ``pylon`` = (``Pylon``) technically only needs the field real_height
        - return    = (``float``) real distance to the pylon in mm
        """
        angle = (
            self.angle
            + (self.vfov / 2)
            - (pylon.get_ymin * self.vfov / self.image_height)
        )
        return float(
            np.tan(np.radians(angle)) * np.abs(self.elevation - Pylon.get_real_height())
        )

    def compute_object_image_dimensions(
        self, distance: float, radius: int
    ) -> tuple[int, int]:
        """
        Computes the width and height in pixels of an object with the\n
        innate camera stats and the real distance and radius of the object.\n
        (Usually a node)\n
        - ``distance``\t= (``float``) how far away from the camera the object is in mm\n
        - ``radius``\t= (``int``) how large the radius of the object is in mm\n
        - return\t= (``int``, ``int``) px width and height how wide the object looks in the image\n
        """
        if distance == 0:
            alpha = 0
        else:
            alpha = np.degrees(np.arctan(distance / self.elevation))
        alpha_dot = np.degrees(np.arctan((distance + radius) / self.elevation))
        alpha_diff = np.abs(alpha_dot - alpha)
        height_img = int(np.abs((alpha_diff / self.vfov * self.image_height)))

        gamma = np.degrees(np.arctan(distance / (self.elevation - radius)))
        beta = 180.0 - (180.0 - gamma) - alpha
        width_img = int(abs(beta / self.vfov * self.image_height))

        return (width_img, height_img)

    def compute_hidden_node_image_position(self, pylon: Pylon) -> VisualNode:
        """
        Computes the center point of a node that is being hidden by a pylon.
        Uses the stats of the image of the pylon and the camera to do it.
        - ``pylon``    = (``Pylon``) pylon image detecteted
        - return   = (``int``, ``int``) px width and height where the node should be
        """
        distance: float = self._compute_pylon_distance(pylon)
        px_width, px_height = self.compute_object_image_dimensions(
            distance, RealNode.get_real_radius()
        )

        pos_x = pylon.get_xmin + pylon.get_width // 2
        pos_y = pylon.get_ymax - px_height // 2

        return VisualNode(pylon.get_id, pos_x, pos_y, px_width, px_height)

    def _compute_obstacle_distance(self, obstacle: Obstacle) -> float:
        """
        Computes the distance to an obstacle based on its height and the camera stats.

        Parameters:
            obstacle (Obstacle): Must have get_height() and get_upper_left() methods.

        Returns:
            float: real distance to the obstacle in mm.
        """
        angle = (
            self.angle
            + (self.vfov / 2)
            - (obstacle.get_upper_left[1] * self.vfov / self.image_height)
        )
        return float(
            np.tan(np.radians(angle)) * np.abs(self.elevation - Obstacle.get_height())
        )

    def compute_groundplate(self, obstacle: Obstacle) -> VisualNode:
        """computes where in the image the groundplate/shadow of an obstacle should be"""
        distance: float = self._compute_obstacle_distance(obstacle)
        o_width, o_height = self.compute_object_image_dimensions(
            distance, Obstacle.get_length() // 2
        )

        pos_x = (obstacle.get_upper_left[0] + obstacle.get_lower_right[0]) // 2
        pos_y = obstacle.get_lower_right[1] - o_height // 2

        return VisualNode(obstacle.get_id, pos_x, pos_y, o_width, o_height)
