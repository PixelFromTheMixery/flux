# region Docs
"""
Pydantic models for app settings

Classes:
    AnytypeSettings: Anytype settings for automations and tracking
    SPSettings: Super Productivity settings for automation and flow
    TraggoSettings: Traggo settings for automation and tracking

    Integrations: Collection of all below integrations


TODO: SP and Traggo
"""
# endregion

from typing import Optional

from pydantic import BaseModel


class AnytypeSettings(BaseModel):
    # region Docs
    """
    Settings for Anytype

    Attributes:
        space_id (str): target space to interact with
    """

    # endregion

    space_id: str


class SPSettings(BaseModel):
    # region Docs
    """
    Settings for Super Productivity

    Attributes:
        sync_file? (str): may moved to env for volume mounting
    """

    # endregion

    sync_file: str


class TraggoSettings(BaseModel):
    # region Docs
    """
    Settings for Traggo

    Attributes:
        Unknown
    """

    # endregion
    traggo_url: str = "http://localhost:3030/graphql"


class Integrations(BaseModel):
    # region Docs
    """
    Collective Class for all above integrations

    Attributes:
        testing (dict): object to perform tests on

        anytype (AnytypeSettings): N/A
        superprod (SPSettings): N/A
        traggo (TraggoSettings): N/A

    """

    # endregion
    anytype: Optional[AnytypeSettings] = None
    superprod: Optional[SPSettings] = None
    traggo: Optional[TraggoSettings] = None
