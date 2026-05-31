# region Docs
"""
Module: /app/routers/general_routers.py

Tests:
    root_check
    health_check

"""

import pytest


# endregion
@pytest.mark.asyncio
async def test_root_check(app_client):
    # region Docs
    """
    Root point check

    Notes: placed in here for convenience, and it is general

    Expected result: (Response): (200, { Flux: Fluctuating data to create synergies })
    """
    # endregion

    response = await app_client.get("/")

    assert response.status_code == 200
    assert response.json() == {"Flux": "Fluctuating data to create synergies"}


@pytest.mark.asyncio
async def test_health_check(app_client):
    # region Docs
    """
    Health point check

    Expected result: (Response): (200, { status:ok })
    """
    # endregion

    response = await app_client.get("/general/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
