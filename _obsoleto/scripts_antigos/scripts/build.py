# -*- coding: utf-8 -*-
"""
Build Script - Gera executável e instalador para FinancePro
Execute: python build.py
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path
from datetime import datetime

class BuildFinancePro:
    def __init__(self):
        self.base_dir = Path(__file__).parent.parent  # Sobe um nível para o diretório raiz
        self.dist_dir = self.base_dir / "dist"
        self.build_dir = self.base_dir / "build"
        self.output_dir = self.base_dir / "build_output" / "releases"
        self.version = "1.0.0"
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
    def limpar_builds_anteriores(self):
        """Remove builds anteriores"""
        print("🗑️  Limpando builds anteriores...")
        for dir_path in [self.dist_dir, self.build_dir]:
            if dir_path.exists():
                shutil.rmtree(dir_path)
                print(f"   ✓ Removido: {dir_path.name}")
    
    def criar_pasta_releases(self):
        """Cria pasta de releases se não existir"""
        print("\n📁 Criando pasta de releases...")
        self.output_dir.mkdir(exist_ok=True)
        print(f"   ✓ Pasta criada: {self.output_dir}")
    
    def gerar_executavel(self):
        """Gera executável usando PyInstaller"""
        print("\n⚙️  Gerando executável com PyInstaller...")
        
        # Verificar se PyInstaller está instalado
        try:
            import PyInstaller
        except ImportError:
            print("   ⚠️  PyInstaller não está instalado!")
            print("   Instalando...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        
        # Comando PyInstaller
        cmd = [
            sys.executable,
            "-m", "PyInstaller",
            "--onefile",  # Gera um único executável
            "--windowed",  # Sem console
            "--name", "FinancePro",
            "--icon", str(self.base_dir / "assets" / "icon.ico") if (self.base_dir / "assets" / "icon.ico").exists() else None,
            "--add-data", f"{self.base_dir / 'data'}{os.pathsep}data",
            "--hidden-import=matplotlib",
            "--hidden-import=openpyxl",
            "--hidden-import=customtkinter",
            "--distpath", str(self.dist_dir),
            "--buildpath", str(self.build_dir),
            str(self.base_dir / "main.py")
        ]
        
        # Remover None do comando
        cmd = [c for c in cmd if c is not None]
        
        try:
            subprocess.run(cmd, check=True)
            print("   ✓ Executável gerado com sucesso!")
            return True
        except subprocess.CalledProcessError as e:
            print(f"   ✗ Erro ao gerar executável: {e}")
            return False
    
    def criar_instalador_nsis(self):
        """Cria um instalador NSIS"""
        print("\n📦 Gerando instalador NSIS...")
        
        # Verificar se NSIS está instalado
        nsis_path = Path(r"C:\Program Files (x86)\NSIS\makensis.exe")
        
        if not nsis_path.exists():
            print("   ⚠️  NSIS não está instalado!")
            print("   Baixe em: https://nsis.sourceforge.io/")
            print("   Continuando sem instalador...")
            return False
        
        # Criar arquivo NSI (script do NSIS)
        nsi_script = self._gerar_script_nsis()
        nsi_file = self.base_dir / "installer.nsi"
        
        with open(nsi_file, 'w', encoding='utf-8') as f:
            f.write(nsi_script)
        
        print(f"   ✓ Script NSIS criado: {nsi_file.name}")
        
        # Executar NSIS
        try:
            subprocess.run([str(nsis_path), str(nsi_file)], check=True)
            print("   ✓ Instalador gerado com sucesso!")
            
            # Mover instalador para releases
            installer_name = f"FinancePro_Setup_{self.version}.exe"
            installer_src = self.base_dir / "FinancePro_Setup.exe"
            installer_dst = self.output_dir / installer_name
            
            if installer_src.exists():
                shutil.move(str(installer_src), str(installer_dst))
                print(f"   ✓ Instalador movido para: releases/{installer_name}")
                return True
            
        except subprocess.CalledProcessError as e:
            print(f"   ✗ Erro ao gerar instalador: {e}")
        
        return False
    
    def _gerar_script_nsis(self):
        """Gera o script NSIS para o instalador"""
        exe_path = self.dist_dir / "FinancePro.exe"
        
        script = f"""
; FinancePro Installer Script
; Gerado automaticamente pelo build.py

!include "MUI2.nsh"

; Nome e versão
Name "FinancePro v{self.version}"
OutFile "FinancePro_Setup.exe"
InstallDir "$PROGRAMFILES\\FinancePro"

; MUI Settings
!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH

!insertmacro MUI_LANGUAGE "PortugueseBR"

; Instalação
Section "FinancePro"
    SetOutPath "$INSTDIR"
    
    ; Copiar executável
    File "{exe_path}"
    
    ; Copiar pasta data (se existir)
    SetOutPath "$INSTDIR\\data"
    File /r "data\\*.*"
    
    ; Criar atalho no menu iniciar
    CreateDirectory "$SMPROGRAMS\\FinancePro"
    CreateShortCut "$SMPROGRAMS\\FinancePro\\FinancePro.lnk" "$INSTDIR\\FinancePro.exe"
    CreateShortCut "$SMPROGRAMS\\FinancePro\\Desinstalar.lnk" "$INSTDIR\\uninstall.exe"
    
    ; Criar atalho na área de trabalho
    CreateShortCut "$DESKTOP\\FinancePro.lnk" "$INSTDIR\\FinancePro.exe"
    
    ; Criar desinstalador
    WriteUninstaller "$INSTDIR\\uninstall.exe"
SectionEnd

