"""
Script de Migração: JSON → SQLite
Converte dados existentes do formato JSON para SQLite com segurança
"""
import json
from pathlib import Path
from datetime import datetime
import logging

from models.database_sqlite import DatabaseSQLite
from models.cliente import Cliente
from models.emprestimo import Emprestimo
from models.usuario import Usuario

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class JSONMigrator:
    """Migra dados de JSON para SQLite"""
    
    def __init__(self, json_dir: Path, sqlite_path: Path, senha_mestra: str = None):
        """
        Args:
            json_dir: Diretório com arquivos JSON
            sqlite_path: Caminho para novo banco SQLite
            senha_mestra: Senha mestra para criptografia (None = sem criptografia)
        """
        self.json_dir = json_dir
        self.sqlite_path = sqlite_path
        self.senha_mestra = senha_mestra
    
    def migrar(self) -> bool:
        """
        Executa migração completa
        
        Returns:
            True se sucesso, False se erro
        """
        try:
            logger.info("=" * 60)
            logger.info("INICIANDO MIGRAÇÃO JSON → SQLite")
            logger.info("=" * 60)
            
            # Fazer backup dos JSONs antes
            self._backup_json()
            
            # Criar novo banco SQLite
            logger.info(f"Criando banco SQLite em: {self.sqlite_path}")
            db = DatabaseSQLite(self.sqlite_path, self.senha_mestra)
            
            # Migrar clientes
            clientes_migrados = self._migrar_clientes(db)
            logger.info(f"✓ {clientes_migrados} clientes migrados")
            
            # Migrar empréstimos
            emprestimos_migrados = self._migrar_emprestimos(db)
            logger.info(f"✓ {emprestimos_migrados} empréstimos migrados")
            
            # Migrar usuários
            usuarios_migrados = self._migrar_usuarios(db)
            logger.info(f"✓ {usuarios_migrados} usuários migrados")
            
            logger.info("=" * 60)
            logger.info("MIGRAÇÃO CONCLUÍDA COM SUCESSO!")
            logger.info("=" * 60)
            logger.info(f"Clientes: {clientes_migrados}")
            logger.info(f"Empréstimos: {emprestimos_migrados}")
            logger.info(f"Usuários: {usuarios_migrados}")
            logger.info(f"Backup JSON em: {self.json_dir / 'backups'}")
            logger.info("=" * 60)
            
            return True
            
        except Exception as e:
            logger.error(f"ERRO na migração: {e}", exc_info=True)
            return False
    
    def _backup_json(self):
        """Cria backup dos arquivos JSON originais"""
        backup_dir = self.json_dir / "backups"
        backup_dir.mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        for json_file in ['clientes.json', 'emprestimos.json', 'usuarios.json']:
            source = self.json_dir / json_file
            if source.exists():
                dest = backup_dir / f"{json_file.replace('.json', '')}_{timestamp}.json"
                import shutil
                shutil.copy2(source, dest)
                logger.info(f"Backup: {json_file} → {dest.name}")
    
    def _migrar_clientes(self, db: DatabaseSQLite) -> int:
        """Migra clientes do JSON"""
        json_file = self.json_dir / "clientes.json"
        if not json_file.exists():
            logger.warning("Arquivo clientes.json não encontrado")
            return 0
        
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        count = 0
        for cliente_data in data:
            try:
                cliente = Cliente(
                    nome=cliente_data['nome'],
                    cpf_cnpj=cliente_data['cpf_cnpj'],
                    telefone=cliente_data['telefone'],
                    email=cliente_data['email'],
                    endereco=cliente_data.get('endereco', '')
                )
                cliente.id = cliente_data['id']
                cliente.data_cadastro = cliente_data.get('data_cadastro', datetime.now().isoformat())
                
                db.adicionar_cliente(cliente)
                count += 1
            except Exception as e:
                logger.error(f"Erro ao migrar cliente {cliente_data.get('nome')}: {e}")
        
        return count
    
    def _migrar_emprestimos(self, db: DatabaseSQLite) -> int:
        """Migra empréstimos do JSON"""
        json_file = self.json_dir / "emprestimos.json"
        if not json_file.exists():
            logger.warning("Arquivo emprestimos.json não encontrado")
            return 0
        
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        count = 0
        for emp_data in data:
            try:
                emprestimo = Emprestimo(
                    cliente_id=emp_data['cliente_id'],
                    valor_emprestado=float(emp_data['valor_emprestado']),
                    taxa_juros=float(emp_data['taxa_juros']),
                    data_emprestimo=emp_data['data_emprestimo'],
                    data_vencimento=emp_data['data_vencimento'],
                    metodo_calculo=emp_data.get('metodo_calculo', 'simples')
                )
                emprestimo.id = emp_data['id']
                emprestimo.valor_total = float(emp_data['valor_total'])
                emprestimo.saldo_devedor = float(emp_data['saldo_devedor'])
                emprestimo.ativo = emp_data.get('ativo', True)
                emprestimo.observacoes = emp_data.get('observacoes', '')
                emprestimo.pagamentos = emp_data.get('pagamentos', [])
                
                db.adicionar_emprestimo(emprestimo)
                
                # Atualizar pagamentos
                if emprestimo.pagamentos:
                    db.atualizar_emprestimo(emprestimo)
                
                count += 1
            except Exception as e:
                logger.error(f"Erro ao migrar empréstimo {emp_data.get('id')}: {e}")
        
        return count
    
    def _migrar_usuarios(self, db: DatabaseSQLite) -> int:
        """Migra usuários do JSON"""
        json_file = self.json_dir / "usuarios.json"
        if not json_file.exists():
            logger.warning("Arquivo usuarios.json não encontrado")
            return 0
        
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        count = 0
        for user_data in data:
            try:
                usuario = Usuario(user_data['username'], "")
                usuario.password_hash = user_data['password_hash']
                
                db.adicionar_usuario(usuario)
                count += 1
            except Exception as e:
                logger.error(f"Erro ao migrar usuário {user_data.get('username')}: {e}")
        
        return count


