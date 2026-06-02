from cryptography.fernet import Fernet


class Cryptor:
    def __init__(self, field_encryption_key):
        self.fernet = Fernet(field_encryption_key.encode())

    def crypt_string(self, text: str | bytes, decrypt: bool = True) -> bytes:
        if decrypt:
            return self.fernet.decrypt(text).decode()
        return self.fernet.encrypt(text.encode())
