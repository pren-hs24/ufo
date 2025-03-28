# -*- coding: utf-8 -*-
"""UFO Logger"""

__copyright__ = "Copyright (c) 2025 HSLU PREN Team 2, FS25. All rights reserved."

import logging
import datetime
from collections import deque
from typing import Awaitable, Callable
from dataclasses import dataclass, field

from aiosignal import Signal

from uart.receiver import UARTReceiver
from ufo.listener import BaseUfoListener
from network.network import Network
from network.node import Node


@dataclass
class UfoLogMessage:
    """Ufo Log Message"""

    message: str
    level: int = field(default=logging.INFO)
    timestamp: datetime.datetime = field(default_factory=datetime.datetime.now)

    def __str__(self) -> str:
        return f"{self.timestamp.isoformat()} {self.level:7}: {self.message}"


_UfoLogSignal = Signal[Callable[[UfoLogMessage], Awaitable[None]]]


class UfoLogger(BaseUfoListener):
    """Ufo Logger"""

    def __init__(self, network: Network, receiver: UARTReceiver):
        super().__init__(network, receiver)
        self._events: deque[UfoLogMessage] = deque([], maxlen=50)
        self._listeners: _UfoLogSignal = Signal(self)

    @property
    def events(self) -> deque[UfoLogMessage]:
        """events"""
        return self._events

    @property
    def listeners(self) -> _UfoLogSignal:
        """listeners"""
        return self._listeners

    async def _log(self, event: UfoLogMessage) -> None:
        self._events.append(event)
        await self._listeners.send(event)

    async def _on_start(self, target: Node) -> None:
        await self._log(UfoLogMessage(f"Start to {target}"))

    async def _on_point_reached(self) -> None:
        await self._log(UfoLogMessage("Point reached"))

    async def _on_no_line_found(self) -> None:
        await self._log(UfoLogMessage("No line found"))

    async def _on_next_point_blocked(self) -> None:
        await self._log(UfoLogMessage("Next point blocked"))

    async def _on_obstacle_detected(self) -> None:
        await self._log(UfoLogMessage("Obstacle detected"))

    async def _on_aligned(self) -> None:
        await self._log(UfoLogMessage("Aligned"))

    async def _on_returning(self) -> None:
        await self._log(UfoLogMessage("Returning"))
