#!/bin/bash
# Setup script para MagicSniffer
# Configura el repositorio con validaciones de seguridad
#
# Uso: bash setup.sh

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}════════════════════════════════════════════════${NC}"
echo -e "${BLUE}🔐 MagicSniffer - Setup de Seguridad${NC}"
echo -e "${BLUE}════════════════════════════════════════════════${NC}"
echo ""

# Verificar que estamos en la raíz del proyecto
if [ ! -f "setup.py" ]; then
    echo -e "${RED}❌ Error: setup.py no encontrado${NC}"
    echo "   Ejecuta este script desde la raíz del proyecto magic-sniffer/"
    exit 1
fi

# 1. Configurar pre-commit hook
echo -e "${YELLOW}📝 Paso 1: Configurando pre-commit hook...${NC}"

GIT_HOOKS_DIR=".git/hooks"
HOOK_SOURCE=".githooks/pre-commit"
HOOK_DEST="$GIT_HOOKS_DIR/pre-commit"

if [ ! -d "$GIT_HOOKS_DIR" ]; then
    echo -e "${RED}❌ No estamos en un repositorio Git${NC}"
    exit 1
fi

if [ ! -f "$HOOK_SOURCE" ]; then
    echo -e "${RED}❌ Hook source no encontrado: $HOOK_SOURCE${NC}"
    exit 1
fi

# Copiar hook
cp "$HOOK_SOURCE" "$HOOK_DEST"
chmod +x "$HOOK_DEST"
echo -e "${GREEN}✅ Pre-commit hook instalado en $HOOK_DEST${NC}"

# 2. Verificar .gitignore
echo ""
echo -e "${YELLOW}📝 Paso 2: Verificando .gitignore...${NC}"

REQUIRED_PATTERNS=(
    "reporte_"
    "trampa_"
    "test_output"
    "credentials.json"
    ".env.local"
)

MISSING=0
for pattern in "${REQUIRED_PATTERNS[@]}"; do
    if ! grep -q "$pattern" ".gitignore"; then
        echo -e "${YELLOW}⚠️  Patrón no encontrado en .gitignore: $pattern${NC}"
        MISSING=1
    fi
done

if [ $MISSING -eq 0 ]; then
    echo -e "${GREEN}✅ .gitignore correctamente configurado${NC}"
else
    echo -e "${YELLOW}⚠️  Algunos patrones pueden faltar en .gitignore${NC}"
    echo "   Revisa el archivo manualmente"
fi

# 3. Verificar estructura del proyecto
echo ""
echo -e "${YELLOW}📝 Paso 3: Verificando estructura del proyecto...${NC}"

REQUIRED_FILES=(
    "magic_sniffer/__init__.py"
    "magic_sniffer/scanner.py"
    "magic_sniffer/database.py"
    "magic_sniffer/cli.py"
    "tests/"
    "pyproject.toml"
    "SECURITY.md"
)

for file in "${REQUIRED_FILES[@]}"; do
    if [ ! -e "$file" ]; then
        echo -e "${RED}❌ Archivo/carpeta no encontrado: $file${NC}"
        exit 1
    fi
done

echo -e "${GREEN}✅ Estructura del proyecto correcta${NC}"

# 4. Configurar Git local
echo ""
echo -e "${YELLOW}📝 Paso 4: Configurando Git local...${NC}"

# Configurar hooks.hooksPath para usar .githooks/
git config core.hooksPath .githooks
echo -e "${GREEN}✅ Git configurado para usar .githooks/${NC}"

# 5. Instalar dependencias
echo ""
echo -e "${YELLOW}📝 Paso 5: Instalando dependencias...${NC}"

if command -v pip &> /dev/null; then
    pip install -e . --quiet
    echo -e "${GREEN}✅ Paquete instalado en modo desarrollo${NC}"
else
    echo -e "${YELLOW}⚠️  pip no encontrado, saltando instalación${NC}"
fi

# 6. Resumen final
echo ""
echo -e "${BLUE}════════════════════════════════════════════════${NC}"
echo -e "${GREEN}🎉 Setup completado correctamente!${NC}"
echo -e "${BLUE}════════════════════════════════════════════════${NC}"
echo ""

echo -e "${YELLOW}Próximos pasos:${NC}"
echo "1. Revisa SECURITY.md para buenas prácticas"
echo "2. Instala GitHub Student Developer Pack:"
echo "   → https://education.github.com/pack"
echo "3. Activa GitHub Advanced Security en tu repositorio"
echo ""

echo -e "${YELLOW}Validaciones automáticas instaladas:${NC}"
echo "✅ Pre-commit hook detectará archivos sensibles"
echo "✅ .gitignore previene commits accidentales"
echo ""

echo -e "${BLUE}¿Preguntas? Revisa SECURITY.md${NC}"
echo ""
