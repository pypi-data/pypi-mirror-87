from pathlib import Path
from unittest.mock import Mock

import pytest

from simio.app.builder import AppBuilder
from simio.app.config_names import APP, CLIENTS, VARS, WORKERS, OTHER, CRONS


async def example_worker(app, return_value):
    return return_value


async def example_cron(app):
    app[CLIENTS][Mock].check(alive=True)


TEST_APP_CONFIG = {
    APP: {
        APP.name: "example_project",
        APP.enable_swagger: False,
        APP.handlers_path: Path(__file__).parent.parent,
    },
    CLIENTS: {Mock: {"host": "localhost", "port": 27017,},},
    VARS: {"x": 1, "y": 2,},
    WORKERS: {example_worker: {"return_value": 5}},
    CRONS: {"*/1 * * * *": (example_cron,)},
    OTHER: {"something": 1,},
}


@pytest.fixture
@pytest.mark.asyncio
def builder(loop):
    return AppBuilder(TEST_APP_CONFIG, loop=loop)


@pytest.fixture
def app(builder):
    return builder.build_app()
