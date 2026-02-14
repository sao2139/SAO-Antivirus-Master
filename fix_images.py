from PIL import Image
import os

def convertir_a_bmp():
    images = [
        ("assets/banner_install.png", "assets/banner_install.bmp"),
        ("assets/logo_sao.png", "assets/logo_sao.bmp")
    ]

    print("--- INICIANDO CONVERSIÓN PARA INNO SETUP ---")

    for input_path, output_path in images:
        if os.path.exists(input_path):
            try:
                print(f"Procesando: {input_path}...")
                with Image.open(input_path) as img:
                    # Inno Setup odia la transparencia (RGBA).
                    # Convertimos a RGB (fondo sólido) para evitar errores.
                    # Si tu fondo era transparente, ahora será negro (perfecto para SAO).
                    rgb_img = img.convert("RGB")
                    rgb_img.save(output_path, "BMP")
                print(f"✅ Creado: {output_path}")
            except Exception as e:
                print(f"❌ Error en {input_path}: {e}")
        else:
            print(f"⚠️ No encuentro: {input_path}")

if __name__ == "__main__":
    convertir_a_bmp()