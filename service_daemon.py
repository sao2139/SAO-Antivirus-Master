import time
import logging
import json
import os
import sys
from watchdog.observers import Observer

# Importar Core
from core.file_monitor import FileSystemMonitor
from core.honeypot import HoneyPotSystem
from security.quarantine import QuarantineManager

# Configuración de Logging (Sin UI)
logging.basicConfig(
    filename='database/service.log',
    level=logging.INFO,
    format='%(asctime)s - [DAEMON] - %(message)s'
)

def load_config():
    with open('config.json', 'r') as f:
        return json.load(f)

class GuardianService:
    def __init__(self):
        self.config = load_config()
        self.quarantine = QuarantineManager()
        self.running = True
        
        # Sistemas de vigilancia
        self.observer = Observer()
        self.honeypot = None

    def threat_detected_callback(self, file_path, reason):
        """Callback cuando el Monitor de Archivos encuentra algo."""
        logging.warning(f"¡AMENAZA DETECTADA! {file_path} ({reason})")
        print(f"[ALERTA] Neutralizando: {file_path}")
        
        # Acción automática: Cuarentena
        success, msg = self.quarantine.isolate_file(file_path, reason)
        if success:
            logging.info(f"Archivo neutralizado exitosamente: {msg}")
        else:
            logging.error(f"Fallo al neutralizar: {msg}")

    def panic_mode(self, threat_type):
        """Callback cuando el Honeypot es tocado."""
        logging.critical(f"¡ATAQUE DE RANSOMWARE EN PROGRESO! ({threat_type})")
        # Aquí podrías activar un bloqueo de escritura global
        
    def start(self):
        logging.info("Iniciando Servicio Guardian SAO...")
        
        # 1. Iniciar Monitor de Sistema de Archivos (Watchdog)
        # Monitorear Descargas y Escritorio por defecto
        paths_to_watch = [
            os.path.expanduser("~/Downloads"),
            os.path.expanduser("~/Desktop")
        ]
        
        event_handler = FileSystemMonitor(self.threat_detected_callback)
        
        for path in paths_to_watch:
            if os.path.exists(path):
                self.observer.schedule(event_handler, path, recursive=False)
                logging.info(f"Vigilando: {path}")

        self.observer.start()

        # 2. Desplegar Honeypot (Trampa)
        self.honeypot = HoneyPotSystem("C:\\HoneyPot_Trap", self.panic_mode)
        self.honeypot.deploy()
        logging.info("Trampas Honeypot desplegadas.")

        # Bucle infinito eficiente
        try:
            while self.running:
                time.sleep(1)
        except KeyboardInterrupt:
            self.stop()

    def stop(self):
        logging.info("Deteniendo servicio...")
        self.observer.stop()
        self.observer.join()
        if self.honeypot:
            self.honeypot.stop()
        sys.exit(0)

if __name__ == "__main__":
    print("--- SAO GUARDIAN SERVICE (BACKGROUND) ---")
    print("Presiona Ctrl+C para detener.")
    service = GuardianService()
    service.start()