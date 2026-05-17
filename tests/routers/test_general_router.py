import pytest


def test_health_check(client):
    response = client.get("/general/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
