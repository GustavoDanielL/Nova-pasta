import json
from datetime import datetime

class Cliente:
    def __init__(self, nome, cpf_cnpj, telefone, email, endereco, id=None, chave_pix=None):
        self.id = id or self.gerar_id()
        self.nome = nome
        self.cpf_cnpj = cpf_cnpj
        self.telefone = telefone
        self.email = email
        self.endereco = endereco
        self.chave_pix = chave_pix or ""
        self.data_cadastro = datetime.now().isoformat()
        self.ativo = True
        
    def gerar_id(self):
        return f"CLI{datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'cpf_cnpj': self.cpf_cnpj,
            'telefone': self.telefone,
            'email': self.email,
            'endereco': self.endereco,
            'chave_pix': self.chave_pix,
            'data_cadastro': self.data_cadastro,
            'ativo': self.ativo
        }
    
    @classmethod
    def from_dict(cls, data):
        cliente = cls(
            nome=data['nome'],
            cpf_cnpj=data['cpf_cnpj'],
            telefone=data['telefone'],
            email=data['email'],
            endereco=data['endereco'],
            id=data['id'],
            chave_pix=data.get('chave_pix', "")
        )
        cliente.data_cadastro = data['data_cadastro']
        cliente.ativo = data['ativo']
        return cliente