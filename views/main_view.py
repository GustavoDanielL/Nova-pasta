import customtkinter as ctk
from views.clientes_view import ClientesView
from views.emprestimos_view import EmprestimosView
from views.dashboard_view import DashboardView
from views.notificacoes_view import NotificacoesView

# Modern palette: light / dark tuples
SIDEBAR_BG = ("#f4f7fb", "#0f1724")
CONTENT_BG = ("#ffffff", "#0b1220")
ACCENT = "#1abc9c"

class MainView:
    def __init__(self, root, database):
        self.root = root
        self.database = database
        
        self.criar_layout()
        self.mostrar_dashboard()
    
    def criar_layout(self):
        # Configurar grid
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        
        # Sidebar (modern, padded)
        self.sidebar = ctk.CTkFrame(self.root, corner_radius=12, fg_color=SIDEBAR_BG)
        self.sidebar.grid(row=0, column=0, sticky="nsew", padx=(12,6), pady=12)
        self.sidebar.grid_rowconfigure(5, weight=1)
        
        # Logo
        logo_label = ctk.CTkLabel(self.sidebar, text="FinancePro", 
                    font=("Arial", 20, "bold"), text_color=ACCENT)
        logo_label.grid(row=0, column=0, padx=20, pady=20)
        
        # Botões do menu
        # Contador de notificações (empréstimos atrasados)
        try:
            atrasados_count = len(self.database.get_overdue_emprestimos())
        except Exception:
            atrasados_count = 0

        botoes_menu = [
            ("📊 Dashboard", self.mostrar_dashboard),
            ("👥 Clientes", self.mostrar_clientes),
            ("💰 Empréstimos", self.mostrar_emprestimos),
            (f"🔔 Notificações ({atrasados_count})", self.mostrar_notificacoes),
            ("📥 Exportar", self.mostrar_exportacao),
            ("⚙️ Configurações", self.mostrar_configuracoes)
        ]
        
        for i, (texto, comando) in enumerate(botoes_menu, 1):
            btn = ctk.CTkButton(self.sidebar, text=texto, command=comando,
                              height=44, fg_color="transparent", anchor="w", 
                              hover_color=("#e6fffa", "#062926"))
            btn.grid(row=i, column=0, padx=12, pady=6, sticky="ew")
        
        # Frame principal
        self.main_frame = ctk.CTkFrame(self.root, corner_radius=12, fg_color=CONTENT_BG)
        self.main_frame.grid(row=0, column=1, sticky="nsew")
        self.main_frame.grid_propagate(False)
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)
    
    def limpar_main_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()
    
    def mostrar_dashboard(self):
        self.limpar_main_frame()
        DashboardView(self.main_frame, self.database)
    
    def mostrar_clientes(self):
        self.limpar_main_frame()
        ClientesView(self.main_frame, self.database)
    
    def mostrar_emprestimos(self):
        self.limpar_main_frame()
        EmprestimosView(self.main_frame, self.database)
    
    def mostrar_notificacoes(self):
        self.limpar_main_frame()
        NotificacoesView(self.main_frame, self.database)

    def mostrar_exportacao(self):
        self.limpar_main_frame()
        from views.exportacao_view import ExportacaoView
        ExportacaoView(self.main_frame, self.database)

    def mostrar_configuracoes(self):
        self.limpar_main_frame()
        from views.settings_view import SettingsView
        SettingsView(self.main_frame, self.database)