def verificar_migracao_necessaria(data_dir: Path) -> bool:
    """
    Verifica se é necessário migrar dados
    
    Returns:
        True se existem JSONs e não existe SQLite
    """
    json_exists = (data_dir / "clientes.json").exists()
    sqlite_exists = (data_dir / "financepro.db").exists()
    
    return json_exists and not sqlite_exists


def executar_migracao_automatica(data_dir: Path, senha_mestra: str = None):
    """
    Executa migração automática se necessário
    
    Args:
        data_dir: Diretório de dados
        senha_mestra: Senha mestra para criptografia
    """
    if verificar_migracao_necessaria(data_dir):
        logger.info("Detectados dados em JSON. Iniciando migração automática...")
        
        sqlite_path = data_dir / "financepro.db"
        migrator = JSONMigrator(data_dir, sqlite_path, senha_mestra)
        
        sucesso = migrator.migrar()
        
        if sucesso:
            logger.info("Migração automática concluída!")
        else:
            logger.error("Falha na migração automática!")
            raise Exception("Erro ao migrar dados para SQLite")


if __name__ == "__main__":
    # Teste de migração
    from pathlib import Path
    
    data_dir = Path.home() / "Documentos" / "FinancePro"
    sqlite_path = data_dir / "financepro.db"
    
    print("=" * 60)
    print("MIGRAÇÃO JSON → SQLite")
    print("=" * 60)
    print(f"Diretório de dados: {data_dir}")
    print(f"Banco SQLite: {sqlite_path}")
    print()
    
    if verificar_migracao_necessaria(data_dir):
        resposta = input("Deseja migrar os dados? (s/n): ")
        if resposta.lower() == 's':
            usar_crypto = input("Usar criptografia? (s/n): ")
            senha = None
            if usar_crypto.lower() == 's':
                senha = input("Digite a senha mestra: ")
            
            migrator = JSONMigrator(data_dir, sqlite_path, senha)
            migrator.migrar()
    else:
        print("Nenhuma migração necessária.")
