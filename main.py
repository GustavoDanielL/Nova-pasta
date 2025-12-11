import customtkinter as ctk
from views.login_view import LoginView
from models.database import Database
from license_manager import LicenseManager
from tkinter import messagebox

class App:
    def __init__(self):
        try:
            # Set light theme with modern appearance
            ctk.set_appearance_mode("Light")
            ctk.set_default_color_theme("blue")
            
            # Inicializar gerenciador de licenças
            self.license_manager = LicenseManager()
            
            # Inicializar database (cria pasta em Documentos)
            self.db = Database()
            self.db.carregar_dados()
            
            self.root = ctk.CTk()
            self.root.title("Sistema de Empréstimos - FinancePro")
            self.root.geometry("1200x700")
            self.root.minsize(1000, 600)
            
            # Adicionar handler para fechar janela com segurança
            self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
            # Passar license_manager para login_view
            self.login_view = LoginView(self.root, self.db, self.iniciar_sistema, self.license_manager)
        except Exception as e:
            print(f"Erro na inicialização: {e}")
            raise
    
    def on_closing(self):
        """Fecha o app com segurança"""
        try:
            # Parar notifier se existir
            if hasattr(self, '_notifier') and self._notifier:
                self._notifier.stop()
            
            # Salvar dados
            self.db.salvar_dados()
            
            # Fechar janela
            self.root.quit()
            self.root.destroy()
        except Exception as e:
            print(f"Erro ao fechar: {e}")
            self.root.destroy()
        
    def mostrar_loading(self):
        """Mostra indicator de loading no canto"""
        self.loading_label = ctk.CTkLabel(
            self.root, 
            text="⏳ Carregando...",
            font=("Segoe UI", 11),
            text_color="#2563eb",
            fg_color="#e0f2fe",
            corner_radius=8,
            width=140,
            height=35
        )
        self.loading_label.place(relx=0.98, rely=0.02, anchor="ne")
    
    def esconder_loading(self):
        """Esconde loading e mostra notificação de sucesso"""
        if hasattr(self, 'loading_label'):
            self.loading_label.place_forget()
        
        # Mostrar notificação de sucesso
        success_label = ctk.CTkLabel(
            self.root,
            text="✅ Pronto!",
            font=("Segoe UI", 11, "bold"),
            text_color="#10b981",
            fg_color="#d1fae5",
            corner_radius=8,
            width=120,
            height=35
        )
        success_label.place(relx=0.98, rely=0.02, anchor="ne")
        
        # Remover após 2 segundos
        self.root.after(2000, success_label.place_forget)
    
    def iniciar_sistema(self):
        try:
            self.login_view.destroy()
            
            # Mostrar loading
            self.mostrar_loading()
            
            # Carregar MainView em background
            def carregar_views():
                from views.main_view import MainView
                self.main_view = MainView(self.root, self.db, self.license_manager)
                
                # Pré-carregar e cachear as views principais
                self.root.after(50, lambda: self.main_view.pre_carregar_views())
                
                # Esconder loading após tudo carregar
                self.root.after(100, self.esconder_loading)
                
                self._notifier = None
            
            # Executar carregamento após pequeno delay
            self.root.after(50, carregar_views)
            
        except Exception as e:
            print(f"Erro ao iniciar sistema: {e}")
            raise
        
    def run(self):
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            print("\nAplicativo interrompido pelo usuário")
        except Exception as e:
            print(f"Erro durante execução: {e}")
            raise
        finally:
            # Sempre salvar dados ao sair
            try:
                self.db.salvar_dados()
                print("Dados salvos com sucesso")
            except Exception as e:
                print(f"Erro ao salvar dados: {e}")

if __name__ == "__main__":
    try:
        app = App()
        app.run()
    except Exception as e:
        print(f"ERRO CRÍTICO: {e}")
        import traceback
        traceback.print_exc()
        input("Pressione Enter para sair...")