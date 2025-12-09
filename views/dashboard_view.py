import customtkinter as ctk
from datetime import datetime, timedelta
from utils.calculos import formatar_moeda
from pathlib import Path
from config import *

# Configurar matplotlib para usar backend seguro ANTES de importar pyplot
import matplotlib
matplotlib.use('Agg')  # Backend sem GUI - mais seguro
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

# Colors
CARD_BG = ("#ffffff", "#0b1220")
ACCENT = "#3b82f6"
CHART_COLORS = ["#10b981", "#ef4444", "#f59e0b", "#3b82f6", "#8b5cf6", "#ec4899"]

class DashboardView(ctk.CTkFrame):
    def __init__(self, parent, database):
        super().__init__(parent, fg_color="transparent")
        self.database = database
        self.current_chart = "pizza_status"
        self.fig = None
        self.canvas_widget = None
        self.chart_buttons = {}
        self.filtro_periodo = "todos"  # todos, mes, semana
        self.filtro_cliente = None
        self.pack(fill="both", expand=True)
        self.criar_widgets()

    def criar_widgets(self):
        # Header com título e filtros
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(pady=(16,12), padx=20, fill="x")
        
        title = ctk.CTkLabel(header_frame, text="📊 Dashboard", font=FONT_TITLE, text_color=COLOR_TEXT_PRIMARY)
        title.pack(side="left")
        
        # Filtros
        filtros_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        filtros_frame.pack(side="right")
        
        ctk.CTkLabel(filtros_frame, text="Período:", font=FONT_NORMAL).pack(side="left", padx=(0, 8))
        
        periodos = [("Todos", "todos"), ("Último Mês", "mes"), ("Última Semana", "semana")]
        for label, periodo in periodos:
            btn = ctk.CTkButton(
                filtros_frame, text=label, width=100, height=28,
                font=FONT_SMALL,
                fg_color=ACCENT if self.filtro_periodo == periodo else COLOR_BG_LIGHT,
                text_color="white" if self.filtro_periodo == periodo else COLOR_TEXT_PRIMARY,
                hover_color=COLOR_HOVER,
                command=lambda p=periodo: self.aplicar_filtro_periodo(p)
            )
            btn.pack(side="left", padx=2)

        # Stats cards row com hover effect
        stats_frame = ctk.CTkFrame(self, fg_color="transparent")
        stats_frame.pack(pady=12, padx=20, fill="x")

        def make_card(parent, icon, title_text, value_text, color):
            card = ctk.CTkFrame(parent, corner_radius=12, fg_color=CARD_BG, 
                               border_width=1, border_color=COLOR_BORDER_LIGHT)
            card.pack(side="left", padx=8, fill="both", expand=True)
            
            # Bind hover effect
            def on_enter(e):
                card.configure(border_color=color, border_width=2)
            def on_leave(e):
                card.configure(border_color=COLOR_BORDER_LIGHT, border_width=1)
            
            card.bind("<Enter>", on_enter)
            card.bind("<Leave>", on_leave)
            
            ctk.CTkLabel(card, text=icon, font=("Arial", 24)).pack(pady=(12,4), padx=12)
            ctk.CTkLabel(card, text=title_text, font=FONT_SMALL, 
                        text_color=COLOR_TEXT_SECONDARY).pack(pady=(0,4), padx=12)
            ctk.CTkLabel(card, text=value_text, font=FONT_HEADING, 
                        text_color=color).pack(pady=(0,12), padx=12)
            return card

        # Compute totals com filtro
        emprestimos_filtrados = self.filtrar_emprestimos()
        total_clientes = len(self.database.clientes)
        total_emprestado = sum(getattr(e, 'valor_emprestado', 0.0) for e in emprestimos_filtrados)
        total_owed = sum(getattr(e, 'saldo_devedor', 0.0) for e in emprestimos_filtrados if e.ativo)
        emprestimos_ativos = len([e for e in emprestimos_filtrados if e.ativo])

        make_card(stats_frame, "👥", "Clientes", str(total_clientes), COLOR_INFO)
        make_card(stats_frame, "💰", "Emprestado", formatar_moeda(total_emprestado), COLOR_SUCCESS)
        make_card(stats_frame, "⚠️", "Em Aberto", formatar_moeda(total_owed), COLOR_WARNING)
        make_card(stats_frame, "📈", "Empréstimos Ativos", str(emprestimos_ativos), ACCENT)

        # Chart controls frame
        control_frame = ctk.CTkFrame(self, fg_color="transparent")
        control_frame.pack(pady=12, padx=20, fill="x")

        ctk.CTkLabel(control_frame, text="Visualizações:", font=FONT_NORMAL, 
                    text_color=COLOR_TEXT_PRIMARY).pack(side="left", padx=(0, 12))
        
        chart_options = [
            ("Status", "pizza_status"),
            ("Ativos/Inativos", "pizza_ativo"),
        ]
        
        for label, chart_type in chart_options:
            btn = ctk.CTkButton(
                control_frame,
                text=label,
                width=120,
                height=32,
                font=FONT_SMALL,
                corner_radius=8,
                fg_color=ACCENT if self.current_chart == chart_type else COLOR_BG_LIGHT,
                text_color="white" if self.current_chart == chart_type else COLOR_TEXT_PRIMARY,
                hover_color=COLOR_HOVER if self.current_chart != chart_type else ACCENT,
                command=lambda ct=chart_type: self.trocar_grafico(ct)
            )
            btn.pack(side="left", padx=4)
            self.chart_buttons[chart_type] = btn

        # Chart frame
        self.chart_frame = ctk.CTkFrame(self, corner_radius=12, fg_color=CARD_BG, 
                                       border_width=1, border_color=COLOR_BORDER_LIGHT)
        self.chart_frame.pack(pady=12, padx=20, fill="both", expand=True)

        # Renderizar gráfico inicial
        self.trocar_grafico(self.current_chart)
    
    def filtrar_emprestimos(self):
        """Filtra empréstimos baseado no período selecionado."""
        emprestimos = self.database.emprestimos
        
        if self.filtro_periodo == "todos":
            return emprestimos
        
        hoje = datetime.now()
        
        if self.filtro_periodo == "mes":
            data_limite = hoje - timedelta(days=30)
        elif self.filtro_periodo == "semana":
            data_limite = hoje - timedelta(days=7)
        else:
            return emprestimos
        
        # Filtrar por data de criação
        return [e for e in emprestimos if datetime.fromisoformat(e.data_emprestimo) >= data_limite]
    
    def aplicar_filtro_periodo(self, periodo):
        """Aplica filtro de período e atualiza dashboard."""
        self.filtro_periodo = periodo
        # Recriar widgets com novo filtro
        for widget in self.winfo_children():
            widget.destroy()
        self.criar_widgets()

    def trocar_grafico(self, chart_type):
        """Alterna entre diferentes tipos de gráficos com transição suave."""
        self.current_chart = chart_type
        
        # Atualizar cores dos botões - desativar todos, ativar o selecionado
        for ct, btn in self.chart_buttons.items():
            if ct == chart_type:
                btn.configure(fg_color=ACCENT, text_color="white")
            else:
                btn.configure(fg_color=("#e0e0e0", "#333"), text_color=("black", "white"))
        
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
        ativos = len([e for e in self.database.emprestimos if e.ativo])
        inativos = len([e for e in self.database.emprestimos if not e.ativo])
        
        try:
            atrasados = len(self.database.get_overdue_emprestimos())
        except:
            atrasados = 0

        dados = [ativos - atrasados, atrasados, inativos] if ativos > 0 else [0]
        labels = ["Ativo (em dia)", "Atrasado", "Inativo"]
        cores = ["#27ae60", "#e74c3c", "#95a5a6"]

        fig = Figure(figsize=(6, 4), dpi=100, facecolor='#0b1220' if self._get_appearance() == "Dark" else "#ffffff")
        ax = fig.add_subplot(111)
        wedges, texts, autotexts = ax.pie(dados, labels=labels, colors=cores, autopct='%1.1f%%', startangle=90)
        # Mudar cores das labels para branco
        for text in texts:
            text.set_color('white')
            text.set_fontsize(11)
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontsize(10)
        ax.set_title("Distribuição de Empréstimos por Status", fontsize=12, fontweight='bold', color='white')
        
        self._renderizar_grafico(fig)

    def criar_pizza_ativo(self):
        """Gráfico de pizza: Ativos vs Inativos."""
        ativos = len([e for e in self.database.emprestimos if e.ativo])
        inativos = len([e for e in self.database.emprestimos if not e.ativo])

        dados = [ativos, inativos] if (ativos + inativos) > 0 else [1]
        labels = [f"Ativos ({ativos})", f"Inativos ({inativos})"]
        cores = ["#27ae60", "#95a5a6"]

        fig = Figure(figsize=(6, 4), dpi=100, facecolor='#0b1220' if self._get_appearance() == "Dark" else "#ffffff")
        ax = fig.add_subplot(111)
        wedges, texts, autotexts = ax.pie(dados, labels=labels, colors=cores, autopct='%1.1f%%', startangle=90)
        # Mudar cores das labels para branco
        for text in texts:
            text.set_color('white')
            text.set_fontsize(11)
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontsize(10)
        ax.set_title("Empréstimos: Ativos vs Inativos", fontsize=12, fontweight='bold', color='white')

        self._renderizar_grafico(fig)



    def criar_barras_valores(self):
        """Gráfico de barras: Distribuição de valores de empréstimos."""
        faixas = {
            "0-500": 0,
            "500-1000": 0,
            "1000-5000": 0,
            "5000-10000": 0,
            "10000+": 0
        }

        for emp in self.database.emprestimos:
            valor = getattr(emp, 'valor_emprestado', 0.0)
            if valor < 500:
                faixas["0-500"] += 1
            elif valor < 1000:
                faixas["500-1000"] += 1
            elif valor < 5000:
                faixas["1000-5000"] += 1
            elif valor < 10000:
                faixas["5000-10000"] += 1
            else:
                faixas["10000+"] += 1

        fig = Figure(figsize=(10, 4), dpi=100, facecolor='#0b1220' if self._get_appearance() == "Dark" else "#ffffff")
        ax = fig.add_subplot(111)
        bars = ax.bar(faixas.keys(), faixas.values(), color=CHART_COLORS[:len(faixas)])
        ax.set_ylabel("Quantidade de Empréstimos", color='white')
        ax.set_xlabel("Faixa de Valor (R$)", color='white')
        ax.set_title("Distribuição de Empréstimos por Faixa de Valor", fontsize=12, fontweight='bold', color='white')
        ax.tick_params(axis='x', rotation=45, colors='white')
        ax.tick_params(axis='y', colors='white')

        # Adicionar valores nas barras
        for bar in bars:
            height = bar.get_height()
            if height > 0:
                ax.text(bar.get_x() + bar.get_width()/2., height,
                       f'{int(height)}',
                       ha='center', va='bottom', color='white', fontsize=9)

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
