# -*- coding: utf-8 -*-
"""Main module of the PREN project FS25 HSLU Team 2."""

__copyright__ = "Copyright (c) 2025 HSLU PREN Team 2, FS25. All rights reserved."

import logging
import logging.config
import asyncio
from argparse import ArgumentParser, Namespace

import uvloop

from common.application import log_configuration
from common.competition import create_network
from uart.bus import UARTBus
from uart.sender import UARTSender
from uart.receiver import UARTReceiver
from ufo.engine import Engine


def _get_args(logger: logging.Logger) -> Namespace:
    """Parse command line arguments."""
    parser = ArgumentParser(description="PREN project FS25 HSLU Team 2")
    parser.add_argument("--debug", action="store_true", help="Enable debug logging")
    parser.add_argument(
        "--bus", type=str, default="/dev/serial0", help="UART bus device"
    )
    parser.add_argument(
        "--baudrate", type=int, default=115200, help="UART bus baudrate"
    )
    parser.add_argument(
        "--demo", action="store_true", default=False, help="Run the demo mode"
    )
    args = parser.parse_args()
    logger.debug("args: %s", args)
    return args


async def demo(args: Namespace) -> None:
    """Main async function."""
    reader, writer = await asyncio.open_connection(args.bus, args.baudrate)
    uart = UARTBus(reader, writer)
    sender = UARTSender(uart)

    await sender.set_debug_logging(args.debug)
    await sender.turn(90)
    await sender.set_speed(50)
    await asyncio.sleep(1)
    await sender.set_speed(0)


async def async_main(args: Namespace) -> None:
    """Main async function."""
    reader, writer = await asyncio.open_connection(args.bus, args.baudrate)
    uart = UARTBus(reader, writer)
    sender = UARTSender(uart)
    receiver = UARTReceiver(uart)

    Engine(sender, receiver, create_network)

    loop = asyncio.get_running_loop()
    loop.run_forever()


def main() -> None:
    """main"""
    logging.config.dictConfig(log_configuration())
    logger = logging.getLogger(__name__)
    logger.info("[main]")
    args = _get_args(logger)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    if args.demo:
        asyncio.run(demo(args))
    else:
        asyncio.run(async_main(args))

    logger.info("[main] exit")
    logging.shutdown()


if __name__ == "__main__":
    main()
