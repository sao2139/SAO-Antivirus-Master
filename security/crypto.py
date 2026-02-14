from cryptography.fernet import Fernet
from .key_manager import KeyManager

class CryptoEngine:
    def __init__(self):
        self.key_manager = KeyManager()
        self.cipher = Fernet(self.key_manager.get_key())

    def encrypt_bytes(self, data: bytes) -> bytes:
        """Convierte datos binarios en datos cifrados seguros."""
        return self.cipher.encrypt(data)

    def decrypt_bytes(self, token: bytes) -> bytes:
        """Restaura los datos originales (Solo con la llave correcta)."""
        return self.cipher.decrypt(token)
    
    def encrypt_file_in_place(self, file_path):
        """(Peligroso) Cifra un archivo sobreescribiéndolo. Usar con precaución."""
        with open(file_path, 'rb') as f:
            data = f.read()
        encrypted = self.encrypt_bytes(data)
        with open(file_path, 'wb') as f:
            f.write(encrypted)