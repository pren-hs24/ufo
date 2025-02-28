# -*- coding: utf-8 -*-
"""UART receiver module."""

__copyright__ = "Copyright (c) 2025 HSLU PREN Team 2, FS25. All rights reserved."

import logging

from .protocol import UARTEvent, UARTProtocol


class UARTReceiver:
    """Receive events from the vehicle."""

    def __init__(self, uart: UARTProtocol) -> None:
        self._uart = uart
        self._uart.on_event.add(self._on_event)
        self._logger = logging.getLogger("uart.recv")

    async def _on_event(self, event: UARTEvent, payload: bytes) -> None:
        """Handle incoming events."""
        if event == UARTEvent.START:
            print("Start event received!")
        elif event == UARTEvent.LOG_MESSAGE:
            message = payload.decode("utf-8").strip("\x00")
            self._logger.debug("DEBUG: %s", message)
        else:
            print(f"Unhandled event: {event}")
