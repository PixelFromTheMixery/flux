# region Docs
"""
Database manager for mapping id's between integrations

Creates a database with columns: name, group, and integration id n

Classes:
    RefDB: The interactor class that manages and reads db

#TODO: Query Builder as String method is prone to human error
"""

# endregion
from functools import lru_cache

from tinydb import Query, TinyDB

from ..models.data_models import TinyDBDoc
from ..settings import Settings, generate_settings
from ..utils.logger import logger


class RefDB:
    # region Docs
    """
    interactor class that manages and reads db

    Attributes:
        table_name (str): singular table for managing id's, I don't image expanding
        settings (Settings): for integration column gen
        db (TinyDB): database object for interaction
        table (str): table name, for easier access as is there is only one
        query (Query): cached Query instance for faster operations
    """

    # endregion

    def __init__(self, settings: Settings = None) -> None:
        self.table_name = "id_maps"
        self.settings = settings if settings else generate_settings()
        self.db = TinyDB(self.settings.db_file)
        self.table = self.db.table(self.table_name)
        self.query = Query()
        self.get_mapping = lru_cache(maxsize=128)(self._get_mapping_internal)

    def close(self) -> None:
        # region Docs
        """
        Closes connection to database, useful for testing.
        """
        # endregion

        self.db.storage.close()
        self.get_mapping.cache_clear()

    def _get_mapping_internal(self, search_filter: int | dict[str, str]) -> dict | None:
        # region Docs
        """
        Gets an entry from the db based on name and group

        Args:
            id (int): doc id if provided
            name (str): name of entry
            group (str): project, tag, etc.

        Returns:
            dict: full matching entry from database
        Raises:
            Exception: Read Error, unlikely with None safetynet
        """
        # endregion
        entry = None
        if isinstance(search_filter, int):
            entry = self.table.get(doc_id=search_filter)
        else:
            entry = self.table.get(
                (self.query.name == search_filter["name"])
                & (self.query.group == search_filter["group"])
            )
        if entry:
            result = dict(entry)
            result["id"] = entry.doc_id
            return result
        return None

    def upsert_entry(self, name: str, group: str, int_name: str, int_id: str):
        # region Docs
        """
        Updates existing, or inserts new entry based on provided info

        Args:
            name (str): entry name
            group (str): project, tag, etc.
            int_name (str): name of the integration
            int_id (str): id from integration

        Raises:
            Exception: Error writing to db/file
        """
        # endregion

        action = ""
        entry = self._get_mapping_internal({"name": name, "group": group})
        if entry:
            entry["integrations"][int_name] = int_id
            TinyDBDoc(**entry)

            entry_id = self.table.update(entry, doc_ids=[entry["id"]])
            action = "Updated"
        else:
            new_entry = {
                "name": name,
                "group": group,
                "integrations": {int_name: int_id},
            }
            TinyDBDoc(**new_entry)

            entry_id = self.table.insert(new_entry)
            action = "Created"

        self.get_mapping.cache_clear()

        logger.info(
            "%s entry: %s (%s) with %s: %s",
            action,
            name,
            group,
            int_name,
            int_id,
        )
        return entry_id

    def show_table(self):
        # region Docs
        """
        Returns all current data, cache assumed

        Returns:
            dict: All entries in table
        """
        # endregion

        return self.table.all()
