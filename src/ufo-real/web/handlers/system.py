# -*- coding: utf-8 -*-
"""system web handler"""

__copyright__ = "Copyright (c) 2025 HSLU PREN Team 2, FS25. All rights reserved."

from aiohttp import web
from pyaddict.schema import Object, Integer, Boolean

from common.constants import VERSION
from .base_handler import BaseHandler


class SystemHandler(BaseHandler):
    """system handler"""

    def add_routes(self, app: web.Application) -> None:
        app.router.add_get("/api/version", self._version)

    async def _version(self, _: web.Request) -> web.Response:
        return web.Response(text = VERSION)

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
