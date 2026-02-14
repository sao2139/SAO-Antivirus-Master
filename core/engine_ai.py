import math
import pefile
import os
import joblib
import numpy as np
from sklearn.ensemble import RandomForestClassifier
import hashlib 
import json

class AIEngine:
    def __init__(self, model_path='database/ai_model.pkl'):
        self.model = None
        self.model_path = model_path
        self._load_model()

    def _load_model(self):
        """Carga el modelo de IA si existe, si no, inicia modo heurístico puro."""
        if os.path.exists(self.model_path):
            try:
                self.model = joblib.load(self.model_path)
            except Exception:
                self.model = None

    def calculate_entropy(self, data):
        """
        Calcula la Entropía de Shannon.
        Rango: 0 (todo igual) a 8 (aleatoriedad total).
        Malware/Ransomware suele tener entropía > 7.0.
        """
        if not data:
            return 0
        entropy = 0
        for x in range(256):
            p_x = float(data.count(bytes([x]))) / len(data)
            if p_x > 0:
                entropy += - p_x * math.log(p_x, 2)
        return entropy

    def scan_file(self, file_path):
        """
        Analiza un archivo en busca de amenazas.
        Retorna: (is_threat: bool, reason: str, score: int)
        """
        try:
            if not os.path.exists(file_path):
                return False, "Archivo no encontrado", 0

            with open(file_path, 'rb') as f:
                data = f.read()

                file_hash = hashlib.md5(data).hexdigest()

                db_path = os.path.join("database", "signatures.json")
            if os.path.exists(db_path):
                with open(db_path, 'r') as db_file:
                    signatures = json.load(db_file)
                    if file_hash in signatures:
                        return True, f"FIRMA CONOCIDA: {signatures[file_hash]}", 100

            # 1. Análisis de Entropía (Detección de Ransomware/Packers)
            entropy = self.calculate_entropy(data)
            
            # 2. Análisis de Estructura PE (Solo Windows .exe/.dll)
            suspicious_apis = 0
            is_pe = False
            try:
                pe = pefile.PE(file_path)
                is_pe = True
                # Buscar APIs usadas para inyección de código
                bad_apis = [b"VirtualAlloc", b"WriteProcessMemory", b"CreateRemoteThread", b"ShellExecute"]
                for entry in pe.DIRECTORY_ENTRY_IMPORT:
                    for imp in entry.imports:
                        if imp.name in bad_apis:
                            suspicious_apis += 1
            except:
                pass # No es un PE válido

            # --- DECISIÓN HEURÍSTICA ---
            risk_score = 0
            reasons = []

            if entropy > 7.2:
                risk_score += 60
                reasons.append("Alta Entropía (Posible Ransomware)")
            elif entropy > 6.5:
                risk_score += 30
            
            if suspicious_apis >= 2:
                risk_score += 40
                reasons.append(f"APIs Peligrosas ({suspicious_apis})")

            # Si tenemos modelo de IA entrenado, lo usamos para desempatar
            if self.model and is_pe:
                # Aquí iría la extracción de features vectorial para el modelo
                pass 

            if risk_score >= 60:
                return True, " | ".join(reasons), risk_score
            
            return False, "Seguro", risk_score

        except Exception as e:
            return False, f"Error de escaneo: {str(e)}", 0