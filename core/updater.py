# core/updater.py
import requests
import os
import subprocess
import sys
from packaging import version

class SAOUpdater:
    def __init__(self, current_version, config_url):
        self.current_version = current_version
        self.config_url = config_url
        self.update_info = None

    def check_for_updates(self):
        try:
            print(f"[UPDATER] Buscando actualizaciones... (Actual: {self.current_version})")
            # Usamos un timeout corto para no congelar la app si no hay internet
            response = requests.get(self.config_url, timeout=3)
            if response.status_code == 200:
                data = response.json()
                remote_ver = data.get("version", "0.0.0")
                
                # Limpieza simple de strings para comparar (quita texto extra)
                clean_local = self.current_version.split(" ")[0]
                clean_remote = remote_ver.split(" ")[0]

                if version.parse(clean_remote) > version.parse(clean_local):
                    self.update_info = data
                    return True, f"Versión {remote_ver} disponible"
            return False, "Sistema actualizado"
        except Exception as e:
            return False, f"Sin conexión: {str(e)[:20]}..."

    def download_and_install(self, callback_progress=None):
        if not self.update_info: return
        url = self.update_info["download_url"]
        filename = "update_setup.exe"
        try:
            with requests.get(url, stream=True) as r:
                r.raise_for_status()
                with open(filename, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        f.write(chunk)
            # Ejecutar instalador silencioso
            subprocess.Popen([filename, "/SILENT", "/SP-", "/CLOSEAPPLICATIONS"])
            os._exit(0) 
        except Exception as e:
            print(f"[ERROR UPDATE] {e}")