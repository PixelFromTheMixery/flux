"""
Pydantic models for app settings

Classes:
    AnytypeSettings: Anytype settings for automations and tracking
    SPSettings: Super Productivity settings for automation and flow
    TraggoSettings: Traggo settings for automation and tracking

TODO: SP and Traggo
"""

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
