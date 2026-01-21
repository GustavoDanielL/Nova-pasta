"""
Gerenciador de Senha Mestra
Tela para configurar senha na primeira execução
"""
import customtkinter as ctk
from tkinter import messagebox
import hashlib
import os
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


class MasterPasswordManager:
    """Gerencia senha mestra do sistema"""
    
    def __init__(self, config_dir: Path):
        """
        Args:
            config_dir: Diretório de configuração (~/.config/FinancePro)
        """
        self.config_dir = config_dir
        self.config_dir.mkdir(parents=True, exist_ok=True)
        self.password_file = config_dir / ".master_password"
    
    def existe_senha(self) -> bool:
        """Verifica se já existe senha configurada"""
        return self.password_file.exists()
    
    def salvar_senha(self, senha: str):
        """
        Salva hash da senha com salt
        
        Args:
            senha: Senha em texto plano
        """
        # Gerar salt aleatório
        salt = os.urandom(32)
        
        # Hash da senha com salt
        pwd_hash = hashlib.pbkdf2_hmac('sha256', senha.encode(), salt, 100000)
        
        # Salvar salt + hash
        with open(self.password_file, 'wb') as f:
            f.write(salt + pwd_hash)
        
        logger.info("Senha mestra configurada")
    
    def verificar_senha(self, senha: str) -> bool:
        """
        Verifica se senha está correta
        
        Args:
            senha: Senha em texto plano
            
        Returns:
            True se senha correta
        """
        if not self.password_file.exists():
            return False
        
        with open(self.password_file, 'rb') as f:
            data = f.read()
        
        # Extrair salt e hash
        salt = data[:32]
        saved_hash = data[32:]
        
        # Calcular hash da senha fornecida
        pwd_hash = hashlib.pbkdf2_hmac('sha256', senha.encode(), salt, 100000)
        
        # Comparar
        return pwd_hash == saved_hash


