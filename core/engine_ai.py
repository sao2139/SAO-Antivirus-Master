# core/engine_ai.py
import math
import pefile
import os
import joblib
import hashlib 
import json
# Eliminamos sklearn por ahora si no lo tienes instalado para evitar conflictos
# from sklearn.ensemble import RandomForestClassifier 

class AIEngine:  # <--- ESTA LÍNEA DEBE ESTAR AL INICIO (SIN ESPACIOS)
    def __init__(self, model_path='database/ai_model.pkl'):
        self.model = None
        self.model_path = model_path
        self._load_model()

    def _load_model(self):
        """Carga el modelo de IA si existe."""
        if os.path.exists(self.model_path):
            try:
                self.model = joblib.load(self.model_path)
            except Exception:
                self.model = None

    def _calculate_hash_stream(self, file_path, block_size=65536):
        """Calcula hash leyendo por bloques (fix memoria)"""
        md5 = hashlib.md5()
        try:
            with open(file_path, 'rb') as f:
                for block in iter(lambda: f.read(block_size), b''):
                    md5.update(block)
            return md5.hexdigest()
        except Exception:
            return None

    def calculate_entropy(self, data):
        if not data:
            return 0
        entropy = 0
        for x in range(256):
            p_x = float(data.count(bytes([x]))) / len(data)
            if p_x > 0:
                entropy += - p_x * math.log(p_x, 2)
        return entropy

    def scan_file(self, file_path):
        try:
            if not os.path.exists(file_path):
                return False, "Archivo no encontrado", 0

            # 1. Hash Check
            file_hash = self._calculate_hash_stream(file_path)
            db_path = os.path.join("database", "signatures.json")
            
            if os.path.exists(db_path) and file_hash:
                try:
                    with open(db_path, 'r') as db_file:
                        signatures = json.load(db_file)
                        if file_hash in signatures:
                            return True, f"FIRMA CONOCIDA: {signatures[file_hash]}", 100
                except: pass

            # 2. Heurística (Solo lee 1MB)
            try:
                with open(file_path, 'rb') as f:
                    header_data = f.read(1024 * 1024)
            except:
                return False, "Error de lectura", 0

            entropy = self.calculate_entropy(header_data)
            
            # 3. PE Scan
            suspicious_apis = 0
            if file_path.lower().endswith(('.exe', '.dll', '.sys')):
                try:
                    pe = pefile.PE(file_path, fast_load=True)
                    pe.parse_data_directories()
                    bad_apis = [b"VirtualAlloc", b"WriteProcessMemory", b"CreateRemoteThread", b"ShellExecute"]
                    if hasattr(pe, 'DIRECTORY_ENTRY_IMPORT'):
                        for entry in pe.DIRECTORY_ENTRY_IMPORT:
                            for imp in entry.imports:
                                if imp.name and imp.name in bad_apis:
                                    suspicious_apis += 1
                except: pass 

            # Decisión
            risk_score = 0
            reasons = []
            if entropy > 7.2:
                risk_score += 60
                reasons.append("Alta Entropía")
            if suspicious_apis >= 2:
                risk_score += 40
                reasons.append(f"APIs Peligrosas ({suspicious_apis})")

            if risk_score >= 60:
                return True, " | ".join(reasons), risk_score
            
            return False, "Seguro", risk_score

        except Exception as e:
            print(f"Error scan: {e}")
            return False, str(e), 0