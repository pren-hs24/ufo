from Components import Camera, Graph, RealNode, Robot
from Basic import Colour

import numpy as np
import cv2
import matplotlib.pyplot as plt

ALPHA: float = 0.8
REAL_WIDTH: int = 4500

def generate_map_overlay(camera: Camera, graph: Graph, robot: Robot, img) -> None:
    overlay = img.copy()

    image_width: int = camera.getWidth()
    image_height: int = camera.getHeight()

    size: int = int(min(image_width//2, image_height//2))

    boarder: int = int(size // 10)

    ratio: float = size / REAL_WIDTH

    map_size: int = size - boarder
    map_upper_left: tuple[int, int] = (image_width - map_size - boarder, boarder)
    map_lower_right: tuple[int, int] = (image_width - boarder, map_size + boarder)

    # draw map background
    cv2.rectangle(overlay, map_upper_left, map_lower_right, Colour.BLACK.value, -1)
    cv2.rectangle(overlay, map_upper_left, map_lower_right, Colour.LIGHT.value, 1)

    # Draw all nodes
    for n in graph.getNodes():
        point = _convert_to_map_coordinates(n.get_coordinates(), ratio, map_upper_left)

        cv2.circle(overlay, point, 5, Colour.LIGHT.value, -1)

    # Draw all edges
    for e in graph.getEdges():
        nodeA, nodeB = e.getNodes()

        pointA = _convert_to_map_coordinates(nodeA.get_coordinates(), ratio, map_upper_left)
        pointB = _convert_to_map_coordinates(nodeB.get_coordinates(), ratio, map_upper_left)

        cv2.line(overlay, pointA, pointB, Colour.LIGHT.value, 1)

    # Draw robot and FOV triangle
    fov_length: int = 1000  # in mm
    left_angle: float = np.radians(robot.getDirection()) - np.radians(camera.getHFOV()) / 2
    right_angle: float = np.radians(robot.getDirection()) + np.radians(camera.getHFOV()) / 2
    robot_x: int = robot.getPosX()
    robot_y: int = robot.getPosY()

    p1 = (int(robot_x), int(robot_y))
    p2 = (int(robot_x + fov_length * np.cos(left_angle)), int(robot_y + fov_length * np.sin(left_angle)))
    p3 = (int(robot_x + fov_length * np.cos(right_angle)), int(robot_y + fov_length * np.sin(right_angle)))

    m1 = _convert_to_map_coordinates(p1, ratio, map_upper_left)
    m2 = _convert_to_map_coordinates(p2, ratio, map_upper_left)
    m3 = _convert_to_map_coordinates(p3, ratio, map_upper_left)

    cv2.circle(overlay, m1, 10, Colour.GREEN.value, -1)  # robot position
    cv2.line(overlay, m1, m2, Colour.GREEN.value, 1)
    cv2.line(overlay, m1, m3, Colour.GREEN.value, 1)

    cv2.addWeighted(overlay, ALPHA, img, 1 - ALPHA, 0, img)

def _convert_to_map_coordinates(node: tuple[int, int], ratio: float, offset: tuple[int, int]) -> tuple[int, int]:
    px = int(np.round(node[0] * ratio) + offset[0])
    py = int(np.round(node[1] * ratio) + offset[1])

    return (px, py)

