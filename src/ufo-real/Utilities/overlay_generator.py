# -*- coding: utf-8 -*-
"""
Overlay Module:
Utility class that adds a minimap to the overlay in the image.
"""

__copyright__ = "Copyright (c) 2025 HSLU PREN Team 2, FS25. All rights reserved."

import cv2
import numpy as np
from basic import Colour as c
from components import Camera, Graph, Robot

ALPHA: float = 0.8
REAL_WIDTH: int = 4500

# Colour presets
BLACK = c.bgr("BLACK")
LIGHT = c.bgr("LIGHT")
GREEN = c.bgr("GREEN")


def generate_map_overlay(camera: Camera, graph: Graph, robot: Robot, img) -> None:
    """Generate Minimap"""
    overlay = img.copy()

    image_width: int = camera.get_width
    image_height: int = camera.get_height

    size: int = int(min(image_width // 2, image_height // 2))

    boarder: int = int(size // 10)

    ratio: float = size / REAL_WIDTH

    map_size: int = size - boarder
    map_upper_left: tuple[int, int] = (image_width - map_size - boarder, boarder)
    map_lower_right: tuple[int, int] = (image_width - boarder, map_size + boarder)

    # draw map background
    cv2.rectangle(overlay, map_upper_left, map_lower_right, BLACK, -1)  # pylint: disable=no-member
    cv2.rectangle(overlay, map_upper_left, map_lower_right, LIGHT, 1)  # pylint: disable=no-member

    # Draw all nodes
    for n in graph.get_nodes:
        point = _convert_to_map_coordinates(n.get_coordinates, ratio, map_upper_left)

        cv2.circle(overlay, point, 5, LIGHT, -1)  # pylint: disable=no-member

    # Draw all edges
    for e in graph.get_edges:
        node_a, node_b = e.get_nodes

        point_a = _convert_to_map_coordinates(
            node_a.get_coordinates, ratio, map_upper_left
        )
        point_b = _convert_to_map_coordinates(
            node_b.get_coordinates, ratio, map_upper_left
        )

        cv2.line(overlay, point_a, point_b, LIGHT, 1)  # pylint: disable=no-member

    # Draw robot and FOV triangle
    fov_length: int = 1000  # in mm
    left_angle: float = (
        np.radians(robot.get_direction) - np.radians(camera.get_hfov) / 2
    )
    right_angle: float = (
        np.radians(robot.get_direction) + np.radians(camera.get_hfov) / 2
    )
    robot_x: int = robot.get_pos_x
    robot_y: int = robot.get_pos_y

    p1 = (int(robot_x), int(robot_y))
    p2 = (
        int(robot_x + fov_length * np.cos(left_angle)),
        int(robot_y + fov_length * np.sin(left_angle)),
    )
    p3 = (
        int(robot_x + fov_length * np.cos(right_angle)),
        int(robot_y + fov_length * np.sin(right_angle)),
    )

    m1 = _convert_to_map_coordinates(p1, ratio, map_upper_left)
    m2 = _convert_to_map_coordinates(p2, ratio, map_upper_left)
    m3 = _convert_to_map_coordinates(p3, ratio, map_upper_left)

    cv2.circle(overlay, m1, 10, GREEN, -1)  # pylint: disable=no-member
    cv2.line(overlay, m1, m2, GREEN, 1)  # pylint: disable=no-member
    cv2.line(overlay, m1, m3, GREEN, 1)  # pylint: disable=no-member

    cv2.addWeighted(overlay, ALPHA, img, 1 - ALPHA, 0, img)  # pylint: disable=no-member


def _convert_to_map_coordinates(
    node: tuple[int, int], ratio: float, offset: tuple[int, int]
) -> tuple[int, int]:
    px = int(np.round(node[0] * ratio) + offset[0])
    py = int(np.round(node[1] * ratio) + offset[1])

    return (px, py)
