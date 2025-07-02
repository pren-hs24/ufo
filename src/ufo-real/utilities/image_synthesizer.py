# -*- coding: utf-8 -*-
"""Image Calculator Module"""

__copyright__ = "Copyright (c) 2025 HSLU PREN Team 2, FS25. All rights reserved."

from typing import TypeVar
from math import sqrt

from components import Camera, Graph, Obstacle, RealNode, Robot, VisualNode

from .node_matcher import find_best_matching

# enabling polymorphism
T = TypeVar("T")


class ImageSynthesizer:
    """Class to synthesize information from the images taken by the robot"""

    def __init__(self, camera: Camera, robot: Robot, graph: Graph) -> None:
        self.camera = camera
        self.robot = robot
        self.graph = graph

    def update_graph_by_objects(
        self,
        nodes: list[VisualNode],
        obstacles: list[Obstacle],
    ) -> None:
        """evaluate an image and update the values in the graph accordingly"""
        # renaming for clarification
        detected_obstacles = obstacles
        detected_nodes = nodes
        computed_nodes = self._compute_image_nodes_from_graph()

        # compare the mesured locations of nodes with the one the
        # #system computed and find the best matching
        node_matching: list[tuple[str, str]] = find_best_matching(
            detected_nodes, computed_nodes
        )
        # sorts all the nodes to match the order of the matching
        # detected_nodes -> verified_nodes
        # computed_nodes -> rendered_nodes
        sorted_matching, verified_nodes, rendered_nodes = _sort_matching_and_nodes_(
            node_matching, detected_nodes, computed_nodes
        )
        # combine them and get their location in the picture
        # as well as the names of the ones that are blocked
        matched_nodes, blocked_nodes = self.render_nodes_match_overlay(
            sorted_matching, verified_nodes, rendered_nodes
        )

        # compute whiche areas are blocked by the obstacles
        blocked_areas = self.render_groundplate_obstacle(detected_obstacles)
        # compute how it affects the edges
        self.render_edges(matched_nodes, blocked_areas, blocked_nodes)

    def _compute_image_nodes_from_graph(self) -> list[VisualNode]:
        result: list[VisualNode] = []

        for i in self.graph.get_nodes:
            r, d = self.robot.compute_distance_and_difference(i.get_coordinates)
            x, y = self.camera.compute_image_position(r, d)
            w, h = self.camera.compute_object_image_dimensions(
                d, RealNode.get_real_radius()
            )
            result.append(VisualNode(i.get_label, (x, y), w, h))

        return result

    def render_nodes_match_overlay(
        self,
        matching: list[tuple[str, str]],
        measured_nodes: list[VisualNode],
        computed_nodes: list[VisualNode],
    ) -> tuple[list[VisualNode], list[str]]:
        """compare the nodes with the generated overlay and asign the most likely labels to them"""

        offset_x, offset_y = calculate_average_offset(
            matching, measured_nodes, computed_nodes
        )

        result: list[VisualNode] = []
        pylons: list[str] = []

        for n, m in matching:
            if (
                not n == ""
                and n in computed_nodes
                and not m == ""
                and m in measured_nodes
            ):  # classical match found
                ms_x, ms_y = _find_node_by_str(measured_nodes, m).get_coordinates
                if "P" in m:  # special case for pylon nodes since they are blocked
                    pylons.append(n)
                    _find_node_by_str(self.graph.get_nodes, n).is_blocked()
                else:
                    _find_node_by_str(self.graph.get_nodes, n).is_available()

                result.append(VisualNode.position_only_and_label(n, (ms_x, ms_y)))
            elif (
                not n == "" and n in computed_nodes and m == ""
            ):  # missed a node that got computed but not found in the image
                cp_x, cp_y = _find_node_by_str(computed_nodes, n).get_coordinates

                ms_x = cp_x + offset_x
                ms_y = cp_y + offset_y

                result.append(VisualNode.position_only_and_label(n, (ms_x, ms_y)))

        return (result, pylons)

    def render_groundplate_obstacle(
        self, obstacles: list[Obstacle]
    ) -> list[VisualNode]:
        """add the groundplate/shadow of objects to an image"""

        obstacles_images: list[VisualNode] = []

        for o in obstacles:
            temp = self.camera.compute_groundplate(o)
            x, y = temp.get_coordinates
            w, h = temp.get_dimensions

            obstacles_images.append(VisualNode(f"O{o.get_id}", (x, y), w, h))

        return obstacles_images

    def render_edges(
        self, nodes: list[VisualNode], obstacles: list[VisualNode], pylons: list[str]
    ) -> None:
        """render what the edges should look like in the image"""

        for e in self.graph.get_edges:
            n, m = e.get_nodes
            label1 = n.get_label
            label2 = m.get_label
            if label1 in nodes and label2 in nodes:
                x_1, y_1 = _find_node_by_str(nodes, label1).get_coordinates
                x_2, y_2 = _find_node_by_str(nodes, label2).get_coordinates

                if label1 in pylons or label2 in pylons:
                    e.is_missing()
                elif _does_line_cross_any_obstacle((x_1, y_1), (x_2, y_2), obstacles):
                    e.is_blocked()
                else:
                    e.is_available()


