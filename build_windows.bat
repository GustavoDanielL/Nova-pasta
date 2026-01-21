@echo off
REM Build script para Windows usando Python
REM Execute a partir do diretório raiz do projeto

cd /d "%~dp0"

echo.
echo ========================================
echo   FinancePro - Build Script (Windows)
echo ========================================
echo.

REM Verificar se Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERRO] Python não está instalado!
    echo.
    echo Baixe Python 3.10+ em: https://www.python.org/
    echo.
    pause
    exit /b 1
)

REM Ativar ambiente virtual se existir
if exist ".venv\Scripts\activate.bat" (
    echo [INFO] Ativando ambiente virtual...
    call .venv\Scripts\activate.bat
) else (
    echo [AVISO] Ambiente virtual não encontrado
    echo [INFO] Use: python -m venv .venv
    echo.
)

REM Instalar dependências se necessário
echo [INFO] Verificando dependências...
pip install -q -r requirements.txt >nul 2>&1

echo [INFO] Instalando PyInstaller...
pip install -q pyinstaller >nul 2>&1

echo.
echo [INFO] Iniciando processo de build...
echo [INFO] Isso pode levar alguns minutos...
echo.

REM Executar o script de build Python
python scripts\build.py

if errorlevel 1 (
    echo.
    echo [ERRO] Falha ao gerar build!
    echo.
    pause
    exit /b 1
)

echo.
echo [SUCESSO] Build concluído!
echo.
echo Arquivos gerados em: build_output\releases\
echo.
pause
