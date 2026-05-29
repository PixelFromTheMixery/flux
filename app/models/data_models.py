# region Docs
"""
Quality Check for the docs in the TinyDB

Classes:
    TinyDBDoc: Simple object with id, name, type, and integration id's

"""
# endregion

from typing import Optional
from pydantic import BaseModel

from .shared_models import BasicModel


class TinyDBDoc(BaseModel):
    # region Docs
    """
    Basic shape for TinyDB document

    Attributes:
        id (int): doc_id of doc, saved for local access
        name (str): pretty name
        type (str): project or tag
        intrgration (dict): list of integration:id mappings
    """

    # endregion

    id: Optional[int] = None
    name: str
    group: str
    integrations: BasicModel


class DocSearch(BaseModel):
    name: str
    group: str


class NewDoc(BaseModel):
    entry_filter: int | DocSearch
    int_name: str
    int_id: str
