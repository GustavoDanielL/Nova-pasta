@echo off
REM Build FinancePro - Execute do diretório raiz
REM Este arquivo gera o executável e instalador para Windows

cd /d "%~dp0"

echo.
echo ========================================
echo   FinancePro - Gerar Instalador
echo ========================================
echo.

REM Executar o script de build
call build_windows.bat

echo.
echo.
echo ========================================
echo   Próximos Passos
echo ========================================
echo.
echo 1. Abra a pasta: build_output\releases
echo.
echo 2. Envie os arquivos para seu cliente:
echo    - FinancePro.exe
echo    - Instalar.bat
echo    - LEIA-ME.txt
echo.
echo 3. Cliente pode executar:
echo    a) Instalar.bat (para instalação com atalho)
echo    b) Ou executar FinancePro.exe diretamente
echo.
pause
