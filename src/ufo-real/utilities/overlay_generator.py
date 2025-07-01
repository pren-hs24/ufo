# -*- coding: utf-8 -*-
"""
Overlay Module:
Utility class that adds a minimap to the overlay in the image.
"""

__copyright__ = "Copyright (c) 2025 HSLU PREN Team 2, FS25. All rights reserved."

from math import cos, sin, radians
import cv2

from basic import Colour as c
from components import Camera, Graph, Robot

ALPHA: float = 0.8
REAL_WIDTH: int = 4500

# Colour presets
BLACK = c.bgr("BLACK")
LIGHT = c.bgr("LIGHT")
GREEN = c.bgr("GREEN")


class OverlayGenerator:
    """Class to generate an overlay for easier debugging."""

    def __init__(self, camera: Camera, graph: Graph, robot: Robot) -> None:
        self.camera = camera
        self.graph = graph
        self.robot = robot

    def draw_minimap(self, img: cv2.typing.MatLike) -> None:
        """Draw the minimap overlay on the image."""
        minimap_gen = MinimapOverlay(self)
        minimap_gen.draw_minimap_on_image(img)


class MinimapOverlay:
    """Class to generate a minimap to show birdseye view."""

    def __init__(self, generator: OverlayGenerator) -> None:
        self.generator: OverlayGenerator = generator
        self.size: int = int(
            min(generator.camera.image_width // 2, generator.camera.image_height // 2)
        )
        self.boarder: int = int(self.size // 10)
        self.ratio: float = self.size / REAL_WIDTH
        self.map_size: int = self.size - self.boarder
        self.upper_left: tuple[int, int] = (
            generator.camera.image_width - self.map_size - self.boarder,
            self.boarder,
        )
        self.lower_right: tuple[int, int] = (
            generator.camera.image_width - self.boarder,
            self.map_size + self.boarder,
        )

    def draw_minimap_on_image(self, img: cv2.typing.MatLike) -> None:
        """Generate the minimap overlay."""

        self._draw_minimap_background(img)
        self._draw_graph_nodes_on_minimap(img)
        self._draw_graph_edges_on_minimap(img)
        self._draw_robot_and_fov(img)

    def _draw_minimap_background(self, img: cv2.typing.MatLike) -> None:
        """Draw the background of the minimap."""
        overlay = img.copy()

        # draw map background
        cv2.rectangle(overlay, self.upper_left, self.lower_right, BLACK, -1)  # pylint: disable=no-member
        cv2.rectangle(overlay, self.upper_left, self.lower_right, LIGHT, 1)  # pylint: disable=no-member

        cv2.addWeighted(overlay, ALPHA, img, 1 - ALPHA, 0, img)  # pylint: disable=no-member

    def _draw_graph_nodes_on_minimap(self, img: cv2.typing.MatLike) -> None:
        """Draw the graph nodes on the minimap."""
        overlay = img.copy()

        # Draw all nodes
        for n in self.generator.graph.get_nodes:
            point = _convert_to_map_coordinates(
                n.get_coordinates, self.ratio, self.upper_left
            )

            cv2.circle(overlay, point, 5, LIGHT, -1)  # pylint: disable=no-member

        cv2.addWeighted(overlay, ALPHA, img, 1 - ALPHA, 0, img)  # pylint: disable=no-member

    def _draw_graph_edges_on_minimap(self, img: cv2.typing.MatLike) -> None:
        """Draw the graph edges on the minimap."""
        overlay = img.copy()

        # Draw all edges
        for e in self.generator.graph.get_edges:
            node_a, node_b = e.get_nodes

            point_a = _convert_to_map_coordinates(
                node_a.get_coordinates, self.ratio, self.upper_left
            )
            point_b = _convert_to_map_coordinates(
                node_b.get_coordinates, self.ratio, self.upper_left
            )

            cv2.line(overlay, point_a, point_b, LIGHT, 1)  # pylint: disable=no-member

        cv2.addWeighted(overlay, ALPHA, img, 1 - ALPHA, 0, img)  # pylint: disable=no-member

    def _draw_robot_and_fov(self, img: cv2.typing.MatLike) -> None:
        """Draw the robot and its field of view on the minimap."""
        overlay = img.copy()

        # Draw robot and FOV triangle
        fov_length: int = 1000  # in mm
        left_angle: float = (
            radians(self.generator.robot.get_direction)
            - radians(self.generator.camera.get_hfov) / 2
        )
        right_angle: float = (
            radians(self.generator.robot.get_direction)
            + radians(self.generator.camera.get_hfov) / 2
        )
        robot_x: int = self.generator.robot.get_pos_x
        robot_y: int = self.generator.robot.get_pos_y

        p1 = (int(robot_x), int(robot_y))
        p2 = (
            int(robot_x + fov_length * cos(left_angle)),
            int(robot_y + fov_length * sin(left_angle)),
        )
        p3 = (
            int(robot_x + fov_length * cos(right_angle)),
            int(robot_y + fov_length * sin(right_angle)),
        )

        m1 = _convert_to_map_coordinates(p1, self.ratio, self.upper_left)
        m2 = _convert_to_map_coordinates(p2, self.ratio, self.upper_left)
        m3 = _convert_to_map_coordinates(p3, self.ratio, self.upper_left)

        cv2.circle(overlay, m1, 10, GREEN, -1)  # pylint: disable=no-member
        cv2.line(overlay, m1, m2, GREEN, 1)  # pylint: disable=no-member
        cv2.line(overlay, m1, m3, GREEN, 1)  # pylint: disable=no-member

        cv2.addWeighted(overlay, ALPHA, img, 1 - ALPHA, 0, img)  # pylint: disable=no-member


def _convert_to_map_coordinates(
    node: tuple[int, int], ratio: float, offset: tuple[int, int]
) -> tuple[int, int]:
    px = int(round(node[0] * ratio) + offset[0])
    py = int(round(node[1] * ratio) + offset[1])

    return (px, py)
