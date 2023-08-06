import json
from typing import Any, Type, List, Optional as Opt, Callable, get_type_hints

from aiohttp.web_exceptions import HTTPBadRequest
from trafaret import Trafaret, DataError
from typingplus import cast

from simio.app.builder import AppBuilder
from simio.handler.base import BaseHandler, HandlerMethod, RequestSchema
from simio.handler.http_methods import HTTP_METHODS
from simio.utils import is_typing, cast_cap_words_to_lower


def route(
    path: str, name: Opt[str] = None  # pylint: disable=unused-argument
) -> Callable:
    """
        Decorator to add app route

        Usage:
            >>> @route('/v1/hello/')
            >>> class SomeHandler(BaseHandler):

    :param path: http path of route
    :param name: Optional. Name of your handler
    """

    def decorator(cls: Type[BaseHandler]) -> Callable:
        nonlocal name

        if name is None:
            name = cast_cap_words_to_lower(cls.__name__)

        AppBuilder.add_route(path=path, handler=cls, name=name)
        handler_methods = _prepare_handler_methods(cls, path)

        cls.handler_methods = handler_methods

        def wrapper(*args, **kwargs) -> BaseHandler:
            return cls(*args, **kwargs)

        return wrapper

    return decorator


def get_bad_request_exception(message: Any) -> HTTPBadRequest:
    """
    :param message: text of your exception
    :return: returns HTTPBadRequest exception with json:
            {"error": message}
    """
    body = {"error": message}
    return HTTPBadRequest(reason="Bad Request", body=json.dumps(body))


def _prepare_handler_methods(cls: Type[BaseHandler], path: str) -> List[HandlerMethod]:
    """
        Extracts from class all request handlers by http methods name,
        setups handler_method property of class and adds decorator _handler.
    """
    handler_methods_name = HTTP_METHODS.intersection(set(dir(cls)))
    handler_methods = []

    for method_name in handler_methods_name:
        handler = getattr(cls, method_name)
        handler_method = HandlerMethod(method=method_name)
        method_args = get_type_hints(handler)
        method_args.pop("return", None)

        for arg_name, type_hint in method_args.items():
            if not is_typing(type_hint) and isinstance(type_hint, Trafaret):
                handler_method.request_schema = RequestSchema(
                    trafaret=type_hint, name=arg_name
                )
            elif f"{{{arg_name}}}" in path:
                handler_method.path_args[arg_name] = type_hint
            else:
                handler_method.query_args[arg_name] = type_hint

        handler_methods.append(handler_method)
        setattr(cls, method_name, _handler(handler, handler_method))

    return handler_methods


def _handler(func: Callable, handler_method: HandlerMethod):
    """
        Decorator that collects data from request and adds them to function kwargs

    :param func: request handler
    """

    async def wrapper(self: BaseHandler, *args, **kwargs) -> Any:
        for arg_name, type_hint in handler_method.path_args.items():
            value = _cast_type(self.request.match_info.get(arg_name), type_hint)

            if value is not None:
                kwargs[arg_name] = value

        for arg_name, type_hint in handler_method.query_args.items():
            value = _cast_type(self.request.query.get(arg_name), type_hint)

            if value is not None:
                kwargs[arg_name] = value

        if handler_method.request_schema is not None:
            value = _cast_type(
                await self.request.json(), handler_method.request_schema.trafaret
            )
            kwargs[handler_method.request_schema.name] = value

        return await func(self, *args, **kwargs)

    return wrapper


def _cast_type(value, type_hint):
    """
        Casting request data
    """
    try:
        if isinstance(type_hint, Trafaret):
            return type_hint.check(value)
        return cast(type_hint, value)
    except DataError as e:
        raise get_bad_request_exception(e.as_dict())
    except (ValueError, TypeError) as e:
        raise get_bad_request_exception(str(e))
