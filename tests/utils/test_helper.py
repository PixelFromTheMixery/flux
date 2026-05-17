# region Docs
"""
Module: /app/utils/helper.py

Notes: will likely be deleted soon with the addition of anypython

Tests:
    make_deeplink

"""
# endregion

import pytest

from app.utils.helper import Helper


@pytest.fixture
def helper() -> Helper:
    # region Docs
    """
    Brings in Helper for testing
    Returns:
        Helper: holds methods to test
    """
    # endregion

    return Helper()
