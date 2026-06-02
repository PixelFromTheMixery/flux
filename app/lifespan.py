from contextlib import asynccontextmanager
from fastapi import FastAPI

from .data.database import RefDB
from .settings import get_settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = get_settings()
    db_instance = await RefDB.db_singleton(
        settings.secrets.mongodb_uri,
        settings.secrets.field_encryption_key,
    )

    app.state.db = db_instance

    yield

    if hasattr(app.state.db, "client"):
        await app.state.db.client.close()

    RefDB.instance = None
