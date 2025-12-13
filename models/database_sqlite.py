"""
Sistema de Banco de Dados com SQLite + Criptografia AES
Substitui JSON por banco relacional seguro
"""
import sqlite3
import json
import threading
from pathlib import Path
from datetime import datetime
from typing import List, Optional
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
import base64
import os
import logging

from models.cliente import Cliente
from models.emprestimo import Emprestimo
from models.usuario import Usuario

logger = logging.getLogger(__name__)


class CryptoManager:
    """Gerencia criptografia de dados sensíveis"""
    
    def __init__(self, senha_mestra: str, salt: bytes = None):
        """
        Inicializa o gerenciador de criptografia
        
        Args:
            senha_mestra: Senha mestra do usuário para derivar chave
            salt: Salt para PBKDF2 (gerado automaticamente se None)
        """
        if salt is None:
            salt = os.urandom(16)
        
        self.salt = salt
        
        # Derivar chave da senha usando PBKDF2HMAC
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend()
        )
        key = base64.urlsafe_b64encode(kdf.derive(senha_mestra.encode()))
        self.cipher = Fernet(key)
    
    def encrypt(self, data: str) -> str:
        """Criptografa string"""
        if not data:
            return ""
        return self.cipher.encrypt(data.encode()).decode()
    
    def decrypt(self, encrypted_data: str) -> str:
        """Descriptografa string"""
        if not encrypted_data:
            return ""
        try:
            return self.cipher.decrypt(encrypted_data.encode()).decode()
        except Exception as e:
            logger.error(f"Erro ao descriptografar: {e}")
            return ""


