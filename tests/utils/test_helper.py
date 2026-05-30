# region Docs
"""
Module: /app/utils/helper.py

Notes: will likely be deleted soon with the addition of anypython

Tests:
    make_deeplink

"""

# endregion
from app.models.shared_models import BasicModel

from app.utils.helper import transformer


def test_transformer():
    mock_model = BasicModel(name="mock", id="model")
    result = transformer(mock_model)

    assert result["name"] == "mock"
    assert result["id"] == "model"
