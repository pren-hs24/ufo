# -*- coding: utf-8 -*-
"""OverSight implementation"""

__copyright__ = "Copyright (c) 2025 HSLU PREN Team 2, FS25. All rights reserved."

# code that uses image recognition

import asyncio

# newly added imports - subject to change
from components import Camera, Edge, Graph, RealNode, RealNodeLabel, Robot
from network.network import NetworkProvider
from network.node import Node, NodeLabel
from uart.receiver import UARTReceiver
from uart.sender import UARTSender
from utilities.image_synthesizer import ImageSynthesizer
from yolo_model_v11 import ImageDetection

from .road_sense import RoadSenseAlgorithm

# TODO: pylint: disable=fixme
# allocate outside - from Utilities.alpha_image_recognition_adapter
# import run_image_recognition_async


class OverSightAlgorithm(RoadSenseAlgorithm):
    """OverSight"""

    camera: Camera
    graph: Graph
    robot: Robot

    IMAGE_RECOGNITION_EXPECTED_TIME: float = 4.0  # seconds

    # YOLO specific parameters
    # TODO: # pylint: disable=fixme
    # refactor, make dynamic, test best settings
    _PATH_MODEL: str = "YOLO_Model_v11\\my_model.pt"  # final
    _PATH_SOURCE: str = (
        "YOLO_Model_v11\\test_image2.jpg"  # fake, change to picamera asap
    )
    _FRESHHOLD: float = (
        0.3  # test to see which one yields best result -> Range 0.3 to 1.0
    )
    _RESOLUTION: str = (
        "1280x720"  # final - could come from camere once its setup properly
    )
    _SAFE: bool = False  # test

    def __init__(
        self,
        network_provider: NetworkProvider,
        sender: UARTSender,
        receiver: UARTReceiver,
    ) -> None:
        super().__init__(network_provider, sender, receiver)
        self._image_recognition_setup()

    async def _on_start(self, target: Node) -> None:
        self._image_recognition_setup()  # ensure camera and robot are set up
        await super()._on_start(target)

    async def _on_aligned(self, hold: bool) -> None:
        # TODO: oversight here
        self._logger.debug("Taking a picture real quick...")
        await self._on_sight()  # run image recognition
        await asyncio.sleep(
            self.IMAGE_RECOGNITION_EXPECTED_TIME
        )  # wait for the image recognition to finish
        if hold:
            return
        await self._ufo.follow_to_next_node()
        self._is_moving = True

    # TODO: behold here my chaos takes over
    async def _on_sight(self) -> None:
        self._logger.debug("Running image recognition...")

        # 1.) Check if the system knows where we are and where we would like to go.
        if not self._current_node or not self._next_node:
            self._logger.warning("Cannot run sight: missing current or next node")
            return

        # 2.) Pass these information down to the robot-class for the calculations
        self.robot.change_position(
            self._convert_networknode_to_graphcoordinates(self._current_node)
        )
        self.robot.turn_towards(
            self._convert_networknode_to_graphcoordinates(self._next_node)
        )

        # 3.) Trigger the image callculation and let it update the graph-object
        # TODO: create a temporary snapshot of the graph with this method for the next one
        await self._run_image_recognition_async()

        # 4. Transfer information in updated graph-object to network
        self._apply_recognition_result_to_network()  # TODO: add argument of current snapshot graph

        # 5.) Trigger replanning
        self._recalculation_required = True
        self._logger.debug("Image recognition finished and network updated.")

    # <-- TODO: Helper-Methods that will need to be allocated somewhere else. -->

    async def _run_image_recognition_async(self) -> None:  # Graph:
        """
        Runs the YOLO image recognition pipeline asynchronously and returns
        an updated Graph with states for nodes and edges.
        """
        self._logger.debug("Taking picture now ...")
        detected_nodes, detected_obstacles, _ = (
            self.image_detection.yolo_detect_by_image(self._PATH_SOURCE)
        )
        self._logger.debug("Evaluating picture ...")
        self.image_synthesizer.update_graph_by_objects(
            detected_nodes,
            detected_obstacles,
        )

    def _apply_recognition_result_to_network(self) -> None:
        """
        Takes the result Graph from the image recognition and updates the
        internal Network accordingly.
        """

        # Update node states
        for node in self.graph.get_nodes:
            network_node = self._network.get_node_by_label(
                OverSightAlgorithm._str_to_nodelabel(node.get_label)
            )

            if node.state.name == "BLOCKED":
                network_node.disabled = True
            elif node.state.name == "FREE":
                network_node.disabled = False
            # else UNKNOWN = no change

        # Update edge states
        for edge in self.graph.get_edges:
            node1_label = OverSightAlgorithm._str_to_nodelabel(edge.start.get_label)
            node2_label = OverSightAlgorithm._str_to_nodelabel(edge.end.get_label)
            network_edge = self._network.get_edge_by_label(node1_label, node2_label)
            if edge.status.name == "MISSING":
                network_edge.disabled = True
                network_edge.obstructed = False
            elif edge.status.name == "BLOCKED":
                network_edge.obstructed = True
                network_edge.disabled = False
            elif edge.status.name == "FREE":
                network_edge.disabled = False
                network_edge.obstructed = False
            # else UNKNOWN = no change

    def _image_recognition_setup(self) -> None:
        """
        Pass all the in real life messured values for the positions
        of the nodes, the values for the camera and the specs of
        the robot.
        """
        # TODO: Change static setup of Graph,
        # Robot and YOLO to be dynamic

        # -----------------SETUP-CAMERA-------------------#
        self.camera = Camera((1280, 720), 300, 60, 70)

        # -----------------SETUP-ROBOT--------------------#
        self.robot = Robot(2250, 3000, 270)

        self.graph = _setup_graph()

        self.image_detection = ImageDetection(self._PATH_MODEL, self.camera, 4.0)
        self.image_synthesizer = ImageSynthesizer(self.camera, self.robot, self.graph)

    @staticmethod
    def _str_to_nodelabel(label: str) -> NodeLabel:
        """Adapter that turns a string into the matching NodeLabel."""
        try:
            return NodeLabel(label)
        except ValueError:
            return NodeLabel.UNDEFINED

    def _convert_networknode_to_graphcoordinates(self, node: Node) -> tuple[int, int]:
        return self.graph.get_node_by_str(node.label.value).get_coordinates


def _setup_graph() -> Graph:  # pylint: disable=too-many-locals
    """--------------SETUP-NETWORK------------------"""
    a = RealNode(RealNodeLabel.A, 2933, 900)
    b = RealNode(RealNodeLabel.B, 1586, 250)
    c = RealNode(RealNodeLabel.C, 487, 666)
    x = RealNode(RealNodeLabel.X, 2020, 2700)
    y = RealNode(RealNodeLabel.Y, 1692, 1500)
    z = RealNode(RealNodeLabel.Z, 3150, 2650)
    w = RealNode(RealNodeLabel.W, 500, 2150)
    start = RealNode(RealNodeLabel.START, 1800, 5100)

    ab = Edge(a, b)
    ay = Edge(a, y)
    az = Edge(a, z)
    bc = Edge(b, c)
    by = Edge(b, y)
    cw = Edge(c, w)
    wx = Edge(w, x)
    ws = Edge(w, start)
    xy = Edge(x, y)
    xz = Edge(x, z)
    xs = Edge(x, start)

    nodes: list[RealNode] = [a, b, c, x, y, z, start]
    edges: list[Edge] = [ab, ay, az, bc, by, cw, wx, ws, xy, xz, xs]

    return Graph(nodes, edges)
