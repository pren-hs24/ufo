# -*- coding: utf-8 -*-
"""Main module of the PREN project FS25 HSLU Team 2."""

__copyright__ = "Copyright (c) 2025 HSLU PREN Team 2, FS25. All rights reserved."

import logging
import logging.config
import asyncio
from argparse import ArgumentParser, Namespace
from typing import Awaitable, Callable

import uvloop
from aiohttp import web
from serial_asyncio import open_serial_connection  # type: ignore

from common.application import log_configuration
from common.competition import create_network
from uart.bus import UARTBus
from uart.mock.log_bus import LogUARTBus
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
    args = parser.parse_args()
    logger.debug("args: %s", args)
    return args


async def create_and_start_bus(args: Namespace, logger: logging.Logger) -> None:
    """create bus"""
    if args.demo:
        logger.info("demo mode")
        bus = LogUARTBus()
        await bus.start()
        return bus
    reader, writer = await open_serial_connection(url=args.bus, baudrate=args.baudrate)
    logger.debug("connected to %s with baudrate %d", args.bus, args.baudrate)
    bus = UARTBus(reader, writer)
    await bus.start()
    return bus


async def init_web(engine: Engine, args: Namespace, logger: logging.Logger) -> None:
    """Main async function."""
    uart = await create_and_start_bus(args, logger)
    engine.init(uart)


async def demo(engine: Engine, args: Namespace, logger: logging.Logger) -> None:
    """Main async function."""
    uart = await create_and_start_bus(args, logger)
    engine.init(uart)
    sender = engine.sender

    await sender.set_debug_logging(args.debug)
    await sender.turn(90)
    await sender.set_speed(50)
    await asyncio.sleep(1)
    await sender.set_speed(0)


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
    logger.info("[main]")
    args = _get_args(logger)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    engine = Engine(create_network)
    server = WebServer(engine)
    server.on_startup.append(_on_startup(engine, args, logger))
    server.run(args.port)

    logger.info("[main] exit")
    logging.shutdown()


if __name__ == "__main__":
    main()
