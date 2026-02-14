from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
import os
import platform
from .engine_ai import AIEngine

class FileSystemMonitor(FileSystemEventHandler):
    def __init__(self, quarantine_callback):
        self.ai = AIEngine()
        self.quarantine_callback = quarantine_callback 
        self.system_os = platform.system()

    def on_created(self, event):
        if not event.is_directory:
            self._process_event(event.src_path, "CREADO")

    def on_modified(self, event):
        if not event.is_directory:
            self._process_event(event.src_path, "MODIFICADO")

    def _should_ignore(self, file_path):
        """
        Filtro inteligente para evitar bucles o falsos positivos según el SO.
        """
        # 1. Ignorar archivos propios del Antivirus (Evita auto-escaneo)
        if "SAO-Antivirus" in file_path or "quarantine_vault" in file_path:
            return True
        
        # 2. Filtros Generales
        if file_path.endswith(('.tmp', '.log', '.swp')):
            return True

        # 3. Filtros Específicos por Sistema Operativo
        if self.system_os == "Windows":
            # Ignorar carpetas de sistema profundas que dan error de permiso
            if "AppData\\Local\\Temp" in file_path or "Windows\\Prefetch" in file_path:
                return True
        else: # Linux / macOS
            # CRÍTICO: No escanear sistemas de archivos virtuales
            if file_path.startswith(("/proc", "/sys", "/dev", "/run")):
                return True
            
        return False

    def _process_event(self, file_path, action):
        # Aplicar filtro de ignorados
        if self._should_ignore(file_path):
            return

        # Escanear archivo
        # Nota: engine_ai.py ya maneja la lectura segura por bloques (stream)
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
        # Verificar que la ruta exista antes de vigilar
        if not os.path.exists(self.path):
            print(f"[WATCHDOG] Advertencia: La ruta {self.path} no existe. Omitiendo.")
            return

        self.observer.schedule(self.handler, self.path, recursive=True)
        try:
            self.observer.start()
            print(f"[WATCHDOG] Vigilancia activa en: {self.path}")
        except OSError as e:
            print(f"[ERROR] No se pudo iniciar el Watchdog en {self.path}: {e}")

    def stop(self):
        if self.observer.is_alive():
            self.observer.stop()
            self.observer.join()