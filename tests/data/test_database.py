from types import SimpleNamespace
import sqlite3
import tracemalloc
import warnings

import pytest

from app.data.database import RefDB


tracemalloc.start()
warnings.filterwarnings("default", category=ResourceWarning)


@pytest.fixture(name="mock_db")
def manage_db_connection(monkeypatch, tmp_path, integrations=("anytype", "traggo")):
    settings = SimpleNamespace(
        db_file=str(tmp_path / "test.db"), integrations=list(integrations)
    )
    monkeypatch.setattr("app.data.database.generate_settings", lambda: settings)
    db = RefDB()

    yield db

    db.close()


def test_setup_create_tables_and_columns(mock_db):
    table_info = mock_db.execute_sql(
        f"PRAGMA table_info ({mock_db.table_name})", "Collecting table info", read=True
    )

    cols = [row[1] for row in table_info]

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


def test_db_sanity_check(mock_db):
    with pytest.raises(sqlite3.OperationalError) as exc_info:
        mock_db.execute_sql("Bad query", "Bad query")

    assert exc_info.type == sqlite3.OperationalError
