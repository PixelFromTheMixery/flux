# region Docs
"""
Basic encryption tool

Used for en/decrypting api keys from the database using the key env var generated during startup

Classes:
    cryptor: bi-directional encryption tool
"""
# endregion

from cryptography.fernet import Fernet


class Cryptor:
    # region Docs
    """
    bi-directional encryption tool

    Attributes:
        fernet (Fernet): the key that enables all other keys
    """

    # endregion

    def __init__(self, field_encryption_key):
        self.fernet = Fernet(field_encryption_key.encode())

    def crypt_string(self, text: str | bytes, decrypt: bool = True) -> bytes | str:
        # region Docs
        """
        Two-way magic

        Args:
            text (str|bytes): The object to be en/decrypted
            decrypted (bool): Assumption the user wants to decrypt as it will happen more often

        Returns:
            bytes or str: Depending on which way the cryption went.
        """
        # endregion

        if decrypt:
            return self.fernet.decrypt(text).decode()
        return self.fernet.encrypt(text.encode())