class MasterPasswordDialog(ctk.CTkToplevel):
    """Dialog para configurar/solicitar senha mestra"""
    
    def __init__(self, parent, manager: MasterPasswordManager, modo='configurar'):
        """
        Args:
            parent: Widget pai
            manager: MasterPasswordManager
            modo: 'configurar' (primeira vez) ou 'solicitar' (login)
        """
        super().__init__(parent)
        
        self.manager = manager
        self.modo = modo
        self.senha_result = None
        
        # Configurar janela
        self.title("Senha Mestra" if modo == 'configurar' else "Autenticação")
        self.geometry("500x400")
        self.resizable(False, False)
        
        # Centralizar
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - (500 // 2)
        y = (self.winfo_screenheight() // 2) - (400 // 2)
        self.geometry(f"500x400+{x}+{y}")
        
        # Modal
        self.transient(parent)
        self.grab_set()
        
        self._criar_interface()
    
    def _criar_interface(self):
        """Cria interface do dialog"""
        # Frame principal
        main_frame = ctk.CTkFrame(self, corner_radius=15)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        if self.modo == 'configurar':
            self._criar_interface_configurar(main_frame)
        else:
            self._criar_interface_solicitar(main_frame)
    
    def _criar_interface_configurar(self, parent):
        """Interface para configurar senha pela primeira vez"""
        # Título
        titulo = ctk.CTkLabel(
            parent,
            text="🔐 Configure sua Senha Mestra",
            font=("Segoe UI", 20, "bold")
        )
        titulo.pack(pady=(20, 10))
        
        # Descrição
        desc = ctk.CTkLabel(
            parent,
            text="Esta senha será usada para proteger seus dados sensíveis.\n"
                 "Escolha uma senha forte e não a esqueça!\n"
                 "Não há recuperação de senha.",
            font=("Segoe UI", 11),
            text_color="gray"
        )
        desc.pack(pady=10)
        
        # Aviso
        aviso = ctk.CTkLabel(
            parent,
            text="⚠️ IMPORTANTE: Anote esta senha em local seguro!",
            font=("Segoe UI", 11, "bold"),
            text_color="#f39c12"
        )
        aviso.pack(pady=10)
        
        # Campos
        ctk.CTkLabel(parent, text="Nova Senha:", font=("Segoe UI", 12)).pack(pady=(20, 5))
        self.entry_senha = ctk.CTkEntry(parent, width=350, height=40, show="●", font=("Segoe UI", 12))
        self.entry_senha.pack(pady=5)
        
        ctk.CTkLabel(parent, text="Confirmar Senha:", font=("Segoe UI", 12)).pack(pady=(10, 5))
        self.entry_confirmar = ctk.CTkEntry(parent, width=350, height=40, show="●", font=("Segoe UI", 12))
        self.entry_confirmar.pack(pady=5)
        
        # Checkbox mostrar senha
        self.var_mostrar = ctk.CTkCheckBox(
            parent,
            text="Mostrar senha",
            command=self._toggle_senha_visivel
        )
        self.var_mostrar.pack(pady=10)
        
        # Botões
        btn_frame = ctk.CTkFrame(parent, fg_color="transparent")
        btn_frame.pack(pady=20)
        
        btn_confirmar = ctk.CTkButton(
            btn_frame,
            text="Confirmar",
            command=self._confirmar_configuracao,
            width=150,
            height=40,
            font=("Segoe UI", 13, "bold"),
            fg_color="#27ae60",
            hover_color="#229954"
        )
        btn_confirmar.pack(side="left", padx=10)
        
        btn_cancelar = ctk.CTkButton(
            btn_frame,
            text="Cancelar",
            command=self._cancelar,
            width=150,
            height=40,
            font=("Segoe UI", 13),
            fg_color="#95a5a6",
            hover_color="#7f8c8d"
        )
        btn_cancelar.pack(side="left", padx=10)
        
        # Focus no primeiro campo
        self.entry_senha.focus()
        
        # Enter para confirmar
        self.entry_confirmar.bind('<Return>', lambda e: self._confirmar_configuracao())
    
    def _criar_interface_solicitar(self, parent):
        """Interface para solicitar senha existente"""
        # Título
        titulo = ctk.CTkLabel(
            parent,
            text="🔐 Senha Mestra",
            font=("Segoe UI", 20, "bold")
        )
        titulo.pack(pady=(40, 10))
        
        # Descrição
        desc = ctk.CTkLabel(
            parent,
            text="Digite sua senha mestra para acessar o sistema",
            font=("Segoe UI", 12),
            text_color="gray"
        )
        desc.pack(pady=10)
        
        # Campo senha
        ctk.CTkLabel(parent, text="Senha:", font=("Segoe UI", 12)).pack(pady=(30, 5))
        self.entry_senha = ctk.CTkEntry(parent, width=350, height=40, show="●", font=("Segoe UI", 12))
        self.entry_senha.pack(pady=5)
        
        # Checkbox mostrar senha
        self.var_mostrar = ctk.CTkCheckBox(
            parent,
            text="Mostrar senha",
            command=self._toggle_senha_visivel
        )
        self.var_mostrar.pack(pady=10)
        
        # Label erro
        self.label_erro = ctk.CTkLabel(parent, text="", text_color="#e74c3c", font=("Segoe UI", 11))
        self.label_erro.pack(pady=5)
        
        # Botões
        btn_frame = ctk.CTkFrame(parent, fg_color="transparent")
        btn_frame.pack(pady=30)
        
        btn_entrar = ctk.CTkButton(
            btn_frame,
            text="Entrar",
            command=self._verificar_senha,
            width=150,
            height=40,
            font=("Segoe UI", 13, "bold"),
            fg_color="#3498db",
            hover_color="#2980b9"
        )
        btn_entrar.pack(side="left", padx=10)
        
        btn_sair = ctk.CTkButton(
            btn_frame,
            text="Sair",
            command=self._sair,
            width=150,
            height=40,
            font=("Segoe UI", 13),
            fg_color="#95a5a6",
            hover_color="#7f8c8d"
        )
        btn_sair.pack(side="left", padx=10)
        
        # Focus no campo
        self.entry_senha.focus()
        
        # Enter para entrar
        self.entry_senha.bind('<Return>', lambda e: self._verificar_senha())
    
    def _toggle_senha_visivel(self):
        """Alterna visibilidade da senha"""
        if self.var_mostrar.get():
            self.entry_senha.configure(show="")
            if hasattr(self, 'entry_confirmar'):
                self.entry_confirmar.configure(show="")
        else:
            self.entry_senha.configure(show="●")
            if hasattr(self, 'entry_confirmar'):
                self.entry_confirmar.configure(show="●")
    
    def _confirmar_configuracao(self):
        """Confirma configuração de nova senha"""
        senha = self.entry_senha.get().strip()
        confirmar = self.entry_confirmar.get().strip()
        
        # Validações
        if not senha:
            messagebox.showerror("Erro", "Digite uma senha!")
            return
        
        if len(senha) < 6:
            messagebox.showerror("Erro", "A senha deve ter no mínimo 6 caracteres!")
            return
        
        if senha != confirmar:
            messagebox.showerror("Erro", "As senhas não coincidem!")
            return
        
        # Salvar senha
        try:
            self.manager.salvar_senha(senha)
            self.senha_result = senha
            messagebox.showinfo(
                "Sucesso",
                "Senha mestra configurada com sucesso!\n\n"
                "⚠️ IMPORTANTE: Anote esta senha em local seguro!\n"
                "Não há recuperação de senha."
            )
            self.destroy()
        except Exception as e:
            logger.error(f"Erro ao salvar senha: {e}")
            messagebox.showerror("Erro", f"Erro ao salvar senha: {e}")
    
    def _verificar_senha(self):
        """Verifica senha informada"""
        senha = self.entry_senha.get().strip()
        
        if not senha:
            self.label_erro.configure(text="Digite a senha!")
            return
        
        if self.manager.verificar_senha(senha):
            self.senha_result = senha
            self.destroy()
        else:
            self.label_erro.configure(text="❌ Senha incorreta!")
            self.entry_senha.delete(0, 'end')
            self.entry_senha.focus()
    
    def _cancelar(self):
        """Cancela configuração"""
        resposta = messagebox.askyesno(
            "Cancelar",
            "Sem senha mestra, seus dados não serão criptografados.\n\n"
            "Deseja continuar sem proteção?"
        )
        if resposta:
            self.senha_result = None
            self.destroy()
    
    def _sair(self):
        """Sai do aplicativo"""
        self.senha_result = None
        self.destroy()
    
    def get_senha(self) -> str:
        """Retorna senha digitada (ou None se cancelou)"""
        return self.senha_result


def solicitar_senha_mestra(parent, config_dir: Path) -> str:
    """
    Solicita senha mestra (configurar ou login)
    
    Args:
        parent: Widget pai
        config_dir: Diretório de configuração
        
    Returns:
        Senha em texto plano (ou None se cancelou/sem senha)
    """
    manager = MasterPasswordManager(config_dir)
    
    if manager.existe_senha():
        # Solicitar senha existente
        dialog = MasterPasswordDialog(parent, manager, modo='solicitar')
    else:
        # Configurar nova senha
        dialog = MasterPasswordDialog(parent, manager, modo='configurar')
    
    parent.wait_window(dialog)
    return dialog.get_senha()
