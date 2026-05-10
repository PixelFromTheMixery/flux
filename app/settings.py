"""
Settings for API

Processor of the config.yaml file, which will configure the way the app functions at runtime

Variables:
    helper (Helper): Imported for the read writ file class, but might just want to move it into here.

Classes:
    ConfigSettings: Pydantic model for config settings file
    Settings: Root for config settings and reference data

Methods:
    generate_settings: @lru_cached method that fetches the same settings instance

TODO: Move file update mechanism in here as it is not used anywhere else
"""

from functools import lru_cache
from pathlib import Path
from typing import Annotated, Optional

from pydantic import BaseModel, Field

from .models.settings_models import AnytypeSettings, SPSettings, TraggoSettings
from .models.data_models import ReferenceData
from .utils.helper import Helper

helper = Helper()


class ConfigSettings(BaseModel):
    """App configuration"""

    # General
    local: Annotated[
        bool,
        Field(
            description="Flag for development mode, turns off scheduler and notifications",
        ),
    ] = True

    api_addr: Annotated[
        str,
        Field(
            description="Web address at which API is running, for inner use URL generation",
        ),
    ]

    # Integrations
    super_productivity: Optional[
        SPSettings,
        Field(
            description="Settings for Super Productivity",
        ),
    ] = None

    anytype: Optional[
        AnytypeSettings,
        Field(
            description="Settings for Anytype",
        ),
    ] = None

    traggo: Optional[
        TraggoSettings, Field(description="If Traggo side car is used")
    ] = None


class Settings(BaseModel):
    """The Top-Level Singleton Registry"""

    config: ConfigSettings = Field(default_factory=ConfigSettings)
    data: ReferenceData = Field(default_factory=ReferenceData)


@lru_cache
def generate_settings() -> Settings:
    """Constructor for the weird data sources"""
    try:
        config_yaml = helper.read_write("config.yaml", "r")
    except FileNotFoundError as exc:
        raise FileNotFoundError("config.yaml required") from exc
    data_path = "data/data.yaml"
    try:
        data_yaml = helper.read_write(data_path, "r")
    except FileNotFoundError:
        make_dir = Path(data_path).parent
        make_dir.mkdir(parents=True, exist_ok=True)
        print("Reference data file requires generation")
        data_yaml = {}

    return Settings(
        config=ConfigSettings(**config_yaml),
        data=ReferenceData(**data_yaml),
    )
