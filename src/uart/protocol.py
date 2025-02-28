# -*- coding: utf-8 -*-
"""UART protocol module."""

__copyright__ = "Copyright (c) 2025 HSLU PREN Team 2, FS25. All rights reserved."

from typing import Awaitable, Callable
from enum import Enum
from abc import ABC, abstractmethod


class UARTCommand(Enum):
    """UART commands."""

    TURN = 0x01
    FOLLOW_LINE = 0x02
    SET_DEBUG_LOGGING = 0x04
    SET_SPEED = 0x05


class UARTEvent(Enum):
    """UART events."""

    START = 0x10
    POINT_REACHED = 0x11
    NO_LINE_FOUND = 0x12
    NEXT_POINT_BLOCKED = 0x13
    OBSTACLE_DETECTED = 0x14
    ALIGNED = 0x15
    RETURNING = 0x16
    LOG_MESSAGE = 0x17


class UARTProtocol(ABC):
    """Abstract base class for a UART protocol."""

    OnEventT = Callable[[UARTEvent, bytes], Awaitable[None]]

    @abstractmethod
    async def start(self) -> None:
        """Start receiving events."""

    @property
    @abstractmethod
    def on_event(self) -> set[OnEventT]:
        """Return the set of event handlers"""

    @abstractmethod
    async def send_command(self, command: UARTCommand, payload: bytes = b"") -> None:
        """Send a command with an optional payload."""
