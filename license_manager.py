"""
Sistema de Licenças Simples
UMA CHAVE = UMA MÁQUINA
"""
import hashlib
import platform
import uuid
import json
from pathlib import Path

# CHAVES VÁLIDAS
CHAVES_VALIDAS = {
    "FINANCEPRO-2025-PREMIUM": {"usado": False, "maquina_id": None},
    "TRIAL-30DIAS-FREE": {"usado": False, "maquina_id": None},
    "GUSTAVO-DEV-KEY": {"usado": False, "maquina_id": None},
}


class LicenseManager:
    def __init__(self):
        if platform.system() == "Windows":
            self.license_file = Path.home() / "AppData" / "Local" / "FinancePro" / ".license"
        else:
            self.license_file = Path.home() / ".config" / "FinancePro" / ".license"
        
        self.license_file.parent.mkdir(parents=True, exist_ok=True)
    
    def get_machine_id(self):
        try:
            info = f"{platform.node()}{uuid.getnode()}{platform.machine()}"
            return hashlib.sha256(info.encode()).hexdigest()[:32]
        except:
            return None
    
    def is_licensed(self):
        if not self.license_file.exists():
            return False
        
        try:
            with open(self.license_file, 'r') as f:
                data = json.load(f)
            
            saved_machine_id = data.get('machine_id')
            current_machine_id = self.get_machine_id()
            
            return saved_machine_id == current_machine_id
        except:
            return False
    
    def validate_key(self, key):
        key = key.strip().upper()
        
        if key not in CHAVES_VALIDAS:
            return False, "Chave não encontrada"
        
        chave_info = CHAVES_VALIDAS[key]
        current_machine = self.get_machine_id()
        
        if not chave_info["usado"]:
            return True, "Chave válida"
        
        if chave_info["maquina_id"] == current_machine:
            return True, "Chave já ativada nesta máquina"
        
        return False, "Esta chave já foi ativada em outra máquina"
    
    def activate_license(self, key):
        key = key.strip().upper()
        
        is_valid, message = self.validate_key(key)
        if not is_valid:
            return False, message
        
        machine_id = self.get_machine_id()
        if not machine_id:
            return False, "Erro ao identificar máquina"
        
        try:
            CHAVES_VALIDAS[key]["usado"] = True
            CHAVES_VALIDAS[key]["maquina_id"] = machine_id
            
            license_data = {
                'machine_id': machine_id,
                'key': key,
                'activated': True
            }
            
            with open(self.license_file, 'w') as f:
                json.dump(license_data, f)
            
            return True, "Licença ativada com sucesso!"
        except Exception as e:
            return False, f"Erro ao salvar licença: {e}"
    
    def get_license_info(self):
        if not self.license_file.exists():
            return None
        
        try:
            with open(self.license_file, 'r') as f:
                return json.load(f)
        except:
            return None
