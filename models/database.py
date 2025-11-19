import json
import os
from pathlib import Path
from models.cliente import Cliente
from models.emprestimo import Emprestimo
from models.usuario import Usuario
import shutil
from datetime import datetime, date

class Database:
    def __init__(self):
        self.data_dir = Path("data")
        self.data_dir.mkdir(exist_ok=True)
        
        self.arquivos = {
            'clientes': self.data_dir / "clientes.json",
            'emprestimos': self.data_dir / "emprestimos.json",
            'usuarios': self.data_dir / "usuarios.json",
            'lembretes': self.data_dir / "lembretes.json"
        }
        
        self.clientes = []
        self.emprestimos = []
        self.usuarios = []
        self.lembretes = []
        
    def carregar_dados(self):
        for key, arquivo in self.arquivos.items():
            if arquivo.exists():
                try:
                    with open(arquivo, 'r', encoding='utf-8') as f:
                        dados = json.load(f)
                        
                    if key == 'clientes':
                        self.clientes = [Cliente.from_dict(item) for item in dados]
                    elif key == 'emprestimos':
                        self.emprestimos = [Emprestimo.from_dict(item) for item in dados]
                    elif key == 'usuarios':
                        # Load users; if any user has a legacy plain password, re-hash it for security
                        self.usuarios = [Usuario.from_dict(item) for item in dados]
                        users_changed = False
                        for u in self.usuarios:
                            if u.senha and not str(u.senha).startswith('pbkdf2_sha256$'):
                                # Re-hash plain password
                                try:
                                    hashed = Usuario.hash_password(u.senha)
                                    u.senha = hashed
                                    users_changed = True
                                except Exception:
                                    pass
                        if users_changed:
                            # Save updated users with hashed passwords
                            try:
                                with open(self.arquivos['usuarios'], 'w', encoding='utf-8') as f2:
                                    json.dump([user.to_dict() for user in self.usuarios], f2, indent=2, ensure_ascii=False)
                            except Exception as e:
                                print(f"Erro ao re-salvar usuarios com hash: {e}")
                    elif key == 'lembretes':
                        self.lembretes = dados
                        
                except Exception as e:
                    print(f"Erro ao carregar {arquivo}: {e}")
    
    def salvar_dados(self):
        # Criar pasta de backups
        backup_dir = self.data_dir / "backups"
        backup_dir.mkdir(exist_ok=True)

        for key, arquivo in self.arquivos.items():
            try:
                if key == 'clientes':
                    dados = [cliente.to_dict() for cliente in self.clientes]
                elif key == 'emprestimos':
                    dados = [emp.to_dict() for emp in self.emprestimos]
                elif key == 'usuarios':
                    dados = [user.to_dict() for user in self.usuarios]
                elif key == 'lembretes':
                    dados = self.lembretes

                # Antes de sobrescrever, salvar backup do arquivo existente
                if arquivo.exists():
                    ts = datetime.now().strftime('%Y%m%d%H%M%S')
                    backup_path = backup_dir / f"{arquivo.stem}_{ts}.json"
                    try:
                        shutil.copy2(str(arquivo), str(backup_path))
                    except Exception:
                        pass

                with open(arquivo, 'w', encoding='utf-8') as f:
                    json.dump(dados, f, indent=2, ensure_ascii=False)

            except Exception as e:
                print(f"Erro ao salvar {arquivo}: {e}")

    def get_overdue_emprestimos(self):
        """Retorna lista de empréstimos com parcelas vencidas (heurística mensal)."""
        atrasados = []
        hoje = date.today()
        for emp in self.emprestimos:
            try:
                # data_inicio pode ser YYYY-MM-DD
                data_inicio = emp.data_inicio
                dt = None
                if isinstance(data_inicio, str):
                    try:
                        dt = datetime.strptime(data_inicio[:10], "%Y-%m-%d").date()
                    except Exception:
                        # fallback para data_criacao
                        dt = datetime.strptime(emp.data_criacao[:10], "%Y-%m-%d").date()
                elif isinstance(data_inicio, date):
                    dt = data_inicio
                else:
                    dt = datetime.strptime(emp.data_criacao[:10], "%Y-%m-%d").date()

                # Meses passados desde inicio (aproximado)
                meses_passados = (hoje.year - dt.year) * 12 + (hoje.month - dt.month)
                if meses_passados <= 0:
                    continue

                # Quantas parcelas deveriam ter sido pagas até agora
                parcelas_devidas = min(meses_passados, emp.prazo_meses)
                parcelas_pagas = len([p for p in emp.pagamentos if p.get('tipo') == 'Parcela'])

                if parcelas_pagas < parcelas_devidas and emp.saldo_devedor > 0:
                    atrasados.append(emp)
            except Exception:
                continue

        return atrasados
    
    # Métodos para Clientes
    def adicionar_cliente(self, cliente):
        self.clientes.append(cliente)
        self.salvar_dados()
    
    def buscar_cliente(self, termo):
        termo = termo.lower()
        resultados = []
        for cliente in self.clientes:
            if (termo in cliente.nome.lower() or 
                termo in cliente.cpf_cnpj or 
                termo in cliente.telefone):
                resultados.append(cliente)
        return resultados
    
    def get_cliente_por_id(self, cliente_id):
        for cliente in self.clientes:
            if cliente.id == cliente_id:
                return cliente
        return None
    
    # Métodos para Empréstimos
    def adicionar_emprestimo(self, emprestimo):
        self.emprestimos.append(emprestimo)
        self.salvar_dados()
    
    def get_emprestimos_cliente(self, cliente_id):
        return [emp for emp in self.emprestimos if emp.cliente_id == cliente_id]
    
    def get_emprestimos_ativos(self):
        return [emp for emp in self.emprestimos if emp.ativo]