# region Docs
"""
Settings for API

Processor of the config.yaml file, which will configure the way the app functions at runtime

Classes:
    ConfigSettings: Pydantic model for config settings file
    Settings: Root for config settings and reference data

Methods:
    generate_settings: @lru_cached method that fetches the same settings instance
    read_write_file: interacts with files for cold storage across loads

TODO: Move file update mechanism in here as it is not used anywhere else
"""
# endregion

from functools import lru_cache
from pathlib import Path
from typing import Annotated, Optional

from pydantic import BaseModel, Field
import yaml

from .models.settings_models import AnytypeSettings, SPSettings, TraggoSettings
from .models.data_models import ReferenceData


class ConfigSettings(BaseModel):
    # region Docs
    """
    App configuration
    Attributes:
        local(bool) = True: Flag for development mode, turns off scheduler and notifications
        api_addr(str): Web address at which API is running, for inner use URL generation
        ### Integrations
        sp(SPSettings): Settings for Super Productivity
        anytype(AnytypeSettings): Settings for Anytype
        trago(TraggoSettings): Settings for Traggo
    """

    # endregion

    # General
    local: Annotated[bool, Field()] = True

    api_addr: Annotated[str, Field()]

    # Integrations
    sp: Annotated[Optional[SPSettings, Field()]] = None

    anytype: Annotated[Optional[AnytypeSettings, Field()]] = None

    traggo: Annotated[Optional[TraggoSettings, Field()]] = None


class Settings(BaseModel):
    # region Docs
    """
    The Top-Level Singleton Registry

    Attributes:
        config (ConfigSettings): Runtime configuration
        data (ReferenceData): Reference data for reducing path discovery
    """

    # endregion

    config: ConfigSettings = Field(default_factory=ConfigSettings)
    data: ReferenceData = Field(default_factory=ReferenceData)


@lru_cache
def generate_settings() -> Settings:
    # region Docs
    """
    Constructor for the irregular sources

    Args:
        arg1 (type): Description of arg1.
        arg2 (type): Description of arg2.
        arg3 (type): Description of arg3.

    Returns:
        Settings: Distributed settings object for global use
    Raises:
        FileNotFoundError: If the config.yaml is not found.
    """

    try:
        config_yaml = read_write("config.yaml", "r")
    except FileNotFoundError as exc:
        raise FileNotFoundError("config.yaml required") from exc
    data_path = "data/data.yaml"
    try:
        data_yaml = read_write(data_path, "r")
    except FileNotFoundError:
        make_dir = Path(data_path).parent
        make_dir.mkdir(parents=True, exist_ok=True)
        print("Reference data file requires generation")
        data_yaml = {}

    return Settings(
        config=ConfigSettings(**config_yaml),
        data=ReferenceData(**data_yaml),
    )


def read_write(path, method, data=None):
    """
    File read and write combo for yaml sync to local instance.

    Args:
        path (str): path to file to interact with.
        method (str): "r" or "w" for with open.
        data (dict): data to store into yaml.

    Returns:
        dict: from data if provided
    """
    # endregion

    with open(path, method, encoding="utf-8") as f:
        if data:
            f.write(yaml.safe_dump(data, sort_keys=False))
        return yaml.safe_load(f)
