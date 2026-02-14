# utils/i18n.py
import json
import os

class LanguagePack:
    def __init__(self, lang_code="es"):
        self.lang_code = lang_code
        self.translations = {
            "es": {
                "app_title": "SAO-ANTIVIRUS | SYSTEM CALL: PROTECT",
                "nav_dashboard": "DASHBOARD",
                "nav_scan": "ESCANEO",
                "nav_vault": "BÓVEDA",
                "nav_settings": "AJUSTES",
                "nav_lockdown": "⚠ LOCKDOWN",
                "card_integrity": "Integridad",
                "card_threats": "Amenazas",
                "card_vault": "Bóveda",
                "log_title": "REGISTRO DE SISTEMA",
                "log_start": ">> LINK START! Sistema en línea.",
                "vault_title": "BÓVEDA DE CUARENTENA (AES-256)",
                "vault_empty": "No hay amenazas contenidas actualmente.",
                "btn_purge": "PURGAR",
                "settings_title": "CONFIGURACIÓN DEL SISTEMA",
                "opt_realtime": "Protección en Tiempo Real",
                "opt_ai": "Escaneo Heurístico (IA)",
                "opt_netguard": "Monitor de Red (NetGuard)",
                "opt_usb": "Protección USB",
                "opt_silent": "Modo Silencioso (Gaming)",
                "update_btn": "⬇ ACTUALIZAR AHORA",
                "update_msg": "Nueva versión disponible"
            },
            "en": {
                "app_title": "SAO-ANTIVIRUS | SYSTEM CALL: PROTECT",
                "nav_dashboard": "DASHBOARD",
                "nav_scan": "SCAN",
                "nav_vault": "VAULT",
                "nav_settings": "SETTINGS",
                "nav_lockdown": "⚠ LOCKDOWN",
                "card_integrity": "Integrity",
                "card_threats": "Threats",
                "card_vault": "Vault",
                "log_title": "SYSTEM LOG",
                "log_start": ">> LINK START! System Online.",
                "vault_title": "QUARANTINE VAULT (AES-256)",
                "vault_empty": "No threats currently contained.",
                "btn_purge": "PURGE",
                "settings_title": "SYSTEM CONFIGURATION",
                "opt_realtime": "Real-Time Protection",
                "opt_ai": "Heuristic Scan (AI)",
                "opt_netguard": "Network Monitor (NetGuard)",
                "opt_usb": "USB Protection",
                "opt_silent": "Silent Mode (Gaming)",
                "update_btn": "⬇ UPDATE NOW",
                "update_msg": "New version available"
            },
            "fr": {
                "app_title": "SAO-ANTIVIRUS | SYSTEM CALL: PROTECT",
                "nav_dashboard": "TABLEAU DE BORD",
                "nav_scan": "SCANNER",
                "nav_vault": "COFFRE-FORT",
                "nav_settings": "PARAMÈTRES",
                "nav_lockdown": "⚠ VERROUILLAGE",
                "card_integrity": "Intégrité",
                "card_threats": "Menaces",
                "card_vault": "Coffre",
                "log_title": "JOURNAL SYSTÈME",
                "log_start": ">> LINK START! Système en ligne.",
                "vault_title": "COFFRE DE QUARANTAINE (AES-256)",
                "vault_empty": "Aucune menace contenue actuellement.",
                "btn_purge": "PURGER",
                "settings_title": "CONFIGURATION SYSTÈME",
                "opt_realtime": "Protection en Temps Réel",
                "opt_ai": "Scan Heuristique (IA)",
                "opt_netguard": "Moniteur Réseau (NetGuard)",
                "opt_usb": "Protection USB",
                "opt_silent": "Mode Silencieux (Jeu)",
                "update_btn": "⬇ METTRE À JOUR",
                "update_msg": "Nouvelle version disponible"
            }
        }

    def get(self, key):
        """Devuelve el texto traducido o el key si no existe"""
        return self.translations.get(self.lang_code, self.translations["es"]).get(key, key)