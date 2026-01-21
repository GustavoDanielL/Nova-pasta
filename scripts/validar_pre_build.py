#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script de Validação Pré-Build
Verifica se tudo está ok antes de gerar o executável
"""

import sys
import os
from pathlib import Path
from importlib.util import find_spec

def check_python_version():
    """Verifica versão do Python"""
    print("\n📌 Verificando Python...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"   ✅ Python {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print(f"   ❌ Python {version.major}.{version.minor} (requerido 3.8+)")
        return False

def check_required_files():
    """Verifica arquivos necessários"""
    print("\n📁 Verificando arquivos necessários...")
    
    required = {
        'main.py': 'Arquivo principal da aplicação',
        'requirements.txt': 'Lista de dependências',
        'config.py': 'Configurações',
        'theme_colors.py': 'Cores do tema',
        'models/': 'Pasta de modelos',
        'views/': 'Pasta de views',
        'utils/': 'Pasta de utilitários',
        'scripts/build.py': 'Script de build',
    }
    
    all_ok = True
    for file_path, description in required.items():
        full_path = Path(file_path)
        if full_path.exists():
            print(f"   ✅ {file_path:30} - {description}")
        else:
            print(f"   ❌ {file_path:30} - {description} [NÃO ENCONTRADO]")
            all_ok = False
    
    return all_ok

def check_dependencies():
    """Verifica se as dependências principais estão instaladas"""
    print("\n📦 Verificando dependências...")
    
    required = [
        ('customtkinter', 'Interface gráfica'),
        ('PIL', 'Processamento de imagens'),
        ('openpyxl', 'Excel'),
        ('fpdf2', 'PDF'),
        ('cryptography', 'Criptografia'),
        ('qrcode', 'QR Code'),
        ('pyinstaller', 'Build do executável'),
    ]
    
    all_ok = True
    for module, description in required:
        try:
            if find_spec(module):
                print(f"   ✅ {module:20} - {description}")
            else:
                print(f"   ⚠️  {module:20} - Não encontrado (será instalado ao fazer build)")
        except (ImportError, ModuleNotFoundError):
            print(f"   ⚠️  {module:20} - Não encontrado (será instalado ao fazer build)")
    
    return True

def check_imports():
    """Testa se os imports do main.py funcionam"""
    print("\n🔗 Testando imports do main.py...")
    
    try:
        from views.login_view import LoginView
        print("   ✅ views.login_view")
    except ImportError as e:
        print(f"   ❌ views.login_view: {e}")
        return False
    
    try:
        from models.database_sqlite import DatabaseSQLite
        print("   ✅ models.database_sqlite")
    except ImportError as e:
        print(f"   ❌ models.database_sqlite: {e}")
        return False
    
    try:
        from license_manager import LicenseManager
        print("   ✅ license_manager")
    except ImportError as e:
        print(f"   ❌ license_manager: {e}")
        return False
    
    try:
        from utils.json_migrator import executar_migracao_automatica, verificar_migracao_necessaria
        print("   ✅ utils.json_migrator")
    except ImportError as e:
        print(f"   ❌ utils.json_migrator: {e}")
        return False
    
    try:
        from utils.master_password import solicitar_senha_mestra
        print("   ✅ utils.master_password")
    except ImportError as e:
        print(f"   ❌ utils.master_password: {e}")
        return False
    
    try:
        from utils.logger_config import configurar_logging, log_operacao
        print("   ✅ utils.logger_config")
    except ImportError as e:
        print(f"   ❌ utils.logger_config: {e}")
        return False
    
    return True

def check_database_tables():
    """Verifica se o banco de dados está ok"""
    print("\n💾 Verificando banco de dados...")
    
    try:
        from models.database_sqlite import DatabaseSQLite
        from pathlib import Path
        
        test_db = Path.home() / "test_financepro.db"
        if test_db.exists():
            test_db.unlink()
        
        db = DatabaseSQLite(test_db, None)
        print("   ✅ Banco de dados criado com sucesso")
        
        # Limpar
        test_db.unlink()
        
        return True
    except Exception as e:
        print(f"   ❌ Erro ao criar banco de dados: {e}")
        return False

def main():
    """Executa todas as verificações"""
    print("\n" + "="*60)
    print("  Validação Pré-Build - FinancePro")
    print("="*60)
    
    checks = [
        ("Python", check_python_version()),
        ("Arquivos", check_required_files()),
        ("Dependências", check_dependencies()),
        ("Imports", check_imports()),
        ("Database", check_database_tables()),
    ]
    
    print("\n" + "="*60)
    print("  Resultado da Validação")
    print("="*60)
    
    all_passed = True
    for name, result in checks:
        status = "✅ PASSOU" if result else "❌ FALHOU"
        print(f"{name:20} - {status}")
        if not result:
            all_passed = False
    
    print("="*60)
    
    if all_passed:
        print("\n✅ Tudo OK! Você pode rodar: GERAR_INSTALADOR.bat")
    else:
        print("\n❌ Corrija os erros acima antes de fazer o build.")
        print("\nDicas:")
        print("1. Verifique se está na pasta correta")
        print("2. Instale dependências: pip install -r requirements.txt")
        print("3. Crie ambiente virtual: python -m venv .venv")
        print("4. Ative: .venv\\Scripts\\activate")
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main())
