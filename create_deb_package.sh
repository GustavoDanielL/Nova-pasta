#!/bin/bash
# Script para criar pacote .deb para Debian/Ubuntu

APP_NAME="financepro"
APP_VERSION="2.0.0"
ARCH="amd64"

# Criar estrutura de diretórios
mkdir -p "${APP_NAME}_${APP_VERSION}_${ARCH}/DEBIAN"
mkdir -p "${APP_NAME}_${APP_VERSION}_${ARCH}/usr/local/bin"
mkdir -p "${APP_NAME}_${APP_VERSION}_${ARCH}/usr/share/applications"
mkdir -p "${APP_NAME}_${APP_VERSION}_${ARCH}/usr/share/doc/${APP_NAME}"

# Copiar executável
cp build_output/FinancePro "${APP_NAME}_${APP_VERSION}_${ARCH}/usr/local/bin/financepro"
chmod +x "${APP_NAME}_${APP_VERSION}_${ARCH}/usr/local/bin/financepro"

# Criar arquivo control
cat > "${APP_NAME}_${APP_VERSION}_${ARCH}/DEBIAN/control" << EOF
Package: ${APP_NAME}
Version: ${APP_VERSION}
Section: office
Priority: optional
Architecture: ${ARCH}
Maintainer: GustavoDanielL <seu@email.com>
Description: Sistema de Gestão de Empréstimos
 FinancePro é um sistema profissional para gerenciar empréstimos e clientes
 com criptografia AES-256 e conformidade LGPD.
 .
 Características:
  - Banco de dados SQLite criptografado
  - Dashboard com gráficos interativos
  - Exportação para Excel
  - Notificações automáticas
  - Gestão completa de clientes e empréstimos
EOF

# Criar .desktop (atalho)
cat > "${APP_NAME}_${APP_VERSION}_${ARCH}/usr/share/applications/financepro.desktop" << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=FinancePro
Comment=Sistema de Gestão de Empréstimos
Exec=/usr/local/bin/financepro
Icon=financepro
Terminal=false
Categories=Office;Finance;
EOF

# Copiar documentação
cp README.md "${APP_NAME}_${APP_VERSION}_${ARCH}/usr/share/doc/${APP_NAME}/"
cp CHANGELOG.md "${APP_NAME}_${APP_VERSION}_${ARCH}/usr/share/doc/${APP_NAME}/"

# Criar pacote
dpkg-deb --build "${APP_NAME}_${APP_VERSION}_${ARCH}"

echo "✓ Pacote .deb criado: ${APP_NAME}_${APP_VERSION}_${ARCH}.deb"
echo ""
echo "Para instalar:"
echo "  sudo dpkg -i ${APP_NAME}_${APP_VERSION}_${ARCH}.deb"
echo ""
echo "Para desinstalar:"
echo "  sudo apt remove ${APP_NAME}"
