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

from pydantic import BaseModel, field_validator
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
        db_file (str) = path to json file that glues everything together
        integrations(Integrations) = Integration settings capsule

    """

    # endregion

    # General
    local: bool = True

    api_addr: str = "https://127.0.0.1"
    api_port: str = "8090"

    db_file: str = "app/data/data.json"
    # Integrations

    integrations: Integrations = Integrations()

    @field_validator("db_file", mode="after")
    @classmethod
    def ensure_json_db(cls, value):
        # region Docs
        """
        tinyDB uses json files exclusively.

        Args:
            cls (Settings): Settings instance that is validated
            value (str): key in instance to be validated

        Returns:
            value: If valid json filename, returns
        Raises:
            ValueError: If the value does not end with '.json'
        """
        # endregion

        if not value.endswith(".json"):
            raise ValueError(f"{value} must be a .json file name")
        return value


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

    try:
        with open("settings.yaml", "r", encoding="UTF-8") as f:
            contents = yaml.safe_load(f)
            if contents:
                return Settings(**contents)
            return Settings()

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

    if supplied:
        return Settings(**supplied)

    return load_settings_from_file()
