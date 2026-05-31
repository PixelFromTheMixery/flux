from contextlib import asynccontextmanager
from fastapi import FastAPI

from .data.database import RefDB


@asynccontextmanager
async def lifespan(app: FastAPI):
    db_instance = await RefDB.db_singleton(
        app.state.settings.secrets.mongodb_uri,
        app.state.settings.secrets.field_encryption_key,
    )

    app.state.db = db_instance

    yield

    if hasattr(app.state.db, "client"):
        await app.state.db.client.close()

    RefDB.instance = None
