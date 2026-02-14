import unittest
import os
import sys

# Añadir directorio raíz al path para importar módulos
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from security.crypto import CryptoEngine
from security.key_manager import KeyManager

class TestSecurity(unittest.TestCase):
    def setUp(self):
        # Usar una llave temporal para pruebas
        self.crypto = CryptoEngine()

    def test_encryption_reversible(self):
        original_text = b"DATO_SECRETO_DEL_VIRUS"
        encrypted = self.crypto.encrypt_bytes(original_text)
        
        self.assertNotEqual(original_text, encrypted, "El dato no se cifró")
        
        decrypted = self.crypto.decrypt_bytes(encrypted)
        self.assertEqual(original_text, decrypted, "El dato descifrado no coincide")

if __name__ == '__main__':
    unittest.main()