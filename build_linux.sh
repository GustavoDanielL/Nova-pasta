#!/bin/bash
# Build script para Linux
# Gera executável standalone do FinancePro

echo "🚀 Iniciando build do FinancePro para Linux..."

# Ativar ambiente virtual se existir
if [ -d ".venv" ]; then
    echo "✓ Ativando ambiente virtual..."
    source .venv/bin/activate
fi

# Instalar PyInstaller se necessário
echo "✓ Verificando PyInstaller..."
pip install pyinstaller --quiet

# Limpar builds anteriores
echo "🗑️  Limpando builds anteriores..."
rm -rf build dist

# Criar executável
echo "⚙️  Gerando executável..."
pyinstaller --clean --noconfirm \
    --name="FinancePro" \
    --onefile \
    --windowed \
    --icon=icon.png \
    --add-data="theme_colors.py:." \
    --add-data="config.py:." \
    --add-data="license_config.py:." \
    --hidden-import="PIL._tkinter_finder" \
    --hidden-import="babel.numbers" \
    --collect-all="customtkinter" \
    --collect-all="PIL" \
    main.py

# Criar pasta de distribuição
echo "📦 Criando pacote de distribuição..."
mkdir -p build_output/FinancePro-Linux
cp dist/FinancePro build_output/FinancePro-Linux/
cp README.md build_output/FinancePro-Linux/ 2>/dev/null || true

# Criar instalador simples
cat > build_output/FinancePro-Linux/instalar.sh << 'EOF'
#!/bin/bash
echo "📦 Instalando FinancePro..."

# Criar diretório no opt
sudo mkdir -p /opt/financepro
sudo cp FinancePro /opt/financepro/

# Criar atalho no desktop
cat > ~/Desktop/FinancePro.desktop << 'DESKTOP'
[Desktop Entry]
Version=1.0
Type=Application
Name=FinancePro
Comment=Sistema de Gestão Financeira
Exec=/opt/financepro/FinancePro
Icon=accessories-calculator
Terminal=false
Categories=Office;Finance;
DESKTOP

chmod +x ~/Desktop/FinancePro.desktop

echo "✓ FinancePro instalado com sucesso!"
echo "✓ Atalho criado na área de trabalho"
EOF

chmod +x build_output/FinancePro-Linux/instalar.sh
chmod +x build_output/FinancePro-Linux/FinancePro

echo ""
echo "✅ Build concluído com sucesso!"
echo "📁 Executável: build_output/FinancePro-Linux/FinancePro"
echo "📋 Execute: ./build_output/FinancePro-Linux/FinancePro"
echo "📋 Ou instale: cd build_output/FinancePro-Linux && sudo ./instalar.sh"
