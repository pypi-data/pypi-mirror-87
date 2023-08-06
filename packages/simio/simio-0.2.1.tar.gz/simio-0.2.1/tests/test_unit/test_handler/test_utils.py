import pytest
import typing

from simio.app.builder import AppBuilder
from simio.app.entities import AppRoute
from simio.handler.base import BaseHandler, HandlerMethod, RequestSchema
from simio.handler.utils import route
from tests.conftest import SampleHandlerOneRaw, SampleSchemaOne, SampleHandlerTwoRaw


@pytest.mark.parametrize(
    "handler_class, path, name, expected_routes, expected_handler_methods",
    (
        # fmt: off
        (
            SampleHandlerOneRaw,
            '/v1/some_path/{user_id}/',
            None,
            [AppRoute(handler=BaseHandler, path='/v1/some_path/{user_id}/', name='test_handler')],
            [
                HandlerMethod(method='post', request_schema=RequestSchema(name='data', trafaret=SampleSchemaOne), path_args={'user_id': int}, query_args={}),
                HandlerMethod(method='get', request_schema=None, path_args={'user_id': int}, query_args={'q': typing.Optional[str]})
            ],
        ),
        (
            SampleHandlerTwoRaw,
            '/v1/some_path/',
            'name',
            [AppRoute(handler=BaseHandler, path='/v1/some_path/', name='name')],
            [HandlerMethod(method='get', request_schema=None, path_args={}, query_args={'q': typing.Optional[str]})],
        ),
        # fmt: on
    ),
)
def test_route_decorator(
    handler_class: BaseHandler, path, name, expected_routes, expected_handler_methods
):
    class TestHandler(handler_class):
        ...

    route(path=path, name=name)(TestHandler)

    for app_route in AppBuilder.get_app_routes():
        app_route.handler = BaseHandler

    assert AppBuilder.get_app_routes() == expected_routes

    result = sorted(TestHandler.handler_methods, key=lambda x: x.method)
    assert result == sorted(expected_handler_methods, key=lambda x: x.method)
