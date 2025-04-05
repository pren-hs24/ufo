# -*- coding: utf-8 -*-
"""ui web handler"""

__copyright__ = "Copyright (c) 2025 HSLU PREN Team 2, FS25. All rights reserved."

from pathlib import Path

from aiohttp import web

from .base_handler import BaseHandler


class UiHandler(BaseHandler):
    """ui handler"""

    def add_routes(self, app: web.Application) -> None:
        app.router.add_get("/{tail:.*}", self._root_handler)

    async def _root_handler(self, request: web.Request) -> web.StreamResponse:
        relative_file_path = Path(request.path).relative_to("/")  # remove root '/'
        file_path = "./public" / relative_file_path  # rebase into static dir
        if not file_path.exists():
            return web.FileResponse("./public/index.html")
        if file_path.is_dir():
            file_path /= "index.html"
            if not file_path.exists():
                return web.HTTPNotFound()
        return web.FileResponse(file_path)
