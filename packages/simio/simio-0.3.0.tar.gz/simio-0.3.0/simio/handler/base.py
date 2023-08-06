from dataclasses import dataclass, field
from typing import Any, Optional as Opt, List

from aiohttp import web


__doc__ = "Module with base entities for Handler"

from trafaret import Trafaret


@dataclass
class RequestSchema:
    trafaret: Trafaret
    name: str


@dataclass
class HandlerMethod:
    """
        Describes HTTP method of BaseHandler

        path_args and query_args contains dict where
        keys are names of args and value are type hints
    """

    method: str

    request_schema: Opt[RequestSchema] = None
    path_args: dict = field(default_factory=dict)
    query_args: dict = field(default_factory=dict)


class BaseHandler(web.View):
    """
        Use this class to create your own handlers


        Has some useful properties:
            self.app -- get your application
            self.config -- get config of your application
            await self.request_json -- get json of request

        And methods:
            self.response(body, status, **kwargs) -- get json web.Response

        `handler_methods` is property only for framework. Don't change value of this

    """

    handler_methods: Opt[List[HandlerMethod]] = None

    @property
    def app(self) -> web.Application:
        return self.request.app

    @property
    def config(self) -> dict:
        return self.app["config"]

    @property
    async def request_json(self) -> dict:
        return await self.request.json()

    @staticmethod
    def response(body: Any, status: int = 200, **kwargs) -> web.Response:
        return web.json_response(body, status=status, **kwargs)
