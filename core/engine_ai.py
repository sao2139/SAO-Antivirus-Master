import sys
import os
import subprocess

def is_admin():
    """
    Verifica si el script tiene permisos de Superusuario.
    Retorna: True si es Admin (Windows) o Root (Linux).
    """
    try:
        if os.name == 'nt':  # Si estamos en Windows
            import ctypes
            return ctypes.windll.shell32.IsUserAnAdmin()
        else:  # Si estamos en Linux / macOS
            return os.geteuid() == 0
    except Exception:
        return False

def require_admin():
    """
    Si no somos admin, reinicia el script pidiendo permisos.
    """
    if is_admin():
        return True

    print(f"[SYSTEM] Solicitando elevación de privilegios en {os.name.upper()}...")

    if os.name == 'nt':  # Lógica Windows (UAC)
        import ctypes
        try:
            ctypes.windll.shell32.ShellExecuteW(
                None, "runas", sys.executable, " ".join(sys.argv), None, 1
            )
        except Exception as e:
            print(f"[ERROR] Fallo UAC: {e}")
            return False
            
    else:  # Lógica Linux (Sudo)
        try:
            # 'sudo -E' mantiene las variables de entorno (importante para pip/python)
            args = ['sudo', '-E', sys.executable] + sys.argv
            os.execlpe('sudo', *args)
        except Exception as e:
            print(f"[ERROR] Fallo Sudo: {e}")
            return False

    sys.exit() # Cierra el proceso original sin permisos