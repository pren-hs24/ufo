# -*- coding: utf-8 -*-
"""Main module of the PREN project FS25 HSLU Team 2."""

__copyright__ = "Copyright (c) 2025 HSLU PREN Team 2, FS25. All rights reserved."

import logging
import logging.config
import asyncio
from argparse import ArgumentParser, Namespace
from typing import Awaitable, Callable, cast

import uvloop
from aiohttp import web
from serial_asyncio import open_serial_connection

from common.application import log_configuration
from common.competition import create_dynamic_network
from common.constants import VERSION
from uart.protocol import UARTProtocol
from uart.bus import UARTBus
from uart.mock.bus import UARTBus as MockUARTBus
from ufo.engine import Engine
from web.server import WebServer


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
    parser.add_argument("--port", type=int, default=8080, help="Debug web server port")
    parser.add_argument(
        "--demo", action="store_true", default=False, help="Run the demo mode"
    )
    parser.add_argument(
        "-m",
        "--manual",
        action="store_true",
        default=False,
        help="Run manual mode (for testing, disables autonomy)",
    )
    args = parser.parse_args()
    logger.debug("args: %s", args)
    return args


async def create_and_start_bus(args: Namespace, logger: logging.Logger) -> UARTProtocol:
    """create bus"""
    bus: UARTProtocol
    if args.demo:
        logger.info("demo mode")
        bus = MockUARTBus()
    else:
        reader, writer = await open_serial_connection(
            url=args.bus, baudrate=args.baudrate
        )
        logger.debug("connected to %s with baudrate %d", args.bus, args.baudrate)
        bus = UARTBus(reader, writer)
    await bus.start()
    return bus


async def init_web(engine: Engine, args: Namespace, logger: logging.Logger) -> None:
    """Main async function."""
    uart = await create_and_start_bus(args, logger)
    engine.init(uart, args.manual)


async def demo(engine: Engine, args: Namespace, logger: logging.Logger) -> None:
    """Main async function."""
    uart = await create_and_start_bus(args, logger)
    engine.init(uart, args.manual)
    sender = engine.sender
    bus = cast(MockUARTBus, engine.receiver.bus)

    await sender.set_debug_logging(args.debug)
    await sender.turn(90)
    await sender.set_speed(50)
    await asyncio.sleep(1)
    await sender.set_speed(0)

    events = [
        b"\x10\x00\x10",  # TARGET A
        b"\x11\x11",  # REACHED
        b"\x15\x00\x15",  # ALIGNED
        b"\x14\x14",  # OBSTACLE DETECTED
    ]

    await bus.mock_receive_message(events[0])

    async def _implement_random_messages() -> None:
        while True:
            for event in events:
                await bus.mock_receive_message(event)
                await asyncio.sleep(10)

    asyncio.create_task(_implement_random_messages())


def _on_startup(
    engine: Engine, args: Namespace, logger: logging.Logger
) -> Callable[[web.Application], Awaitable[None]]:
    async def _impl(_: web.Application) -> None:
        """Startup handler."""

        if args.demo:
            logger.info("demo mode")
            await demo(engine, args, logger)

        logger.info("web mode")
        await init_web(engine, args, logger)

    return _impl


def main() -> None:
    """main"""
    logging.config.dictConfig(log_configuration())
    logger = logging.getLogger(__name__)
    logger.info("Welcome to %s", VERSION)
    logger.info("[main]")
    args = _get_args(logger)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    engine = Engine(create_dynamic_network)
    server = WebServer(engine)
    server.on_startup.append(_on_startup(engine, args, logger))
    server.run(args.port)

    logger.info("[main] exit")
    logging.shutdown()


if __name__ == "__main__":
    main()
