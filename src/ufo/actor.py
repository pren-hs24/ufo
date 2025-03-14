# -*- coding: utf-8 -*-
"""ufo actor"""

__copyright__ = "Copyright (c) 2025 HSLU PREN Team 2, FS25. All rights reserved."

from common.helper import Math
from uart.sender import UARTSender
from network.node import Node


class Ufo:
    """UFO"""

    def __init__(self, sender: UARTSender, start_node: Node) -> None:
        self._sender = sender
        self._current_deg = 0.0
        self.current_or_last_node = start_node

    async def turn_on_node(self, on_node: Node, to_node: Node) -> None:
        """performs a turn on a node to a next node"""
        new_angle = Math.calculate_angle_deg(on_node, to_node)
        current_angle = Math.optimise_for_next_angle(self._current_deg, new_angle)
        d = int(new_angle - current_angle)
        await self._sender.turn(d, snap=True)
        self._current_deg = new_angle

    async def follow_to_next_node(self) -> None:
        """follow line to next node"""
        await self._sender.follow_line()

    async def destination_reached(self) -> None:
        """destination reached"""
        await self._sender.destination_reached()
