import customtkinter as ctk
from tkinter import messagebox
from models.usuario import Usuario
import threading
import time
from theme_colors import *

class LoginView(ctk.CTkFrame):
    def __init__(self, parent, database, on_login_success):
        super().__init__(parent)
        self.database = database
        self.on_login_success = on_login_success
        
        self.pack(fill="both", expand=True)
        self.criar_widgets()
        
        # Criar usuário admin padrão se não existir (senha será armazenada com hash)
        if not self.database.usuarios:
            admin = Usuario("admin", Usuario.hash_password("admin123"), "Administrador")
            self.database.usuarios.append(admin)
            self.database.salvar_dados()
    
    def criar_widgets(self):
        # Frame principal
        main_frame = ctk.CTkFrame(self, fg_color=COR_FUNDO)
        main_frame.pack(expand=True, fill="both")
        
        # Título
        title = ctk.CTkLabel(main_frame, text="FinancePro", 
                           font=("Segoe UI", 32, "bold"),
                           text_color=COR_PRIMARIA)
        title.pack(pady=20)
        
        subtitle = ctk.CTkLabel(main_frame, text="Sistema de Gestão de Empréstimos",
                              font=("Segoe UI", 16),
                              text_color=COR_TEXTO_SEC)
        subtitle.pack(pady=5)
        
        # Frame do formulário
        form_frame = ctk.CTkFrame(main_frame, width=400, fg_color=COR_CARD,
                                 border_width=2, border_color=COR_BORDA)
        form_frame.pack(pady=40, padx=20)
        
        # Campos de login
        ctk.CTkLabel(form_frame, text="Usuário:", font=("Segoe UI", 14),
                    text_color=COR_TEXTO).pack(pady=10)
        self.entry_usuario = ctk.CTkEntry(form_frame, width=300, height=40,
                                         font=("Segoe UI", 12),
                                         border_color=COR_BORDA)
        self.entry_usuario.pack(pady=10)
        self.entry_usuario.insert(0, "admin")
        
        ctk.CTkLabel(form_frame, text="Senha:", font=("Segoe UI", 14),
                    text_color=COR_TEXTO).pack(pady=10)
        self.entry_senha = ctk.CTkEntry(form_frame, width=300, height=40, show="•",
                                       font=("Segoe UI", 12),
                                       border_color=COR_BORDA)
        self.entry_senha.pack(pady=10)
        self.entry_senha.insert(0, "admin123")
        
        # Botão de login
        btn_login = ctk.CTkButton(form_frame, text="Entrar", 
                                command=self.fazer_login,
                                height=45, font=("Segoe UI", 16, "bold"),
                                fg_color=COR_PRIMARIA,
                                hover_color=COR_SECUNDARIA)
        btn_login.pack(pady=20)
        
        # Bind Enter para login
        self.entry_senha.bind("<Return>", lambda e: self.fazer_login())
    
    def fazer_login(self):
        usuario = self.entry_usuario.get().strip()
        senha = self.entry_senha.get()
        
        if not usuario or not senha:
            messagebox.showerror("Erro", "Preencha todos os campos!")
            return
        
        # Verificar credenciais diretamente (sem thread - fix para Linux)
        for user in self.database.usuarios:
            if user.usuario == usuario:
                # Use verify_password to detect legacy plain-text entries that need re-hash
                ok, rehash = Usuario.verify_password(user.senha, senha)
                if ok:
                    # If password was plain-text, re-hash and persist
                    if rehash:
                        try:
                            user.senha = Usuario.hash_password(senha)
                            self.database.salvar_dados()
                        except Exception:
                            pass
                    
                    # Sucesso - chamar callback diretamente
                    self.on_login_success()
                    return
        
        # Falha
        messagebox.showerror("Erro", "Usuário ou senha incorretos!")
        