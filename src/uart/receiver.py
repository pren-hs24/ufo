# -*- coding: utf-8 -*-
"""UART receiver module."""

__copyright__ = "Copyright (c) 2025 HSLU PREN Team 2, FS25. All rights reserved."

import logging
from typing import Callable, Awaitable, overload, cast

from .protocol import UARTEvent, UARTProtocol


class UARTReceiver:
    """Receive events from the vehicle."""

    CallbackT = Callable[[], Awaitable[None]]
    EventCallbackT = Callable[[UARTEvent], Awaitable[None]]
    EventPayloadCallbackT = Callable[[UARTEvent, bytes], Awaitable[None]]
    AnyCallbackT = CallbackT | EventCallbackT | EventPayloadCallbackT

    def __init__(self, uart: UARTProtocol) -> None:
        self._uart = uart
        self._uart.on_event.add(self._on_event)
        self._logger = logging.getLogger("uart.recv")
        self._event_handlers: dict[UARTEvent, set[UARTReceiver.AnyCallbackT]] = {
            event: set() for event in UARTEvent
        }

    @overload
    def on(self, event: UARTEvent, handler: CallbackT) -> None:
        """Register an event handler."""

    @overload
    def on(self, event: UARTEvent, handler: EventCallbackT) -> None:
        """Register an event handler."""

    @overload
    def on(self, event: UARTEvent, handler: EventPayloadCallbackT) -> None:
        """Register an event handler."""

    def on(self, event: UARTEvent, handler: AnyCallbackT) -> None:
        """Register an event handler."""
        self._event_handlers[event].add(handler)

    async def _on_event(self, event: UARTEvent, payload: bytes) -> None:
        """Handle incoming events."""
        if event.value in UARTEvent:
            await self._on_generic_event(event, payload)
        if event == UARTEvent.LOG_MESSAGE:
            self._on_log_message(payload)
        else:
            self._logger.warning("Unhandled event: %s", event)

    async def _on_generic_event(self, event: UARTEvent, payload: bytes) -> None:
        """Handle generic events."""
        self._logger.debug("Received event: %s", event)
        for handler in self._event_handlers[event]:
            if handler.__code__.co_argcount == 2:
                handler = cast(UARTReceiver.EventPayloadCallbackT, handler)
                await handler(event, payload)
            elif handler.__code__.co_argcount == 1:
                handler = cast(UARTReceiver.EventCallbackT, handler)
                await handler(event)
            else:
                handler = cast(UARTReceiver.CallbackT, handler)
                await handler()

    def _on_log_message(self, payload: bytes) -> None:
        """Handle the log message event."""
        message = payload.decode("utf-8").strip("\x00")
        self._logger.debug("DEBUG: %s", message)
