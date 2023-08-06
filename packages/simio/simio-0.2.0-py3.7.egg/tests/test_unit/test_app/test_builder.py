import asyncio

import pytest

from simio.app.builder import _deep_merge_dicts
from simio.app.config_names import CLIENTS, WORKERS
from simio.app.default_config import get_default_config
from tests.test_unit.test_app.conftest import TEST_APP_CONFIG


@pytest.mark.parametrize(
    "lhs, rhs, expected_result",
    (
        (
            {"key": {"key1": 2, "key2": 3,}, "key1": 1},
            {"key": {"key1": 0, "key3": 4}, "key1": 2, "key2": 3,},
            {"key": {"key1": 0, "key2": 3, "key3": 4,}, "key1": 2, "key2": 3,},
        ),
    ),
)
def test_merge_configs(lhs, rhs, expected_result):
    result = _deep_merge_dicts(lhs, rhs)
    assert result == expected_result


class TestAppBuilder:
    def test_initiated_app_config(self, app):
        assert app["config"] == _deep_merge_dicts(get_default_config(), TEST_APP_CONFIG)

    def test_created_clients(self, app):
        assert len(app[CLIENTS]) == len(TEST_APP_CONFIG[CLIENTS])

        for client, client_instance in app[CLIENTS].items():
            for attr_name, attr_value in TEST_APP_CONFIG[CLIENTS][client].items():
                assert getattr(client_instance, attr_name) == attr_value

    @pytest.mark.asyncio
    async def test_created_workers(self, app):
        assert len(app[WORKERS]) == len(TEST_APP_CONFIG[WORKERS])

        for worker, worker_instance in app[WORKERS].items():
            result = await asyncio.gather(worker_instance)
            assert result[0] == TEST_APP_CONFIG[WORKERS][worker]["return_value"]
