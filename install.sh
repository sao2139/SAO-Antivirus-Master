#!/bin/bash

# --- SAO ANTIVIRUS INSTALLER v1.0.2 (LINUX) ---
# Colores para la terminal
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

INSTALL_DIR="/opt/sao-av"
BIN_PATH="/usr/bin/sao-av"

echo -e "${BLUE}
╔══════════════════════════════════════════════╗
║      SAO-ANTIVIRUS | GUARDIAN EDITION        ║
║         Instalador Linux v1.0.2              ║
╚══════════════════════════════════════════════╝
${NC}"

# 1. Verificar si es Root (Sudo)
if [ "$EUID" -ne 0 ]; then
  echo -e "${RED}[ERROR] Por favor, ejecuta como root: sudo ./install.sh${NC}"
  exit 1
fi

# 2. Instalar dependencias del sistema
echo -e "${BLUE}[1/5] Instalando librerías del sistema...${NC}"
apt-get update -qq
# Instalamos python3-tk para la interfaz gráfica y pip
apt-get install -y python3-tk python3-pip python3-venv

# 3. Crear directorio de instalación profesional (/opt/sao-av)
echo -e "${BLUE}[2/5] Copiando archivos a ${INSTALL_DIR}...${NC}"
if [ -d "$INSTALL_DIR" ]; then
    echo "   ...Limpiando instalación anterior..."
    rm -rf "$INSTALL_DIR"
fi
mkdir -p "$INSTALL_DIR"
cp -r . "$INSTALL_DIR"

# 4. Instalar dependencias de Python (Entorno Virtual opcional, aquí directo al sistema para simplicidad)
echo -e "${BLUE}[3/5] Instalando requerimientos de Python...${NC}"
pip3 install -r "$INSTALL_DIR/requirements.txt" --break-system-packages

# 5. Configurar permisos
echo -e "${BLUE}[4/5] Ajustando permisos de seguridad...${NC}"
chmod +x "$INSTALL_DIR/main.py"
# Aseguramos que la base de datos y logs sean escribibles
chmod -R 777 "$INSTALL_DIR/database"
chmod -R 777 "$INSTALL_DIR/quarantine_vault"
chmod -R 777 "$INSTALL_DIR/logs" 2>/dev/null || true

# 6. Crear el comando global 'sao-av'
echo -e "${BLUE}[5/5] Creando acceso directo global...${NC}"
# Creamos un pequeño script lanzador
cat > "$BIN_PATH" <<EOF
#!/bin/bash
cd "$INSTALL_DIR"
# Usamos sudo -E para mantener variables gráficas si es necesario
exec python3 main.py "\$@"
EOF

chmod +x "$BIN_PATH"

echo -e "${GREEN}
✅ ¡INSTALACIÓN COMPLETADA CON ÉXITO!
-------------------------------------
Para iniciar el antivirus, escribe en cualquier terminal:
    ${BLUE}sao-av${NC}
-------------------------------------
${NC}"