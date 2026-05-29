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
from app.settings import Settings


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


@pytest.fixture(name="mock_settings")
def fake_settings(monkeypatch, tmp_path):
    # region Docs
    """
    Fake settings object as to not fail the settings generation step on various objects

    Args:
        monkeypatch (monkeypatch): Allows dynamics adjustment of attributes, methods, and data
        tmp_path (Posix): Temporary pathing tool

    Returns:
        Settings: With minimum required values.
    """
    # endregion

    mock = Settings(db_file=str(tmp_path / "test.json"))
    monkeypatch.setattr("app.settings.generate_settings", lambda: Settings(**mock))

    return mock


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
