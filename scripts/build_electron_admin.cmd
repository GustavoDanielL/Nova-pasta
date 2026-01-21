@echo off
REM Build Electron com Privilégios Admin
REM Este script limpa o cache e compila o app Electron

echo.
echo ========================================
echo   FinancePro - Build Electron
echo   (Rodando com Privilégios Admin)
echo ========================================
echo.

REM Verificar se esta como admin
openfiles >nul 2>&1
if errorlevel 1 (
    echo [ERRO] Este script precisa ser executado como ADMINISTRADOR!
    echo.
    echo Clique com botao direito no arquivo .cmd e escolha "Executar como administrador"
    echo.
    pause
    exit /b 1
)

echo [OK] Rodando como ADMINISTRADOR

REM Mudar para diretorio do projeto
cd /d "%~dp0.."
if not exist "frontend" (
    echo [ERRO] Pasta frontend nao encontrada!
    pause
    exit /b 1
)

REM Limpar cache electron-builder
echo.
echo [LIMPEZA] Deletando cache electron-builder...
if exist "%LOCALAPPDATA%\electron-builder" (
    rmdir /s /q "%LOCALAPPDATA%\electron-builder"
    echo [OK] Cache deletado
)

REM Limpar dist anterior
echo [LIMPEZA] Removendo build anterior...
if exist "dist" (
    rmdir /s /q "dist"
    echo [OK] Pasta dist removida
)

REM Instalar dependencias
echo.
echo [DEPENDENCIAS] Verificando npm modules...
cd frontend
if not exist "node_modules" (
    echo [INSTALANDO] npm install...
    call npm install
) else (
    echo [OK] node_modules ja existente
)

REM Compilar Electron
echo.
echo [BUILD] Compilando Electron (pode levar alguns minutos)...
echo.
call npm run build:win

REM Verificar resultado
if errorlevel 1 (
    echo.
    echo [ERRO] Falha ao compilar!
    pause
    exit /b 1
)

echo.
echo ========================================
echo   [OK] Build concluido com sucesso!
echo ========================================
echo.

REM Listar arquivos gerados
echo [ARQUIVOS GERADOS]
if exist "..\dist" (
    dir /b "..\dist" | findstr /R "\.exe$"
    if exist "..\dist\*.exe" (
        echo.
        echo Instaladores em: ..\dist\
        pause
    )
)

exit /b 0
