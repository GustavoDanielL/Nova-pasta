#!/bin/bash

# ============================================
# FinancePro - Script de Build para Linux
# ============================================

set -e

echo "╔════════════════════════════════════════════╗"
echo "║     FinancePro - Build System v2.0         ║"
echo "╚════════════════════════════════════════════╝"
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
FRONTEND_DIR="$PROJECT_DIR/frontend"

echo -e "${BLUE}📁 Diretório do projeto: $PROJECT_DIR${NC}"
echo ""

# Check Node.js
check_node() {
    echo -e "${YELLOW}🔍 Verificando Node.js...${NC}"
    if ! command -v node &> /dev/null; then
        echo -e "${RED}❌ Node.js não encontrado. Por favor, instale o Node.js 18+${NC}"
        exit 1
    fi
    
    NODE_VERSION=$(node -v)
    echo -e "${GREEN}✅ Node.js encontrado: $NODE_VERSION${NC}"
}

# Check npm
check_npm() {
    echo -e "${YELLOW}🔍 Verificando npm...${NC}"
    if ! command -v npm &> /dev/null; then
        echo -e "${RED}❌ npm não encontrado${NC}"
        exit 1
    fi
    
    NPM_VERSION=$(npm -v)
    echo -e "${GREEN}✅ npm encontrado: $NPM_VERSION${NC}"
}

# Install dependencies
install_deps() {
    echo ""
    echo -e "${YELLOW}📦 Instalando dependências do Electron...${NC}"
    cd "$FRONTEND_DIR"
    npm install
    echo -e "${GREEN}✅ Dependências instaladas${NC}"
}

# Build for Linux
build_linux() {
    echo ""
    echo -e "${YELLOW}🔨 Compilando para Linux...${NC}"
    cd "$FRONTEND_DIR"
    
    # Clean previous builds
    rm -rf ../dist 2>/dev/null || true
    
    # Build
    npm run build:linux
    
    echo ""
    echo -e "${GREEN}✅ Build concluído!${NC}"
    echo ""
    echo -e "${BLUE}📦 Os arquivos foram gerados em:${NC}"
    echo "   $PROJECT_DIR/dist/"
    echo ""
    
    # List generated files
    if [ -d "$PROJECT_DIR/dist" ]; then
        echo -e "${BLUE}📋 Arquivos gerados:${NC}"
        ls -lah "$PROJECT_DIR/dist/"
    fi
}

# Build AppImage only
build_appimage() {
    echo ""
    echo -e "${YELLOW}🔨 Compilando AppImage...${NC}"
    cd "$FRONTEND_DIR"
    npm run build:linux:appimage
    echo -e "${GREEN}✅ AppImage gerado!${NC}"
}

# Build Deb only
build_deb() {
    echo ""
    echo -e "${YELLOW}🔨 Compilando .deb...${NC}"
    cd "$FRONTEND_DIR"
    npm run build:linux:deb
    echo -e "${GREEN}✅ Pacote .deb gerado!${NC}"
}

# Development mode
dev_mode() {
    echo ""
    echo -e "${YELLOW}🚀 Iniciando em modo de desenvolvimento...${NC}"
    cd "$FRONTEND_DIR"
    npm run dev
}

# Run the app
run_app() {
    echo ""
    echo -e "${YELLOW}🚀 Iniciando FinancePro...${NC}"
    cd "$FRONTEND_DIR"
    npm start
}

# Show help
show_help() {
    echo "Uso: $0 [comando]"
    echo ""
    echo "Comandos disponíveis:"
    echo "  install     Instalar dependências"
    echo "  build       Compilar para Linux (AppImage + deb)"
    echo "  appimage    Compilar apenas AppImage"
    echo "  deb         Compilar apenas .deb"
    echo "  run         Executar o aplicativo"
    echo "  dev         Executar em modo de desenvolvimento"
    echo "  help        Mostrar esta ajuda"
    echo ""
}

# Main
main() {
    check_node
    check_npm
    
    case "${1:-build}" in
        install)
            install_deps
            ;;
        build)
            install_deps
            build_linux
            ;;
        appimage)
            install_deps
            build_appimage
            ;;
        deb)
            install_deps
            build_deb
            ;;
        run)
            install_deps
            run_app
            ;;
        dev)
            install_deps
            dev_mode
            ;;
        help|--help|-h)
            show_help
            ;;
        *)
            echo -e "${RED}❌ Comando desconhecido: $1${NC}"
            show_help
            exit 1
            ;;
    esac
}

main "$@"
