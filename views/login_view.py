import customtkinter as ctk
from tkinter import messagebox
from models.usuario import Usuario
import threading
import time
from theme_colors import *

class LoginView(ctk.CTkFrame):
    def __init__(self, parent, database, on_login_success, license_manager):
        super().__init__(parent)
        self.database = database
        self.on_login_success = on_login_success
        self.license_manager = license_manager
        
        self.pack(fill="both", expand=True)
        
        # Verificar licença primeiro
        if not self.license_manager.is_licensed():
            self.mostrar_tela_ativacao()
        else:
            self.criar_widgets()
        
        # USUÁRIO PADRÃO (mantido para todas as instalações)
        # Login: admin
        # Senha: admin123
        # Criar usuário admin padrão se não existir (senha armazenada com hash PBKDF2)
        if not self.database.usuarios:
            admin = Usuario("admin", Usuario.hash_password("admin123"), "Administrador")
            self.database.usuarios.append(admin)
            self.database.salvar_dados()
    
    def mostrar_tela_ativacao(self):
        """Tela para cliente digitar a chave de licença"""
        # Limpar tela
        for widget in self.winfo_children():
            widget.destroy()
        
        # Frame principal
        main_frame = ctk.CTkFrame(self, fg_color=COR_FUNDO)
        main_frame.pack(expand=True, fill="both")
        
        # Título
        title = ctk.CTkLabel(main_frame, text="🔐 Ativação de Licença", 
                           font=("Segoe UI", 32, "bold"),
                           text_color=COR_PRIMARIA)
        title.pack(pady=30)
        
        subtitle = ctk.CTkLabel(main_frame, 
                              text="Digite a chave de licença fornecida pelo desenvolvedor",
                              font=("Segoe UI", 14),
                              text_color=COR_TEXTO_SEC)
        subtitle.pack(pady=10)
        
        # Frame do formulário
        form_frame = ctk.CTkFrame(main_frame, width=500, fg_color=COR_CARD,
                                 corner_radius=12, border_width=2, border_color=COR_PRIMARIA)
        form_frame.pack(pady=40, padx=20)
        
        # Campo de chave
        ctk.CTkLabel(form_frame, text="Chave de Licença:", 
                    font=("Segoe UI", 16, "bold"),
                    text_color=COR_TEXTO).pack(pady=20, padx=20)
        
        entry_key = ctk.CTkEntry(form_frame, width=400, height=50,
                                font=("Segoe UI", 14),
                                placeholder_text="Ex: FINANCEPRO-2025-PREMIUM",
                                border_color=COR_PRIMARIA,
                                border_width=2)
        entry_key.pack(pady=10, padx=20)
        
        # Botão ativar
        def ativar():
            key = entry_key.get().strip()
            if not key:
                messagebox.showerror("Erro", "Digite a chave de licença!")
                return
            
            success, message = self.license_manager.activate_license(key)
            
            if success:
                messagebox.showinfo("✅ Sucesso", 
                                  f"{message}\n\nO FinancePro está ativado permanentemente nesta máquina!")
                # Limpar e mostrar tela de login
                for widget in self.winfo_children():
                    widget.destroy()
                self.criar_widgets()
            else:
                messagebox.showerror("❌ Erro", message)
        
        btn_ativar = ctk.CTkButton(form_frame, text="🔓 Ativar Licença",
                                  command=ativar,
                                  width=300, height=50,
                                  font=("Segoe UI", 16, "bold"),
                                  fg_color=COR_SUCESSO,
                                  hover_color=COR_HOVER,
                                  corner_radius=8)
        btn_ativar.pack(pady=30, padx=20)
        
        # Info
        info = ctk.CTkLabel(form_frame, 
                          text="💡 Após ativar, você não precisará digitar a chave novamente\n"
                               "🔒 Cada chave funciona em apenas UMA máquina",
                          font=("Segoe UI", 11),
                          text_color=COR_TEXTO_SEC)
        info.pack(pady=(0, 20), padx=20)
    
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
        
        # Campos de login - ZERADOS (sem auto-preenchimento)
        ctk.CTkLabel(form_frame, text="Usuário:", font=("Segoe UI", 14),
                    text_color=COR_TEXTO).pack(pady=10)
        self.entry_usuario = ctk.CTkEntry(form_frame, width=300, height=40,
                                         font=("Segoe UI", 12),
                                         placeholder_text="Digite o usuário",
                                         border_color=COR_BORDA)
        self.entry_usuario.pack(pady=10)
        # Campo zerado - sem auto-preenchimento
        
        ctk.CTkLabel(form_frame, text="Senha:", font=("Segoe UI", 14),
                    text_color=COR_TEXTO).pack(pady=10)
        self.entry_senha = ctk.CTkEntry(form_frame, width=300, height=40, show="•",
                                       font=("Segoe UI", 12),
                                       placeholder_text="Digite a senha",
                                       border_color=COR_BORDA)
        self.entry_senha.pack(pady=10)
        # Campo zerado - Senha padrão: admin123
        
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
        