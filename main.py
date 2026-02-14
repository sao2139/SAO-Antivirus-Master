import sys
import os
import ctypes
import threading
import subprocess

# Asegurar que Python encuentre los módulos
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from ui.dashboard import MainDashboard
    from utils.admin_privileges import require_admin
except ImportError as e:
    print(f"Error crítico de importación: {e}")
    print("Asegúrate de ejecutar 'pip install -r requirements.txt' y mantener la estructura de carpetas.")
    input("Presiona Enter para salir...")
    sys.exit(1)

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def check_environment():
    """Verifica que las carpetas críticas existan antes de iniciar UI."""
    required_dirs = ["database", "quarantine_vault", "assets"]
    for d in required_dirs:
        if not os.path.exists(d):
            print(f"[INIT] Creando directorio faltante: {d}")
            os.makedirs(d)

def launch_daemon():
    """
    Opcional: Lanza el servicio en segundo plano si no está corriendo.
    En un entorno real, esto sería un Servicio de Windows.
    Aquí lo simulamos lanzando el script en un subproceso independiente.
    """
    # Verificación simple para no duplicar procesos (en producción usaría PID files)
    # subprocess.Popen([sys.executable, "service_daemon.py"], creationflags=subprocess.CREATE_NO_WINDOW)
    pass 

def main():
    # 1. Comprobación de Seguridad (Permisos de Admin)
    # SAO-Antivirus necesita acceso a red (raw sockets) y sistema de archivos.
    if not is_admin():
        print("[SYSTEM] Solicitando acceso Root (Admin)...")
        # El script se reiniciará a sí mismo con permisos elevados
        if require_admin():
            return # Si requiere admin, el proceso actual termina y nace el nuevo
    
    # 2. Preparación del Entorno
    check_environment()
    
    # 3. Lanzar Daemon (Opcional, desactivado por defecto para no saturar en pruebas)
    # launch_daemon()

    # 4. Iniciar Interfaz Gráfica (Link Start!)
    print("[SYSTEM] Iniciando Interfaz Neural SAO...")
    app = MainDashboard()
    
    # Manejo seguro de cierre
    try:
        app.mainloop()
    except KeyboardInterrupt:
        print("Cierre forzado detectado.")
        sys.exit()

if __name__ == "__main__":
    main()