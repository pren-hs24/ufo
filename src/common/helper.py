# -*- coding: utf-8 -*-
"""helper module"""

__copyright__ = "Copyright (c) 2025 HSLU PREN Team 2, FS25. All rights reserved."

import math
from network.node import Node


class Math:
    """math helper"""

    @staticmethod
    def calculate_angle_deg(on_node: Node, to_node: Node) -> float:
        """
        calculates the angle between two points

        :param on_node: point A
        :param to_node: point B
        :return angle: in degrees
        """
        dx = -1 * (to_node.x - on_node.x)
        dy = to_node.y - on_node.y
        rad = math.atan2(dy, dx)
        return math.degrees(rad) - 90

    @staticmethod
    def optimise_for_next_angle(
        with_current_angle: float, for_next_angle: float
    ) -> float:
        """
        optimises an angle by transforming it to an equivalent angle
        that is closer to the target angle.

        for example, an angle of 0° will be transformed to the equivalent 360°,
        if the target angle is 350°, as the absolute difference of these angles abs(360 - 350)
        will be less than that of untransformed angles abs(360 - 0).

        :param with_current_angle: the angle to be optimised and returned
        :param to_node: the target angle
        :return optimised_current_angle: in degrees
        """
        diff = abs(for_next_angle - with_current_angle)
        diff_plus_360 = abs(for_next_angle - (with_current_angle + 360))
        diff_min_360 = abs(for_next_angle - (with_current_angle - 360))

        if diff < diff_plus_360:
            if diff < diff_min_360:
                return with_current_angle
            return with_current_angle - 360
        if diff_plus_360 < diff_min_360:
            return with_current_angle + 360
        return with_current_angle - 360
