# -*- coding: utf-8 -*-
"""OverSight implementation"""

__copyright__ = "Copyright (c) 2025 HSLU PREN Team 2, FS25. All rights reserved."

# code that uses image recognition

import asyncio

# newly added imports - subject to change
from components import Camera, Edge, Graph, RealNode, RealNodeLabel, Robot
from network.network import Network
from network.node import Node, NodeLabel
from uart.receiver import UARTReceiver
from uart.sender import UARTSender
from utilities.image_predictor import analyze_image
from yolo_model_v11 import yolo_detect

from .base_algorithm import BaseAlgorithm

# TODO: allocate outside - from Utilities.alpha_image_recognition_adapter import run_image_recognition_async


class OverSightAlgorithm(BaseAlgorithm):
    """OverSight"""

    _CAMERA: Camera
    _GRAPH: Graph
    _ROBOT: Robot

    # YOLO specific parameters
    # TODO: refactor, make dynamic, test best settings
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
        network: Network,
        sender: UARTSender,
        receiver: UARTReceiver,
    ) -> None:
        super().__init__(network, sender, receiver)
        self._recalculation_required = False
        self._in_start_zone = True
        self._is_moving = False
        self._image_recognition_setup()

    async def _restart(self) -> None:
        self._set_new_path()
        self._node_index = 0
        await self._turn_to_next_node()

    async def _on_start(self, target: Node) -> None:
        await super()._on_start(target)
        self._in_start_zone = True
        await self._ufo.follow_to_next_node()  # to start
        self._is_moving = True
        self._logger.debug("Started navigation to %s", target)

    async def _on_point_reached(self) -> None:
        self._is_moving = False

        if self._in_start_zone:
            self._logger.debug("Start point reached")
            self._in_start_zone = False
            await self._restart()
            return

        if self._recalculation_required:
            self._logger.debug("Recalculating path...")
            self._recalculation_required = False
            await self._restart()
            return

        self._node_index += 1
        self._ufo.current_or_last_node = self._path[self._node_index]
        self._logger.debug("Reached node %s", self._path[self._node_index])

        if self._ufo.current_or_last_node == self._target:
            await self._on_destination_reached()
            return
        await self._turn_to_next_node()

    async def _turn_to_next_node(self) -> None:
        on_node = self._current_node
        to_node = self._next_node
        assert on_node is not None, "Current node must not be None"
        assert to_node is not None, "Next node must not be None"
        await self._ufo.turn_on_node(on_node, to_node)
        self._logger.debug("Turn on %s to %s", on_node, to_node)

    async def _on_next_point_blocked(self) -> None:
        self._ufo.on_next_node_blocked()
        if self._is_moving:
            self._logger.debug("Next point blocked, handle after returning")
            return
        self._logger.debug("Next point blocked, recalculating path...")
        self._path[self._next_node_index].disabled = True
        await self._restart()

    async def _on_no_line_found(self) -> None:
        node1 = self._current_node
        node2 = self._next_node
        assert node1 is not None, "Current node must not be None"
        assert node2 is not None, "Next node must not be None"
        self._network.get_edge(node1, node2).disabled = True
        self._logger.debug("Line %s -> %s is missing, recalculating...", node1, node2)
        await asyncio.sleep(100 / 1000)  # 100ms
        await self._restart()

    async def _on_returning(self) -> None:
        self._path[self._next_node_index].disabled = True
        self._recalculation_required = True

    async def _on_aligned(self, hold: bool) -> None:
        self._logger.debug("Aligned, %s", "holding" if hold else "proceed")
        if hold:
            return
        await self._ufo.follow_to_next_node()
        self._is_moving = True

    @property
    def name(self) -> str:
        return "OverSight"

    # TODO: behold here my chaos takes over
    async def _on_sight(self) -> None:
        self._logger.debug("Running image recognition...")

        # 1.) Check if the system knows where we are and where we would like to go.
        if not self._current_node or not self._next_node:
            self._logger.warning("Cannot run sight: missing current or next node")
            return

        # 2.) Pass these information down to the robot-class for the calculations
        self._ROBOT.change_position(
            self._convert_networknode_to_graphcoordinates(self._current_node)
        )
        self._ROBOT.turn_towards(
            self._convert_networknode_to_graphcoordinates(self._next_node)
        )

        # 3.) Trigger the image callculation and let it update the graph-object
        # TODO: create a temporary snapshot of the graph with this method for the next one
        await self.run_image_recognition_async()

        # 4. Transfer information in updated graph-object to network
        self._apply_recognition_result_to_network()  # TODO: add argument of current snapshot graph

        # 5.) Trigger replanning
        self._recalculation_required = True
        self._logger.debug("Image recognition finished and network updated.")

    # <-- TODO: Helper-Methods that will need to be allocated somewhere else. -->

    async def run_image_recognition_async(self) -> None:  # Graph:
        """
        Runs the YOLO image recognition pipeline asynchronously and returns
        an updated Graph with states for nodes and edges.
        """
        self._logger.debug("Taking picture now ...")
        detected_nodes, detected_obstacles, frame = yolo_detect(
            self._PATH_MODEL,
            self._PATH_SOURCE,
            self._CAMERA,
            self._FRESHHOLD,
            self._RESOLUTION,
            self._SAFE,
        )  # type: ignore
        self._logger.debug("Evaluating picture ...")
        analyze_image(
            self._CAMERA,
            self._ROBOT,
            self._GRAPH,
            detected_nodes,
            detected_obstacles,
            frame,
        )

    def _apply_recognition_result_to_network(self) -> None:
        """
        Takes the result Graph from the image recognition and updates the
        internal Network accordingly.
        """

        # Update node states
        for node in self._GRAPH.get_nodes:
            try:
                network_node = self._network.get_node_by_label(
                    OverSightAlgorithm._str_to_nodelabel(node.get_label)
                )
            except Exception as e:
                self._logger.warning(
                    f"Node label {node.get_label} not found in network: {e}"
                )
                continue

            if node.state.name == "BLOCKED":
                network_node.disabled = True
            elif node.state.name == "FREE":
                network_node.disabled = False
            # else UNKNOWN = no change

        # Update edge states
        for edge in self._GRAPH.get_edges:
            node1_label = OverSightAlgorithm._str_to_nodelabel(edge.start.get_label)
            node2_label = OverSightAlgorithm._str_to_nodelabel(edge.end.get_label)
            try:
                network_edge = self._network.get_edge_by_label(node1_label, node2_label)
            except Exception as e:
                self._logger.warning(
                    f"Edge ({node1_label}, {node2_label}) not found in network: {e}"
                )
                continue

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
        # TODO: Change static setup of Graph, Robot and YOLO to be dynamic

        # -----------------SETUP-CAMERA-------------------#
        self._CAMERA = Camera(1280, 720, 300, 60, 70)

        # -----------------SETUP-ROBOT--------------------#
        self._ROBOT = Robot(2250, 3000, 270)

        # -----------------SETUP-NETWORK------------------#
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

        self._GRAPH = Graph(nodes, edges)

    @staticmethod
    def _str_to_nodelabel(label: str) -> NodeLabel:
        """Adapter that turns a string into the matching NodeLabel."""
        try:
            return NodeLabel(label)
        except ValueError:
            return NodeLabel.UNDEFINED

    def _convert_networknode_to_graphcoordinates(self, node: Node) -> tuple[int, int]:
        return self._GRAPH.get_node_by_str(node.label.value).get_coordinates
