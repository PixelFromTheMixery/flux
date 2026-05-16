from types import SimpleNamespace
import sqlite3

import pytest

from app.data.database import RefDB

PATH = "app.data.database."


@pytest.fixture(scope="session", autouse=True, name="mock_db")
def manage_db_connection(monkeypatch, tmp_path, integrations=("anytype", "traggo")):
    settings = SimpleNamespace(
        db_file=str(tmp_path / "test.db"), integrations=list(integrations)
    )
    monkeypatch.setattr(PATH + "generate_settings", lambda: settings)
    db = RefDB()
    db.connect()

    yield

    db.close_all_connections()


def test_setup_create_tables_and_columns(mock_db):
    with sqlite3.connect(mock_db.settings.db_file) as conn:
        cur = conn.execute(f"PRAGMA table_info({mock_db.table_name})")
        cols = [row[1] for row in cur.fetchall()]

    assert "name" in cols
    assert "type" in cols
    assert "anytype" in cols
    assert "traggo" in cols


def test_execute_sql_write_and_read(mock_db):
    mock_db.execute_sql(
        "INSERT INTO id_maps (name, type) VALUES (?,?)",
        "test insert of project test",
        ("test", "project"),
    )
    rows = mock_db.execute_sql(
        "SELECT * FROM id_maps WHERE name = ?", "read test row", ("test",), True
    )

    assert len(rows) == 1
    assert rows[0]["name"] == "test"
    assert rows[0]["type"] == "project"
