# -*- coding: utf-8 -*-
"""monitoring web handler"""

__copyright__ = "Copyright (c) 2025 HSLU PREN Team 2, FS25. All rights reserved."

from aiohttp import web

from ufo.engine import Engine
from ufo.logger import UfoLogger, UfoLogMessage
from .base_handler import BaseHandler


class MonitoringHandler(BaseHandler):
    """monitoring handler"""

    def __init__(self, engine: Engine) -> None:
        BaseHandler.__init__(self, engine)

        self._ufo_logger = UfoLogger(engine.create_network(), engine.receiver)
        self._ufo_logger.listeners.append(self._on_message)
        self._listeners: list[web.WebSocketResponse] = []

    def add_routes(self, app: web.Application) -> None:
        app.router.add_get("/api/monitoring", self._on_subscribe)

    async def _on_message(self, message: UfoLogMessage) -> None:
        for listener in self._listeners:
            await listener.send_str(str(message))

    async def _on_subscribe(self, request: web.Request) -> web.WebSocketResponse:
        ws = web.WebSocketResponse()
        await ws.prepare(request)
        self._logger.debug("New monitoring client connected")
        for event in self._ufo_logger.events:
            await ws.send_str(str(event))
        self._listeners.append(ws)
        return ws
