import customtkinter as ctk
from tkinter import messagebox
from models.usuario import Usuario
import threading
import time
from config import *

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
        # Frame principal (use contrasting colors for light/dark themes)
        # Light background for light mode, darker for dark mode
        main_frame = ctk.CTkFrame(self, fg_color=("#ffffff", "#2b2b2b"))
        # Fill both so widgets are centered and visible across window sizes
        main_frame.pack(expand=True, fill="both")
        
        # Título
        title = ctk.CTkLabel(main_frame, text="FinancePro", 
                           font=FONT_TITLE, text_color=COLOR_TEXT_PRIMARY)
        title.pack(pady=20)
        
        subtitle = ctk.CTkLabel(main_frame, text="Sistema de Gestão de Empréstimos",
                              font=FONT_SUBTITLE, text_color=COLOR_TEXT_SECONDARY)
        subtitle.pack(pady=5)
        
        # Frame do formulário (contrasting panel)
        form_frame = ctk.CTkFrame(main_frame, width=400, fg_color=("#f7f7f7", "#3a3a3a"))
        form_frame.pack(pady=40, padx=20)
        
        # Campos de login
        ctk.CTkLabel(form_frame, text="Usuário:", font=FONT_NORMAL, text_color=COLOR_TEXT_PRIMARY).pack(pady=10)
        self.entry_usuario = ctk.CTkEntry(form_frame, width=300, height=40, font=FONT_NORMAL)
        self.entry_usuario.pack(pady=10)
        self.entry_usuario.insert(0, "admin")
        
        ctk.CTkLabel(form_frame, text="Senha:", font=FONT_NORMAL, text_color=COLOR_TEXT_PRIMARY).pack(pady=10)
        self.entry_senha = ctk.CTkEntry(form_frame, width=300, height=40, show="•", font=FONT_NORMAL)
        self.entry_senha.pack(pady=10)
        self.entry_senha.insert(0, "admin123")
        
        # Botão de login
        btn_login = ctk.CTkButton(form_frame, text="Entrar", 
                                command=self.fazer_login,
                                height=45, font=FONT_BUTTON)
        btn_login.pack(pady=20)
        
        # Bind Enter para login
        self.entry_senha.bind("<Return>", lambda e: self.fazer_login())
    
    def fazer_login(self):
        usuario = self.entry_usuario.get().strip()
        senha = self.entry_senha.get()
        
        if not usuario or not senha:
            messagebox.showerror("Erro", "Preencha todos os campos!")
            return
        
        # Verificar credenciais diretamente (sem thread)
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
        