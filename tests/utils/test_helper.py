# region Docs
"""
Module: /app/utils/helper.py

Notes: will likely be deleted soon with the addition of anypython

Tests:
    test_transformer

"""

# endregion

from pydantic import BaseModel

from app.utils.helper import transformer


class BasicModel(BaseModel):
    id: str
    name: str


def test_transformer():
    mock_model = BasicModel(name="mock", id="model")
    result = transformer(mock_model)

    assert result["name"] == "mock"
    assert result["id"] == "model"
