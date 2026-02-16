# core/engine_ai.py
# VERSION: 2.0.0 (TrueSight Engine)
import math
import pefile
import os
import joblib
import hashlib 
import json
import zipfile
import tempfile
import re 

class AIEngine:
    def __init__(self, model_path='database/ai_model.pkl'):
        self.model = None
        self.model_path = model_path
        self._load_model()
        
        # --- NUEVO: Base de datos de Magic Numbers (Huellas digitales) ---
        self.magic_signatures = {
            b'MZ': 'Ejecutable Windows (EXE/DLL)',
            b'%PDF': 'Documento PDF',
            b'PK': 'Archivo Comprimido (ZIP/Office)',
            b'\x89PNG': 'Imagen PNG',
            b'\xFF\xD8\xFF': 'Imagen JPG',
            b'\x00\x00\x00\x18': 'Video MP4',
            b'\x00\x00\x00\x20': 'Video MP4',
            b'Rar!': 'Archivo RAR',
            b'\x7fELF': 'Ejecutable Linux (ELF)'
        }
        
        # Extensiones que descomprimiremos
        self.archive_extensions = ('.zip', '.jar', '.apk')

    def _load_model(self):
        if os.path.exists(self.model_path):
            try:
                self.model = joblib.load(self.model_path)
            except Exception:
                self.model = None

    def _calculate_hash_stream(self, file_path, block_size=65536):
        """SHA-256 para identificación precisa."""
        sha256 = hashlib.sha256()
        try:
            with open(file_path, 'rb') as f:
                for block in iter(lambda: f.read(block_size), b''):
                    sha256.update(block)
            return sha256.hexdigest()
        except Exception:
            return None

    def calculate_entropy(self, data):
        if not data: return 0
        entropy = 0
        for x in range(256):
            p_x = float(data.count(bytes([x]))) / len(data)
            if p_x > 0:
                entropy += - p_x * math.log(p_x, 2)
        return entropy

    # --- NUEVO: DETECCIÓN DE FALSIFICACIÓN DE EXTENSIÓN (Anti-Spoofing) ---
    def _check_extension_spoofing(self, file_path, header_bytes):
        """
        Verifica si la extensión coincide con la realidad.
        Detecta: 'video.mp4' que en realidad es un .exe
        """
        filename = os.path.basename(file_path).lower()
        
        # 1. Detectar ejecutables camuflados (La trampa más común)
        if header_bytes.startswith(b'MZ'): 
            # Si empieza como programa pero no termina como programa...
            if not filename.endswith(('.exe', '.dll', '.sys', '.scr')):
                return True, "ALERTA CRÍTICA: Ejecutable oculto con doble extensión o icono falso."

        # 2. Detectar Scripts en PDFs (Caso de exploits)
        if header_bytes.startswith(b'%PDF'):
            try:
                with open(file_path, 'rb') as f:
                    content = f.read(4096) # Leer primeros 4KB
                    if b'/JavaScript' in content or b'/JS' in content or b'/OpenAction' in content:
                        return True, "PDF Malicioso: Contiene scripts de ejecución automática."
            except: pass

        return False, ""

    def _scan_archive_contents(self, file_path):
        """Escaneo recursivo de ZIPs (Descomprime en memoria)."""
        try:
            with tempfile.TemporaryDirectory() as temp_dir:
                with zipfile.ZipFile(file_path, 'r') as zf:
                    for member_info in zf.infolist():
                        # Protección básica contra Zip Slip
                        if '..' in member_info.filename or member_info.filename.startswith('/'): continue
                        if member_info.is_dir(): continue
                        
                        zf.extract(member_info, temp_dir)
                        extracted_path = os.path.join(temp_dir, member_info.filename)
                        
                        # Escaneo profundo recursivo
                        is_threat, reason, score = self.scan_file(extracted_path, is_recursive=True)
                        if is_threat:
                            return True, f"Amenaza oculta en ZIP ({member_info.filename}): {reason}", score
        except zipfile.BadZipFile: pass
        except Exception: pass
        return False, "", 0

    def scan_file(self, file_path, is_recursive=False):
        """
        Motor V2.0.0: Soporte TrueSight y Anti-Spoofing.
        """
        try:
            if not os.path.exists(file_path): return False, "No encontrado", 0
            if "quarantine_vault" in file_path: return False, "", 0

            # 1. Leer cabecera (Magic Bytes)
            try:
                with open(file_path, 'rb') as f:
                    header_data = f.read(2048) # Leemos 2KB para análisis forense
            except: return False, "Error de Lectura", 0

            # 2. ANÁLISIS DE SPOOFING (Prioridad Máxima)
            is_spoofed, spoof_reason = self._check_extension_spoofing(file_path, header_data)
            if is_spoofed:
                return True, spoof_reason, 100 # ¡Bloqueo inmediato!

            # 3. Recursividad ZIP (Si es un zip, miramos dentro)
            if not is_recursive and file_path.lower().endswith(self.archive_extensions):
                is_threat, reason, score = self._scan_archive_contents(file_path)
                if is_threat: return True, reason, score

            # 4. Hash Check (SHA-256)
            file_hash = self._calculate_hash_stream(file_path)
            
            # (Aquí mantienes tu lógica de signatures.json si tienes base de datos)

            # 5. Análisis PE (Solo si es realmente un PE o estamos paranoicos)
            suspicious_apis = 0
            # Analizamos PE si tiene extensión EXE O si empieza con MZ
            if file_path.lower().endswith(('.exe', '.dll')) or header_data.startswith(b'MZ'):
                try:
                    pe = pefile.PE(file_path, fast_load=True) 
                    pe.parse_data_directories()
                    bad_apis = [b"VirtualAlloc", b"WriteProcessMemory", b"ShellExecute", b"URLDownloadToFile", b"RegOpenKey"]
                    if hasattr(pe, 'DIRECTORY_ENTRY_IMPORT'):
                        for entry in pe.DIRECTORY_ENTRY_IMPORT:
                            for imp in entry.imports:
                                if imp.name and imp.name in bad_apis: suspicious_apis += 1
                except: pass 

            # 6. Heurística Universal (Entropía)
            entropy = self.calculate_entropy(header_data)
            
            risk_score = 0
            reasons = []

            # Umbrales
            if entropy > 7.4:
                risk_score += 50
                reasons.append("Entropía Alta (Cifrado/Packer)")
            
            if suspicious_apis >= 2:
                risk_score += 50
                reasons.append(f"APIs Peligrosas ({suspicious_apis})")

            # Detectar comandos de consola peligrosos en texto plano
            file_content_lower = header_data.lower()
            if b'powershell' in file_content_lower or b'cmd.exe' in file_content_lower:
                risk_score += 40
                reasons.append("Scripts de Terminal detectados")

            if risk_score >= 50:
                final_score = min(risk_score, 100)
                return True, " | ".join(reasons), final_score
            
            return False, "Seguro", risk_score

        except Exception as e:
            return False, f"Error System: {str(e)}", 0