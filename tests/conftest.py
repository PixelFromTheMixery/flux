# region Docs
"""
Base settings and fixtures for other tests

Methods:
    anytype_test_space_id
    client_fixture
"""

# endregion

from asgi_lifespan import LifespanManager
from httpx import AsyncClient, ASGITransport
from cryptography.fernet import Fernet
from testcontainers.core.generic import DockerContainer
import pytest

from app.settings import Settings, Secrets


@pytest.fixture(name="mock_settings")
def fake_settings(monkeypatch, mongo_conn):
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

    monkeypatch.setenv("MONGODB_URI", mongo_conn)

    secrets = Secrets()
    mock = Settings(config={}, secrets=secrets)
    monkeypatch.setattr("app.settings.generate_settings", lambda: mock)

    return mock


@pytest.fixture(name="app_client")
async def app_client_fixture(mock_settings):
    # region Docs
    """
    Test client for endpoint/end-to-end tests.

    Returns:
        TestClient: instance of the base server with mock settings attached
    """
    # endregion

    # Import app after mock_settings fixture runs so tests can monkeypatch settings
    from app.main import app

    # ASGITransport is required in newer HTTPX versions to route directly to FastAPI

    async with LifespanManager(app=app) as manager:
        async with AsyncClient(
            transport=ASGITransport(app=manager.app), base_url="http://test"
        ) as client:
            yield client


@pytest.fixture(name="mongo_conn", scope="session")
def mongo_uri():
    mongo = DockerContainer("mongo:6.0").with_exposed_ports(27017)

    with mongo:
        host = mongo.get_container_host_ip()
        port = mongo.get_exposed_port(27017)
        conn_str = f"mongodb://{host}:{port}/flux_db"
        yield conn_str
