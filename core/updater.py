
import requests
import json
import os
import sys
import subprocess
import threading
from packaging import version 

class SAOUpdater:
    def __init__(self, current_version, config_url):
        self.current_version = current_version
        self.config_url = config_url 
        self.update_info = None

    def check_for_updates(self):
        """Consulta al servidor si hay una versión nueva."""
        try:
            print(f"[UPDATER] Buscando actualizaciones... (Actual: {self.current_version})")
            response = requests.get(self.config_url, timeout=5)
            if response.status_code == 200:
                data = response.json()
                remote_ver = data.get("version", "0.0.0")
                
                # Comparamos versiones de forma inteligente (1.0.1 > 1.0.0)
                if version.parse(remote_ver) > version.parse(self.current_version):
                    self.update_info = data
                    return True, f"Nueva versión {remote_ver} disponible"
            return False, "Sistema actualizado"
        except Exception as e:
            return False, f"Error de conexión: {e}"

    def download_and_install(self, callback_progress=None):
        """Descarga el instalador y lo ejecuta."""
        if not self.update_info:
            return

        url = self.update_info["download_url"]
        filename = "update_setup.exe"
        
        try:
            # Descarga con stream para no llenar la RAM
            with requests.get(url, stream=True) as r:
                r.raise_for_status()
                total_length = int(r.headers.get('content-length', 0))
                downloaded = 0
                
                with open(filename, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        f.write(chunk)
                        downloaded += len(chunk)
                        if callback_progress and total_length > 0:
                            percent = int((downloaded / total_length) * 100)
                            callback_progress(percent)

            # Ejecutar el instalador de Inno Setup
            # /SILENT y /SP- hacen que se instale rápido sin preguntar tanto
            subprocess.Popen([filename, "/SILENT", "/SP-", "/CLOSEAPPLICATIONS"])
            
            # Cerrar el antivirus actual para permitir la sobreescritura
            os._exit(0) 
            
        except Exception as e:
            print(f"[ERROR UPDATE] {e}")