from types import SimpleNamespace
import sqlite3

import pytest

from app.settings import Settings
from app.data.database import RefDB

PATH = "app.data.database."


def make_settings(tmp_path, integrations=("anytype", "traggo")):
    return SimpleNamespace(
        db_file=str(tmp_path / "test.db"), integrations=list(integrations)
    )


def test_setup_create_tables_and_columns(monkeypatch, tmp_path):
    monkeypatch.setattr(PATH + "generate_settings", lambda: make_settings(tmp_path))
    db = RefDB()
    with sqlite3.connect(db.settings.db_file) as conn:
        cur = conn.execute(f"PRAGMA table_info({db.table_name})")
        cols = [row[1] for row in cur.fetchall()]

    assert "name" in cols
    assert "type" in cols
    assert "anytype" in cols
    assert "traggo" in cols


def test_execute_sql_write_and_read(monkeypatch, tmp_path):
    monkeypatch.setattr(PATH + "generate_settings", lambda: make_settings(tmp_path))
    db = RefDB()
    db.execute_sql(
        "INSERT INTO id_maps (name, type) VALUES (?,?)",
        "test insert of project test",
        ("test", "project"),
    )
    rows = db.execute_sql(
        "SELECT * FROM id_maps WHERE name = ?", "read test row", ("test",), True
    )
    assert len(rows) == 1
    assert rows[0]["name"] == "test"
    assert rows[0]["type"] == "project"
