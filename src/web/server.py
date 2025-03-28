# -*- coding: utf-8 -*-
"""web server"""

__copyright__ = "Copyright (c) 2025 HSLU PREN Team 2, FS25. All rights reserved."

import logging
from typing import Awaitable, Callable

from aiosignal import Signal
from aiohttp import web

from ufo.engine import Engine
from .handlers.base_handler import BaseHandler
from .handlers.command import CommandHandler
from .handlers.monitoring import MonitoringHandler


class WebServer:
    """WebServer"""

    AppSignalT = Signal[Callable[["web.Application"], Awaitable[None]]]

    def __init__(self, engine: Engine) -> None:
        self._app = web.Application()
        self._logger = logging.getLogger("web")

        self._handlers: list[BaseHandler] = [
            CommandHandler(engine),
            MonitoringHandler(engine),
        ]

        for handler in self._handlers:
            handler.add_routes(self._app)

    @property
    def on_startup(self) -> AppSignalT:
        """on_startup"""
        return self._app.on_startup

    def run(self, port: int) -> None:
        """run app"""
        web.run_app(self._app, port=port)
