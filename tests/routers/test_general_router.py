# region Docs
"""
Module: /app/routers/general_routers.py

Tests:
    health_check

"""
# endregion


def test_health_check(client):
    # region Docs
    """
    Health point check

    Expected result: (Response): (200, { status:ok })
    """
    # endregion

    response = client.get("/general/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
