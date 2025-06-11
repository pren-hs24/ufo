# -*- coding: utf-8 -*-
"""system web handler"""

__copyright__ = "Copyright (c) 2025 HSLU PREN Team 2, FS25. All rights reserved."

from aiohttp import web

from common.constants import VERSION
from algorithms import ALGORITHMS
from .base_handler import BaseHandler


class SystemHandler(BaseHandler):
    """system handler"""

    def add_routes(self, app: web.Application) -> None:
        app.router.add_get("/api/version", self._version)
        app.router.add_get("/api/system/algorithm", self._algorithm)
        app.router.add_put("/api/system/algorithm", self._set_algorithm)
        app.router.add_get("/api/system/algorithms", self._algorithms)
        app.router.add_post("/api/system/algorithm/reset", self.reset)

    async def _version(self, _: web.Request) -> web.Response:
        return web.Response(text=VERSION)

    async def _algorithm(self, _: web.Request) -> web.Response:
        if self._engine.algorithm is None:
            return web.HTTPNoContent()
        return web.Response(text=self._engine.algorithm.name)

    async def _set_algorithm(self, request: web.Request) -> web.Response:
        if "name" not in request.query:
            return web.HTTPBadRequest(text="Algorithm name is required")

        algorithm_name = request.query.get("name")

        if algorithm_name not in (*ALGORITHMS.keys(), ""):
            return web.HTTPBadRequest(text=f"Unknown algorithm: {algorithm_name}")
        algorithm = ALGORITHMS.get(algorithm_name)

        self._engine.change_algorithm(algorithm)
        if self._engine.algorithm is None:
            return web.HTTPNoContent()
        return web.Response(text=self._engine.algorithm.name)

    async def _algorithms(self, _: web.Request) -> web.Response:
        return web.json_response(list(ALGORITHMS.keys()))

    async def reset(self, _: web.Request) -> web.Response:
        """Reset the system"""
        self._engine.reset()
        return web.Response(text="Engine reset")
