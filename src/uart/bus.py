# -*- coding: utf-8 -*-
"""UART bus module."""

__copyright__ = "Copyright (c) 2025 HSLU PREN Team 2, FS25. All rights reserved."

from typing import Awaitable, Callable
import asyncio

from .protocol import UARTEvent, UARTCommand, UARTProtocol


class UARTBus(UARTProtocol):
    """Implementation of the UART protocol."""

    def __init__(
        self,
        reader: asyncio.StreamReader,
        writer: asyncio.StreamWriter,
    ) -> None:
        self._reader = reader
        self._writer = writer
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
        self._writer.write(message + bytes([checksum]))
        await self._writer.drain()

    async def _receive_event(self) -> None:
        """Receive and process an event message."""
        data = await self._reader.readexactly(1)
        event_id = data[0]

        payload = b""
        if event_id in [UARTEvent.START.value, UARTEvent.LOG_MESSAGE.value]:
            payload_size = 1 if event_id == UARTEvent.START.value else 20
            payload = await self._reader.readexactly(payload_size)

        checksum = await self._reader.readexactly(1)
        message = bytes([event_id]) + payload

        if self.calculate_checksum(message) != checksum[0]:
            print("Checksum mismatch! Ignoring message.")
            return None

        if event_id in [UARTEvent.START.value, UARTEvent.LOG_MESSAGE.value]:
            event = UARTEvent(event_id)
            await self._fire_event(event, payload)

    async def _fire_event(self, event: UARTEvent, payload: bytes) -> None:
        """Call all event handlers for the given event."""
        for handler in self._event_handlers:
            await handler(event, payload)

    async def _handle_events(self) -> None:
        """Continuously read and process incoming events."""
        while True:
            await self._receive_event()
