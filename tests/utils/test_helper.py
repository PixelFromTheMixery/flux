# region Docs
"""
Tests for the helper module

Tests:
    test_make_deeplink

#TODO: Upcoming task or fix.
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


def test_make_deeplink(helper, anytype_test_space_id) -> None:
    # region Docs
    """
    Generation of anytype deeplink

    Notes: Points to a specific page in testing space space

    Inputs:
        space_id (str): antytype space id
        object_id (str): anytype object id

    Expected outputs:
        result (str): anytype deeplink.
    """
    # endregion

    deeplink_page = "bafyreiahoc6a3vq7mwoufsvt445twijviag2g6vzbw4mi66zhr4oyz4fkq"
    result = helper.make_deeplink(anytype_test_space_id, deeplink_page)

    assert result == (
        "anytype://object?"
        "objectId=bafyreiahoc6a3vq7mwoufsvt445twijviag2g6vzbw4mi66zhr4oyz4fkq&"
        "spaceId=bafyreifepifytna2qjc73kcpk56bdz5remhmtj43iqz3eigdw2ypy64k4e.2bx9tjqqte21g"
    )
