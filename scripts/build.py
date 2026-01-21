#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Build Script - Gera executável para FinancePro no Windows
Execute: python scripts/build.py
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path
from datetime import datetime

class BuildFinancePro:
    def __init__(self):
        self.base_dir = Path(__file__).parent.parent  # Diretório raiz do projeto
        self.dist_dir = self.base_dir / "dist"
        self.build_dir = self.base_dir / "build"
        self.output_dir = self.base_dir / "build_output" / "releases"
        self.version = "2.0.0"
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
    def log(self, message):
        """Exibe mensagem de log com timestamp"""
        print(f"[{datetime.now().strftime('%H:%M:%S')}] {message}")
    
    def limpar_builds_anteriores(self):
        """Remove builds anteriores"""
        self.log("[LIMPEZA] Limpando builds anteriores...")
        for dir_path in [self.dist_dir, self.build_dir]:
            if dir_path.exists():
                shutil.rmtree(dir_path)
                self.log(f"   OK Removido: {dir_path.name}")
    
    def criar_pasta_releases(self):
        """Cria pasta de releases se não existir"""
        self.log("[PASTA] Criando pasta de releases...")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.log(f"   OK Pasta criada: {self.output_dir}")
    
    def verificar_dependencias(self):
        """Verifica e instala dependências necessárias"""
        self.log("[DEPENDENCIAS] Verificando dependencias...")
        
        dependencias = [
            "pyinstaller",
            "customtkinter",
            "pillow",
            "cryptography",
            "openpyxl",
            "fpdf2",
            "qrcode",
            "python-dotenv"
        ]
        
        for dep in dependencias:
            try:
                __import__(dep.replace("-", "_"))
                self.log(f"   OK {dep}")
            except ImportError:
                self.log(f"   INSTALANDO {dep}...")
                subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", dep])
    
    def gerar_executavel(self):
        """Gera executável usando PyInstaller"""
        self.log("[COMPILACAO] Gerando executavel com PyInstaller...")
        
        # Verificar se PyInstaller está instalado
        try:
            import PyInstaller
        except ImportError:
            self.log("   INSTALANDO PyInstaller...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", "pyinstaller"])
        
        # Preparar dados para incluir
        datas = [
            f"{self.base_dir / 'config.py'}{os.pathsep}.",
            f"{self.base_dir / 'theme_colors.py'}{os.pathsep}.",
            f"{self.base_dir / 'models'}{os.pathsep}models",
            f"{self.base_dir / 'views'}{os.pathsep}views",
            f"{self.base_dir / 'utils'}{os.pathsep}utils",
        ]
        
        # Hidden imports necessários
        hidden_imports = [
            "customtkinter",
            "PIL",
            "openpyxl",
            "fpdf2",
            "qrcode",
            "cryptography",
            "dotenv",
        ]
        
        # Construir comando PyInstaller
        cmd = [
            sys.executable,
            "-m", "PyInstaller",
            "--onefile",
            "--windowed",
            "--name", "FinancePro",
            "--distpath", str(self.dist_dir),
            "--workpath", str(self.build_dir),
            "--specpath", str(self.build_dir),
        ]
        
        # Adicionar dados
        for data in datas:
            if data:
                cmd.extend(["--add-data", data])
        
        # Adicionar hidden imports
        for imp in hidden_imports:
            cmd.extend(["--hidden-import", imp])
        
        # Arquivo principal
        cmd.append(str(self.base_dir / "main.py"))
        
        try:
            self.log("   Executando PyInstaller (pode levar alguns minutos)...")
            self.log("")
            # Não captura output para evitar problemas de timeout e permitir visualizar progresso
            result = subprocess.run(cmd)
            
            if result.returncode != 0:
                self.log("   [ERRO] Erro ao gerar executavel!")
                return False
            
            self.log("   [OK] Executavel gerado com sucesso!")
            
            # Copiar para output_dir
            exe_source = self.dist_dir / "FinancePro.exe"
            if exe_source.exists():
                shutil.copy(exe_source, self.output_dir / "FinancePro.exe")
                self.log(f"   [OK] Copiado para: {self.output_dir / 'FinancePro.exe'}")
            
            return True
            
        except Exception as e:
            self.log(f"   [ERRO] Erro ao gerar executavel: {e}")
            return False
    
    def criar_instalador_simples(self):
        """Cria script de instalacao melhorado"""
        self.log("[INSTALADOR] Criando script de instalacao...")
        
        installer_script = r"""@echo off
REM Instalador FinancePro - Menu
REM Oferece opcoes de instalacao ou modo portatil

setlocal enabledelayedexpansion
cd /d "%~dp0"

:MENU
cls
echo.
echo ========================================
echo   Instalador FinancePro 2.0
echo ========================================
echo.
echo [1] Instalar no Program Files
echo [2] Modo Portatil (executar daqui)
echo [3] Sair
echo.
set /p OPCAO="Escolha uma opcao [1-3]: "

if "%OPCAO%"=="1" goto INSTALAR_PROGRAMA_FILES
if "%OPCAO%"=="2" goto INSTALAR_PORTATIL
if "%OPCAO%"=="3" goto SAIR
cls
echo [ERRO] Opcao invalida!
timeout /t 2 >nul
goto MENU

:INSTALAR_PROGRAMA_FILES
echo.
echo Verificando permissoes de administrador...
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo [ERRO] Este script requer permissoes de administrador!
    echo.
    echo Para instalacao em Program Files:
    echo 1. Clique com botao direito em Instalar.bat
    echo 2. Selecione "Executar como administrador"
    echo.
    pause
    goto MENU
)

if not exist "FinancePro.exe" (
    echo.
    echo [ERRO] FinancePro.exe nao encontrado!
    echo.
    echo Certifique-se que estao na mesma pasta.
    echo.
    pause
    goto MENU
)

echo.
echo Instalando FinancePro em Program Files...

REM Criar diretorio primeiro
if not exist "%ProgramFiles%\FinancePro" (
    echo Criando diretorio...
    mkdir "%ProgramFiles%\FinancePro" >nul 2>&1
    if %errorlevel% neq 0 (
        echo.
        echo [ERRO] Falha ao criar diretorio!
        echo.
        pause
        goto MENU
    )
)

REM Copiar executavel
echo Copiando executavel...
copy "FinancePro.exe" "%ProgramFiles%\FinancePro\" /Y >nul 2>&1

if %errorlevel% neq 0 (
    echo.
    echo [ERRO] Falha ao copiar arquivo!
    echo.
    pause
    goto MENU
)

REM Criar atalho na Desktop
echo Criando atalho na Desktop...
powershell -NoProfile -ExecutionPolicy Bypass -Command "& {$WshShell = New-Object -ComObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%USERPROFILE%\Desktop\FinancePro.lnk'); $Shortcut.TargetPath = '%ProgramFiles%\FinancePro\FinancePro.exe'; $Shortcut.WorkingDirectory = '%ProgramFiles%\FinancePro'; $Shortcut.Description = 'FinancePro - Sistema de Gestao Financeira'; $Shortcut.Save()}" >nul 2>&1

echo.
echo ========================================
echo OK - FinancePro instalado com sucesso!
echo ========================================
echo.
echo Abra pelo atalho na Desktop ou:
echo %ProgramFiles%\FinancePro\FinancePro.exe
echo.
pause
goto MENU

:INSTALAR_PORTATIL
cls
echo.
echo ========================================
echo   Modo Portatil
echo ========================================
echo.
echo FinancePro esta pronto para usar!
echo Clique em FinancePro.exe para abrir.
echo.
echo Vantagens:
echo - Sem necessidade de administrador
echo - Pode usar em pendrive ou CD
echo.
pause
echo.
echo Abrindo FinancePro...
start "" "FinancePro.exe"
goto SAIR

:SAIR
exit /b 0
"""
        
        installer_path = self.output_dir / "Instalar.bat"
        with open(installer_path, 'w', encoding='utf-8') as f:
            f.write(installer_script)
        
        self.log(f"   [OK] Script criado: {installer_path.name}")
    
    def criar_readme(self):
        """Cria README com instrucoes"""
        self.log("[README] Criando README...")
        
        readme = """# FinancePro - Instrucoes de Instalacao

## Opcao 1: Instalacao com Script (Recomendado)

1. Execute `Instalar.bat` como Administrador
   - Clique com botao direito -> "Executar como administrador"
   
2. Aguarde a instalacao concluir
   - Um atalho sera criado na Desktop

3. Abra o atalho da Desktop para iniciar o FinancePro

## Opcao 2: Execucao Direta

Execute `FinancePro.exe` diretamente sem instalacao previa.

## Requisitos

- Windows 7 ou superior
- Nenhuma dependencia adicional (tudo incluido no executavel)

## Solucao de Problemas

### "FinancePro nao abre"
- Tente executar como Administrador
- Desabilite antivirus temporariamente

### "Erro ao instalar"
- Execute `Instalar.bat` como Administrador
- Feche qualquer instancia do FinancePro em execucao

### "Arquivo nao encontrado"
- Certifique-se que `FinancePro.exe` esta na mesma pasta que `Instalar.bat`

## Desinstalacao

1. Va para Painel de Controle -> Programas -> Desinstalar um programa
2. Localize "FinancePro" e clique em Desinstalar
3. Opcionalmente, delete a pasta %ProgramFiles%\\FinancePro

Versao: 2.0.0
Data: 21/01/2026
"""
        
        readme_path = self.output_dir / "LEIA-ME.txt"
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(readme)
        
        self.log(f"   [OK] README criado: {readme_path.name}")
    
    def run(self):
        """Executa o build completo"""
        try:
            print("\n" + "="*60)
            print("  FinancePro - Build Script")
            print("="*60 + "\n")
            
            self.limpar_builds_anteriores()
            self.criar_pasta_releases()
            self.verificar_dependencias()
            self.gerar_executavel()
            self.criar_instalador_simples()
            self.criar_readme()
            
            self.log("\n[OK] Build concluido com sucesso!")
            self.log(f"\n[SAIDA] Arquivos gerados em:")
            self.log(f"   {self.output_dir}")
            self.log(f"\n[ARQUIVOS]:")
            self.log(f"   - FinancePro.exe (executavel)")
            self.log(f"   - Instalar.bat (script de instalacao)")
            self.log(f"   - LEIA-ME.txt (instrucoes)")
            self.log("\n[DISTRIBUICAO] Para distribuir, comprima a pasta 'releases'")
            
            return True
            
        except Exception as e:
            self.log(f"\n[ERRO] Erro durante o build: {e}")
            import traceback
            traceback.print_exc()
            return False

if __name__ == "__main__":
    builder = BuildFinancePro()
    success = builder.run()
    
    if not success:
        sys.exit(1)
