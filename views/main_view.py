import customtkinter as ctk
from theme_colors import *

# Usar cores do tema
SIDEBAR_BG = COR_SIDEBAR
CONTENT_BG = COR_CARD
ACCENT = COR_PRIMARIA

class MainView:
    def __init__(self, root, database):
        self.root = root
        self.database = database
        self.view_cache = {}  # Cache para views já carregadas
        self.current_view = None
        
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
                    font=("Segoe UI", 20, "bold"), text_color=ACCENT)
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
                              font=("Segoe UI", 13),
                              text_color=COR_TEXTO,
                              hover_color=COR_HOVER)
            btn.grid(row=i, column=0, padx=12, pady=6, sticky="ew")
        
        # Frame principal
        self.main_frame = ctk.CTkFrame(self.root, corner_radius=12, fg_color=CONTENT_BG)
        self.main_frame.grid(row=0, column=1, sticky="nsew")
        self.main_frame.grid_propagate(False)
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)
    
    def limpar_main_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.pack_forget()  # Usar pack_forget ao invés de destroy para manter o cache
    
    def _carregar_view(self, view_name, view_class, module_path):
        """Carrega view com cache para melhor performance"""
        self.limpar_main_frame()
        
        # Se a view já existe no cache e é a mesma que queremos, apenas re-empacota
        if view_name in self.view_cache:
            self.view_cache[view_name].pack(fill="both", expand=True)
            self.current_view = view_name
            # Atualizar dados se necessário
            if hasattr(self.view_cache[view_name], 'atualizar_lista'):
                self.view_cache[view_name].atualizar_lista()
            elif hasattr(self.view_cache[view_name], 'atualizar_tabela'):
                self.view_cache[view_name].atualizar_tabela()
        else:
            # Carregar a view pela primeira vez
            module = __import__(module_path, fromlist=[view_class])
            view_cls = getattr(module, view_class)
            view = view_cls(self.main_frame, self.database)
            self.view_cache[view_name] = view
            self.current_view = view_name
    
    def mostrar_dashboard(self):
        self._carregar_view('dashboard', 'DashboardView', 'views.dashboard_view')
    
    def mostrar_clientes(self):
        self._carregar_view('clientes', 'ClientesView', 'views.clientes_view')
    
    def mostrar_emprestimos(self):
        self._carregar_view('emprestimos', 'EmprestimosView', 'views.emprestimos_view')
    
    def mostrar_notificacoes(self):
        self._carregar_view('notificacoes', 'NotificacoesView', 'views.notificacoes_view')

    def mostrar_exportacao(self):
        # Exportação e configurações podem não precisar de cache
        self.limpar_main_frame()
        # Limpar cache para forçar reload
        if 'exportacao' in self.view_cache:
            self.view_cache['exportacao'].destroy()
            del self.view_cache['exportacao']
        from views.exportacao_view import ExportacaoView
        ExportacaoView(self.main_frame, self.database)

    def mostrar_configuracoes(self):
        self.limpar_main_frame()
        if 'configuracoes' in self.view_cache:
            self.view_cache['configuracoes'].destroy()
            del self.view_cache['configuracoes']
        from views.settings_view import SettingsView
        SettingsView(self.main_frame, self.database)
    
    def pre_carregar_views(self):
        """Pré-carrega as views principais em background para melhor performance"""
        print("[CACHE] Pré-carregando views...")
        
        # Já temos dashboard carregado no __init__, agora carregar as outras
        def carregar_clientes():
            if 'clientes' not in self.view_cache:
                try:
                    module = __import__('views.clientes_view', fromlist=['ClientesView'])
                    view_cls = getattr(module, 'ClientesView')
                    view = view_cls(self.main_frame, self.database)
                    view.pack_forget()  # Esconder por enquanto
                    self.view_cache['clientes'] = view
                    print("[CACHE] ClientesView carregada")
                except Exception as e:
                    print(f"[CACHE] Erro ao carregar ClientesView: {e}")
        
        def carregar_emprestimos():
            if 'emprestimos' not in self.view_cache:
                try:
                    module = __import__('views.emprestimos_view', fromlist=['EmprestimosView'])
                    view_cls = getattr(module, 'EmprestimosView')
                    view = view_cls(self.main_frame, self.database)
                    view.pack_forget()  # Esconder por enquanto
                    self.view_cache['emprestimos'] = view
                    print("[CACHE] EmprestimosView carregada")
                except Exception as e:
                    print(f"[CACHE] Erro ao carregar EmprestimosView: {e}")
        
        def carregar_notificacoes():
            if 'notificacoes' not in self.view_cache:
                try:
                    module = __import__('views.notificacoes_view', fromlist=['NotificacoesView'])
                    view_cls = getattr(module, 'NotificacoesView')
                    view = view_cls(self.main_frame, self.database)
                    view.pack_forget()  # Esconder por enquanto
                    self.view_cache['notificacoes'] = view
                    print("[CACHE] NotificacoesView carregada")
                except Exception as e:
                    print(f"[CACHE] Erro ao carregar NotificacoesView: {e}")
        
        # Carregar com delays pequenos para não travar UI
        self.root.after(100, carregar_clientes)
        self.root.after(200, carregar_emprestimos)
        self.root.after(300, carregar_notificacoes)
        self.root.after(400, lambda: print("[CACHE] Todas as views pré-carregadas!"))