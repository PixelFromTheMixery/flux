# region Docs
"""
Database manager for mongo interactions

Contains mapping id's between integrations and API keys for them.
E.g.:
    Traggo's API key is stored encrypted on its own table,
    Super producutivity has a project, stored as a randomised string
    Everything is tags in traggo, so the project is a tag value
    Anytype has object id's, so the project value is another randomised string

Example mapping

| --- | --- | --- | ---| --- |
| Name | Group | Traggo | SP | Anytype |
| Test | Project | Test | Vtnj... | byaf...|

Classes:
    RefDB: The interactor class that manages and reads db

#TODO: Review delete necessity?
"""

# endregion

import asyncio
from beanie import init_beanie
from pymongo import AsyncMongoClient

from .encryption import Cryptor

from ..utils.helper import transformer
from ..models.data_models import (
    MappingDoc,
    EncryptedCredential,
    UpsertRequest,
    NewDoc,
)

from ..utils.logger import logger


class RefDB:
    # region Docs
    """
    interactor class that manages and reads db

    Attributes:
        client (AsyncMongoClient): async executor of requested actions
        cryptor (Cryptor): en/decryt secret strings like api keys
        instance (RefDb): Provides a singleton to the app root
    """

    instance = None

    # endregion

    def __init__(
        self, client: AsyncMongoClient = None, cryptor: Cryptor = None
    ) -> None:
        self.client: AsyncMongoClient = client
        self.cryptor: Cryptor = cryptor

    @classmethod
    async def db_singleton(cls, mongo_uri, field_encryption_key) -> RefDB:
        # region Docs
        """
        Singleton handler for the class.
        Beanie performs the json to document translation.

        Args:
            mongo_uri (str): address at which mongo sits
            field_encryption_key (str): env var with encryption key

        Returns:
            RefDB: Singular object of this class.
        Raises:
            Exception: Mongo handshake failure. Ensure it is running and accessible
        """
        # endregion

        if cls.instance is not None:
            return cls.instance

        client = AsyncMongoClient(mongo_uri, serverSelectionTimeoutMS=2000)

        try:
            await client.admin.command("ping")
        except Exception as e:
            await client.close()
            logger.error("MongoDB connection failed %s", e)
            raise

        await init_beanie(
            database=client.get_database("flux_db"),
            document_models=[MappingDoc, EncryptedCredential],
        )
        logger.info("Mongo/Beanie initialised with mapping and credential tables")

        cls.instance = cls(client=client, cryptor=Cryptor(field_encryption_key))

        return cls.instance

    async def close(self) -> None:
        # region Docs
        """
        Closes connection to database and waits politely for connections to close,
        useful for testing.
        """
        # endregion

        if self.client:
            await self.client.close()
            await asyncio.sleep(0)
        logger.info("Mongo connection closed")

    async def get_entry(
        self,
        group: str,
        name: str,
    ) -> dict:
        # region Docs
        """
        Finds a mapping according to group, then name and returns the entry.

        Args:
            group (str): entry category
            name (str): name within category

        Returns:
            dict: Transformed entry or empty messaging
        """
        # endregion

        entry = await MappingDoc.find_one(
            MappingDoc.name == name, MappingDoc.group == group
        )
        if entry:
            return transformer(entry)

        logger.error("Attempt to find a non-existent entry")
        return {"Error": "Not Found"}

    async def upsert_entry(self, request: UpsertRequest):
        # region Docs
        """
        Updates existing, or inserts new entry based on provided info

        Args:
            request (UpsertRequest): May be one of NewDoc or NewKey
        Returns:
            dict: newly created MappingDoc or EncryptedCredential
        Raises:
            Exception: Error writing to db/file
        """
        # endregion

        action = ""

        if isinstance(request.incoming, NewDoc):
            doc_request = request.incoming
            entry = await MappingDoc.find_one(
                MappingDoc.name == doc_request.name,
                MappingDoc.group == doc_request.group,
            )
            if entry:
                setattr(entry.integrations, doc_request.int_name, doc_request.int_id)
                action = "Updated"

            else:
                entry = MappingDoc(
                    name=doc_request.name,
                    group=doc_request.group,
                    integrations={doc_request.int_name: doc_request.int_id},
                )
                action = "Created"

        else:
            key_request = request.incoming
            entry = await EncryptedCredential.find_one(
                EncryptedCredential.service == key_request.service
            )
            encrypted_cred = self.cryptor.crypt_string(key_request.key, False)
            if entry:
                setattr(
                    entry,
                    "encrypted_api_key",
                    encrypted_cred,
                )
                action = "Updated"
            else:
                entry = EncryptedCredential(
                    service=key_request.service,
                    encrypted_api_key=encrypted_cred,
                )
                action = "Created"

        await entry.save()

        if isinstance(request.incoming, NewDoc):
            logger.info(
                "%s entry: %s (%s) with %s: %s",
                action,
                doc_request.name,
                doc_request.group,
                doc_request.int_name,
                doc_request.int_id,
            )

        else:
            logger.info(
                "%s key: %s",
                action,
                key_request.service,
            )
        return entry

    async def show_table(self):
        # region Docs
        """
        Returns all current mapping data, cache assumed

        Returns:
            dict: All entries in table
        """
        # endregion

        entries = await MappingDoc.find_all().to_list()
        formatted_entries = []
        for entry in entries:
            formatted_entries.append(transformer(entry))
        return formatted_entries

    async def get_key(self, service: str):
        # region Docs
        """
        Fetches and decrypts key based on service

        Args:
            service (str): for searching
        Returns:
            str: unencrypted string, only for authorisation
        """
        # endregion

        entry = await EncryptedCredential.find_one(
            EncryptedCredential.service == service
        )
        return self.cryptor.crypt_string(entry.encrypted_api_key)

    async def delete_entry(self, doc_id):
        # region Docs
        """
        Shapes will change. This allows entry deletion.

        Args:
            doc_id (str): entry id generated by mongo

        Returns:
            dict: deleted entry, in case of recreation
        """
        # endregion

        entry = await MappingDoc.get(doc_id)
        if entry:
            await entry.delete()
            return {"Deleted": transformer(entry)}
        return {"Error": "Not Found"}
