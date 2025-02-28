# -*- coding: utf-8 -*-
"""Main module of the PREN project FS25 HSLU Team 2."""

__copyright__ = "Copyright (c) 2025 HSLU PREN Team 2, FS25. All rights reserved."

import logging
import logging.config
import asyncio

import uvloop  # evdev
from common.application import log_configuration


def main() -> None:
    """main"""
    logging.config.dictConfig(log_configuration())
    logger = logging.getLogger(__name__)
    logger.info("[main]")

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    logger.info("[main] exit")
    logging.shutdown()


if __name__ == "__main__":
    main()
