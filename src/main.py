# -*- coding: utf-8 -*-
"""Main module of the PREN project FS25 HSLU Team 2."""

__copyright__ = "Copyright (c) 2025 HSLU PREN Team 2, FS25. All rights reserved."

import logging
import logging.config
import asyncio

import uvloop  # evdev

from common.application import log_configuration
from uart.bus import UARTBus
from uart.sender import UARTSender


async def async_main() -> None:
    """Main async function."""
    reader, writer = await asyncio.open_connection("/dev/ttyUSB0", 115200)
    uart = UARTBus(reader, writer)
    sender = UARTSender(uart)
    # receiver = UARTReceiver(uart)

    await sender.set_debug_logging(True)
    await sender.turn(90)
    await sender.set_speed(50)
    await sender.set_speed(0)


def main() -> None:
    """main"""
    logging.config.dictConfig(log_configuration())
    logger = logging.getLogger(__name__)
    logger.info("[main]")

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    asyncio.run(async_main())

    logger.info("[main] exit")
    logging.shutdown()


if __name__ == "__main__":
    main()
