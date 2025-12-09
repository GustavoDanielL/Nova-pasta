import customtkinter as ctk
from views.login_view import LoginView
from models.database import Database

class App:
    def __init__(self):
        try:
            # Set light theme with modern appearance
            ctk.set_appearance_mode("Light")
            ctk.set_default_color_theme("blue")
            
            self.db = Database()
            self.db.carregar_dados()
            
            self.root = ctk.CTk()
            self.root.title("Sistema de Empréstimos - FinancePro")
            self.root.geometry("1200x700")
            self.root.minsize(1000, 600)
            
            # Adicionar handler para fechar janela com segurança
            self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
            
            self.login_view = LoginView(self.root, self.db, self.iniciar_sistema)
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
        
    def iniciar_sistema(self):
        try:
            self.login_view.destroy()
            from views.main_view import MainView
            self.main_view = MainView(self.root, self.db)
            # Iniciar notifier em background (DESATIVADO POR SEGURANÇA)
            # Remova o comentário abaixo se quiser reativar
            # try:
            #     from utils.notifier import Notifier
            #     self._notifier = Notifier(self.db)
            #     self._notifier.start()
            # except Exception as e:
            #     print(f"Notifier desativado: {e}")
            #     self._notifier = None
            self._notifier = None
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