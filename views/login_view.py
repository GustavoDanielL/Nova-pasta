import customtkinter as ctk
from tkinter import messagebox
from models.usuario import Usuario
import threading
import time

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
                           font=("Arial", 32, "bold"))
        title.pack(pady=20)
        
        subtitle = ctk.CTkLabel(main_frame, text="Sistema de Gestão de Empréstimos",
                              font=("Arial", 16))
        subtitle.pack(pady=5)
        
        # Frame do formulário (contrasting panel)
        form_frame = ctk.CTkFrame(main_frame, width=400, fg_color=("#f7f7f7", "#3a3a3a"))
        form_frame.pack(pady=40, padx=20)
        
        # Campos de login
        ctk.CTkLabel(form_frame, text="Usuário:", font=("Arial", 14)).pack(pady=10)
        self.entry_usuario = ctk.CTkEntry(form_frame, width=300, height=40)
        self.entry_usuario.pack(pady=10)
        self.entry_usuario.insert(0, "admin")
        
        ctk.CTkLabel(form_frame, text="Senha:", font=("Arial", 14)).pack(pady=10)
        self.entry_senha = ctk.CTkEntry(form_frame, width=300, height=40, show="•")
        self.entry_senha.pack(pady=10)
        self.entry_senha.insert(0, "admin123")
        
        # Botão de login
        btn_login = ctk.CTkButton(form_frame, text="Entrar", 
                                command=self.fazer_login,
                                height=45, font=("Arial", 16))
        btn_login.pack(pady=20)
        
        # Bind Enter para login
        self.entry_senha.bind("<Return>", lambda e: self.fazer_login())
    
    def fazer_login(self):
        usuario = self.entry_usuario.get().strip()
        senha = self.entry_senha.get()
        
        if not usuario or not senha:
            messagebox.showerror("Erro", "Preencha todos os campos!")
            return
        
        # Desabilitar botão e mostrar loading
        btn_login = None
        for widget in self.winfo_children():
            for child in widget.winfo_children() if hasattr(widget, 'winfo_children') else []:
                if isinstance(child, ctk.CTkButton) and "Entrar" in child.cget("text"):
                    btn_login = child
                    break
        
        if btn_login:
            btn_login.configure(state="disabled", text="🔄 Autenticando...")
            self.update()
        
        # Executar login em thread para não bloquear UI
        def fazer_login_async():
            try:
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
                            
                            # Sucesso - chamar callback
                            self.after(500, self.on_login_success)
                            return
                
                # Falha
                self.after(0, lambda: messagebox.showerror("Erro", "Usuário ou senha incorretos!"))
            except Exception as e:
                self.after(0, lambda: messagebox.showerror("Erro", f"Erro durante autenticação: {e}"))
            finally:
                if btn_login:
                    self.after(0, lambda: btn_login.configure(state="normal", text="Entrar"))
        
        # Iniciar thread de login
        login_thread = threading.Thread(target=fazer_login_async, daemon=True)
        login_thread.start()
        