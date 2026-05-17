# region Docs
"""
Database manager for mapping id's between integrations

Creates a database with columns: name, type, and integration id n

Classes:
    RefDB: The interactor class that manages and reads db

#TODO: Query Builder as String method is prone to human error
"""
# endregion

import sqlite3
from sqlite3 import Row

from ..settings import generate_settings
from ..utils.logger import logger


class RefDB:
    # region Docs
    """
    interactor class that manages and reads db

    Attributes:
        table_name (str): singular table for managing id's, I don't image expanding
        settings (Settings): for integration column gen
        conn (SQLiteConnection): Connection to db to make query reads and changes
        conn.row_factory(Row): Converter for tuples and CS dicts

    """

    # endregion

    def __init__(self) -> None:
        self.table_name = "id_maps"
        self.settings = generate_settings()
        self.conn = sqlite3.connect(self.settings.db_file)
        self.conn.row_factory = Row
        self.setup_database()

    def close(self) -> None:
        # region Docs
        """
        Closes connection to database, useful for testing.
        """
        # endregion

        if self.conn:
            self.conn.close()

    def execute_sql(
        self,
        query: str,
        query_summary: str,
        params: tuple = (),
        read: bool = False,
    ) -> None | list[Row]:
        # region Docs
        """
        Executor of SQL Queries

        Args:
            query (str): query to be enacted on database
            query_summary (str): human readable intention
            params (tuple): arguments for write changes
            read (bool): if just performing read actions

        Returns:
            list[Row]: If read, any entries that match criteria
        Raises:
            OperationalError: If query is bad
            ProgrammingError: Logical error in code
        """
        # endregion

        try:
            cur = self.conn.execute(query, params)
            if read:
                rows = cur.fetchall()
                logger.info(query_summary)
                return rows
            self.conn.commit()
            logger.info(query_summary)

        except sqlite3.Error as e:
            logger.exception("DB Error: %s", e)
            raise e

    def setup_database(self) -> None:
        # region Docs
        """
        Prepares the database for intended interaction as descrined in module doc.

        First creates table and then adds required columns based on dynamic inputs
        """
        # endregion

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

        for integration in self.settings.integrations.model_dump().keys():
            if integration not in columns:
                self.execute_sql(
                    f"ALTER TABLE {self.table_name} ADD COLUMN {integration} TEXT",
                    f"Adding column for {integration}",
                )
