from datetime import datetime
import os
import hashlib

class Usuario:
    def __init__(self, usuario, password_hash=None, titulo="", id=None):
        self.id = id or self.gerar_id()
        self.usuario = usuario
        # password_hash stores the PBKDF2 serialized string; keep None if not set
        self.password_hash = password_hash
        self.titulo = titulo
        self.data_criacao = datetime.now().isoformat()
        self.ativo = True

    def gerar_id(self):
        return f"USR{datetime.now().strftime('%Y%m%d%H%M%S%f')}"

    @staticmethod
    def hash_password(password, iterations=100000):
        """Hash password using PBKDF2-HMAC-SHA256 and return a serialized string."""
        salt = os.urandom(16)
        dk = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, iterations)
        return f"pbkdf2_sha256${iterations}${salt.hex()}${dk.hex()}"

    @staticmethod
    def verify_password(stored, provided):
        """Verify a provided password against the stored hash.
        Supports legacy plain-text stored passwords: returns (ok, rehash_needed).
        """
        if stored is None:
            return False, False

        if stored.startswith('pbkdf2_sha256$'):
            try:
                _, iter_s, salt_hex, dk_hex = stored.split('$')
                iterations = int(iter_s)
                salt = bytes.fromhex(salt_hex)
                dk_stored = bytes.fromhex(dk_hex)
                dk_check = hashlib.pbkdf2_hmac('sha256', provided.encode('utf-8'), salt, iterations)
                return dk_check == dk_stored, False
            except Exception:
                return False, False
        else:
            # legacy plain-text password — verify and indicate rehash needed
            ok = (stored == provided)
            return ok, ok

    def verificar_senha(self, senha):
        ok, rehash = Usuario.verify_password(self.password_hash, senha)
        return ok

    def to_dict(self):
        return {
            'id': self.id,
            'usuario': self.usuario,
            'password_hash': self.password_hash,
            'titulo': self.titulo,
            'data_criacao': self.data_criacao,
            'ativo': self.ativo
        }

    @classmethod
    def from_dict(cls, data):
        # support legacy key 'senha' or new 'password_hash'
        ph = data.get('password_hash') if data.get('password_hash') is not None else data.get('senha')
        usuario = cls(
            usuario=data['usuario'],
            password_hash=ph,
            titulo=data.get('titulo', ''),
            id=data.get('id')
        )
        usuario.data_criacao = data.get('data_criacao', usuario.data_criacao)
        usuario.ativo = data.get('ativo', True)
        return usuario
