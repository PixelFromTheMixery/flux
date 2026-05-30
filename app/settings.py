# region Docs
"""
Settings for API

Processor of the config.yaml file, which will configure the way the app functions at runtime

Classes:
    ConfigSettings: Pydantic model for config settings file
    Settings: Root for config settings and reference data

Methods:
    generate_settings: @lru_cached method that fetches the same settings instance

TODO: Move file update mechanism in here as it is not used anywhere else
"""
# endregion

from functools import lru_cache

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
    local: bool = True

    # Integrations
    integrations: Integrations = Integrations()


class Settings(BaseModel):
    secrets: Secrets
    config: Config


@lru_cache
def load_settings_from_file() -> Settings:
    # region Docs

    """
    Returns:
        Settings: Distributed settings object for global use
    Raises:
        FileNotFoundError: If the config.yaml is not found.
    """
    # endregion
    secrets = Secrets()

    try:
        with open("settings.yaml", "r", encoding="UTF-8") as f:
            contents = yaml.safe_load(f)
            if contents:
                return Settings(config=Config(**contents), secrets=secrets)

    except FileNotFoundError as exc:
        raise FileNotFoundError("settings.yaml required") from exc


def generate_settings(supplied: dict = None) -> Settings:
    # region Docs
    """
    Build Settings from dict if provided, otherwise from file

    Args:
        supplied (dict): settings dict, usually for testing

    Returns:
        Settings: from code
    """
    # endregion
    secrets = Secrets()

    if supplied:
        config = Config(**supplied)
        return Settings(config=config, secrets=secrets)

    return load_settings_from_file()
