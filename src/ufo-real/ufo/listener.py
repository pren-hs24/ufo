# -*- coding: utf-8 -*-
"""Base UFO Listener implementation."""

__copyright__ = "Copyright (c) 2025 HSLU PREN Team 2, FS25. All rights reserved."

from abc import ABC
from uart.protocol import UARTEvent
from uart.receiver import UARTReceiver
from network.network import Network
from network.node import Node, NodeLabel


class BaseUfoListener(ABC):
    """Base Ufo Listener"""

    def __init__(
        self,
        network: Network,
        receiver: UARTReceiver,
    ) -> None:
        self._network = network
        self._receiver = receiver

        self._receiver.on(UARTEvent.START, self._on_event)
        self._receiver.on(UARTEvent.ALIGNED, self._on_event)
        self._receiver.on(UARTEvent.POINT_REACHED, self._on_point_reached)
        self._receiver.on(UARTEvent.NO_LINE_FOUND, self._on_no_line_found)
        self._receiver.on(UARTEvent.NEXT_POINT_BLOCKED, self._on_next_point_blocked)
        self._receiver.on(UARTEvent.OBSTACLE_DETECTED, self._on_obstacle_detected)
        self._receiver.on(UARTEvent.RETURNING, self._on_returning)

    async def _on_start(self, target: Node) -> None:
        pass

    async def _on_point_reached(self) -> None:
        pass

    async def _on_no_line_found(self) -> None:
        pass

    async def _on_next_point_blocked(self) -> None:
        pass

    async def _on_obstacle_detected(self) -> None:
        pass

    async def _on_aligned(self, hold: bool) -> None:
        pass

    async def _on_returning(self) -> None:
        pass

    # internal
    async def _on_event(self, event: UARTEvent, payload: bytes) -> None:
        """do not overwrite"""
        if event == UARTEvent.START:
            end_node_labels = [NodeLabel.A, NodeLabel.B, NodeLabel.C]
            end_node_label = end_node_labels[payload[0]]
            await self._on_start(self._network.get_node_by_label(end_node_label))
        if event == UARTEvent.ALIGNED:
            hold = payload[0] == 1
            await self._on_aligned(hold)
