import os
from cryptography.fernet import Fernet

class KeyManager:
    def __init__(self, key_path='security/master.key'):
        self.key_path = key_path
        self.key = self._load_or_generate_key()

    def _load_or_generate_key(self):
        """
        Carga la llave maestra existente o crea una nueva si es la primera ejecución.
        """
        if os.path.exists(self.key_path):
            with open(self.key_path, 'rb') as key_file:
                return key_file.read()
        else:
            # Generar una nueva llave segura de 32 url-safe base64-encoded bytes
            print("[SECURITY] Generando nueva Llave Maestra de Cifrado...")
            key = Fernet.generate_key()
            # Asegurar que el directorio existe
            os.makedirs(os.path.dirname(self.key_path), exist_ok=True)
            with open(self.key_path, 'wb') as key_file:
                key_file.write(key)
            return key

    def get_key(self):
        return self.key