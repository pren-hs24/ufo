# -*- coding: utf-8 -*-
"""UART sender module."""

__copyright__ = "Copyright (c) 2025 HSLU PREN Team 2, FS25. All rights reserved."

import struct

from .protocol import UARTCommand, UARTProtocol


class UARTSender:
    """Send commands to the vehicle."""

    def __init__(self, sender: UARTProtocol) -> None:
        self._sender = sender

    async def turn(self, angle: int, *, snap: bool = True) -> None:
        """Send a turn command."""
        payload = struct.pack("<hB", angle, int(snap))
        await self._sender.send_command(UARTCommand.TURN, payload)

    async def follow_line(self) -> None:
        """Send a follow line command."""
        await self._sender.send_command(UARTCommand.FOLLOW_LINE)

    async def set_debug_logging(self, enabled: bool) -> None:
        """Enable or disable debug logging."""
        await self._sender.send_command(
            UARTCommand.SET_DEBUG_LOGGING, bytes([int(enabled)])
        )

    async def set_speed(self, speed: int) -> None:
        """Set the speed of the vehicle."""
        payload = struct.pack("<b", speed)
        await self._sender.send_command(UARTCommand.SET_SPEED, payload)
