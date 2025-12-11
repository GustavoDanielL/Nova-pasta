import customtkinter as ctk
from theme_colors import *

# Usar cores do tema
SIDEBAR_BG = COR_SIDEBAR
CONTENT_BG = COR_CARD
ACCENT = COR_PRIMARIA

class MainView:
    def __init__(self, root, database, license_manager=None):
        self.root = root
        self.database = database
        self.license_manager = license_manager  # Adicionar license_manager
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
        
        # Botão "Sobre" no final
        btn_sobre = ctk.CTkButton(self.sidebar, text="ℹ️ Sobre", command=self.mostrar_sobre,
                                 height=40, fg_color="transparent", anchor="w",
                                 font=("Segoe UI", 12),
                                 text_color=COR_TEXTO_SEC,
                                 hover_color=COR_HOVER)
        btn_sobre.grid(row=20, column=0, padx=12, pady=(6, 12), sticky="ew")
        
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
            print(f"[CACHE] Reutilizando {view_name} do cache (instantâneo)")
            self.view_cache[view_name].pack(fill="both", expand=True)
            self.current_view = view_name
            # NÃO atualizar dados automaticamente - só quando necessário
            # Isso evita re-renderização pesada toda vez
        else:
            print(f"[CACHE] Primeira carga de {view_name}")
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
    
    def mostrar_sobre(self):
        """Mostra guia de uso do sistema"""
        janela = ctk.CTkToplevel(self.root)
        janela.title("Guia de Uso - FinancePro")
        janela.geometry("900x700")
        janela.transient(self.root)
        
        # Frame scrollable
        scroll = ctk.CTkScrollableFrame(janela, fg_color=COR_FUNDO)
        scroll.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Título
        ctk.CTkLabel(scroll, text="GUIA DE USO - FINANCEPRO", 
                    font=("Segoe UI", 24, "bold"),
                    text_color=COR_PRIMARIA).pack(pady=(0, 20))
        
        # Conteúdo do guia
        guia = """
1. CADASTRAR CLIENTE

   Passo 1: Clique no botão verde "Novo Cliente" no topo da tela
   Passo 2: Preencha todos os campos obrigatórios (marcados com *)
   
   - Nome Completo: Digite o nome do cliente
   - CPF ou CNPJ: Digite apenas os números, a formatação é automática
   - Telefone: Digite apenas os números, a formatação é automática
   - Email: Digite o email completo
   - Endereço: Campo opcional
   
   Passo 3: Clique em "Salvar"
   
   PRONTO! O cliente aparece na lista principal.


2. CRIAR EMPRÉSTIMO

   Passo 1: Clique em "Empréstimos" no menu lateral esquerdo
   Passo 2: Clique no botão "Novo Empréstimo"
   Passo 3: Preencha os dados:
   
   - Cliente: Selecione o cliente da lista
   - Valor: Digite o valor do empréstimo (ex: 1000 ou 1500,50)
   - Taxa de Juros: Digite a porcentagem (ex: 5 para 5% ao mês)
   - Prazo: Digite quantos meses (ex: 12)
   - Data Vencimento: Opcional, digite DD/MM/AAAA ou deixe em branco
   
   Passo 4: Clique em "Criar Empréstimo"
   
   PRONTO! O empréstimo foi criado e já calcula os juros automaticamente.


3. REGISTRAR PAGAMENTO

   Passo 1: Na lista de empréstimos, clique no botão "Detalhes"
   Passo 2: Na janela que abrir, clique em "Adicionar Pagamento"
   Passo 3: Digite o valor recebido
   Passo 4: Digite a data do pagamento ou deixe em branco para usar hoje
   Passo 5: Clique em "Registrar"
   
   O sistema atualiza o saldo devedor automaticamente.


4. VER CLIENTES DEVEDORES

   Passo 1: Clique em "Clientes" no menu lateral
   
   Os clientes aparecem com cores:
   - Borda VERMELHA com círculo vermelho: Cliente devendo dinheiro
   - Borda VERDE com check verde: Cliente em dia (sem dívidas)
   - Borda CINZA com círculo vazio: Cliente sem empréstimos


5. ENVIAR COBRANÇA

   Passo 1: Na lista de clientes, procure cliente com borda vermelha
   Passo 2: Clique no botão "Cobrar" (envelope)
   
   Isso abre seu programa de email com mensagem pronta para enviar.


6. DASHBOARD (VISÃO GERAL)

   Clique em "Dashboard" no menu lateral para ver:
   
   - Total emprestado
   - Total a receber
   - Empréstimos ativos
   - Gráficos de desempenho
   
   Use os filtros no topo para ver por cliente ou período.


7. NOTIFICAÇÕES

   Clique em "Notificações" no menu lateral para ver:
   
   - Empréstimos atrasados (precisam cobrar)
   - Lembretes importantes
   
   Lista mostra quem está devendo e quanto.


8. EDITAR OU EXCLUIR

   EDITAR CLIENTE:
   - Vá em Clientes
   - Clique no botão "Editar" (lápis)
   - Altere o que precisar
   - Clique em "Salvar"
   
   EXCLUIR CLIENTE:
   - Vá em Clientes
   - Clique no botão "Excluir" (lixeira)
   - Confirme a exclusão
   
   ATENÇÃO: Não pode excluir cliente com empréstimos ativos!


9. ONDE OS DADOS SÃO SALVOS

   Todos os dados ficam salvos em:
   
   Windows: C:\\Users\\SeuNome\\Documents\\FinancePro
   Linux: /home/seunome/Documentos/FinancePro
   
   IMPORTANTE: Faça backup dessa pasta regularmente!


10. BACKUP MANUAL

    Os dados são salvos automaticamente toda vez que você faz alguma alteração.
    
    Para fazer backup manualmente:
    - Copie a pasta FinancePro de Documentos para um pendrive ou nuvem
    
    Para restaurar backup:
    - Cole a pasta FinancePro de volta em Documentos


DICAS IMPORTANTES:

- Os campos de CPF, telefone e datas formatam sozinhos enquanto você digita
- O sistema calcula juros compostos automaticamente
- Clientes com empréstimos aparecem com cores diferentes
- Use o botão Buscar para encontrar clientes rapidamente
- O Dashboard mostra resumo de tudo


PROBLEMAS COMUNS:

Problema: "Não consigo cadastrar cliente"
Solução: Certifique-se de preencher TODOS os campos obrigatórios (*)

Problema: "Cliente não aparece na lista"
Solução: Use a busca no topo ou role a lista para baixo

Problema: "Empréstimo não foi criado"
Solução: Verifique se o cliente existe antes de criar empréstimo

Problema: "Perdi meus dados"
Solução: Verifique a pasta Documentos/FinancePro
           Se vazia, restaure do backup


LOGIN E SENHA PADRÃO:

Login: admin
Senha: admin123

(Digite exatamente assim, tudo minúsculo)


SUPORTE:

Em caso de dúvidas, entre em contato com o desenvolvedor.


Versão: 1.0
Sistema: FinancePro - Gestão de Empréstimos
"""
        
        # Texto do guia
        texto = ctk.CTkTextbox(scroll, width=800, height=500,
                              font=("Courier New", 11),
                              fg_color=COR_CARD,
                              text_color=COR_TEXTO,
                              wrap="word")
        texto.pack(pady=10, fill="both", expand=True)
        texto.insert("1.0", guia)
        texto.configure(state="disabled")
        
        # Botão fechar
        ctk.CTkButton(scroll, text="Fechar", command=janela.destroy,
                     width=200, height=40,
                     fg_color=COR_PRIMARIA,
                     hover_color=COR_HOVER).pack(pady=20)