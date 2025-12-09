import customtkinter as ctk
from datetime import datetime
from utils.calculos import formatar_moeda
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from pathlib import Path
from theme_colors import *

class DashboardView(ctk.CTkFrame):
    def __init__(self, parent, database):
        super().__init__(parent, fg_color="transparent")
        self.database = database
        self.current_chart = "pizza_status"
        self.fig = None
        self.canvas_widget = None
        self.chart_buttons = {}
        self.filtro_cliente = "todos"  # todos ou ID específico
        self.pack(fill="both", expand=True)
        self.criar_widgets()

    def criar_widgets(self):
        # Header com título e filtros
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(pady=(16,12), padx=20, fill="x")
        
        title = ctk.CTkLabel(header_frame, text="📊 Dashboard", font=("Segoe UI", 24, "bold"), 
                           text_color=COR_TEXTO)
        title.pack(side="left")
        
        # Filtros
        filtros_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        filtros_frame.pack(side="right")
        
        # Filtro de cliente
        ctk.CTkLabel(filtros_frame, text="Cliente:", font=("Segoe UI", 11),
                    text_color=COR_TEXTO).pack(side="left", padx=(0, 8))
        
        clientes_nomes = ["Todos"] + [c.nome for c in self.database.clientes]
        self.cliente_dropdown = ctk.CTkComboBox(filtros_frame, values=clientes_nomes,
                                               width=180, command=self.aplicar_filtros)
        self.cliente_dropdown.set("Todos")
        self.cliente_dropdown.pack(side="left", padx=4)
        
        # Filtro de data inicial
        ctk.CTkLabel(filtros_frame, text="De:", font=("Segoe UI", 11),
                    text_color=COR_TEXTO).pack(side="left", padx=(12, 8))
        
        self.data_inicio = ctk.CTkEntry(filtros_frame, width=110, placeholder_text="DD/MM/AAAA")
        self.data_inicio.pack(side="left", padx=4)
        self.data_inicio.bind("<KeyRelease>", lambda e: self.aplicar_filtros())
        
        # Filtro de data final
        ctk.CTkLabel(filtros_frame, text="Até:", font=("Segoe UI", 11),
                    text_color=COR_TEXTO).pack(side="left", padx=(8, 8))
        
        self.data_fim = ctk.CTkEntry(filtros_frame, width=110, placeholder_text="DD/MM/AAAA")
        self.data_fim.pack(side="left", padx=4)
        self.data_fim.bind("<KeyRelease>", lambda e: self.aplicar_filtros())
        
        # Botão limpar filtros
        ctk.CTkButton(filtros_frame, text="🔄", width=32, height=28,
                     command=self.limpar_filtros, fg_color=COR_TEXTO_SEC,
                     hover_color=COR_HOVER).pack(side="left", padx=(4, 0))

        # Stats cards row
        self.stats_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.stats_frame.pack(pady=12, padx=20, fill="x")
        
        # Info do filtro
        self.filtro_info = ctk.CTkLabel(self, text="📌 Exibindo: Todos os clientes", 
                                       font=("Segoe UI", 10), text_color=COR_TEXTO_SEC)
        self.filtro_info.pack(pady=(0, 8))
        
        self.criar_cards_stats()

        # Chart controls frame
        control_frame = ctk.CTkFrame(self, fg_color="transparent")
        control_frame.pack(pady=12, padx=20, fill="x")

        ctk.CTkLabel(control_frame, text="📊 Gráficos:", font=("Segoe UI", 12, "bold"),
                    text_color=COR_TEXTO).pack(side="left", padx=(0, 12))
        
        chart_options = [
            ("🥧 Pizza - Status", "pizza_status"),
            ("🥧 Pizza - Ativos/Inativos", "pizza_ativo"),
            ("📊 Barras - Distribuição", "barras_valores"),
        ]
        
        for label, chart_type in chart_options:
            btn = ctk.CTkButton(
                control_frame,
                text=label,
                width=150,
                height=32,
                fg_color=COR_PRIMARIA if self.current_chart == chart_type else "transparent",
                text_color="white" if self.current_chart == chart_type else COR_TEXTO,
                border_width=1,
                border_color=COR_PRIMARIA,
                hover_color=COR_HOVER,
                command=lambda ct=chart_type: self.trocar_grafico(ct),
                font=("Segoe UI", 10)
            )
            btn.pack(side="left", padx=4)
            self.chart_buttons[chart_type] = btn

        # Chart frame
        self.chart_frame = ctk.CTkFrame(self, corner_radius=12, fg_color=COR_CARD, 
                                       border_width=1, border_color=COR_BORDA)
        self.chart_frame.pack(pady=12, padx=20, fill="both", expand=True)

        # Renderizar gráfico inicial
        self.trocar_grafico(self.current_chart)

    def aplicar_filtros(self, escolha=None):
        """Aplica filtros de cliente e data nos dados do dashboard"""
        from datetime import datetime
        
        # Filtro de cliente
        escolha = escolha or self.cliente_dropdown.get()
        if escolha == "Todos":
            self.filtro_cliente = "todos"
        else:
            for c in self.database.clientes:
                if c.nome == escolha:
                    self.filtro_cliente = c.id
                    break
        
        # Construir mensagem de filtro
        filtro_msgs = []
        if escolha != "Todos":
            filtro_msgs.append(escolha)
        
        # Validar datas
        data_inicio_str = self.data_inicio.get().strip()
        data_fim_str = self.data_fim.get().strip()
        
        if data_inicio_str or data_fim_str:
            if data_inicio_str:
                filtro_msgs.append(f"De: {data_inicio_str}")
            if data_fim_str:
                filtro_msgs.append(f"Até: {data_fim_str}")
        
        # Atualizar label de info
        if filtro_msgs:
            self.filtro_info.configure(text=f"📌 Filtros: {' | '.join(filtro_msgs)}")
        else:
            self.filtro_info.configure(text="📌 Exibindo: Todos os dados")
        
        # Atualizar dashboard
        self.atualizar_dashboard()
    
    def limpar_filtros(self):
        """Limpa todos os filtros"""
        self.cliente_dropdown.set("Todos")
        self.data_inicio.delete(0, 'end')
        self.data_fim.delete(0, 'end')
        self.aplicar_filtros()
    
    def filtrar_emprestimos(self):
        """Retorna empréstimos filtrados por cliente e data"""
        from datetime import datetime
        
        # Filtro por cliente
        if self.filtro_cliente == "todos":
            emprestimos = self.database.emprestimos
        else:
            emprestimos = [e for e in self.database.emprestimos if e.cliente_id == self.filtro_cliente]
        
        # Filtro por data
        data_inicio_str = self.data_inicio.get().strip()
        data_fim_str = self.data_fim.get().strip()
        
        if data_inicio_str or data_fim_str:
            emprestimos_filtrados = []
            for e in emprestimos:
                try:
                    # Converter data de criação do empréstimo
                    data_emp = datetime.strptime(e.data_criacao[:10], "%Y-%m-%d")
                    
                    # Validar data inicial
                    if data_inicio_str:
                        try:
                            data_inicio = datetime.strptime(data_inicio_str, "%d/%m/%Y")
                            if data_emp < data_inicio:
                                continue
                        except ValueError:
                            pass  # Ignora formato inválido
                    
                    # Validar data final
                    if data_fim_str:
                        try:
                            data_fim = datetime.strptime(data_fim_str, "%d/%m/%Y")
                            if data_emp > data_fim:
                                continue
                        except ValueError:
                            pass  # Ignora formato inválido
                    
                    emprestimos_filtrados.append(e)
                except:
                    emprestimos_filtrados.append(e)  # Inclui se não conseguir validar
            
            return emprestimos_filtrados
        
        return emprestimos
    
    def atualizar_dashboard(self):
        """Atualiza stats e gráficos com base nos filtros"""
        self.criar_cards_stats()
        self.trocar_grafico(self.current_chart)
    
    def trocar_grafico(self, chart_type):
        """Alterna entre diferentes tipos de gráficos com transição suave."""
        self.current_chart = chart_type
        
        # Atualizar cores dos botões
        for ct, btn in self.chart_buttons.items():
            if ct == chart_type:
                btn.configure(fg_color=COR_PRIMARIA, text_color="white")
            else:
                btn.configure(fg_color="transparent", text_color=COR_TEXTO)
        
        # Limpar frame anterior com fade
        if self.canvas_widget:
            self.canvas_widget.pack_forget()
            self.canvas_widget.destroy()
        
        # Pequeno delay para efeito visual de transição
        self.after(100, lambda: self._renderizar_novo_grafico(chart_type))
    
    def _renderizar_novo_grafico(self, chart_type):
        """Renderiza o novo gráfico após pequeno delay."""
        # Limpar frame anterior
        for widget in self.chart_frame.winfo_children():
            widget.destroy()
        
        # Criar novo gráfico
        if chart_type == "pizza_status":
            self.criar_pizza_status()
        elif chart_type == "pizza_ativo":
            self.criar_pizza_ativo()
        elif chart_type == "barras_valores":
            self.criar_barras_valores()

    def criar_pizza_status(self):
        """Gráfico de pizza: Empréstimos em diferentes status."""
        # Filtrar empréstimos
        emprestimos = self.filtrar_emprestimos()
        
        ativos = len([e for e in emprestimos if e.ativo])
        inativos = len([e for e in emprestimos if not e.ativo])
        
        try:
            todos_atrasados = self.database.get_overdue_emprestimos()
            # Filtrar atrasados pelos empréstimos já filtrados
            emprestimos_ids = set(e.id for e in emprestimos)
            todos_atrasados = [e for e in todos_atrasados if e.id in emprestimos_ids]
            atrasados = len(todos_atrasados)
        except:
            atrasados = 0

        dados = [ativos - atrasados, atrasados, inativos] if ativos > 0 else [0, 0, 1]
        labels = ["Ativo (em dia)", "Atrasado", "Inativo"]
        cores = [COR_SUCESSO, COR_PERIGO, COR_TEXTO_SEC]

        fig = Figure(figsize=(6, 4), dpi=100, facecolor="#ffffff")
        ax = fig.add_subplot(111)
        wedges, texts, autotexts = ax.pie(dados, labels=labels, colors=cores, autopct='%1.1f%%', startangle=90)
        
        for text in texts:
            text.set_color(COR_TEXTO)
            text.set_fontsize(11)
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontsize(10)
        ax.set_title("Distribuição por Status", fontsize=13, fontweight='bold', color=COR_TEXTO, pad=20)
        
        self._renderizar_grafico(fig)

    def criar_pizza_ativo(self):
        """Gráfico de pizza: Ativos vs Inativos."""
        # Filtrar empréstimos
        emprestimos = self.filtrar_emprestimos()
        
        ativos = len([e for e in emprestimos if e.ativo])
        inativos = len([e for e in emprestimos if not e.ativo])

        dados = [ativos, inativos] if (ativos + inativos) > 0 else [1]
        labels = [f"Ativos ({ativos})", f"Inativos ({inativos})"]
        cores = [COR_INFO, COR_TEXTO_SEC]

        fig = Figure(figsize=(6, 4), dpi=100, facecolor="#ffffff")
        ax = fig.add_subplot(111)
        wedges, texts, autotexts = ax.pie(dados, labels=labels, colors=cores, autopct='%1.1f%%', startangle=90)
        
        for text in texts:
            text.set_color(COR_TEXTO)
            text.set_fontsize(11)
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontsize(10)
        ax.set_title("Ativos vs Inativos", fontsize=13, fontweight='bold', color=COR_TEXTO, pad=20)

        self._renderizar_grafico(fig)



    def criar_barras_valores(self):
        """Gráfico de barras: Distribuição de valores de empréstimos."""
        # Filtrar empréstimos
        emprestimos = self.filtrar_emprestimos()
        
        faixas = {
            "0-500": 0,
            "500-1k": 0,
            "1k-5k": 0,
            "5k-10k": 0,
            "10k+": 0
        }

        for emp in emprestimos:
            valor = getattr(emp, 'valor_emprestado', 0.0)
            if valor < 500:
                faixas["0-500"] += 1
            elif valor < 1000:
                faixas["500-1k"] += 1
            elif valor < 5000:
                faixas["1k-5k"] += 1
            elif valor < 10000:
                faixas["5k-10k"] += 1
            else:
                faixas["10k+"] += 1

        fig = Figure(figsize=(10, 4), dpi=100, facecolor="#ffffff")
        ax = fig.add_subplot(111)
        
        cores_barras = [COR_INFO, COR_SUCESSO, COR_ALERTA, COR_PERIGO, "#8b5cf6"]
        bars = ax.bar(faixas.keys(), faixas.values(), color=cores_barras)
        
        ax.set_ylabel("Quantidade", color=COR_TEXTO, fontsize=11)
        ax.set_xlabel("Faixa de Valor (R$)", color=COR_TEXTO, fontsize=11)
        ax.set_title("Distribuição por Faixa de Valor", fontsize=13, fontweight='bold', 
                    color=COR_TEXTO, pad=20)
        ax.tick_params(axis='x', rotation=45, colors=COR_TEXTO)
        ax.tick_params(axis='y', colors=COR_TEXTO)

        # Adicionar valores nas barras
        for bar in bars:
            height = bar.get_height()
            if height > 0:
                ax.text(bar.get_x() + bar.get_width()/2., height,
                       f'{int(height)}',
                       ha='center', va='bottom', color=COR_TEXTO, fontsize=9, fontweight='bold')

        fig.tight_layout()
        self._renderizar_grafico(fig)

    def _renderizar_grafico(self, fig):
        """Renderiza figura matplotlib no canvas do CTk com fade-in suave."""
        canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
        canvas.draw()
        self.canvas_widget = canvas.get_tk_widget()
        self.canvas_widget.pack(fill="both", expand=True, padx=12, pady=12)

    def _get_appearance(self):
        """Retorna modo de aparência atual."""
        try:
            return ctk.get_appearance_mode()
        except:
            return "Light"
    
    def criar_cards_stats(self):
        """Cria/atualiza os cards de estatísticas com filtro aplicado"""
        # Limpar cards anteriores
        for widget in self.stats_frame.winfo_children():
            widget.destroy()
        
        # Filtrar empréstimos
        emprestimos_filtrados = self.filtrar_emprestimos()
        
        if self.filtro_cliente == "todos":
            clientes_unicos = set(e.cliente_id for e in emprestimos_filtrados)
            total_clientes = len(clientes_unicos)
        else:
            total_clientes = 1
        
        # Calcular totais
        total_emprestado = sum(getattr(e, 'valor_emprestado', 0.0) for e in emprestimos_filtrados)
        total_owed = sum(getattr(e, 'saldo_devedor', 0.0) for e in emprestimos_filtrados)
        total_paid = sum(
            float(p.get('valor', 0.0))
            for e in emprestimos_filtrados
            for p in getattr(e, 'pagamentos', [])
        )
        
        # Criar cards
        def make_card(parent, title_text, value_text, icon=""):
            card = ctk.CTkFrame(parent, corner_radius=12, fg_color=COR_CARD, 
                              border_width=1, border_color=COR_BORDA)
            card.pack(side="left", padx=8, fill="both", expand=True)
            
            title_label = ctk.CTkLabel(card, text=f"{icon} {title_text}", 
                                      font=("Segoe UI", 11, "bold"), 
                                      text_color=COR_TEXTO_SEC)
            title_label.pack(pady=(12,6), padx=12)
            
            value_label = ctk.CTkLabel(card, text=value_text, 
                                      font=("Segoe UI", 22, "bold"), 
                                      text_color=COR_PRIMARIA)
            value_label.pack(pady=(0,12), padx=12)
            return card
        
        make_card(self.stats_frame, "Clientes", str(total_clientes), "👥")
        make_card(self.stats_frame, "Total Emprestado", formatar_moeda(total_emprestado), "💰")
        make_card(self.stats_frame, "Em Aberto", formatar_moeda(total_owed), "📊")
        make_card(self.stats_frame, "Total Pago", formatar_moeda(total_paid), "✅")
