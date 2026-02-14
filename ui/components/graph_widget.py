import customtkinter as ctk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np

# COLORES SAO
COLOR_BG_CARD = "#2b2b2b"      # Fondo del contenedor
COLOR_PLOT_BG = "#1a1a1a"      # Fondo del gráfico
COLOR_LINE = "#0099ff"         # Azul Cyber (Data Stream)
COLOR_GRID = "#333333"

class CyberGraph(ctk.CTkFrame):
    def __init__(self, master, title="FLUJO DE DATOS (RED)", **kwargs):
        super().__init__(master, fg_color=COLOR_BG_CARD, corner_radius=10, **kwargs)
        
        # Título del Gráfico
        self.label = ctk.CTkLabel(self, text=title, font=("Consolas", 12, "bold"), text_color=COLOR_LINE)
        self.label.pack(pady=(10, 0), anchor="w", padx=15)

        # Configuración de Matplotlib (Estilo Oscuro SAO)
        plt.style.use('dark_background')
        self.fig, self.ax = plt.subplots(figsize=(5, 2), dpi=100)
        self.fig.patch.set_facecolor(COLOR_BG_CARD) 
        self.ax.set_facecolor(COLOR_PLOT_BG)       
        
        # Estilizar Ejes (Minimalista)
        self.ax.spines['top'].set_visible(False)
        self.ax.spines['right'].set_visible(False)
        self.ax.spines['left'].set_color('#444')
        self.ax.spines['bottom'].set_color('#444')
        self.ax.tick_params(axis='x', colors='#888', labelsize=8)
        self.ax.tick_params(axis='y', colors='#888', labelsize=8)
        self.ax.grid(True, color=COLOR_GRID, linestyle=':', linewidth=0.5)

        # Datos Iniciales
        self.x_data = np.arange(0, 60, 1)
        self.y_data = np.zeros(60)
        
        # Línea de Datos (Efecto Brillante)
        self.line, = self.ax.plot(self.x_data, self.y_data, color=COLOR_LINE, linewidth=1.5)
        # Relleno con transparencia
        self.fill = self.ax.fill_between(self.x_data, 0, self.y_data, color=COLOR_LINE, alpha=0.15)

        # Canvas
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)

    def update_graph(self, new_value):
        # Desplazar datos
        self.y_data = np.roll(self.y_data, -1)
        self.y_data[-1] = new_value

        # Actualizar línea
        self.line.set_ydata(self.y_data)
        
        # Actualizar relleno (optimización simple)
        try:
            self.fill.remove()
        except: pass
        self.fill = self.ax.fill_between(self.x_data, 0, self.y_data, color=COLOR_LINE, alpha=0.15)

        # Escala dinámica
        max_val = np.max(self.y_data)
        if max_val > self.ax.get_ylim()[1] - 10:
            self.ax.set_ylim(0, max_val * 1.5)
        elif max_val < 50 and self.ax.get_ylim()[1] > 100:
             self.ax.set_ylim(0, 100)
        
        self.canvas.draw_idle()