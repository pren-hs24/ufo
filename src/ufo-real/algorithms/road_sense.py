# -*- coding: utf-8 -*-
"""RoadSense implementation"""

__copyright__ = "Copyright (c) 2025 HSLU PREN Team 2, FS25. All rights reserved."

from pathfinder.ipathfinder import IPathfinder
from pathfinder.dijkstra import DijkstraPathfinder
from uart.receiver import UARTReceiver
from uart.sender import UARTSender
from network.network import Network
from network.node import Node
from .base_algorithm import BaseAlgorithm


class RoadSenseAlgorithm(BaseAlgorithm):
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

    def _set_new_path(self) -> None:
        assert self._target is not None
        self._path = self._pathfinder.find_path(
            self._network, self._ufo.current_or_last_node, self._target
        )

    async def _restart(self) -> None:
        self._set_new_path()
        self._node_index = 0
        await self._turn_to_next_node()

    async def _on_start(self, target: Node) -> None:
        self._target = target
        await self._restart()

    async def _on_point_reached(self) -> None:
        if self._recalculation_required:
            await self._restart()
            return
        self._node_index += 1
        self._ufo.current_or_last_node = self._path[self._node_index]

        if self._ufo.current_or_last_node == self._target:
            await self._ufo.destination_reached()
            return
        await self._turn_to_next_node()

    async def _turn_to_next_node(self) -> None:
        await self._ufo.turn_on_node(
            self._path[self._node_index], self._path[self._node_index + 1]
        )

    async def _on_next_point_blocked(self) -> None:
        self._path[self._node_index + 1].disabled = True
        await self._restart()

    async def _on_no_line_found(self) -> None:
        self._network.get_edge(
            self._path[self._node_index], self._path[self._node_index + 1]
        ).disabled = True
        await self._restart()

    async def _on_returning(self) -> None:
        self._path[self._node_index + 1].disabled = True
        self._recalculation_required = True

    async def _on_aligned(self) -> None:
        await self._ufo.follow_to_next_node()

    @property
    def name(self) -> str:
        return "RoadSense"
