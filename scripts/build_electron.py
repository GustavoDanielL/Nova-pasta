#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Build Script CORRETO - Gera versao Electron do FinancePro
Este script:
1. Compila o backend Python (backend/api.py) para financepro-backend.exe
2. Executa electron-builder para empacotar o app completo
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path
from datetime import datetime

class BuildElectronFinancePro:
    def __init__(self):
        self.base_dir = Path(__file__).parent.parent
        self.backend_dir = self.base_dir / "backend"
        self.frontend_dir = self.base_dir / "frontend"
        self.dist_dir = self.base_dir / "dist"
        self.build_dir = self.base_dir / "build"
        self.output_dir = self.base_dir / "build_output" / "electron"
        self.version = "2.0.0"
        
    def log(self, message):
        """Exibe mensagem de log com timestamp"""
        print(f"[{datetime.now().strftime('%H:%M:%S')}] {message}")
    
    def limpar_builds_anteriores(self):
        """Remove builds anteriores"""
        self.log("[LIMPEZA] Removendo builds anteriores...")
        for dir_path in [self.dist_dir, self.build_dir]:
            if dir_path.exists():
                shutil.rmtree(dir_path)
                self.log(f"   OK Removido: {dir_path.name}")
    
    def criar_pastas(self):
        """Cria estrutura de pastas necessaria"""
        self.log("[PASTAS] Criando estrutura...")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.dist_dir.mkdir(parents=True, exist_ok=True)
        self.log("   OK Pastas criadas")
    
    def verificar_dependencias(self):
        """Verifica PyInstaller e Node.js"""
        self.log("[DEPENDENCIAS] Verificando...")
        
        # PyInstaller
        try:
            import PyInstaller
            self.log("   OK PyInstaller")
        except ImportError:
            self.log("   INSTALANDO PyInstaller...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", "pyinstaller"])
        
        # Node.js e npm
        try:
            result = subprocess.run(["node", "--version"], capture_output=True, text=True)
            if result.returncode == 0:
                self.log(f"   OK Node.js {result.stdout.strip()}")
            else:
                raise Exception("Node.js nao encontrado")
        except:
            self.log("   [ERRO] Node.js nao instalado! Instale Node.js primeiro.")
            return False
        
        try:
            # Usar cmd /c para bypass execution policy
            result = subprocess.run(["cmd", "/c", "npm", "--version"], capture_output=True, text=True)
            if result.returncode == 0:
                self.log(f"   OK npm {result.stdout.strip()}")
            else:
                raise Exception("npm nao encontrado")
        except:
            self.log("   [ERRO] npm nao encontrado!")
            return False
        
        return True
    
    def compilar_backend(self):
        """Compila backend Python para exe"""
        self.log("[BACKEND] Compilando backend Python...")
        
        backend_main = self.backend_dir / "run_backend.py"
        if not backend_main.exists():
            self.log(f"   [ERRO] Arquivo nao encontrado: {backend_main}")
            return False
        
        # Preparar dados para incluir no backend
        datas = [
            f"{self.base_dir / 'config.py'}{os.pathsep}.",
            f"{self.base_dir / 'theme_colors.py'}{os.pathsep}.",
            f"{self.base_dir / 'license_manager.py'}{os.pathsep}.",
            f"{self.base_dir / 'models'}{os.pathsep}models",
            f"{self.base_dir / 'utils'}{os.pathsep}utils",
        ]
        
        hidden_imports = [
            "fastapi",
            "uvicorn",
            "pydantic",
            "sqlite3",
            "cryptography",
            "openpyxl",
            "fpdf2",
        ]
        
        # Construir comando PyInstaller
        cmd = [
            sys.executable,
            "-m", "PyInstaller",
            "--onefile",
            "--console",  # Manter console para ver logs do backend
            "--name", "financepro-backend",
            "--distpath", str(self.dist_dir),
            "--workpath", str(self.build_dir / "backend"),
            "--specpath", str(self.build_dir),
        ]
        
        for data in datas:
            if data:
                cmd.extend(["--add-data", data])
        
        for imp in hidden_imports:
            cmd.extend(["--hidden-import", imp])
        
        cmd.append(str(backend_main))
        
        try:
            self.log("   Executando PyInstaller (backend)...")
            result = subprocess.run(cmd)
            
            if result.returncode != 0:
                self.log("   [ERRO] Falha ao compilar backend")
                return False
            
            backend_exe = self.dist_dir / "financepro-backend.exe"
            if backend_exe.exists():
                self.log(f"   [OK] Backend compilado: {backend_exe}")
                return True
            else:
                self.log("   [ERRO] Backend exe nao foi gerado")
                return False
                
        except Exception as e:
            self.log(f"   [ERRO] Erro ao compilar backend: {e}")
            return False
    
    def instalar_dependencias_frontend(self):
        """Verifica se dependencias npm estao instaladas"""
        self.log("[FRONTEND] Verificando dependencias npm...")
        
        node_modules = self.frontend_dir / "node_modules"
        if node_modules.exists():
            self.log("   [OK] Dependencias ja instaladas (node_modules encontrado)")
            return True
        
        self.log("   [INSTALANDO] node_modules nao encontrado, instalando...")
        try:
            result = subprocess.run(
                ["cmd", "/c", "npm", "install"],
                cwd=str(self.frontend_dir)
            )
            
            if result.returncode == 0:
                self.log("   [OK] Dependencias instaladas")
                return True
            else:
                self.log(f"   [ERRO] npm install falhou")
                return False
                
        except Exception as e:
            self.log(f"   [ERRO] Erro ao instalar dependencias: {e}")
            return False
    
    def compilar_electron(self):
        """Compila aplicacao Electron com electron-builder"""
        self.log("[ELECTRON] Compilando aplicacao Electron...")
        
        try:
            # Rodar electron-builder para Windows
            result = subprocess.run(
                ["cmd", "/c", "npm", "run", "build:win"],
                cwd=str(self.frontend_dir),
                env={**os.environ, "CI": "true"}  # CI mode para evitar prompts
            )
            
            if result.returncode == 0:
                self.log("   [OK] Electron build concluido!")
                
                # Verificar se instalador foi gerado
                instalador = list(self.dist_dir.glob("*.exe"))
                if instalador:
                    self.log(f"   [OK] Instalador gerado: {instalador[0].name}")
                    
                    # Copiar para output_dir
                    for inst in instalador:
                        dest = self.output_dir / inst.name
                        shutil.copy2(inst, dest)
                        self.log(f"   [OK] Copiado para: {dest}")
                    
                    return True
                else:
                    self.log("   [AVISO] Nenhum instalador .exe encontrado em dist/")
                    return True  # Electron pode ter gerado em outro formato
                    
            else:
                self.log("   [ERRO] electron-builder falhou")
                return False
                
        except Exception as e:
            self.log(f"   [ERRO] Erro ao compilar Electron: {e}")
            return False
    
    def listar_saidas(self):
        """Lista arquivos gerados"""
        self.log("\n[SAIDA] Arquivos gerados:")
        
        # Verificar dist/
        if self.dist_dir.exists():
            self.log(f"\nEm {self.dist_dir}:")
            for item in self.dist_dir.iterdir():
                if item.is_file():
                    size_mb = item.stat().st_size / (1024 * 1024)
                    self.log(f"   - {item.name} ({size_mb:.1f} MB)")
        
        # Verificar output_dir
        if self.output_dir.exists() and any(self.output_dir.iterdir()):
            self.log(f"\nEm {self.output_dir}:")
            for item in self.output_dir.iterdir():
                if item.is_file():
                    size_mb = item.stat().st_size / (1024 * 1024)
                    self.log(f"   - {item.name} ({size_mb:.1f} MB)")
    
    def run(self):
        """Executa o build completo"""
        try:
            print("\n" + "="*60)
            print("  FinancePro - Build Electron")
            print("="*60 + "\n")
            
            self.limpar_builds_anteriores()
            self.criar_pastas()
            
            if not self.verificar_dependencias():
                self.log("\n[ERRO] Dependencias faltando. Instale Node.js e npm primeiro.")
                return False
            
            if not self.compilar_backend():
                self.log("\n[ERRO] Falha ao compilar backend")
                return False
            
            if not self.instalar_dependencias_frontend():
                self.log("\n[ERRO] Falha ao instalar dependencias npm")
                return False
            
            if not self.compilar_electron():
                self.log("\n[ERRO] Falha ao compilar Electron")
                return False
            
            self.listar_saidas()
            
            self.log("\n[OK] Build Electron concluido com sucesso!")
            self.log(f"\n[DISTRIBUICAO] Instaladores em: {self.dist_dir}")
            
            return True
            
        except Exception as e:
            self.log(f"\n[ERRO] Erro durante o build: {e}")
            import traceback
            traceback.print_exc()
            return False

if __name__ == "__main__":
    builder = BuildElectronFinancePro()
    success = builder.run()
    
    if not success:
        sys.exit(1)
