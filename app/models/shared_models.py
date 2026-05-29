# region Docs
"""
Basic models to share by other model modules

Usually basic or shared shapes

Classes:
    basic: BaseModel of name and id
"""
# endregion

from pydantic import BaseModel


class BasicModel(BaseModel):
    id: str
    name: str
