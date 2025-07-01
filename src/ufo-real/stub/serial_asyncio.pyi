# -*- coding: utf-8 -*-
"""UART uvloop"""

__copyright__ = "Copyright (c) 2025 HSLU PREN Team 2, FS25. All rights reserved."

from typing import Any, Awaitable

def open_serial_connection(url: Any, baudrate: Any) -> Awaitable[Any]:
    """
    This will only return ``None``, please double check your
    imports if you see this message. It means you are using
    a stub instead of the real thing. ```${url}```
    """
    _ = url, baudrate
    return Awaitable[None]  # type: ignore[return-value]
