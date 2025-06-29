# -*- coding: utf-8 -*-
"""system web handler"""

__copyright__ = "Copyright (c) 2025 HSLU PREN Team 2, FS25. All rights reserved."

import dataclasses

from aiohttp import web
from pyaddict.schema import Object, Float

from common.constants import VERSION
from common.competition import update_dynamic_network, create_dynamic_network
from network.node import NodeLabel
from algorithms import ALGORITHMS
from .base_handler import BaseHandler


class SystemHandler(BaseHandler):
    """system handler"""

    def add_routes(self, app: web.Application) -> None:
        app.router.add_get("/api/version", self._version)
        app.router.add_get("/api/system/algorithm", self._algorithm)
        app.router.add_put("/api/system/algorithm", self._set_algorithm)
        app.router.add_get("/api/system/algorithms", self._algorithms)
        app.router.add_post("/api/system/algorithm/reset", self._reset)
        app.router.add_get("/api/system/network", self._get_network)
        app.router.add_put("/api/system/network", self._set_network)

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

    async def _reset(self, _: web.Request) -> web.Response:
        """Reset the system"""
        self._engine.reset()
        return web.Response(text="Engine reset")

    async def _get_network(self, _: web.Request) -> web.Response:
        """Get the current network configuration"""
        network = create_dynamic_network()
        data = [dataclasses.asdict(x) for x in network.nodes]
        return web.json_response(data)

    async def _set_network(self, request: web.Request) -> web.Response:
        """Set the network configuration"""
        location_schema = Object(
            {
                "x": Float().coerce(),
                "y": Float().coerce(),
            }
        )
        schema = Object({x.value: location_schema
                         for x in NodeLabel
                         if x != NodeLabel.UNDEFINED})

        data = await self._get_json_body(request, schema)
        update_dynamic_network(data)
        return web.Response()
