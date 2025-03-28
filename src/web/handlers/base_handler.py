# -*- coding: utf-8 -*-
"""base handler"""

__copyright__ = "Copyright (c) 2025 HSLU PREN Team 2, FS25. All rights reserved."

from abc import ABC, abstractmethod
import logging
from typing import Any
import json

from aiohttp import web
from pyaddict.schema.base import ISchemaType

from ufo.engine import Engine


class BaseHandler(ABC):
    """base handler"""

    def __init__(self, engine: Engine) -> None:
        self._engine = engine
        self._logger = logging.getLogger("server")

    @abstractmethod
    def add_routes(self, app: web.Application) -> None:
        """add routes"""

    @staticmethod
    async def _get_json_body(request: web.Request, schema: ISchemaType[Any]) -> Any:
        """get body"""
        try:
            body = await request.json()
        except json.JSONDecodeError as e:
            raise web.HTTPBadRequest(reason=f"Invalid JSON: {e}")
        try:
            return schema.expect(body)
        except ValueError as e:
            raise web.HTTPBadRequest(reason=f"Invalid body: {e}")
