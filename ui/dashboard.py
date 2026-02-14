import customtkinter as ctk
import threading
import time
import os
import sys
from tkinter import filedialog
from PIL import Image

# Importar Componentes UI
from .components.graph_widget import CyberGraph
from .components.cards import StatusCard

# Importar Backend
from core.engine_ai import AIEngine
from core.net_guard import NetworkGuard
from security.quarantine import QuarantineManager

# --- CONSTANTES DE COLOR SAO ---
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

        # Configuración Ventana
        self.title("SAO-ANTIVIRUS | SYSTEM CALL: PROTECT")
        self.geometry("1100x700")
        self.configure(fg_color=COLOR_BG_DARK)

        # Inicializar Backend
        self.ai = AIEngine()
        self.quarantine = QuarantineManager()
        self.net_guard = NetworkGuard(alert_callback=self.on_network_threat)
        self.net_guard.start()

        # Layout Principal
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.setup_sidebar()
        
        # Frame contenedor para cambiar de "páginas"
        self.content_area = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.content_area.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        
        # Iniciar en Dashboard
        self.show_dashboard_page()
        
        # Iniciar bucle de refresco
        self.after(1000, self.update_system_status)

    def setup_sidebar(self):
        self.sidebar = ctk.CTkFrame(self, width=220, corner_radius=0, fg_color=COLOR_SIDEBAR)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        
        # --- LOGO (IMAGEN REAL) ---
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
        except Exception:
            pass
        
        self.ver_lbl = ctk.CTkLabel(self.sidebar, text="Guardian Ed.", font=("Consolas", 10), text_color=COLOR_GREEN)
        self.ver_lbl.grid(row=1, column=0, padx=20, pady=(0, 30))

        # --- BOTONES DE NAVEGACIÓN ---
        # Ahora conectamos los comandos a funciones reales
        self.btn_home = self.create_nav_btn("DASHBOARD", 2, command=self.show_dashboard_page, active=True)
        self.btn_scan = self.create_nav_btn("ESCANEO", 3, command=self.run_custom_scan)
        self.btn_vault = self.create_nav_btn("BÓVEDA", 4, command=self.show_vault_page)
        self.btn_settings = self.create_nav_btn("AJUSTES", 5, command=self.show_settings_page)
        
        self.sidebar.grid_rowconfigure(6, weight=1)

        self.btn_panic = ctk.CTkButton(self.sidebar, text="⚠ LOCKDOWN", 
                                       fg_color="#330000", border_color=COLOR_RED, border_width=1,
                                       hover_color="#660000", text_color=COLOR_RED,
                                       height=40, font=("Arial", 12, "bold"))
        self.btn_panic.grid(row=7, column=0, padx=20, pady=30, sticky="ew")

    def create_nav_btn(self, text, row, command=None, active=False):
        bg_color = "#222222" if active else "transparent"
        fg_color = COLOR_BLUE if active else "#888888"
        border_col = COLOR_BLUE if active else COLOR_SIDEBAR # Corrección del borde transparente
        
        btn = ctk.CTkButton(self.sidebar, text=text, 
                            fg_color=bg_color, 
                            text_color=fg_color,
                            border_width=1 if active else 0,
                            border_color=border_col,
                            hover_color="#222222",
                            anchor="w", height=45, 
                            font=("Roboto", 12, "bold" if active else "normal"),
                            command=command)
        btn.grid(row=row, column=0, padx=10, pady=5, sticky="ew")
        return btn

    def clear_content_area(self):
        """Borra lo que haya en el centro para mostrar otra pantalla"""
        for widget in self.content_area.winfo_children():
            widget.destroy()

    # --- PÁGINA 1: DASHBOARD ---
    def show_dashboard_page(self):
        self.clear_content_area()
        
        # Tarjetas Superiores
        cards_frame = ctk.CTkFrame(self.content_area, fg_color="transparent")
        cards_frame.pack(fill="x", pady=(0, 25))
        
        self.card_health = StatusCard(cards_frame, "Integridad", "🔰", COLOR_GREEN)
        self.card_health.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        self.card_threats = StatusCard(cards_frame, "Amenazas", "☣️", COLOR_RED)
        self.card_threats.pack(side="left", fill="x", expand=True, padx=10)
        
        self.card_files = StatusCard(cards_frame, "Bóveda", "⛓️", COLOR_BLUE)
        self.card_files.pack(side="left", fill="x", expand=True, padx=(10, 0))

        # Gráfico
        self.net_graph = CyberGraph(self.content_area)
        self.net_graph.pack(fill="x", pady=10, ipady=30)

        # Log
        ctk.CTkLabel(self.content_area, text="REGISTRO DE SISTEMA", anchor="w", 
                     font=("Consolas", 12, "bold"), text_color="#666").pack(fill="x", pady=(20, 5))
        
        self.log_box = ctk.CTkTextbox(self.content_area, height=150, 
                                      fg_color="#0f0f0f", text_color=COLOR_TEXT_LOG,
                                      font=("Consolas", 11))
        self.log_box.pack(fill="both", expand=True)
        self.log_message(">> LINK START! Sistema en línea.")

    # --- PÁGINA 2: BÓVEDA (Cuarentena) ---
    def show_vault_page(self):
        self.clear_content_area()
        
        title = ctk.CTkLabel(self.content_area, text="BÓVEDA DE CUARENTENA (AES-256)", 
                             font=("Impact", 24), text_color=COLOR_BLUE, anchor="w")
        title.pack(fill="x", pady=20)

        # Lista de archivos
        files = self.quarantine.list_quarantined_files()
        
        scroll_frame = ctk.CTkScrollableFrame(self.content_area, fg_color="#111")
        scroll_frame.pack(fill="both", expand=True)

        if not files:
            ctk.CTkLabel(scroll_frame, text="No hay amenazas contenidas actualmente.", 
                         text_color="#666").pack(pady=50)
        else:
            for file_id, meta in files.items():
                row = ctk.CTkFrame(scroll_frame, fg_color="#222")
                row.pack(fill="x", pady=5, padx=5)
                
                info = f"☣ {meta['original_name']} | {meta['threat_name']} | {meta['timestamp']}"
                ctk.CTkLabel(row, text=info, font=("Consolas", 12), anchor="w").pack(side="left", padx=10, pady=10)
                
                # Botón "Eliminar" (Solo visual por ahora)
                ctk.CTkButton(row, text="PURGAR", width=80, fg_color="#550000", hover_color="#880000").pack(side="right", padx=10)

    # --- PÁGINA 3: AJUSTES ---
    def show_settings_page(self):
        self.clear_content_area()
        
        title = ctk.CTkLabel(self.content_area, text="CONFIGURACIÓN DEL SISTEMA", 
                             font=("Impact", 24), text_color=COLOR_GREEN, anchor="w")
        title.pack(fill="x", pady=20)

        opts = [
            ("Protección en Tiempo Real", True),
            ("Escaneo Heurístico (IA)", True),
            ("Monitor de Red (NetGuard)", True),
            ("Protección USB", False),
            ("Modo Silencioso (Gaming)", False)
        ]

        for text, val in opts:
            switch = ctk.CTkSwitch(self.content_area, text=text, progress_color=COLOR_GREEN)
            if val: switch.select()
            switch.pack(anchor="w", pady=10, padx=20)

    # --- LÓGICA DE FONDO ---

    def log_message(self, msg):
        try:
            timestamp = time.strftime('%H:%M:%S')
            self.log_box.insert("end", f"[{timestamp}] {msg}\n")
            self.log_box.see("end")
        except: pass

    def update_system_status(self):
        # Solo actualizamos si estamos en la página del Dashboard (si existe card_health)
        if hasattr(self, 'card_health') and self.card_health.winfo_exists():
            self.card_health.set_value("100%", COLOR_GREEN)
            
            count = len(self.quarantine.list_quarantined_files())
            self.card_files.set_value(f"{count} Archivos", COLOR_BLUE)
            
            # Velocidad de red real
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
            # Solo logueamos si estamos en el dashboard
            if hasattr(self, 'log_box'):
                self.log_message(f"Escaneando: {filename}...")
            
            def thread_scan():
                is_threat, reason, score = self.ai.scan_file(filepath)
                if is_threat:
                    self.quarantine.isolate_file(filepath, reason)
                # (Aquí podrías poner un popup de resultado)
            
            threading.Thread(target=thread_scan).start()

    def on_close(self):
        self.net_guard.stop()
        self.destroy()
        sys.exit()

if __name__ == "__main__":
    app = MainDashboard()
    app.protocol("WM_DELETE_WINDOW", app.on_close)
    app.mainloop()