class DatabaseSQLite:
    """Banco de dados SQLite com criptografia e thread-safe"""
    
    def __init__(self, db_path: Path, senha_mestra: str = None):
        """
        Inicializa o banco de dados
        
        Args:
            db_path: Caminho para o arquivo .db
            senha_mestra: Senha mestra para criptografia (None = sem criptografia)
        """
        self.db_path = db_path
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Lock para operações thread-safe
        self.lock = threading.Lock()
        
        # Gerenciador de criptografia
        self.crypto = None
        if senha_mestra:
            # Carregar ou criar salt
            salt_file = db_path.parent / ".salt"
            if salt_file.exists():
                with open(salt_file, 'rb') as f:
                    salt = f.read()
            else:
                salt = os.urandom(16)
                with open(salt_file, 'wb') as f:
                    f.write(salt)
            
            self.crypto = CryptoManager(senha_mestra, salt)
        
        # Criar tabelas
        self._criar_tabelas()
        
        # Cache de dados
        self._clientes_cache = []
        self._emprestimos_cache = []
        self._usuarios_cache = []
        self._lembretes_cache = []
        self._cache_valido = False
    
    def _criar_tabelas(self):
        """Cria as tabelas do banco"""
        with self.lock:
            conn = sqlite3.connect(str(self.db_path))
            cursor = conn.cursor()
            
            # Tabela de clientes
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS clientes (
                    id TEXT PRIMARY KEY,
                    nome TEXT NOT NULL,
                    cpf_cnpj TEXT NOT NULL,
                    telefone TEXT NOT NULL,
                    email TEXT NOT NULL,
                    endereco TEXT,
                    data_cadastro TEXT NOT NULL
                )
            """)
            
            # Tabela de empréstimos
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS emprestimos (
                    id TEXT PRIMARY KEY,
                    cliente_id TEXT NOT NULL,
                    valor_emprestado REAL NOT NULL,
                    taxa_juros REAL NOT NULL,
                    data_emprestimo TEXT NOT NULL,
                    prazo_meses INTEGER NOT NULL,
                    data_vencimento TEXT NOT NULL,
                    valor_total REAL NOT NULL,
                    saldo_devedor REAL NOT NULL,
                    ativo INTEGER NOT NULL,
                    observacoes TEXT,
                    metodo_calculo TEXT,
                    FOREIGN KEY (cliente_id) REFERENCES clientes(id) ON DELETE CASCADE
                )
            """)
            
            # Tabela de pagamentos
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS pagamentos (
                    id TEXT PRIMARY KEY,
                    emprestimo_id TEXT NOT NULL,
                    data TEXT NOT NULL,
                    valor REAL NOT NULL,
                    tipo TEXT,
                    saldo_anterior REAL,
                    metodo TEXT,
                    FOREIGN KEY (emprestimo_id) REFERENCES emprestimos(id) ON DELETE CASCADE
                )
            """)
            
            # Tabela de usuários
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS usuarios (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL
                )
            """)
            
            # Tabela de lembretes
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS lembretes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    titulo TEXT NOT NULL,
                    descricao TEXT,
                    data TEXT NOT NULL,
                    concluido INTEGER NOT NULL DEFAULT 0
                )
            """)
            
            # Índices para performance
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_emprestimos_cliente ON emprestimos(cliente_id)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_emprestimos_ativo ON emprestimos(ativo)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_pagamentos_emprestimo ON pagamentos(emprestimo_id)")
            
            conn.commit()
            conn.close()
    
    def _encrypt_sensitive(self, data: str) -> str:
        """Criptografa dado sensível se crypto estiver ativo"""
        if self.crypto:
            return self.crypto.encrypt(data)
        return data
    
    def _decrypt_sensitive(self, data: str) -> str:
        """Descriptografa dado sensível se crypto estiver ativo"""
        if self.crypto:
            return self.crypto.decrypt(data)
        return data
    
    # ==================== CLIENTES ====================
    
    @property
    def clientes(self) -> List[Cliente]:
        """Lista de clientes (cache)"""
        if not self._cache_valido:
            self._carregar_cache()
        return self._clientes_cache
    
    def _carregar_cache(self):
        """Carrega dados do banco para cache"""
        with self.lock:
            conn = sqlite3.connect(str(self.db_path))
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            # Carregar clientes
            cursor.execute("SELECT * FROM clientes")
            self._clientes_cache = []
            for row in cursor.fetchall():
                cliente = Cliente(
                    nome=row['nome'],
                    cpf_cnpj=self._decrypt_sensitive(row['cpf_cnpj']),
                    telefone=self._decrypt_sensitive(row['telefone']),
                    email=self._decrypt_sensitive(row['email']),
                    endereco=row['endereco']
                )
                cliente.id = row['id']
                cliente.data_cadastro = row['data_cadastro']
                self._clientes_cache.append(cliente)
            
            # Carregar empréstimos
            cursor.execute("SELECT * FROM emprestimos")
            self._emprestimos_cache = []
            for row in cursor.fetchall():
                # Carregar pagamentos do empréstimo
                cursor.execute("SELECT * FROM pagamentos WHERE emprestimo_id = ?", (row['id'],))
                pagamentos = []
                for p in cursor.fetchall():
                    pag = {
                        'id': p['id'],
                        'valor': p['valor'],
                        'data': p['data'],
                        'tipo': p.get('tipo', 'Parcela'),
                        'saldo_anterior': p.get('saldo_anterior', 0)
                    }
                    if p.get('metodo'):
                        pag['metodo'] = p['metodo']
                    pagamentos.append(pag)
                
                emprestimo = Emprestimo(
                    cliente_id=row['cliente_id'],
                    valor_emprestado=row['valor_emprestado'],
                    taxa_juros=row['taxa_juros'],
                    data_emprestimo=row['data_emprestimo'],
                    prazo_meses=row['prazo_meses'],
                    data_vencimento=row['data_vencimento'],
                    metodo_calculo=row['metodo_calculo']
                )
                emprestimo.id = row['id']
                emprestimo.valor_total = row['valor_total']
                emprestimo.saldo_devedor = row['saldo_devedor']
                emprestimo.ativo = bool(row['ativo'])
                emprestimo.observacoes = row['observacoes']
                emprestimo.pagamentos = pagamentos
                self._emprestimos_cache.append(emprestimo)
            
            # Carregar usuários
            cursor.execute("SELECT * FROM usuarios")
            self._usuarios_cache = []
            for row in cursor.fetchall():
                usuario = Usuario(row['username'], "")
                usuario.password_hash = row['password_hash']
                self._usuarios_cache.append(usuario)
            
            # Carregar lembretes
            cursor.execute("SELECT * FROM lembretes")
            self._lembretes_cache = []
            for row in cursor.fetchall():
                lembrete = {
                    "id": row['id'],
                    "tipo": row['tipo'],
                    "mensagem": row['mensagem'],
                    "data": row['data']
                }
                self._lembretes_cache.append(lembrete)
            
            conn.close()
            self._cache_valido = True
    
    def adicionar_cliente(self, cliente: Cliente):
        """Adiciona novo cliente"""
        with self.lock:
            conn = sqlite3.connect(str(self.db_path))
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO clientes (id, nome, cpf_cnpj, telefone, email, endereco, data_cadastro)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                cliente.id,
                cliente.nome,
                self._encrypt_sensitive(cliente.cpf_cnpj),
                self._encrypt_sensitive(cliente.telefone),
                self._encrypt_sensitive(cliente.email),
                cliente.endereco,
                cliente.data_cadastro
            ))
            
            conn.commit()
            conn.close()
            
            self._clientes_cache.append(cliente)
            logger.info(f"Cliente {cliente.nome} adicionado ao banco")
    
    def buscar_cliente(self, termo: str) -> List[Cliente]:
        """Busca clientes por nome, CPF ou telefone"""
        termo = termo.lower()
        return [c for c in self.clientes 
                if termo in c.nome.lower() 
                or termo in c.cpf_cnpj.lower() 
                or termo in c.telefone.lower()]
    
    def get_cliente_por_id(self, cliente_id: str) -> Optional[Cliente]:
        """Busca cliente por ID"""
        for cliente in self.clientes:
            if cliente.id == cliente_id:
                return cliente
        return None
    
    # ==================== EMPRÉSTIMOS ====================
    
    @property
    def emprestimos(self) -> List[Emprestimo]:
        """Lista de empréstimos (cache)"""
        if not self._cache_valido:
            self._carregar_cache()
        return self._emprestimos_cache
    
    def adicionar_emprestimo(self, emprestimo: Emprestimo):
        """Adiciona novo empréstimo"""
        with self.lock:
            conn = sqlite3.connect(str(self.db_path))
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO emprestimos (
                    id, cliente_id, valor_emprestado, taxa_juros,
                    data_emprestimo, prazo_meses, data_vencimento, valor_total,
                    saldo_devedor, ativo, observacoes, metodo_calculo
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                emprestimo.id,
                emprestimo.cliente_id,
                emprestimo.valor_emprestado,
                emprestimo.taxa_juros,
                emprestimo.data_emprestimo,
                emprestimo.prazo_meses,
                emprestimo.data_vencimento,
                emprestimo.valor_total,
                emprestimo.saldo_devedor,
                1 if emprestimo.ativo else 0,
                emprestimo.observacoes,
                emprestimo.metodo_calculo
            ))
            
            conn.commit()
            conn.close()
            
            self._emprestimos_cache.append(emprestimo)
            logger.info(f"Empréstimo {emprestimo.id} adicionado ao banco")
    
    def atualizar_emprestimo(self, emprestimo: Emprestimo):
        """Atualiza empréstimo existente"""
        with self.lock:
            conn = sqlite3.connect(str(self.db_path))
            cursor = conn.cursor()
            
            cursor.execute("""
                UPDATE emprestimos SET
                    valor_total = ?,
                    saldo_devedor = ?,
                    ativo = ?,
                    observacoes = ?
                WHERE id = ?
            """, (
                emprestimo.valor_total,
                emprestimo.saldo_devedor,
                1 if emprestimo.ativo else 0,
                emprestimo.observacoes,
                emprestimo.id
            ))
            
            # Atualizar pagamentos
            cursor.execute("DELETE FROM pagamentos WHERE emprestimo_id = ?", (emprestimo.id,))
            for pag in emprestimo.pagamentos:
                cursor.execute("""
                    INSERT INTO pagamentos (id, emprestimo_id, data, valor, tipo, saldo_anterior, metodo)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    pag.get('id', f"PGT{datetime.now().strftime('%Y%m%d%H%M%S%f')}"),
                    emprestimo.id,
                    pag['data'],
                    pag['valor'],
                    pag.get('tipo', 'Parcela'),
                    pag.get('saldo_anterior', 0),
                    pag.get('metodo', '')
                ))
            
            conn.commit()
            conn.close()
            logger.info(f"Empréstimo {emprestimo.id} atualizado")
    
    # ==================== USUÁRIOS ====================
    
    @property
    def usuarios(self) -> List[Usuario]:
        """Lista de usuários"""
        if not self._cache_valido:
            self._carregar_cache()
        return self._usuarios_cache
    
    # ==================== LEMBRETES ====================
    
    @property
    def lembretes(self) -> List[dict]:
        """Lista de lembretes"""
        if not self._cache_valido:
            self._carregar_cache()
        return self._lembretes_cache
    
    def adicionar_lembrete(self, tipo: str, mensagem: str, data: str = None):
        """Adiciona um lembrete"""
        if data is None:
            data = datetime.now().isoformat()
        
        with self.lock:
            conn = sqlite3.connect(str(self.db_path))
            cursor = conn.cursor()
            
            lembrete_id = f"LEM{datetime.now().strftime('%Y%m%d%H%M%S%f')}"
            
            cursor.execute("""
                INSERT INTO lembretes (id, tipo, mensagem, data)
                VALUES (?, ?, ?, ?)
            """, (lembrete_id, tipo, mensagem, data))
            
            conn.commit()
            conn.close()
            
            lembrete = {"id": lembrete_id, "tipo": tipo, "mensagem": mensagem, "data": data}
            self._lembretes_cache.append(lembrete)
            logger.info(f"Lembrete adicionado: {tipo}")
        
        return lembrete
    
    def remover_lembrete(self, lembrete_id: str):
        """Remove um lembrete"""
        with self.lock:
            conn = sqlite3.connect(str(self.db_path))
            cursor = conn.cursor()
            
            cursor.execute("DELETE FROM lembretes WHERE id = ?", (lembrete_id,))
            
            conn.commit()
            conn.close()
            
            self._lembretes_cache = [l for l in self._lembretes_cache if l.get('id') != lembrete_id]
            logger.info(f"Lembrete removido: {lembrete_id}")
    
    def adicionar_usuario(self, usuario: Usuario):
        """Adiciona novo usuário"""
        with self.lock:
            conn = sqlite3.connect(str(self.db_path))
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO usuarios (username, password_hash)
                VALUES (?, ?)
            """, (usuario.username, usuario.password_hash))
            
            conn.commit()
            conn.close()
            
            self._usuarios_cache.append(usuario)
            logger.info(f"Usuário {usuario.username} adicionado")
    
    def salvar_dados(self):
        """Salva alterações no banco (já persistido automaticamente)"""
        logger.info("Dados salvos no SQLite")
    
    def get_overdue_emprestimos(self):
        """Retorna empréstimos atrasados (vencidos e não quitados)"""
        atrasados = []
        for emp in self.emprestimos:
            if emp.esta_atrasado():
                atrasados.append(emp)
        return atrasados
    
    def get_emprestimos_by_cliente(self, cliente_id: str):
        """Retorna todos empréstimos de um cliente específico"""
        return [emp for emp in self.emprestimos if emp.cliente_id == cliente_id]
    
    def get_emprestimos_ativos(self):
        """Retorna apenas empréstimos ativos (não quitados)"""
        return [emp for emp in self.emprestimos if emp.ativo and not emp.esta_quitado()]
    
    def fazer_backup(self):
        """Cria backup do banco de dados"""
        backup_dir = self.db_path.parent / "backups"
        backup_dir.mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = backup_dir / f"backup_{timestamp}.db"
        
        with self.lock:
            import shutil
            shutil.copy2(self.db_path, backup_file)
        
        logger.info(f"Backup criado: {backup_file}")
        return backup_file
