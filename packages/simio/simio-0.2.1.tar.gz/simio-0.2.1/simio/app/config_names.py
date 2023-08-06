class AppConfig:
    version: str = "version"
    name: str = "name"
    handlers_path: str = "handlers_path"
    swagger_path: str = "swagger_path"
    autogen_swagger: str = "autogen_swagger"
    enable_swagger: str = "enable_swagger"
    swagger_config: str = "swagger_config"


APP = AppConfig
CLIENTS = "clients"
VARS = "vars"
WORKERS = "workers"
OTHER = "other"
