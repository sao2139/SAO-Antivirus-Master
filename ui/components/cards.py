import customtkinter as ctk

class StatusCard(ctk.CTkFrame):
    def __init__(self, master, title, icon_char="🛡️", main_color="#00ff99", **kwargs):
        super().__init__(master, fg_color="#2b2b2b", corner_radius=10, 
                         border_width=1, border_color="#333", **kwargs)
        self.main_color = main_color

        # Header
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.pack(fill="x", padx=15, pady=(15, 5))
        
        # Icono
        self.icon_lbl = ctk.CTkLabel(self.header_frame, text=icon_char, font=("Arial", 22))
        self.icon_lbl.pack(side="left")
        
        # Título
        self.title_lbl = ctk.CTkLabel(self.header_frame, text=title.upper(), 
                                      font=("Roboto Medium", 11), text_color="#aaaaaa")
        self.title_lbl.pack(side="left", padx=10)

        # Valor Principal
        self.value_lbl = ctk.CTkLabel(self, text="...", font=("Roboto", 26, "bold"), text_color="white")
        self.value_lbl.pack(anchor="w", padx=15, pady=(0, 10))

        # Barra decorativa inferior (Neon)
        self.bar = ctk.CTkProgressBar(self, height=3, progress_color=main_color, fg_color="#1a1a1a")
        self.bar.set(1) # Lleno por defecto
        self.bar.pack(fill="x", side="bottom")

    def set_value(self, value, color=None):
        self.value_lbl.configure(text=str(value))
        if color:
            self.value_lbl.configure(text_color=color)
            self.bar.configure(progress_color=color)