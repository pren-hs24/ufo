# -*- coding: utf-8 -*-
"""UART receiver module."""

__copyright__ = "Copyright (c) 2025 HSLU PREN Team 2, FS25. All rights reserved."

import logging
from typing import Callable, Awaitable

from .protocol import UARTEvent, UARTProtocol


class UARTReceiver:
    """Receive events from the vehicle."""

    def __init__(self, uart: UARTProtocol) -> None:
        self._uart = uart
        self._uart.on_event.add(self._on_event)
        self._logger = logging.getLogger("uart.recv")
        self._event_handlers: dict[
            UARTEvent, set[Callable[[UARTEvent], Awaitable[None]]]
        ] = {event: set() for event in UARTEvent}

    def on(
        self, event: UARTEvent, handler: Callable[[UARTEvent], Awaitable[None]]
    ) -> None:
        """Register an event handler."""
        self._event_handlers[event].add(handler)

    async def _on_event(self, event: UARTEvent, payload: bytes) -> None:
        """Handle incoming events."""
        if event.value in UARTEvent:
            await self._on_generic_event(event)
        if event == UARTEvent.LOG_MESSAGE:
            self._on_log_message(payload)
        else:
            self._logger.warning("Unhandled event: %s", event)

    async def _on_generic_event(self, event: UARTEvent) -> None:
        """Handle generic events."""
        self._logger.debug("Received event: %s", event)
        for handler in self._event_handlers[event]:
            await handler(event)

    def _on_log_message(self, payload: bytes) -> None:
        """Handle the log message event."""
        message = payload.decode("utf-8").strip("\x00")
        self._logger.debug("DEBUG: %s", message)
