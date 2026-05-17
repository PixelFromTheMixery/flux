# region Docs
"""
Base settings and fixtures for other tests

Methods:
    anytype_test_space_id
"""
# endregion

from fastapi.testclient import TestClient
import pytest

from app.settings import generate_settings
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


@pytest.fixture(autouse=True)
def clear_settings_cache():
    # region Docs
    """
    Clears settings before and after every test

    Args:
        autuse (bool): Automatically apply every test, default True
    """
    # endregion

    generate_settings.cache_clear()
    yield
    generate_settings.cache_clear()


@pytest.fixture(name="client")
def client_fixture():
    with TestClient(app) as client:
        yield client
