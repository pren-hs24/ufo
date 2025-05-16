# -*- coding: utf-8 -*-
"""system web handler"""

__copyright__ = "Copyright (c) 2025 HSLU PREN Team 2, FS25. All rights reserved."

from aiohttp import web

from common.constants import VERSION
from .base_handler import BaseHandler


class SystemHandler(BaseHandler):
    """system handler"""

    def add_routes(self, app: web.Application) -> None:
        app.router.add_get("/api/version", self._version)
        app.router.add_get("/api/system/algorithm", self._algorithm)

    async def _version(self, _: web.Request) -> web.Response:
        return web.Response(text=VERSION)

    async def _algorithm(self, _: web.Request) -> web.Response:
        if self._engine.algorithm is None:
            return web.HTTPNoContent()
        return web.Response(text=self._engine.algorithm.name)
