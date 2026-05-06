"""Data model for local caching"""

from typing import Dict, Optional
from pydantic import BaseModel, ConfigDict, Field

from ..utils.helper import Helper
from ..utils.logger import logger


class QueryData(BaseModel):
    """
    Anytype query object reference

    Attributes:
        id (str): anytype object id
        model_config: ConfigDict, used for adding any extra attributes
    """

    id: str
    model_config = ConfigDict(extra="allow")


class TypeData(BaseModel):
    """
    # TODO: move templates into its own Data Class
    Anytype type objects with template reference

    Attributes:
        id (str): anytype object id
        key (str): type key, snake_case encouraged
        templates (Dict[str, str]): associated templates, in the form of name:object_id
    """

    id: str
    key: str
    templates: Optional[Dict[str, str]] = None


class OptionData(BaseModel):
    """
    Option of a select or multi-select Anytype property
    Note: duplicate keys make an error, even across properties

    Attributes:
        id (str): anytype object id
        key (str): option key, snake_case encouraged
        name (str): option name
        colour (str): option colour, must be one of [
            grey, yellow, orange, red, pink, purple, blue, ice, teal, lime
        ]
    """

    id: str
    key: str
    name: str
    color: str = "grey"


class PropData(BaseModel):
    """
    Anytype Property object shape

    Attributes:
        id (str): anytype object id
        key (str): prop key, snake_case encouraged
        name (str): prop name
        format (str): data format, must be one of [
            text, number, select, multi_select, date, files, checkbox, url, email, phone, objects
        ]
        options (OptionData): list of options on available on the tag
    """

    id: str
    key: str
    name: str
    format: str
    options: Optional[Dict[str, OptionData]] = None


class SpaceData(BaseModel):
    """
    Collection of above Anytype data by space.

    Attributes:
        id (str): anytype space id
        queries (QueryData): Space queries
        types (TypeData): Space types
        props (PropData): Space Props
    """

    id: str

    queries: Dict[str, QueryData] = Field(default_factory=dict)
    types: Dict[str, TypeData] = Field(default_factory=dict)
    props: Dict[str, PropData] = Field(default_factory=dict)


class ReferenceData(BaseModel):
    """
    Top-level key map to integrations.

    Attributes:
        anytype (Dict[str, Spacedata]): Per space reference data
    """

    anytype: Dict[str, SpaceData] = {}

    def file_sync(self):
        """
        Writes data model to a local file for reference

        Args:
            None
        Returns:
            None
        """
        logger.info("File sync")
        Helper.read_write("data/data.yaml", "w", self.model_dump())
