import customtkinter as ctk
import threading
import time
import os
import sys
import json
from tkinter import filedialog
from PIL import Image

# Importar Componentes UI
from .components.graph_widget import CyberGraph
from .components.cards import StatusCard

# Importar Backend
from core.engine_ai import AIEngine
from core.net_guard import NetworkGuard
from security.quarantine import QuarantineManager
from core.updater import SAOUpdater

# NUEVO: Importar sistema de idiomas
from utils.i18n import LanguagePack

# ... (CONSTANTES DE COLOR IGUAL QUE ANTES) ...
COLOR_BG_DARK = "#1a1a1a"
COLOR_SIDEBAR = "#111111"
COLOR_BLUE = "#0099ff"
COLOR_GREEN = "#00ff99"
COLOR_RED = "#ff3333"
COLOR_TEXT_LOG = "#00ffcc"

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("dark-blue")

class MainDashboard(ctk.CTk):
    def __init__(self):
        super().__init__()

        # 1. Cargar Configuración e Idioma
        self.local_version = "1.0.0"
        self.current_lang_code = "es" # Default
        try:
            with open('config.json', 'r') as f:
                config = json.load(f)
                self.local_version = config.get("version", "1.0.0").split(" ")[0]
                self.current_lang_code = config.get("language", "es")
        except Exception:
            pass

        # 2. Inicializar Pack de Idioma
        self.lang = LanguagePack(self.current_lang_code)

        # Configuración Ventana
        self.title(self.lang.get("app_title")) # Título traducido
        self.geometry("1100x700")
        self.configure(fg_color=COLOR_BG_DARK)

        # Inicializar Backend
        self.ai = AIEngine()
        self.quarantine = QuarantineManager()
        self.net_guard = NetworkGuard(alert_callback=self.on_network_threat)
        self.net_guard.start()
        
        # Updater logic
        self.repo_json_url = "https://raw.githubusercontent.com/sao2139/SAO-Antivirus-Master/refs/heads/main/version.json"
        threading.Thread(target=self.run_update_check, daemon=True).start()

        # Layout Principal
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.setup_sidebar()
        self.content_area = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.content_area.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        
        self.show_dashboard_page()
        self.after(1000, self.update_system_status)

    def setup_sidebar(self):
        self.sidebar = ctk.CTkFrame(self, width=220, corner_radius=0, fg_color=COLOR_SIDEBAR)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        
        # Logo (Igual que antes)
        try:
            logo_path = os.path.join("assets", "logo_sao.png")
            if os.path.exists(logo_path):
                pil_img = Image.open(logo_path)
                img = ctk.CTkImage(light_image=pil_img, dark_image=pil_img, size=(120, 120))
                self.logo_lbl = ctk.CTkLabel(self.sidebar, image=img, text="")
                self.logo_lbl.grid(row=0, column=0, padx=20, pady=(30, 10))
            else:
                self.logo_lbl = ctk.CTkLabel(self.sidebar, text="SAO-AV", font=("Impact", 30), text_color=COLOR_BLUE)
                self.logo_lbl.grid(row=0, column=0, padx=20, pady=(40, 10))
        except Exception: pass
        
        self.ver_lbl = ctk.CTkLabel(self.sidebar, text=f"v{self.local_version} Guardian", font=("Consolas", 10), text_color=COLOR_GREEN)
        self.ver_lbl.grid(row=1, column=0, padx=20, pady=(0, 30))

        # --- BOTONES TRADUCIDOS ---
        self.btn_home = self.create_nav_btn(self.lang.get("nav_dashboard"), 2, command=self.show_dashboard_page, active=True)
        self.btn_scan = self.create_nav_btn(self.lang.get("nav_scan"), 3, command=self.run_custom_scan)
        self.btn_vault = self.create_nav_btn(self.lang.get("nav_vault"), 4, command=self.show_vault_page)
        self.btn_settings = self.create_nav_btn(self.lang.get("nav_settings"), 5, command=self.show_settings_page)
        
        self.sidebar.grid_rowconfigure(6, weight=1)

        self.btn_panic = ctk.CTkButton(self.sidebar, text=self.lang.get("nav_lockdown"), 
                                       fg_color="#330000", border_color=COLOR_RED, border_width=1,
                                       hover_color="#660000", text_color=COLOR_RED,
                                       height=40, font=("Arial", 12, "bold"))
        self.btn_panic.grid(row=7, column=0, padx=20, pady=30, sticky="ew")

    # ... (run_update_check y create_nav_btn IGUAL que antes) ...
    # Asegúrate de usar self.lang.get("update_btn") en show_update_notification si quieres traducir eso también.

    def run_update_check(self):
        updater = SAOUpdater(self.local_version, self.repo_json_url)
        has_update, msg = updater.check_for_updates()
        if has_update:
            self.after(0, lambda: self.show_update_notification(updater, msg))

    def show_update_notification(self, updater, msg):
        self.log_message(f"SYSTEM: {msg}")
        self.btn_update = ctk.CTkButton(self.sidebar, text=self.lang.get("update_btn"), 
                                 fg_color=COLOR_GREEN, text_color="black",
                                 hover_color="#00cc77",
                                 font=("Arial", 11, "bold"),
                                 command=lambda: self.start_update_process(updater))
        self.btn_update.grid(row=6, column=0, padx=20, pady=10, sticky="ew")

    def start_update_process(self, updater):
        self.btn_update.configure(state="disabled", text="...")
        threading.Thread(target=updater.download_and_install, daemon=True).start()

    def create_nav_btn(self, text, row, command=None, active=False):
        # ... (CÓDIGO ORIGINAL SIN CAMBIOS) ...
        bg_color = "#222222" if active else "transparent"
        fg_color = COLOR_BLUE if active else "#888888"
        border_col = COLOR_BLUE if active else COLOR_SIDEBAR 
        btn = ctk.CTkButton(self.sidebar, text=text, fg_color=bg_color, text_color=fg_color,
                            border_width=1 if active else 0, border_color=border_col, hover_color="#222222",
                            anchor="w", height=45, font=("Roboto", 12, "bold" if active else "normal"), command=command)
        btn.grid(row=row, column=0, padx=10, pady=5, sticky="ew")
        return btn

    def clear_content_area(self):
        for widget in self.content_area.winfo_children():
            widget.destroy()

    # --- PÁGINA 1: DASHBOARD ---
    def show_dashboard_page(self):
        self.clear_content_area()
        
        cards_frame = ctk.CTkFrame(self.content_area, fg_color="transparent")
        cards_frame.pack(fill="x", pady=(0, 25))
        
        # Textos traducidos para las tarjetas
        self.card_health = StatusCard(cards_frame, self.lang.get("card_integrity"), "🔰", COLOR_GREEN)
        self.card_health.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        self.card_threats = StatusCard(cards_frame, self.lang.get("card_threats"), "☣️", COLOR_RED)
        self.card_threats.pack(side="left", fill="x", expand=True, padx=10)
        
        self.card_files = StatusCard(cards_frame, self.lang.get("card_vault"), "⛓️", COLOR_BLUE)
        self.card_files.pack(side="left", fill="x", expand=True, padx=(10, 0))

        self.net_graph = CyberGraph(self.content_area)
        self.net_graph.pack(fill="x", pady=10, ipady=30)

        ctk.CTkLabel(self.content_area, text=self.lang.get("log_title"), anchor="w", 
                     font=("Consolas", 12, "bold"), text_color="#666").pack(fill="x", pady=(20, 5))
        
        self.log_box = ctk.CTkTextbox(self.content_area, height=150, 
                                      fg_color="#0f0f0f", text_color=COLOR_TEXT_LOG,
                                      font=("Consolas", 11))
        self.log_box.pack(fill="both", expand=True)
        self.log_message(self.lang.get("log_start"))

    # --- PÁGINA 2: BÓVEDA ---
    def show_vault_page(self):
        self.clear_content_area()
        
        title = ctk.CTkLabel(self.content_area, text=self.lang.get("vault_title"), 
                             font=("Impact", 24), text_color=COLOR_BLUE, anchor="w")
        title.pack(fill="x", pady=20)

        files = self.quarantine.list_quarantined_files()
        scroll_frame = ctk.CTkScrollableFrame(self.content_area, fg_color="#111")
        scroll_frame.pack(fill="both", expand=True)

        if not files:
            ctk.CTkLabel(scroll_frame, text=self.lang.get("vault_empty"), 
                         text_color="#666").pack(pady=50)
        else:
            for file_id, meta in files.items():
                row = ctk.CTkFrame(scroll_frame, fg_color="#222")
                row.pack(fill="x", pady=5, padx=5)
                info = f"☣ {meta['original_name']} | {meta['threat_name']} | {meta['timestamp']}"
                ctk.CTkLabel(row, text=info, font=("Consolas", 12), anchor="w").pack(side="left", padx=10, pady=10)
                ctk.CTkButton(row, text=self.lang.get("btn_purge"), width=80, fg_color="#550000", hover_color="#880000").pack(side="right", padx=10)

    # --- PÁGINA 3: AJUSTES ---
    def show_settings_page(self):
        self.clear_content_area()
        
        title = ctk.CTkLabel(self.content_area, text=self.lang.get("settings_title"), 
                             font=("Impact", 24), text_color=COLOR_GREEN, anchor="w")
        title.pack(fill="x", pady=20)

        opts = [
            (self.lang.get("opt_realtime"), True),
            (self.lang.get("opt_ai"), True),
            (self.lang.get("opt_netguard"), True),
            (self.lang.get("opt_usb"), False),
            (self.lang.get("opt_silent"), False)
        ]

        for text, val in opts:
            switch = ctk.CTkSwitch(self.content_area, text=text, progress_color=COLOR_GREEN)
            if val: switch.select()
            switch.pack(anchor="w", pady=10, padx=20)

    # ... (Resto del código: log_message, update_system_status, on_close, etc. IGUAL) ...
    def log_message(self, msg):
        try:
            timestamp = time.strftime('%H:%M:%S')
            self.log_box.insert("end", f"[{timestamp}] {msg}\n")
            self.log_box.see("end")
        except: pass

    def update_system_status(self):
        if hasattr(self, 'card_health') and self.card_health.winfo_exists():
            self.card_health.set_value("100%", COLOR_GREEN)
            count = len(self.quarantine.list_quarantined_files())
            self.card_files.set_value(f"{count}", COLOR_BLUE) # Simplifiqué para no concatenar texto hardcoded
            try:
                real_speed = self.net_guard.get_current_traffic()
                self.net_graph.update_graph(real_speed)
            except: pass
        self.after(1000, self.update_system_status)

    def on_network_threat(self, source, msg):
        if hasattr(self, 'log_box'):
            self.log_message(f"ALERTA {source}: {msg}")

    def run_custom_scan(self):
        filepath = filedialog.askopenfilename()
        if filepath:
            filename = os.path.basename(filepath)
            if hasattr(self, 'log_box'):
                self.log_message(f"SCAN: {filename}...")
            def thread_scan():
                is_threat, reason, score = self.ai.scan_file(filepath)
                if is_threat:
                    self.quarantine.isolate_file(filepath, reason)
            threading.Thread(target=thread_scan).start()

    def on_close(self):
        self.net_guard.stop()
        self.destroy()
        sys.exit()

if __name__ == "__main__":
    app = MainDashboard()
    app.protocol("WM_DELETE_WINDOW", app.on_close)
    app.mainloop()