import os
import threading
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class HoneyPotHandler(FileSystemEventHandler):
    def __init__(self, trigger_callback):
        self.trigger = trigger_callback

    def on_modified(self, event):
        if not event.is_directory:
            self.trigger(event.src_path)

class HoneyPotSystem:
    def __init__(self, location, panic_callback):
        self.location = location
        self.decoys = ["passwords.txt", "wallet_backup.dat", "ceo_report.xlsx"]
        self.panic = panic_callback
        self.observer = Observer()

    def deploy(self):
        """Crea los archivos cebo."""
        if not os.path.exists(self.location):
            os.makedirs(self.location)

        for decoy in self.decoys:
            path = os.path.join(self.location, decoy)
            with open(path, 'w') as f:
                f.write("SAO-ANTIVIRUS HONEYPOT DATA - DO NOT TOUCH\n" * 100)
        
        # Iniciar vigilancia exclusiva de esta carpeta
        event_handler = HoneyPotHandler(self._trap_triggered)
        self.observer.schedule(event_handler, self.location, recursive=False)
        self.observer.start()

    def _trap_triggered(self, filepath):
        print(f"!!! HONEYPOT ACTIVADO EN {filepath} !!!")
        # Aquí llamaríamos al process_killer para matar todo lo sospechoso
        self.panic("RANSOMWARE_ATTACK")

    def stop(self):
        self.observer.stop()