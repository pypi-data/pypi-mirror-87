import os

from simio.app.config_names import APP


def get_default_config() -> dict:
    return {
        APP: {
            APP.version: "0.1.0",
            APP.autogen_swagger: True,
            APP.enable_swagger: True,
            APP.swagger_config: {
                "config_path": os.path.join(os.getcwd(), "swagger.json"),
            },
        },
    }
