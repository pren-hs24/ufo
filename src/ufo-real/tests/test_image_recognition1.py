"""# -*- coding: utf-8 -*-
angle calculation tests

__copyright__ = "Copyright (c) 2025 HSLU PREN Team 2, FS25. All rights reserved."


import copy

from components import RealNode, RealNodeLabel, Edge, Graph, Robot, Camera
from utilities import ImageSynthesizer
from yolo_model_v11 import ImageDetection


# alpha_image_recognition_test1
def test_image_recognition_one() -> None:
    ""Test image recognition with a single image and basic setup.""

    camera = _setup_camera()
    robot = _setup_robot()
    graph_is = _setup_graph()
    graph_should = copy.deepcopy(graph_is)

    model_path = "yolo_model_v11\\my_model.pt"

    detection = ImageDetection(model_path, camera, 0.3)
    synthesizer = ImageSynthesizer(camera, robot, graph_is)

    image_path = "tests\\images\\test_image1.jpg"

    detected_nodes, detected_obstacles, _ = detection.yolo_detect_by_image(image_path)
    synthesizer.update_graph_by_objects(detected_nodes, detected_obstacles)

    assert graph_is == graph_should
    print(f"{graph_is == graph_should}")


def _setup_robot() -> Robot:
    ""--------------SETUP-ROBOT--------------------""
    return Robot(1000, 1000, 0)


def _setup_camera() -> Camera:
    ""--------------SETUP-CAMERA-------------------""
    return Camera((1280, 720), 200, 65, 70)


def _setup_graph() -> Graph:
    ""--------------SETUP-NETWORK------------------""
    a = RealNode(RealNodeLabel.A, 1900, 2100)
    b = RealNode(RealNodeLabel.B, 2250, 2600)
    c = RealNode(RealNodeLabel.C, 2500, 2000)
    x = RealNode(RealNodeLabel.X, 3000, 2400)
    y = RealNode(RealNodeLabel.Y, 2300, 2700)
    z = RealNode(RealNodeLabel.Z, 3000, 2800)
    start = RealNode(RealNodeLabel.START, 2000, 3000)

    ab = Edge(a, b)
    bc = Edge(b, c)
    bx = Edge(b, x)
    by = Edge(b, y)
    yz = Edge(y, z)
    bs = Edge(b, start)

    nodes: list[RealNode] = [a, b, c, x, y, z, start]
    edges: list[Edge] = [ab, bc, bx, by, yz, bs]

    return Graph(nodes, edges)


def _manually_setup_should_state(graph: Graph) -> None:
    ""Manually setup the expected state of the graph after image recognition.""

    graph.get_node_by_str("A").is_available()
    graph.get_node_by_str("B").is_available()
    graph.get_node_by_str("X").is_available()

    graph.get_node_by_str("Z").is_blocked()

    graph.get_edge_by_str_tupel(("A", "B")).is_available()
    graph.get_edge_by_str_tupel(("C", "X")).is_available()
    graph.get_edge_by_str_tupel(("B", "X")).is_available()
    graph.get_edge_by_str_tupel(("B", "Y")).is_available()
    graph.get_edge_by_str_tupel(("X", "Y")).is_available()

    graph.get_edge_by_str_tupel(("A", "C")).is_blocked()
    graph.get_edge_by_str_tupel(("START", "X")).is_blocked()

    graph.get_edge_by_str_tupel(("X", "Z")).is_missing()
    graph.get_edge_by_str_tupel(("Y", "Z")).is_missing()
    graph.get_edge_by_str_tupel(("START", "X")).is_missing()
"""
