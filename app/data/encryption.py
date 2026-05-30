from cryptography.fernet import Fernet


class Cryptor:
    def __init__(self, settings):
        self.settings = settings
        self.fernet = Fernet(settings.secrets.field_encryption_key.encode())

    def crypt_string(self, text: str | bytes, encrypt: bool = True) -> bytes:
        if encrypt:
            return self.fernet.encrypt(text.encode())
        else:
            return self.fernet.decrypt(text).decode()
