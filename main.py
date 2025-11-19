import customtkinter as ctk
from views.login_view import LoginView
from models.database import Database

class App:
    def __init__(self):
        # Force dark theme for consistent dark UI
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("blue")
        
        self.db = Database()
        self.db.carregar_dados()
        
        self.root = ctk.CTk()
        self.root.title("Sistema de Empréstimos - FinancePro")
        self.root.geometry("1200x700")
        self.root.minsize(1000, 600)
        
        self.login_view = LoginView(self.root, self.db, self.iniciar_sistema)
        
    def iniciar_sistema(self):
        self.login_view.destroy()
        from views.main_view import MainView
        self.main_view = MainView(self.root, self.db)
        # Iniciar notifier em background
        try:
            from utils.notifier import Notifier
            self._notifier = Notifier(self.db)
            self._notifier.start()
        except Exception:
            self._notifier = None
        
    def run(self):
        self.root.mainloop()
        self.db.salvar_dados()

if __name__ == "__main__":
    app = App()
    app.run()