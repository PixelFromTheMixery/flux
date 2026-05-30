# region Docs
"""
Base settings and fixtures for other tests

Methods:
    anytype_test_space_id
    client_fixture
"""
# endregion

from cryptography.fernet import Fernet
from fastapi.testclient import TestClient
from testcontainers.core.generic import DockerContainer
import pytest

from app.main import app
from app.settings import Settings, Secrets


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
def fake_settings(monkeypatch):
    # region Docs
    """
    Fake settings object as to not fail the settings generation step on various objects

    Args:
        monkeypatch (monkeypatch): Allows dynamics adjustment of attributes, methods, and data

    Returns:
        Settings: With minimum required values.
    """
    # endregion
    monkeypatch.setenv("API_ADDR", "https://api.mock.com")
    monkeypatch.setenv("API_PORT", "123")

    valid_fernet_key = Fernet.generate_key().decode()

    monkeypatch.setenv("FIELD_ENCRYPTION_KEY", valid_fernet_key)

    monkeypatch.setenv("MONGODB_URI", "mongobd://mock.uri")
    secrets = Secrets()
    mock = Settings(config={}, secrets=secrets)
    monkeypatch.setattr("app.settings.generate_settings", lambda: Settings(**mock))

    return mock


@pytest.fixture(name="app_client")
def app_client_fixture():
    # region Docs
    """
    Test client for endpoint/end-to-end tests.

    Returns:
        TestClient: instance of the base server
    """
    # endregion

    with TestClient(app) as client:
        yield client


@pytest.fixture(name="mongo_client")
def mongo_uri():
    mongo = DockerContainer("mongo:6.0").with_exposed_ports(27017)

    with mongo:
        host = mongo.get_container_host_ip()
        port = mongo.get_exposed_port(27017)
        yield f"mongodb://{host}:{port}"
