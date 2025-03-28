# -*- coding: utf-8 -*-
"""UART bus module."""

__copyright__ = "Copyright (c) 2025 HSLU PREN Team 2, FS25. All rights reserved."

from typing import Awaitable, Callable
import asyncio
import logging

import aioconsole  # type: ignore

from ..protocol import UARTEvent, UARTCommand, UARTProtocol


class ConsoleUARTBus(UARTProtocol):
    """Implementation of the UART protocol."""

    def __init__(
        self,
    ) -> None:
        self._logger = logging.getLogger("uart.bus")
        self._event_handlers: set[Callable[[UARTEvent, bytes], Awaitable[None]]] = set()

    async def start(self) -> None:
        """Start the UART protocol."""
        asyncio.create_task(self._handle_events())

    @property
    def on_event(self) -> set[Callable[[UARTEvent, bytes], Awaitable[None]]]:
        """Return the set of event handlers"""
        return self._event_handlers

    def calculate_checksum(self, data: bytes) -> int:
        """Compute the XOR checksum of the given data."""
        checksum = 0
        for byte in data:
            checksum ^= byte
        return checksum

    async def send_command(self, command: UARTCommand, payload: bytes = b"") -> None:
        """Send a command with an optional payload."""
        message = bytes([command.value]) + payload
        checksum = self.calculate_checksum(message)
        data = message + bytes([checksum])
        self._logger.debug("Sending command: %s, payload: %s", command, payload)
        await aioconsole.aprint(data)

    async def _receive_event(self, data: bytes) -> None:
        """Receive and process an event message."""
        event_id = data[0]

        if event_id not in UARTEvent:
            self._logger.warning("Unknown event: %s", event_id)
            return None

        self._logger.debug("Received event: %s", event_id)

        payload = data[1:-1]
        checksum = data[-1]
        message = bytes([event_id]) + payload

        if self.calculate_checksum(message) != checksum:
            self._logger.warning("Checksum mismatch! Ignoring message.")
            return None

        if event_id in UARTEvent:
            event = UARTEvent(event_id)
            await self._fire_event(event, payload)

    async def _fire_event(self, event: UARTEvent, payload: bytes) -> None:
        """Call all event handlers for the given event."""
        for handler in self._event_handlers:
            await handler(event, payload)

    async def _handle_events(self) -> None:
        """Continuously read and process incoming events."""
        while True:
            msg: str = await aioconsole.ainput("Send bytes: ")
            msg.replace("0x", "").replace(" ", "")
            await self._receive_event(bytes.fromhex(msg))
