# -*- coding: utf-8 -*-
"""RoadSense implementation"""

__copyright__ = "Copyright (c) 2025 HSLU PREN Team 2, FS25. All rights reserved."

import asyncio
from logging import getLogger
from datetime import datetime

from pathfinder.ipathfinder import IPathfinder
from pathfinder.dijkstra import DijkstraPathfinder
from uart.receiver import UARTReceiver
from uart.sender import UARTSender
from network.network import Network
from network.node import Node
from .base_algorithm import BaseAlgorithm


class RoadSenseAlgorithm(BaseAlgorithm):  # pylint: disable=too-many-instance-attributes
    """RoadSense"""

    def __init__(
        self,
        network: Network,
        sender: UARTSender,
        receiver: UARTReceiver,
    ) -> None:
        super().__init__(network, sender, receiver)
        self._pathfinder: IPathfinder = DijkstraPathfinder()
        self._node_index = 0
        self._target: Node | None = None
        self._recalculation_required = False
        self._in_start_zone = True
        self._is_moving = False
        self._logger = getLogger("RoadSenseAlgorithm")
        self._start_time = datetime.now()

    def _set_new_path(self) -> None:
        assert self._target is not None
        self._path = self._pathfinder.find_path(
            self._network, self._ufo.current_or_last_node, self._target
        )
        self._logger.debug("New path: %s", self._path)

    async def _restart(self) -> None:
        self._set_new_path()
        self._node_index = 0
        await self._turn_to_next_node()

    async def _on_start(self, target: Node) -> None:
        self._start_time = datetime.now()
        self._in_start_zone = True
        self._target = target
        await self._ufo.follow_to_next_node()  # to start
        self._is_moving = True
        self._logger.debug("Started navigation to %s", target)

    async def _on_destination_reached(self) -> None:
        await self._ufo.destination_reached()
        self._logger.info(
            "Destination %s reached in %s",
            self._target,
            datetime.now() - self._start_time,
        )
        self._target = None
        self._node_index = 0
        self._path = []

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
        on_node = self._path[self._node_index]
        to_node = self._path[self._node_index + 1]
        await self._ufo.turn_on_node(on_node, to_node)
        self._logger.debug("Turn on %s to %s", on_node, to_node)

    async def _on_next_point_blocked(self) -> None:
        self._ufo.on_next_node_blocked()
        if self._is_moving:
            self._logger.debug("Next point blocked, handle after returning")
            return
        self._logger.debug("Next point blocked, recalculating path...")
        self._path[self._node_index + 1].disabled = True
        await self._restart()

    async def _on_no_line_found(self) -> None:
        node1 = self._path[self._node_index]
        node2 = self._path[self._node_index + 1]
        self._network.get_edge(node1, node2).disabled = True
        self._logger.debug("Line %s -> %s is missing, recalculating...", node1, node2)
        await asyncio.sleep(100 / 1000)  # 100ms
        await self._restart()

    async def _on_returning(self) -> None:
        self._path[self._node_index + 1].disabled = True
        self._recalculation_required = True

    async def _on_aligned(self, hold: bool) -> None:
        self._logger.debug("Aligned, %s", "holding" if hold else "proceed")
        if hold:
            return
        await self._ufo.follow_to_next_node()
        self._is_moving = True

    @property
    def name(self) -> str:
        return "RoadSense"
