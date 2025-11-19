@echo off
REM Build FinancePro - Execute do diretório raiz
REM Este arquivo chama o build.py que está em scripts/

cd /d "%~dp0"

echo.
echo ========================================
echo   FinancePro - Build Script
echo ========================================
echo.

REM Verificar se Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo Erro: Python não está instalado!
    echo Baixe em: https://www.python.org/
    pause
    exit /b 1
)

echo Instalando dependências de build...
pip install pyinstaller>nul 2>&1

echo.
echo Gerando executável...
echo Isso pode levar alguns minutos...
echo.

python scripts/build.py

if errorlevel 1 (
    echo.
    echo Erro ao gerar build!
    pause
    exit /b 1
)

echo.
echo Abrindo pasta de releases...
explorer build_output\releases

echo.
echo Build concluído com sucesso!
echo Verifique a pasta "build_output\releases" para ver os arquivos gerados.
pause
