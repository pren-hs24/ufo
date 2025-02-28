# -*- coding: utf-8 -*-
"""Main module of the PREN project FS25 HSLU Team 2."""

__copyright__ = "Copyright (c) 2025 HSLU PREN Team 2, FS25. All rights reserved."

import logging
import logging.config
import asyncio
from argparse import ArgumentParser, Namespace

import uvloop

from common.application import log_configuration
from uart.bus import UARTBus
from uart.sender import UARTSender


def _get_args(logger: logging.Logger) -> Namespace:
    """Parse command line arguments."""
    parser = ArgumentParser(description="PREN project FS25 HSLU Team 2")
    parser.add_argument("--debug", action="store_true", help="Enable debug logging")
    parser.add_argument(
        "--bus", type=str, default="/dev/ttyUSB0", help="UART bus device"
    )
    parser.add_argument(
        "--baudrate", type=int, default=115200, help="UART bus baudrate"
    )
    args = parser.parse_args()
    logger.debug("args: %s", args)
    return args


async def async_main(args: Namespace) -> None:
    """Main async function."""
    reader, writer = await asyncio.open_connection(args.bus, args.baudrate)
    uart = UARTBus(reader, writer)
    sender = UARTSender(uart)
    # receiver = UARTReceiver(uart)

    await sender.set_debug_logging(args.debug)
    await sender.turn(90)
    await sender.set_speed(50)
    await sender.set_speed(0)


def main() -> None:
    """main"""
    logging.config.dictConfig(log_configuration())
    logger = logging.getLogger(__name__)
    logger.info("[main]")
    args = _get_args(logger)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    asyncio.run(async_main(args))

    logger.info("[main] exit")
    logging.shutdown()


if __name__ == "__main__":
    main()
