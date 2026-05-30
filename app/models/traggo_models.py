# region Docs
"""
Models for interactions with Traggo Time Logging software

Includes queries, mutations and request objects for transformation

Classes:
    TimeEntryRequest: For making calls to the services
"""
# endregion

from typing import Optional
from pydantic import BaseModel


class TimeEntryRequest(BaseModel):
    startTime: str
    endTime: Optional[str] = None
    tags: list[str]
    note: str
