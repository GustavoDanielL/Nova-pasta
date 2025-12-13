@echo off
REM Script para gerar executável do FinancePro
REM Execute este arquivo para criar o instalador

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

python build.py

if errorlevel 1 (
    echo.
    echo Erro ao gerar build!
    pause
    exit /b 1
)

echo.
echo Abrindo pasta de releases...
explorer releases

echo.
echo Build concluído com sucesso!
echo Verificar pasta "releases" para ver os arquivos gerados.
pause
