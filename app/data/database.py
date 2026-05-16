import sqlite3

from ..settings import generate_settings
from ..utils.logger import logger


class RefDB:
    def __init__(self):
        self.table_name = "id_maps"
        self.settings = generate_settings()
        self.setup_database()

    def execute_sql(
        self,
        query: str,
        query_summary: str,
        params: tuple = (),
        read: bool = False,
    ):
        try:
            with sqlite3.connect(self.settings.db_file) as conn:
                conn.row_factory = sqlite3.Row
                cur = conn.execute(query, params)
                if read:
                    rows = cur.fetchall()
                    logger.info(query_summary)
                    return rows
                conn.commit()
                logger.info(query_summary)
        except sqlite3.OperationalError as e:
            logger.exception("DB Error: %s", e)
            raise e

    def setup_database(self):
        self.execute_sql(
            f"""
                CREATE TABLE IF NOT EXISTS {self.table_name} (
                    name TEXT PRIMARY KEY,
                    type TEXT NOT NULL
                )
            """,
            "Created table if not existed",
        )
        table = self.execute_sql(
            f"PRAGMA table_info ({self.table_name})", "Collecting table info", read=True
        )
        columns = [row[1] for row in table]

        for integration in self.settings.integrations:
            if integration not in columns:
                self.execute_sql(
                    f"ALTER TABLE {self.table_name} ADD COLUMN {integration} TEXT",
                    f"Adding column for {integration}",
                )
