import os
import json
import shutil
import time
import hashlib
from .crypto import CryptoEngine

class QuarantineManager:
    def __init__(self, vault_path='quarantine_vault', log_path='database/quarantine_log.json'):
        self.vault_path = vault_path
        self.log_path = log_path
        self.crypto = CryptoEngine()
        
        # Crear directorios si no existen
        if not os.path.exists(self.vault_path):
            os.makedirs(self.vault_path)
            # Crear un archivo .gitkeep o readme para que la carpeta no se borre
            with open(os.path.join(self.vault_path, "README.txt"), "w") as f:
                f.write("ZONA DE ALTA SEGURIDAD - NO TOCAR ARCHIVOS AQUI")

        self.registry = self._load_registry()

    def _load_registry(self):
        if os.path.exists(self.log_path):
            with open(self.log_path, 'r') as f:
                try:
                    return json.load(f)
                except:
                    return {}
        return {}

    def _save_registry(self):
        with open(self.log_path, 'w') as f:
            json.dump(self.registry, f, indent=4)

    def isolate_file(self, file_path, threat_name="Unknown"):
        """
        1. Lee el archivo infectado.
        2. Lo cifra en memoria.
        3. Guarda la versión cifrada en la Bóveda.
        4. Elimina el archivo original de forma segura.
        5. Actualiza el registro.
        """
        if not os.path.exists(file_path):
            return False, "Archivo no encontrado"

        try:
            filename = os.path.basename(file_path)
            file_hash = hashlib.sha256(filename.encode() + str(time.time()).encode()).hexdigest()[:16]
            vault_filename = f"{file_hash}.enc"
            vault_full_path = os.path.join(self.vault_path, vault_filename)

            # 1 & 2. Leer y Cifrar
            with open(file_path, 'rb') as f:
                original_data = f.read()
            
            encrypted_data = self.crypto.encrypt_bytes(original_data)

            # 3. Guardar en Bóveda
            with open(vault_full_path, 'wb') as f:
                f.write(encrypted_data)

            # 4. Registrar Metadata (Importante para restaurar)
            self.registry[file_hash] = {
                "original_path": file_path,
                "original_name": filename,
                "threat_name": threat_name,
                "timestamp": time.ctime(),
                "vault_file": vault_filename,
                "size_bytes": len(original_data)
            }
            self._save_registry()

            # 5. Eliminar Origen (Wipe)
            os.remove(file_path) 
            
            print(f"[QUARANTINE] {filename} ha sido aislado y cifrado exitosamente.")
            return True, "Aislado en Bóveda"

        except Exception as e:
            print(f"[ERROR QUARANTINE] Fallo al aislar: {e}")
            return False, str(e)

    def restore_file(self, file_id):
        """Restaura un archivo de la bóveda si fue un falso positivo."""
        if file_id not in self.registry:
            return False, "ID no encontrado en registro"

        meta = self.registry[file_id]
        vault_path = os.path.join(self.vault_path, meta['vault_file'])
        original_path = meta['original_path']

        try:
            # Leer cifrado
            with open(vault_path, 'rb') as f:
                encrypted_data = f.read()
            
            # Descifrar
            decrypted_data = self.crypto.decrypt_bytes(encrypted_data)

            # Restaurar a ubicación original
            # Asegurar que el directorio original aun exista
            os.makedirs(os.path.dirname(original_path), exist_ok=True)
            
            with open(original_path, 'wb') as f:
                f.write(decrypted_data)

            # Limpiar de la bóveda
            os.remove(vault_path)
            del self.registry[file_id]
            self._save_registry()

            return True, f"Archivo restaurado en {original_path}"

        except Exception as e:
            return False, f"Error al restaurar: {e}"

    def list_quarantined_files(self):
        return self.registry