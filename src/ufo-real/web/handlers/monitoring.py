# -*- coding: utf-8 -*-
"""monitoring web handler"""

__copyright__ = "Copyright (c) 2025 HSLU PREN Team 2, FS25. All rights reserved."

import json

import aiohttp
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
        new_listeners: list[web.WebSocketResponse] = []
        for listener in self._listeners:
            try:
                await listener.send_str(
                    json.dumps({"type": "log", "data": message.json()})
                )
                new_listeners.append(listener)
            except aiohttp.ClientConnectionResetError:
                self._logger.debug("Client disconnected")
        self._listeners = new_listeners

    async def _on_subscribe(self, request: web.Request) -> web.WebSocketResponse:
        ws = web.WebSocketResponse()
        await ws.prepare(request)
        self._logger.debug("New monitoring client connected")
        for event in self._ufo_logger.events:
            await ws.send_str(json.dumps({"type": "log", "data": event.json()}))
        self._listeners.append(ws)

        async for msg in ws:
            if msg.type == aiohttp.WSMsgType.TEXT:
                if msg.data == "close":
                    await ws.close()

        return ws
