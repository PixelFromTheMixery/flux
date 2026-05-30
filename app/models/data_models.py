# region Docs
"""
Quality Check for the docs in the TinyDB

Classes:
    TinyDBDoc: Simple object with id, name, type, and integration id's

"""

# endregion

from datetime import datetime
from typing import Optional

from beanie import Document
from pydantic import BaseModel, Field


class EncryptedCredential(Document):
    service: str
    encrypted_api_key: bytes
    updated_at: datetime = Field(default_factory=datetime.now)

    class Settings:
        name = "credentials"


class Integrations(BaseModel):
    traggo: Optional[str] = None
    sp: Optional[str] = None
    anytype: Optional[str] = None


class MappingDoc(Document):
    # region Docs
    """
    Basic shape for Mongo document

    Attributes:
        name (str): pretty name
        type (str): project or tag
        intrgration (dict): list of integration:id mappings
    """

    # endregion

    name: str
    group: str
    integrations: Integrations

    class Settings:
        name = "id_maps"
        indexes = [[("name", 1), ("group", 1)]]


class DocSearch(BaseModel):
    name: str
    group: str


class NewDoc(BaseModel):
    name: str
    group: str
    int_name: str
    int_id: str


class NewKey(BaseModel):
    service: str
    key: str


class UpsertRequest(BaseModel):
    incoming: NewDoc | NewKey
