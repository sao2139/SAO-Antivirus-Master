import psutil

class ProcessTerminator:
    @staticmethod
    def kill_process_by_pid(pid):
        try:
            p = psutil.Process(pid)
            p.terminate()
            return True, f"Proceso {pid} terminado."
        except psutil.NoSuchProcess:
            return False, "El proceso ya no existe."
        except psutil.AccessDenied:
            return False, "Acceso denegado (Requiere Admin)."

    @staticmethod
    def kill_process_by_name(name):
        killed_count = 0
        for proc in psutil.process_iter(['pid', 'name']):
            if proc.info['name'] == name:
                try:
                    proc.terminate()
                    killed_count += 1
                except:
                    pass
        return killed_count