def calculate_average_offset(
    match: list[tuple[str, str]],
    measured_nodes: list[VisualNode],
    computed_nodes: list[VisualNode],
) -> tuple[int, int]:
    """calculate what is the average amount of pixel the objects a shifted in the image"""
    sum_div_x: float = 0.0
    sum_div_y: float = 0.0

    num_matches: float = 1.0

    for mn in measured_nodes:
        for cp in computed_nodes:
            if (f"{mn.get_label}", f"{cp.get_label}") in match or (
                f"{cp.get_label}",
                f"{mn.get_label}",
            ) in match:
                num_matches += 1.0

                x_mn, y_mn = mn.get_coordinates
                x_cp, y_cp = cp.get_coordinates

                sum_div_x += float(x_mn - x_cp)
                sum_div_y += float(y_mn - y_cp)

                break

    avg_div_x = int(sum_div_x / num_matches)
    avg_div_y = int(sum_div_y / num_matches)

    return (avg_div_x, avg_div_y)


def _does_line_intersect_ellipse(  # pylint: disable=too-many-locals # impossible to read otherwise
    point_a: tuple[int, int], point_b: tuple[int, int], obstacle: VisualNode
) -> bool:
    # code by ChatGPT 4.0 <3
    x1, y1 = point_a
    x2, y2 = point_b

    x3, y3 = obstacle.get_coordinates
    w, h = obstacle.get_dimensions

    # Transformiere Koordinaten, damit Ellipse um Ursprung liegt
    dx = x2 - x1
    dy = y2 - y1

    # Parametrische Linie: (x, y) = (x1, y1) + t*(dx, dy), 0 <= t <= 1
    # Ellipsengleichung: ((x - x3)^2 / (w/2)^2) + ((y - y3)^2 / (h/2)^2) = 1

    if h == 0:
        h = 1

    a = (dx**2) / (w / 2) ** 2 + (dy**2) / (h / 2) ** 2
    b = 2 * ((x1 - x3) * dx / (w / 2) ** 2 + (y1 - y3) * dy / (h / 2) ** 2)
    c = ((x1 - x3) ** 2) / (w / 2) ** 2 + ((y1 - y3) ** 2) / (h / 2) ** 2 - 1

    # Löse quadratische Gleichung: at^2 + bt + c = 0
    discriminant = b**2 - 4 * a * c

    if discriminant < 0:
        return False  # Kein Schnittpunkt

    # Schnittpunkte berechnen
    sqrt_disc = float(sqrt(discriminant))
    t1 = (-b - sqrt_disc) / (2 * a)
    t2 = (-b + sqrt_disc) / (2 * a)

    # Prüfen, ob ein Schnittpunkt auf der Linie liegt (0 <= t <= 1)
    return (0 <= t1 <= 1) or (0 <= t2 <= 1)


def _does_line_cross_any_obstacle(
    point_a: tuple[int, int], point_b: tuple[int, int], obstacles: list[VisualNode]
) -> bool:
    result = False

    for o in obstacles:
        if _does_line_intersect_ellipse(point_a, point_b, o):
            result = True
            break

    return result


def _find_index_by_str(nodes: list[T], name: str) -> int:
    for i, node in enumerate(nodes):
        if node == name:
            return i
    raise ValueError(f"{name} not found")


def _find_node_by_str(nodes: list[T], name: str) -> T:
    value: int = _find_index_by_str(nodes, name)
    return nodes[value]


def _sort_matching_and_nodes_(
    match: list[tuple[str, str]],
    nodes1: list[VisualNode],
    nodes2: list[VisualNode],
) -> tuple[
    list[tuple[str, str]],
    list[VisualNode],
    list[VisualNode],
]:
    computed_nodes: list[VisualNode] = []
    measured_nodes: list[VisualNode] = []

    # flip elements in tupel such that the computed labels come first
    if match[0][0].isalpha() and match[0][1].isdigit():
        matching = match
    elif match[0][0].isdigit() and match[0][1].isalpha():
        matching = [(b, a) for (a, b) in match]
    else:
        raise ValueError("Render Fail. Could not assign origin of nodes.")

    # check whiche list contains whiche type of node
    if nodes1[0].get_label.isalpha() and nodes2[0].get_label.isdigit():
        computed_nodes = nodes1
        measured_nodes = nodes2
    elif nodes1[0].get_label.isdigit() and nodes2[0].get_label.isalpha():
        computed_nodes = nodes2
        measured_nodes = nodes1
    else:
        raise ValueError("Render Fail. Could not assign origin of nodes.")

    return (matching, measured_nodes, computed_nodes)
