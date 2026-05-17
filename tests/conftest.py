# region Docs
"""
Base settings and fixtures for other tests

Methods:
    anytype_test_space_id
    client_fixture
"""
# endregion

from fastapi.testclient import TestClient
import pytest

from app.main import app


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


@pytest.fixture(name="client")
def client_fixture():
    # region Docs
    """
    Test client for endpoint/end-to-end tests.

    Returns:
        TestClient: instance of the base server
    """
    # endregion

    with TestClient(app) as client:
        yield client