; Desinstalação
Section "Uninstall"
    RMDir /r "$INSTDIR"
    RMDir /r "$SMPROGRAMS\\FinancePro"
    Delete "$DESKTOP\\FinancePro.lnk"
SectionEnd
"""
        return script
    
    def criar_instalador_simples(self):
        """Cria instalador simples em Python (sem NSIS)"""
        print("\n📦 Criando instalador Python (Portable)...")
        
        # Criar pasta com executável e dados
        portable_dir = self.output_dir / f"FinancePro_v{self.version}_Portable"
        portable_dir.mkdir(exist_ok=True)
        
        # Copiar executável
        exe_src = self.dist_dir / "FinancePro.exe"
        if exe_src.exists():
            shutil.copy(exe_src, portable_dir / "FinancePro.exe")
            print(f"   ✓ Executável copiado")
        
        # Copiar dados
        data_src = self.base_dir / "data"
        if data_src.exists():
            shutil.copytree(data_src, portable_dir / "data", dirs_exist_ok=True)
            print(f"   ✓ Dados copiados")
        
        # Criar arquivo README
        readme = portable_dir / "README.txt"
        readme.write_text("""
FinancePro v{} - Sistema de Gestão de Empréstimos

INSTALAÇÃO:
1. Extraia este arquivo
2. Clique duas vezes em "FinancePro.exe"

REQUISITOS:
- Windows 7 ou superior
- 100 MB de espaço em disco

PARA DESINSTALAR:
1. Abra a pasta
2. Delete a pasta inteira

Desenvolvido com ❤️ para gerenciamento profissional de empréstimos.
""".format(self.version))
        print(f"   ✓ README criado")
        
        # Criar arquivo de boas-vindas
        run_me = portable_dir / "EXECUTE_AQUI.bat"
        run_me.write_text("@echo off\nFinancePro.exe\npause")
        print(f"   ✓ Executável criado (EXECUTE_AQUI.bat)")
        
        # Criar ZIP
        print(f"   ✓ Criando arquivo compactado...")
        zip_name = f"FinancePro_v{self.version}_Portable"
        zip_path = self.output_dir / zip_name
        
        shutil.make_archive(str(zip_path), 'zip', portable_dir)
        print(f"   ✓ Arquivo compactado: {zip_name}.zip")
        
        return True
    
    def copiar_readme_e_dados(self):
        """Copia README e dados para releases"""
        print("\n📋 Copiando arquivos auxiliares...")
        
        # Copiar README
        readme_src = self.base_dir / "README.md"
        if readme_src.exists():
            shutil.copy(readme_src, self.output_dir / "README.md")
            print("   ✓ README.md copiado")
        
        # Copiar requirements.txt
        req_src = self.base_dir / "requirements.txt"
        if req_src.exists():
            shutil.copy(req_src, self.output_dir / "requirements.txt")
            print("   ✓ requirements.txt copiado")
    
    def gerar_relatorio(self):
        """Gera relatório final do build"""
        print("\n" + "=" * 70)
        print("📊 RELATÓRIO DO BUILD")
        print("=" * 70)
        
        print(f"\n📦 Versão: {self.version}")
        print(f"📅 Data: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
        print(f"📍 Pasta de saída: {self.output_dir}")
        
        print(f"\n📋 Arquivos gerados:")
        
        if not self.output_dir.exists():
            print("   (Nenhum arquivo gerado)")
            return
        
        for file in sorted(self.output_dir.glob("*")):
            if file.is_file():
                size_mb = file.stat().st_size / (1024 * 1024)
                print(f"   ✓ {file.name} ({size_mb:.2f} MB)")
            elif file.is_dir():
                print(f"   ✓ {file.name}/ (pasta)")
        
        print("\n" + "=" * 70)
        print("✅ BUILD CONCLUÍDO COM SUCESSO!")
        print("=" * 70)
        print("\n💡 Próximos passos:")
        print("   1. Verifique os arquivos em: releases/")
        print("   2. Teste o executável")
        print("   3. Distribua aos clientes")
        print("\n")
    
    def executar(self):
        """Executa o processo completo de build"""
        print("\n" + "=" * 70)
        print("🚀 BUILD FINANCEPRO")
        print("=" * 70)
        
        try:
            self.limpar_builds_anteriores()
            self.criar_pasta_releases()
            
            # Gerar executável
            if not self.gerar_executavel():
                print("❌ Erro ao gerar executável. Build cancelado.")
                return False
            
            # Criar instalador portável (recomendado)
            self.criar_instalador_simples()
            
            # Tentar criar instalador NSIS (opcional)
            self.criar_instalador_nsis()
            
            # Copiar arquivos auxiliares
            self.copiar_readme_e_dados()
            
            # Gerar relatório
            self.gerar_relatorio()
            
            return True
            
        except Exception as e:
            print(f"\n❌ Erro durante o build: {e}")
            import traceback
            traceback.print_exc()
            return False


def main():
    """Função principal"""
    builder = BuildFinancePro()
    
    # Verificar se PyInstaller está instalado
    print("Verificando dependências...")
    try:
        import PyInstaller
        print("✓ PyInstaller encontrado")
    except ImportError:
        print("\n⚠️  PyInstaller não está instalado!")
        print("Instalando PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # Executar build
    sucesso = builder.executar()
    
    if sucesso:
        print("\n✨ Você pode agora distribuir os arquivos em releases/")
        print("   - FinancePro_v1.0.0_Portable.zip: Versão portável (recomendada)")
        print("   - FinancePro.exe: Executável direto")
    else:
        print("\n❌ Build falhou!")
        sys.exit(1)


if __name__ == "__main__":
    main()
