import sys
import os
import threading
import platform

# Asegurar que Python encuentre los módulos sin importar desde dónde se ejecute
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from ui.dashboard import MainDashboard
    from utils.admin_privileges import require_admin
except ImportError as e:
    print(f"Error crítico de importación: {e}")
    print("Asegúrate de ejecutar 'pip install -r requirements.txt'")
    sys.exit(1)

def check_environment():
    """
    Verifica y crea las carpetas críticas usando rutas compatibles con el SO.
    """
    # Definimos las rutas usando os.path.join para que funcionen con / (Linux) o \ (Windows)
    required_dirs = [
        os.path.join("database"),
        os.path.join("quarantine_vault"),
        os.path.join("assets"),
        os.path.join("logs")
    ]
    
    for d in required_dirs:
        if not os.path.exists(d):
            print(f"[INIT] Creando directorio: {d}")
            os.makedirs(d)

def main():
    # 1. Comprobación de Seguridad Universal
    # Esta función ahora maneja 'sudo' en Linux y 'UAC' en Windows automáticamente
    if not require_admin():
        print("[ERROR] Se requieren permisos de Administrador/Root para proteger el sistema.")
        return
    
    # 2. Preparación del Entorno
    check_environment()
    
    # 3. Detección de Sistema (Para Logs y Debug)
    current_os = platform.system().upper()
    print(f"[SYSTEM] Iniciando SAO-Antivirus (Guardian Edition) en: {current_os}")
    
    # 4. Iniciar Interfaz Gráfica (Link Start!)
    try:
        app = MainDashboard()
        app.mainloop()
    except KeyboardInterrupt:
        print("\n[SYSTEM] Cierre forzado por el usuario.")
        sys.exit()
    except Exception as e:
        print(f"[CRITICAL ERROR] {e}")
        input("Presiona Enter para salir...")

if __name__ == "__main__":
    main()