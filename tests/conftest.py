# region Docs
"""
Base settings and fixtures for other tests

Methods:
    anytype_test_space_id
"""
# endregion

import pytest


@pytest.fixture
def anytype_test_space_id() -> str:
    # region Docs
    """
    Supplies human-unreadable string of the testing space space id

    Returns:
        type: Testing Space space ID
    """
    # endregion
    return "bafyreifepifytna2qjc73kcpk56bdz5remhmtj43iqz3eigdw2ypy64k4e.2bx9tjqqte21g"
