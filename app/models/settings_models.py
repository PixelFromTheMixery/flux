"""Models to be used by the settings module"""

from pydantic import BaseModel


class AnytypeSettings(BaseModel):
    """
    Settings for Anytype

    Attributes:
        space_id (str): target space to interact with
    """

    space_id: str


class SPSettings(BaseModel):
    """
    Settings for Super Productivity

    Attributes:
        sync_file? (str): may moved to env for volume mounting
    """

    sync_file: str


class TraggoSettings(BaseModel):
    """
    Settings for Traggo

    Attributes:
        Unknown
    """
