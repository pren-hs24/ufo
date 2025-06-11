# -*- coding: utf-8 -*-
"""ufo actor"""

__copyright__ = "Copyright (c) 2025 HSLU PREN Team 2, FS25. All rights reserved."

from logging import getLogger

from common.helper import Math
from uart.sender import UARTSender
from network.node import Node


class Ufo:
    """UFO"""

    def __init__(self, sender: UARTSender, start_node: Node) -> None:
        self._sender = sender
        self._current_deg = 0.0
        self._current_or_last_node = start_node
        self._logger = getLogger("ufo.actor.Ufo")

    def on_next_node_blocked(self) -> None:
        """called when next node is blocked"""
        self._logger.debug(
            "Next node blocked, turning 180 degrees from (%d)", self._current_deg
        )
        self._current_deg = self._current_deg + 180
        self._logger.debug(
            "Next node blocked, turning 180 degrees to (%d)", self._current_deg
        )

    async def turn_on_node(self, on_node: Node, to_node: Node) -> None:
        """performs a turn on a node to a next node"""
        new_angle = Math.calculate_angle_deg(on_node, to_node)
        current_angle = Math.optimise_for_next_angle(self._current_deg, new_angle)
        self._logger.debug(
            "Turning on node from %d to %d degrees (current: %d)",
            self._current_deg,
            new_angle,
            current_angle,
        )
        d = int(new_angle - current_angle)
        await self._sender.turn(d, snap=True)
        self._current_deg = new_angle

    async def follow_to_next_node(self) -> None:
        """follow line to next node"""
        await self._sender.follow_line()

    async def destination_reached(self) -> None:
        """destination reached"""
        await self._sender.destination_reached()

    @property
    def current_or_last_node(self) -> Node:
        """current or last node"""
        return self._current_or_last_node
    
    @current_or_last_node.setter
    def current_or_last_node(self, node: Node) -> None:
        """set current or last node"""
        self._current_or_last_node = node

    @property
    def current_deg(self) -> float:
        """current angle in degrees"""
        return self._current_deg
