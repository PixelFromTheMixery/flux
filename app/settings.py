# region Docs
"""
Settings for API

Processor of the config.yaml file, which will configure the way the app functions at runtime

Classes:
    Secrets: reads from env file
    Config: Pydantic model for config settings file
    Settings: Root for config settings and reference data

Methods:
    generate_settings: method that builds the settings object

TODO: Move file update mechanism in here as it is not used anywhere else
"""

# endregion

from typing import Optional

from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict
import yaml

from .models.settings_models import Integrations


class Secrets(BaseSettings):
    api_addr: str = "https://127.0.0.1"
    api_port: str = "8090"
    field_encryption_key: str
    mongodb_uri: str

    model_config = SettingsConfigDict(env_file=".env.docker", extra="ignore")


class Config(BaseModel):
    # region Docs
    """
    App configuration
    Attributes:
        local(bool) = True: Flag for development mode, turns off scheduler and notifications
        api_addr(str): Web address at which API is running, for inner use URL generation
        api_port (str) = port on which API runs?
        db_file (str) = path to json file that glues everything together
        integrations(Integrations) = Integration settings capsule

    """

    # endregion

    # General
    local: bool

    # Integrations
    integrations: Integrations = Integrations()


def load_config_file(file_path: str = None):
    path = file_path or "settings.yaml"
    try:
        with open(path, "r", encoding="UTF-8") as f:
            new_config_data = yaml.safe_load(f)
            config = Config(**new_config_data)
        if SETTINGS:
            SETTINGS.config = config
        return config
    except FileNotFoundError as exc:
        raise FileNotFoundError("settings.yaml required") from exc


def update_config_file(new_config_data):
    SETTINGS.config = Config(**new_config_data)

    with open("settings.yaml", "w", encoding="UTF-8") as f:
        yaml.safe_dump(SETTINGS.config.model_dump(), f)


class Settings(BaseSettings):
    secrets: Secrets = Secrets()
    config: Config

    @classmethod
    def from_dict(cls, supplied: dict) -> Settings:
        return cls(config=Config(**supplied), secrets=Secrets())

    @classmethod
    def from_file(cls) -> Settings:
        config = load_config_file()
        return cls(config=config, secrets=Secrets())


SETTINGS: Optional[Settings] = None


def get_settings() -> Settings:
    global SETTINGS  # This is a global instance modifier. pylint: disable=global-statement
    if SETTINGS is None:
        SETTINGS = Settings.from_file()
    return SETTINGS


def init_test_settings(supplied: dict) -> Settings:
    global SETTINGS  # This is a global instance modifier for testing. pylint: disable=global-statement
    SETTINGS = None
    SETTINGS = Settings.from_dict(supplied)
    return SETTINGS
