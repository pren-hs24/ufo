# -*- coding: utf-8 -*-
"""command web handler"""

__copyright__ = "Copyright (c) 2025 HSLU PREN Team 2, FS25. All rights reserved."

from aiohttp import web
from pyaddict.schema import Object, Integer, Boolean

from .base_handler import BaseHandler


class CommandHandler(BaseHandler):
    """handles commands"""

    def add_routes(self, app: web.Application) -> None:
        app.router.add_post("/api/command/speed", self._set_speed)
        app.router.add_post("/api/command/logging", self._set_logging)
        app.router.add_post(
            "/api/command/destination-reached", self._destination_reached
        )
        app.router.add_post("/api/command/follow", self._follow_line)
        app.router.add_post("/api/command/turn", self._turn)

    async def _set_speed(self, request: web.Request) -> web.Response:
        body = await self._get_json_body(
            request, Object({"speed": Integer().min(-100).max(100)})
        )
        speed = int(body["speed"])
        await self._engine.sender.set_speed(speed)
        return web.Response()

    async def _set_logging(self, request: web.Request) -> web.Response:
        body = await self._get_json_body(
            request,
            Object(
                {
                    "enabled": Boolean(),
                }
            ),
        )
        enabled = bool(body["enabled"])
        await self._engine.sender.set_debug_logging(enabled)
        return web.Response()

    async def _destination_reached(self, _: web.Request) -> web.Response:
        await self._engine.sender.destination_reached()
        return web.Response()

    async def _follow_line(self, _: web.Request) -> web.Response:
        await self._engine.sender.follow_line()
        return web.Response()

    async def _turn(self, request: web.Request) -> web.Response:
        body = await self._get_json_body(
            request,
            Object(
                {
                    "angle": Integer().min(-180).max(180),
                    "snap": Boolean(),
                }
            ),
        )
        angle = int(body["angle"])
        snap = bool(body["snap"])
        await self._engine.sender.turn(angle, snap=snap)
        return web.Response()
