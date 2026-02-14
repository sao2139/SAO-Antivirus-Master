from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
import os
from .engine_ai import AIEngine

class FileSystemMonitor(FileSystemEventHandler):
    def __init__(self, quarantine_callback):
        self.ai = AIEngine()
        self.quarantine_callback = quarantine_callback # Función para aislar archivos

    def on_created(self, event):
        if not event.is_directory:
            self._process_event(event.src_path, "CREADO")

    def on_modified(self, event):
        if not event.is_directory:
            self._process_event(event.src_path, "MODIFICADO")

    def _process_event(self, file_path, action):
        # Ignorar archivos temporales o del propio sistema
        if file_path.endswith(".tmp") or "AppData" in file_path or "SAO-Antivirus" in file_path:
            return

        # Escanear
        is_threat, reason, score = self.ai.scan_file(file_path)
        
        if is_threat:
            print(f"[MONITOR] ¡AMENAZA DETECTADA! ({score}%) Archivo: {file_path}")
            # Ejecutar protocolo de cuarentena
            if self.quarantine_callback:
                self.quarantine_callback(file_path, reason)

class WatchdogService:
    def __init__(self, path_to_watch, quarantine_action):
        self.observer = Observer()
        self.handler = FileSystemMonitor(quarantine_action)
        self.path = path_to_watch

    def start(self):
        self.observer.schedule(self.handler, self.path, recursive=True)
        try:
            self.observer.start()
        except OSError:
            print("[ERROR] No se pudo iniciar el Watchdog (¿Permisos?)")

    def stop(self):
        self.observer.stop()
        self.observer.join()