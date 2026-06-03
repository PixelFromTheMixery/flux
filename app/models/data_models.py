# region Docs
"""
Data Models for interacting with MongoDB

Classes:
    EncryptedCredential: usually an api key stored
    Integrations: list of currently support integrations
    MappingDoc: entry mapping
    NewDoc: For incoming requests
    NewKey: For incoming requests
    UpsertRequest: encapsulator shape for NewDoc or NewKey

Note on pylint warnings muting:
- Disabled as comments are somehow considered ancestors
- Disabled as the Settings for mongo require no additional methods
"""
# pylint: disable=too-many-ancestors, too-few-public-methods
# endregion

from datetime import datetime
from typing import Optional

from beanie import Document
from pydantic import BaseModel, Field


class EncryptedCredential(Document):
    # region Docs
    """
    Encrypted API key for each integration.

    Attributes:
        service (string): name of the service the key is for
        encrypted_api_key (bytes): self explanatory
        updated_at (datetime): #TODO: why is this here?

    """

    # endregion

    service: str
    encrypted_api_key: bytes
    updated_at: datetime = Field(default_factory=datetime.now)

    class Settings:
        """Mongo db details"""

        name = "credentials"
        indexes = [[("service", 1)]]


class Integrations(BaseModel):
    # region Docs
    """
    List of supported integrations for storing app

    Attributes:
        traggo (str): traggo id
        sp (str): super productivity id
        anytype (str): anytype id

    """

    # endregion

    traggo: Optional[str] = None
    sp: Optional[str] = None
    anytype: Optional[str] = None


class MappingDoc(Document):
    # region Docs
    """
    Basic shape for Mongo document

    Attributes:
        name (str): pretty name
        group (str): project, tag, etc.
        intrgration (Integrations): list of integration:id mappings
    """

    # endregion

    name: str
    group: str
    integrations: Integrations

    class Settings:
        """Mongo db details"""

        name = "id_maps"
        indexes = [[("name", 1), ("group", 1)]]


class NewDoc(BaseModel):
    # region Docs
    """
    Shape for incoming mapping entries

    Attributes:
        name (str): pretty name
        group (str): project, tag, etc.
        int_name (str): name of integration to be mapped
        int_id (str): id of the mapping in the integration
    """

    # endregion

    name: str
    group: str
    int_name: str
    int_id: str


class NewKey(BaseModel):
    # region Docs
    """
    Shape for incoming key entries

    Attributes:
        service (str): integration name
        key (str): api key from integration
    """

    # endregion

    service: str
    key: str


class UpsertRequest(BaseModel):
    # region Docs
    """
    Encapsulator, as process is the same for any incoming object

    Attributes:
        incoming (NewDoc or NewKey): incoming object
    """

    # endregion

    incoming: NewDoc | NewKey
