#!/usr/bin/env python3
"""
Script seguro para rodar o FinancePro com logs detalhados
Use este script para debug se houver problemas
"""
import sys
import os
from datetime import datetime

# Criar arquivo de log
log_file = f"financepro_debug_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

print(f"FinancePro - Modo de Debug")
print(f"Log será salvo em: {log_file}")
print("=" * 60)

# Redirecionar stdout e stderr para arquivo
class Logger:
    def __init__(self, filename):
        self.terminal = sys.stdout
        self.log = open(filename, "w", encoding='utf-8')
    
    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)
        self.log.flush()
    
    def flush(self):
        self.terminal.flush()
        self.log.flush()

sys.stdout = Logger(log_file)
sys.stderr = sys.stdout

print(f"[{datetime.now()}] Iniciando FinancePro...")
print(f"Python: {sys.version}")
print(f"Sistema: {sys.platform}")
print(f"Diretório: {os.getcwd()}")

try:
    print("\n[INFO] Importando módulos...")
    import customtkinter as ctk
    print(f"[OK] CustomTkinter {ctk.__version__}")
    
    from views.login_view import LoginView
    print("[OK] LoginView importado")
    
    from models.database import Database
    print("[OK] Database importado")
    
    print("\n[INFO] Criando aplicação...")
    
    class SafeApp:
        def __init__(self):
            print("[INFO] Configurando tema...")
            ctk.set_appearance_mode("Light")
            ctk.set_default_color_theme("blue")
            
            print("[INFO] Carregando database...")
            self.db = Database()
            self.db.carregar_dados()
            print(f"[OK] Database carregado: {len(self.db.clientes)} clientes, {len(self.db.emprestimos)} empréstimos")
            
            print("[INFO] Criando janela principal...")
            self.root = ctk.CTk()
            self.root.title("Sistema de Empréstimos - FinancePro")
            self.root.geometry("1200x700")
            self.root.minsize(1000, 600)
            
            self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
            
            print("[INFO] Criando tela de login...")
            self.login_view = LoginView(self.root, self.db, self.iniciar_sistema)
            print("[OK] Aplicação iniciada com sucesso!")
        
        def iniciar_sistema(self):
            print("[INFO] Login bem-sucedido, carregando sistema principal...")
            try:
                self.login_view.destroy()
                from views.main_view import MainView
                self.main_view = MainView(self.root, self.db)
                print("[OK] Sistema principal carregado")
            except Exception as e:
                print(f"[ERRO] Falha ao carregar sistema: {e}")
                import traceback
                traceback.print_exc()
        
        def on_closing(self):
            print("[INFO] Fechando aplicação...")
            try:
                self.db.salvar_dados()
                print("[OK] Dados salvos")
                self.root.quit()
                self.root.destroy()
                print("[OK] Aplicação fechada com sucesso")
            except Exception as e:
                print(f"[ERRO] Erro ao fechar: {e}")
                self.root.destroy()
        
        def run(self):
            print("[INFO] Iniciando loop principal...")
            try:
                self.root.mainloop()
            except KeyboardInterrupt:
                print("\n[INFO] Interrompido pelo usuário")
            except Exception as e:
                print(f"[ERRO] Erro no loop principal: {e}")
                import traceback
                traceback.print_exc()
            finally:
                print("[INFO] Salvando dados finais...")
                try:
                    self.db.salvar_dados()
                    print("[OK] Dados salvos")
                except Exception as e:
                    print(f"[ERRO] Falha ao salvar: {e}")
    
    print("\n" + "=" * 60)
    print("INICIANDO APLICAÇÃO")
    print("=" * 60 + "\n")
    
    app = SafeApp()
    app.run()
    
    print("\n" + "=" * 60)
    print("APLICAÇÃO ENCERRADA NORMALMENTE")
    print("=" * 60)

except Exception as e:
    print(f"\n{'=' * 60}")
    print("ERRO CRÍTICO!")
    print("=" * 60)
    print(f"Erro: {e}")
    import traceback
    traceback.print_exc()
    print("=" * 60)
    input("\nPressione Enter para sair...")

print(f"\nLog salvo em: {log_file}")
