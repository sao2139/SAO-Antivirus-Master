import threading
import time
import psutil
import socket

class NetworkGuard:
    def __init__(self, alert_callback=None):
        self.alert_callback = alert_callback
        self.running = False
        self.monitor_thread = None
        
        # Puertos conocidos de troyanos/malware
        self.suspicious_ports = [4444, 6667, 1337, 31337, 8080]
        
        # Cache para no alertar la misma conexión mil veces
        self.alerted_connections = set()
        
        # Para medir velocidad real
        self.last_bytes_sent = 0
        self.last_bytes_recv = 0
        self.current_speed = 0 # Bytes por segundo

    def start(self):
        self.running = True
        # Inicializar contadores
        io = psutil.net_io_counters()
        self.last_bytes_sent = io.bytes_sent
        self.last_bytes_recv = io.bytes_recv
        
        print("[NET_GUARD] Iniciando Monitor de Sockets Nativo (Real)...")
        self.monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self.monitor_thread.start()

    def stop(self):
        self.running = False

    def get_current_traffic(self):
        """Devuelve la velocidad actual de la red en KB/s (Real)"""
        return self.current_speed / 1024

    def _monitor_loop(self):
        while self.running:
            try:
                # 1. MEDICIÓN DE VELOCIDAD REAL
                io = psutil.net_io_counters()
                bytes_sent = io.bytes_sent
                bytes_recv = io.bytes_recv
                
                # Calcular delta (lo que pasó en el último segundo)
                sent_per_sec = bytes_sent - self.last_bytes_sent
                recv_per_sec = bytes_recv - self.last_bytes_recv
                
                self.current_speed = sent_per_sec + recv_per_sec
                
                # Actualizar referencias
                self.last_bytes_sent = bytes_sent
                self.last_bytes_recv = bytes_recv

                # 2. DETECCIÓN DE CONEXIONES MALICIOSAS
                # Obtiene todas las conexiones de red del sistema
                connections = psutil.net_connections(kind='inet')
                
                for conn in connections:
                    # Solo nos interesan conexiones establecidas o escuchando
                    if conn.status == 'ESTABLISHED' and conn.raddr:
                        remote_ip = conn.raddr.ip
                        remote_port = conn.raddr.port
                        
                        # Identificador único para no repetir alertas
                        conn_id = f"{remote_ip}:{remote_port}"
                        
                        if conn_id in self.alerted_connections:
                            continue

                        # Lógica de detección: Puertos sospechosos
                        if remote_port in self.suspicious_ports:
                            self._trigger_alert(f"Conexión sospechosa detectada: {remote_ip}:{remote_port}")
                            self.alerted_connections.add(conn_id)

                        # Aquí podrías agregar listas negras de IPs reales si tuvieras una API

            except Exception as e:
                print(f"[NET_GUARD ERROR] {e}")

            time.sleep(1) # Escanear cada segundo

    def _trigger_alert(self, msg):
        if self.alert_callback:
            self.alert_callback("RED", msg)