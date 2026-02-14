import ctypes
import sys
import os

def is_admin():
    """Verifica si el script tiene permisos de administrador."""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def require_admin():
    """
    Si no es admin, relanza el script solicitando permisos UAC (Pantalla de 'Sí/No' de Windows).
    """
    if is_admin():
        return True
    else:
        # Re-ejecutar el programa con privilegios elevados
        print("[SYSTEM] Solicitando elevación de privilegios...")
        try:
            ctypes.windll.shell32.ShellExecuteW(
                None, "runas", sys.executable, " ".join(sys.argv), None, 1
            )
            sys.exit() # Cerrar la instancia sin permisos
        except Exception as e:
            print(f"[ERROR] No se pudo obtener admin: {e}")
            return False