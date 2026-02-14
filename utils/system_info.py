import psutil
import platform

class SystemMonitor:
    @staticmethod
    def get_system_stats():
        """Devuelve uso de CPU y RAM en porcentaje."""
        try:
            cpu_usage = psutil.cpu_percent(interval=0.1)
            ram = psutil.virtual_memory()
            return {
                "cpu": cpu_usage,
                "ram_percent": ram.percent,
                "ram_used_gb": round(ram.used / (1024**3), 2),
                "ram_total_gb": round(ram.total / (1024**3), 2)
            }
        except Exception:
            return {"cpu": 0, "ram_percent": 0}

    @staticmethod
    def get_os_info():
        return f"{platform.system()} {platform.release()}"