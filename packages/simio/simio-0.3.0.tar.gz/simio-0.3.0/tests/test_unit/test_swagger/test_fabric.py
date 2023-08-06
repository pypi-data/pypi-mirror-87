import pytest

from simio.app.config_names import APP
from simio.app.entities import AppRoute
from simio.swagger.fabric import swagger_fabric
from tests.conftest import SampleHandlerOne, SampleHandlerTwo, SampleHandlerThree


@pytest.mark.parametrize(
    "app_config, app_routes, expected_json",
    (
        # fmt: off
        (
            {APP.version: "1.0", APP.name: "test"},
            [
                AppRoute(
                    handler=SampleHandlerOne(None),
                    name="test_handler_one",
                    path="/v1/hello/{user_id}/",
                ),
                AppRoute(
                    handler=SampleHandlerTwo(None),
                    name="test_handler_two",
                    path="/v1/test",
                ),
            ],
            {
                "info": {"title": "test", "version": "1.0"},
                "paths": {
                    "/v1/hello/{user_id}/": {
                        "get": {
                            "parameters": [
                                {"in": "query", "name": "q", "type": "string"},
                                {
                                    "in": "path",
                                    "name": "user_id",
                                    "required": True,
                                    "type": "integer",
                                },
                            ],
                            "responses": {
                                "200": {"description": "Successful request"},
                                "400": {"description": "Invalid input"},
                            },
                            "tags": ["test_handler_one"],
                        },
                        "post": {
                            "parameters": [
                                {
                                    "in": "body",
                                    "name": "data",
                                    "schema": {
                                        "properties": {
                                            "arg_one": {"type": "string"},
                                            "arg_three": {"type": "boolean"},
                                            "arg_two": {"type": "integer"},
                                        },
                                        "type": "object",
                                    },
                                },
                                {
                                    "in": "path",
                                    "name": "user_id",
                                    "required": True,
                                    "type": "integer",
                                },
                            ],
                            "responses": {
                                "200": {"description": "Successful request"},
                                "400": {"description": "Invalid input"},
                            },
                            "tags": ["test_handler_one"],
                        },
                    },
                    "/v1/test": {
                        "get": {
                            "parameters": [
                                {"in": "query", "name": "q", "type": "string"}
                            ],
                            "responses": {
                                "200": {"description": "Successful request"},
                                "400": {"description": "Invalid input"},
                            },
                            "tags": ["test_handler_two"],
                        }
                    },
                },
                "swagger": "2.0",
            },
        ),
        (
            {APP.version: "1.0", APP.name: "test"},
            [
                AppRoute(
                    handler=SampleHandlerOne(None),
                    name="test_handler_one",
                    path="/v1/hello/{user_id}/",
                ),
                AppRoute(
                    handler=SampleHandlerThree(None),
                    name="test_handler_three",
                    path="/v1/test2",
                ),
            ],
            {
                "info": {
                    "title": "test",
                    "version": "1.0"
                },
                "paths": {
                    "/v1/hello/{user_id}/": {
                        "get": {
                            "parameters": [
                                {
                                    "in": "query",
                                    "name": "q",
                                    "type": "string"
                                },
                                {
                                    "in": "path",
                                    "name": "user_id",
                                    "required": True,
                                    "type": "integer"
                                }
                            ],
                            "responses": {
                                "200": {
                                    "description": "Successful request"
                                },
                                "400": {
                                    "description": "Invalid input"
                                }
                            },
                            "tags": [
                                "test_handler_one"
                            ]
                        },
                        "post": {
                            "parameters": [
                                {
                                    "in": "body",
                                    "name": "data",
                                    "schema": {
                                        "properties": {
                                            "arg_one": {
                                                "type": "string"
                                            },
                                            "arg_three": {
                                                "type": "boolean"
                                            },
                                            "arg_two": {
                                                "type": "integer"
                                            }
                                        },
                                        "type": "object"
                                    }
                                },
                                {
                                    "in": "path",
                                    "name": "user_id",
                                    "required": True,
                                    "type": "integer"
                                }
                            ],
                            "responses": {
                                "200": {
                                    "description": "Successful request"
                                },
                                "400": {
                                    "description": "Invalid input"
                                }
                            },
                            "tags": [
                                "test_handler_one"
                            ]
                        }
                    },
                    "/v1/test2": {
                        "get": {
                            "parameters": [
                                {
                                    "in": "body",
                                    "name": "some_schema",
                                    "schema": {
                                        "properties": {
                                            "arg_one": {
                                                "properties": {
                                                    "key": {
                                                        "items": {
                                                            "type": "object",
                                                            "properties": {
                                                                "sub_key": {
                                                                    "type": "integer"
                                                                },
                                                                "sub_key2": {
                                                                    "type": "string"
                                                                }
                                                            }
                                                        },
                                                        "type": "array"
                                                    }
                                                },
                                                "type": "object"
                                            },
                                            "arg_two": {
                                                "items": {
                                                    "type": "integer"
                                                },
                                                "type": "array"
                                            },
                                            'arg_three': {
                                                'items': {
                                                    'items': {
                                                        'type': 'integer'
                                                    },
                                                    'type': 'array'
                                                },
                                                'type': 'array'
                                            },
                                        },
                                        "type": "object"
                                    }
                                }
                            ],
                            "responses": {
                                "200": {
                                    "description": "Successful request"
                                },
                                "400": {
                                    "description": "Invalid input"
                                }
                            },
                            "tags": [
                                "test_handler_three"
                            ]
                        }
                    }
                },
                "swagger": "2.0"
            },
        ),
        # fmt: on
    ),
)
def test_swagger_fabric(app_config, app_routes, expected_json):
    swagger = swagger_fabric(app_config, app_routes)
    assert swagger.json() == expected_json
