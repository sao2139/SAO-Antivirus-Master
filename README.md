#  SAO-Antivirus

> "Link Start into a safer system."

Un sistema de Detección y Respuesta de Endpoint (EDR) programado en Python, inspirado en la estética visual de un leon. Combina análisis heurístico (IA), criptografía de grado militar y monitoreo en tiempo real.

![SAO Antivirus Banner](assets/banner_install.png)

## 🚀 Características Principales

* **Motor Heurístico (A.I. Engine):** Detecta amenazas desconocidas basándose en entropía matemática y análisis de cabeceras PE, no solo firmas.
* **Bóveda de Cuarentena (AES-256):** Los archivos infectados no se borran; se cifran criptográficamente y se aíslan.
* **Escudo de Red (Network Guard):** Sniffer de paquetes en tiempo real (basado en Scapy) para detectar tráfico C&C.
* **Interfaz Neural (UI):** Dashboard moderno creado con `CustomTkinter` y gráficos de datos en tiempo real.
* **Honeypots:** Trampas anti-ransomware que detectan modificaciones ilegales.

## 🛠️ Instalación

1.  **Requisitos:** Python 3.10+ y privilegios de Administrador.
2.  **Instalar dependencias:**
    ```bash
    pip install -r requirements.txt
    ```
    *(Nota: En Windows, necesitarás instalar [Npcap](https://npcap.com/) para que el módulo de red funcione correctamente)*.

3.  **Primer Inicio (Setup):**
    Ejecuta el instalador gráfico para preparar el entorno:
    ```bash
    python ui/installer_ui.py
    ```

## ⚔️ Ejecución

Para iniciar el Dashboard principal:
```bash
python main.py