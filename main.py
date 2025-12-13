import customtkinter as ctk
from views.login_view import LoginView
from models.database_sqlite import DatabaseSQLite
from license_manager import LicenseManager
from utils.json_migrator import executar_migracao_automatica, verificar_migracao_necessaria
from utils.master_password import solicitar_senha_mestra
from utils.logger_config import configurar_logging, log_operacao
from tkinter import messagebox
from pathlib import Path
import logging
import sys

# Configurar logging
logger = configurar_logging()

class App:
    def __init__(self):
        try:
            # Set light theme with modern appearance
            ctk.set_appearance_mode("Light")
            ctk.set_default_color_theme("blue")
            
            # Inicializar gerenciador de licenças
            self.license_manager = LicenseManager()
            
            # Diretório de dados
            data_dir = Path.home() / "Documentos" / "FinancePro"
            config_dir = Path.home() / ".config" / "FinancePro"
            
            # TEMPORÁRIO: Senha mestra desabilitada para teste
            senha_mestra = None
            
            # TODO: Descomentar quando resolver problema de interface
            # # Criar janela temporária para senha mestra
            # temp_root = ctk.CTk()
            # temp_root.withdraw()  # Esconder janela temporária
            # # Solicitar senha mestra (ou None se cancelar/sem senha)
            # senha_mestra = solicitar_senha_mestra(temp_root, config_dir)
            # temp_root.destroy()
            
            # Verificar se precisa migrar JSON → SQLite
            if verificar_migracao_necessaria(data_dir):
                logger.info("Migração de JSON para SQLite necessária")
                executar_migracao_automatica(data_dir, senha_mestra)
            
            # Inicializar database SQLite com criptografia
            db_path = data_dir / "financepro.db"
            self.db = DatabaseSQLite(db_path, senha_mestra)
            
            logger.info("Sistema inicializado com sucesso")
            log_operacao(logger, "Inicialização", True, "Database carregado")
            
            self.root = ctk.CTk()
            self.root.title("Sistema de Empréstimos - FinancePro")
            self.root.geometry("1200x700")
            self.root.minsize(1000, 600)
            
            # Adicionar handler para fechar janela com segurança
            self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
            # Passar license_manager para login_view
            self.login_view = LoginView(self.root, self.db, self.iniciar_sistema, self.license_manager)
        except Exception as e:
            logger.error(f"Erro na inicialização: {e}", exc_info=True)
            messagebox.showerror("Erro Crítico", f"Erro ao inicializar aplicativo:\n{e}")
            raise
    
    def on_closing(self):
        """Fecha o app com segurança"""
        try:
            # Parar notifier se existir
            if hasattr(self, '_notifier') and self._notifier:
                self._notifier.stop()
            
            # Salvar dados
            self.db.salvar_dados()
            logger.info("Aplicativo fechado com sucesso")
            
            # Fechar janela
            self.root.quit()
            self.root.destroy()
        except Exception as e:
            logger.error(f"Erro ao fechar: {e}", exc_info=True)
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
            
            logger.info("Carregando MainView...")
            from views.main_view import MainView
            self.main_view = MainView(self.root, self.db, self.license_manager)
            
            self._notifier = None
            logger.info("Sistema principal carregado")
            
        except Exception as e:
            logger.error(f"Erro ao iniciar sistema: {e}", exc_info=True)
            messagebox.showerror("Erro", f"Erro ao carregar sistema:\n{e}")
            raise
        
    def run(self):
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            logger.warning("Aplicativo interrompido pelo usuário")
        except Exception as e:
            logger.error(f"Erro durante execução: {e}", exc_info=True)
            raise
        finally:
            # Sempre salvar dados ao sair
            try:
                self.db.salvar_dados()
                logger.info("Dados salvos ao sair")
            except Exception as e:
                logger.error(f"Erro ao salvar dados: {e}", exc_info=True)

if __name__ == "__main__":
    try:
        print("=" * 60)
        print("FinancePro - Sistema de Empréstimos")
        print("=" * 60)
        print("Inicializando aplicativo...")
        print(f"Python: {sys.version}")
        print(f"Diretório: {Path.cwd()}")
        print("=" * 60)
        
        app = App()
        print("\n✓ App inicializado com sucesso!")
        print("✓ Abrindo janela principal...\n")
        app.run()
    except Exception as e:
        logger.critical(f"ERRO CRÍTICO: {e}", exc_info=True)
        print(f"\n{'=' * 60}")
        print("✗ ERRO CRÍTICO")
        print(f"{'=' * 60}")
        print(f"{e}")
        print(f"{'=' * 60}\n")
        messagebox.showerror("Erro Crítico", f"O aplicativo encontrou um erro fatal:\n\n{e}\n\nVerifique os logs para mais detalhes.")
        input("Pressione Enter para sair...")