"""Settings for API"""

from functools import lru_cache
from pathlib import Path
from typing import Annotated

from pydantic import BaseModel, Field

from utils.helper import Helper

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

    # Task Management
    anytype_space_id: Annotated[
        str,
        Field(
            description="Anytype space id for logging management",
        ),
    ] = None

    # Pushover
    pushover: Annotated[
        bool,
        Field(
            description="Flag for pushover notifications",
        ),
    ] = False

    log_types: Annotated[
        anytypeObject,
        Field(
            description="types of activities gets logged in journal space",
        ),
    ] = False


    # task_review_threshold: Annotated[
    #     int,
    #     Field(
    #         description=(
    #             "Number of says to reset a task before a prompt is generated. "
    #             "0 is the off switch"
    #         ),
    #     ),
    # ] = 0


    pushover_journal_hours: Annotated[
        list[str],
        Field(
            description="Which hours to send notifications",
        ),
    ] = []

    # Time Tagger
    timetagger: Annotated[
        bool, Field(description="If time tagger side car is used")
    ] = False
    timetagger_url: Annotated[
        str, Field(description="URL to use to make calls to timetagger")
    ] = "http://timetagger:80"


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
