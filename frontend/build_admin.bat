@echo off
REM Script para executar npm run build:win como Administrador
REM Se nao estiver em modo admin, pede elevacao

>nul 2>&1 "%SYSTEMROOT%\system32\cacls.exe" "%SYSTEMROOT%\system32\config\system"
if errorlevel 1 (
    echo.
    echo [ELEVANDO] Solicitando permissoes de Administrador...
    echo.
    
    powershell -Command "Start-Process -FilePath 'cmd.exe' -ArgumentList '/c \"%~f0\"' -Verb RunAs"
    exit /b
)

REM Se chegou aqui, estamos em modo admin
echo.
echo [ADMIN] Executando com privilégios de Administrador
echo.

cd /d "%~dp0"
cmd /c "npm run build:win"

pause
