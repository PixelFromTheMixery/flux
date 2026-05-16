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
import yaml

from .models.settings_models import Integrations


class Settings(BaseModel):
    # region Docs
    """
    App configuration
    Attributes:
        local(bool) = True: Flag for development mode, turns off scheduler and notifications
        api_addr(str): Web address at which API is running, for inner use URL generation
        api_port (str) = port on which API runs?
        db_file (str) = path to file that glues everything together
        integrations(Integrations) = Integration settings capsule

    """

    # endregion

    # General
    local: bool = True

    api_addr: str = "https://127.0.0.1"
    api_port: str = "8090"

    db_file: str = "data/data.db"
    # Integrations

    integrations: Integrations = {}


@lru_cache
def generate_settings() -> Settings:
    # region Docs
    """
    Returns:
        Settings: Distributed settings object for global use
    Raises:
        FileNotFoundError: If the config.yaml is not found.
    """

    try:
        with open("settings.yaml", "r", encoding="UTF-8") as f:
            return Settings(**yaml.safe_load(f))
    except FileNotFoundError as exc:
        raise FileNotFoundError("settings.yaml required") from exc
