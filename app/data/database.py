# region Docs
"""
Database manager for mapping id's between integrations

Creates a database with columns: name, group, and integration id n

Classes:
    RefDB: The interactor class that manages and reads db

#TODO: Change to mongo
"""

# endregion

from typing import Optional
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from .encryption import Cryptor

from ..utils.helper import transformer
from ..models.data_models import MappingDoc, EncryptedCredential, UpsertRequest, NewDoc, NewKey
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
        self.settings = settings if settings else generate_settings()
        self.client: Optional[AsyncIOMotorClient] = None
        self.cryptor = Cryptor(settings)

    async def init_db(self) -> None:
        self.client = AsyncIOMotorClient(self.settings.secrets.mongodb_uri)

        await init_beanie(
            database=self.client["flux"],
            document_models=[MappingDoc, EncryptedCredential],
        )
        logger.info("Mongo/Beanie initialised with mapping and credential tables")

    def close(self) -> None:
        # region Docs
        """
        Closes connection to database, useful for testing.
        """
        # endregion

        if self.client:
            self.client.close()
        logger.info("Mongo connection closed")

    async def get_entry(self, name: str, group: str):
        entry = await MappingDoc.find_one(
            MappingDoc.name == name, MappingDoc.group == group
        )

        return transformer(entry)

    async def upsert_entry(self, request: UpsertRequest):
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

        if isinstance(request.incoming, NewDoc):
            doc_request = request.incoming
            entry = await MappingDoc.find_one(
                MappingDoc.name == doc_request.name, MappingDoc.group == doc_request.group
            )
            if entry:
                entry["integrations"][doc_request.int_name] = doc_request.int_id
                action = "Updated"
            else:
                entry = MappingDoc(
                    name=doc_request.name,
                    group= doc_request.group,
                    integrations={doc_request.int_name:doc_request.int_id},
                )
                action = "Created"
            MappingDoc(**entry)

        else:
            key_request = request.incoming
            entry = await EncryptedCredential.find_one(
                EncryptedCredential.service == incoming.service
            )
            encrypted_cred = Cryptor.crypt_string(incom)
            if entry:
                entry[service] = 
                action = "Updated"
            else:
                entry = EncryptedCredential(
                    service=incoming["service"] ,
                    encrypted_api_key= incoming["group"],
                    integrations= incoming["integrations"],
                )
                action = "Created"

        result = await entry.save() if action == "Updated" else entry.insert()

        logger.info(
            "%s entry: %s (%s) with %s: %s",
            action,
            name,
            group,
            int_name,
            int_id,
        )
        return result

    async def show_table(self):
        # region Docs
        """
        Returns all current data, cache assumed

        Returns:
            dict: All entries in table
        """
        # endregion

        entries = await MappingDoc.find_all().to_list()
        return [entry.model_dump() for entry in entries]

    async def upsert_cred(self, service, key):
        entry = await EncryptedCredential.find_one(
            EncryptedCredential.service == service
        )

        if 
