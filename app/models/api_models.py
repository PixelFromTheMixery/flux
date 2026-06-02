from typing import Optional

from pydantic import BaseModel


class APIRequest(BaseModel):
    target: str
    category: str
    url: str
    info: str
    auth_token: str
    payload: Optional[dict | str] = None
