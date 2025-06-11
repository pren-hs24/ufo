# -*- coding: utf-8 -*-
"""Base Algorithm implementation."""

__copyright__ = "Copyright (c) 2025 HSLU PREN Team 2, FS25. All rights reserved."

from abc import ABC
from datetime import datetime
from logging import getLogger

from pathfinder.ipathfinder import IPathfinder
from pathfinder.dijkstra import DijkstraPathfinder
from uart.receiver import UARTReceiver
from uart.sender import UARTSender
from ufo.actor import Ufo
from ufo.listener import BaseUfoListener
from network.network import Network
from network.node import Node


class BaseAlgorithm(BaseUfoListener, ABC):  # pylint: disable=too-many-instance-attributes
    """Base Algorithm"""

    def __init__(
        self,
        network: Network,
        sender: UARTSender,
        receiver: UARTReceiver,
    ) -> None:
        BaseUfoListener.__init__(self, network, receiver)

        self._sender = sender
        self._ufo = Ufo(sender, network.start)
        self._path: list[Node] = []
        self._target: Node | None = None
        self._start_time = datetime.now()
        self._pathfinder: IPathfinder = DijkstraPathfinder()
        self._node_index = 0
        self._logger = getLogger(self.__class__.__name__)

    def _set_new_path(self) -> None:
        assert self._target is not None
        self._path = self._pathfinder.find_path(
            self._network, self._ufo.current_or_last_node, self._target
        )
        self._logger.debug("New path: %s", self._path)

    async def _on_start(self, target: Node) -> None:
        self._start_time = datetime.now()
        self._target = target

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

    @property
    def name(self) -> str:
        """algorithm name"""
        return self.__class__.__name__

    @property
    def _next_node_index(self) -> int:
        """index of next node in path"""
        return self._node_index + 1

    @property
    def _current_node(self) -> Node:
        """current node in path"""
        if self._node_index < len(self._path):
            return self._path[self._node_index]
        raise IndexError("Current node index is out of bounds")

    @property
    def _next_node(self) -> Node | None:
        """next node in path"""
        if self._next_node_index < len(self._path):
            return self._path[self._next_node_index]
        return None
