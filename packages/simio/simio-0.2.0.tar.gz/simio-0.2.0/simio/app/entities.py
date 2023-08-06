from dataclasses import dataclass
from typing import Type

from aiohttp import web

from simio.handler.base import BaseHandler


@dataclass
class AppRoute:
    handler: Type[BaseHandler]
    path: str
    name: str

    def get_route_def(self) -> web.RouteDef:
        return web.view(path=self.path, handler=self.handler)
