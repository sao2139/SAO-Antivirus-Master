import sys
import os
import subprocess

def is_admin():
    """Verifica si el script tiene permisos de administrador (Root/Admin)."""
    try:
        if os.name == 'nt':  # Windows
            import ctypes
            return ctypes.windll.shell32.IsUserAnAdmin()
        else:  # Linux / macOS
            return os.geteuid() == 0
    except:
        return False

def require_admin():
    """
    Si no es admin, relanza el script solicitando permisos.
    Windows: UAC
    Linux: Sudo
    """
    if is_admin():
        return True

    print("[SYSTEM] Solicitando elevación de privilegios (Root/Admin)...")
    
    if os.name == 'nt':  # Windows
        import ctypes
        try:
            ctypes.windll.shell32.ShellExecuteW(
                None, "runas", sys.executable, " ".join(sys.argv), None, 1
            )
        except Exception as e:
            print(f"[ERROR WINDOWS] No se pudo obtener admin: {e}")
            return False
    else:  # Linux
        try:
            # Relanzamos el script usando 'sudo' y preservando las variables de entorno
            args = ['sudo', '-E', sys.executable] + sys.argv
            os.execlpe('sudo', *args)
        except Exception as e:
            print(f"[ERROR LINUX] Fallo al invocar sudo: {e}")
            return False
            
    sys.exit() # Cerrar la instancia sin permisos