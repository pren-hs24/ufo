# -*- coding: utf-8 -*-
"""UART sender module."""

__copyright__ = "Copyright (c) 2025 HSLU PREN Team 2, FS25. All rights reserved."

import struct
from enum import StrEnum

from .protocol import UARTCommand, UARTProtocol


class Endianness(StrEnum):
    """Endianness of the data."""

    LITTLE = "<"
    BIG = ">"

    def concat(self, fmt: str) -> str:
        """Concatenate the endianness with the format string."""
        return self.value + fmt


class UARTSender:
    """Send commands to the vehicle."""

    def __init__(
        self,
        sender: UARTProtocol,
        *,
        endianness: Endianness = Endianness.LITTLE,
    ) -> None:
        self._uart = sender
        self._endianness = endianness

    @property
    def bus(self) -> UARTProtocol:
        """Return the UART bus."""
        return self._uart

    @bus.setter
    def bus(self, bus: UARTProtocol) -> None:
        """Set the UART bus."""
        self._uart = bus

    async def turn(self, angle: int, *, snap: bool = True) -> None:
        """Send a turn command."""
        payload = struct.pack(
            # short int, bool
            self._endianness.concat("h?"),
            angle,
            snap,
        )
        await self._uart.send_command(UARTCommand.TURN, payload)

    async def follow_line(self) -> None:
        """Send a follow line command."""
        await self._uart.send_command(UARTCommand.FOLLOW_LINE)

    async def set_debug_logging(self, enabled: bool) -> None:
        """Enable or disable debug logging."""
        await self._uart.send_command(
            UARTCommand.SET_DEBUG_LOGGING, bytes([int(enabled)])
        )

    async def set_speed(self, speed: int) -> None:
        """Set the speed of the vehicle."""
        payload = struct.pack(
            # signed char
            self._endianness.concat("b"),
            speed,
        )
        await self._uart.send_command(UARTCommand.SET_SPEED, payload)

    async def destination_reached(self) -> None:
        """signalise that the destination was reached"""
        await self._uart.send_command(UARTCommand.DESTINAITON_REACHED)
