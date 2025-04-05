# -*- coding: utf-8 -*-
"""UART bus that only logs (no real uart interaction)."""

__copyright__ = "Copyright (c) 2025 HSLU PREN Team 2, FS25. All rights reserved."

from typing import Awaitable, Callable
import logging

from ..protocol import UARTEvent, UARTCommand, UARTProtocol


class LogUARTBus(UARTProtocol):
    """Implementation of the UART protocol."""

    def __init__(
        self,
    ) -> None:
        self._logger = logging.getLogger("uart.bus.logbus")

    async def start(self) -> None:
        """Start the UART protocol."""
        self._logger.info("LogUARTBus started")

    async def send_command(self, command: UARTCommand, payload: bytes = b"") -> None:
        self._logger.debug("command: %s, payload: %s", command, payload)

    @property
    def on_event(self) -> set[Callable[[UARTEvent, bytes], Awaitable[None]]]:
        """Return the set of event handlers"""
        return set()
