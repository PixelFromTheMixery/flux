# region Docs
"""
Models for interactions with Traggo Time Logging software

Includes queries, mutations and request objects for transformation

Classes:
    TimeEntryRequest: For making calls to the services
"""
# endregion

from typing import Optional
from datetime import datetime

from pydantic import BaseModel, field_validator


class TagUpsert(BaseModel):
    # region Docs
    """
    Tag Upsert shape

    Attributes:
        key (str): name of tag key
        value (str): name of tag value if assigning value
        color (str): HTML colour code if creating new tags
    """

    # endregion

    name: str
    old_name: Optional[str] = None
    color: Optional[str] = "#FFFFFF"

    @field_validator("color")
    @classmethod
    def color_code(cls, v):
        if v is None:
            return v
        if not isinstance(v, str) or not v.startswith("#") or len(v) != 7:
            raise ValueError("color is not valid html code.")
        return v


class Tag(BaseModel):
    key: str
    value: str


class TimeEntryRequest(BaseModel):
    # region Docs
    """
    Basic Time Entry shape

    Attributes:
        start_time (str): datetime string in iso
        end_time (str): datetime string in iso
        tag (list[Tag]): list of key:value pairs.
        note (str): Usually the name of the task or task parent
    """

    # endregion

    start_time: str
    end_time: Optional[str] = None
    tags: list[Tag]
    note: str

    @field_validator("start_time", "end_time")
    @classmethod
    def check_iso(cls, v):
        """Ensures time values are in iso format"""
        try:
            assert datetime.fromisoformat(v.replace("Z", "+00:00"))
        except ValueError as exc:
            raise ValueError(
                "Time values must be stored as iso format strings"
            ) from exc

        return v
