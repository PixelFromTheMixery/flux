import os

from testcontainers.core.generic import DockerContainer
import pytest


from app.services.traggo_service import TraggoService

TEST_API_KEY = "51Y9Ya4gumzvX9vURVT6"
TEST_DB_FILE = os.path.abspath("./traggodata")


@pytest.fixture(name="traggo_conn", scope="session")
def traggo_uri():
    """Traggo container for testing"""

    print(f"\n[TESTINFO] Mounting Traggo DB from: {TEST_DB_FILE}")

    traggo = (
        DockerContainer("traggo/server:latest")
        .with_exposed_ports(3030)
        .with_volume_mapping(TEST_DB_FILE, "/data")
    )
    with traggo:
        uri = f"http://{traggo.get_container_host_ip()}:{traggo.get_exposed_port(3030)}/graphql"
        yield uri


@pytest.fixture(name="mock_traggo")
def get_traggo(traggo_conn):
    service: TraggoService = TraggoService(traggo_conn, TEST_API_KEY)
    return service


@pytest.mark.asyncio
async def test_connection(mock_traggo):
    result = await mock_traggo.connection_check()

    assert isinstance(result, dict)
    assert "version" in result
    assert "name" in result["version"]
