import customtkinter as ctk
from datetime import datetime
from utils.calculos import formatar_moeda
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from pathlib import Path

# Colors
CARD_BG = ("#ffffff", "#0b1220")
ACCENT = "#1abc9c"
CHART_COLORS = ["#1abc9c", "#e74c3c", "#f39c12", "#27ae60", "#3498db", "#9b59b6"]

class DashboardView(ctk.CTkFrame):
    def __init__(self, parent, database):
        super().__init__(parent, fg_color="transparent")
        self.database = database
        self.current_chart = "pizza_status"  # Default chart type
        self.fig = None
        self.canvas_widget = None
        self.chart_buttons = {}  # Para rastrear os botões
        self.pack(fill="both", expand=True)
        self.criar_widgets()

    def criar_widgets(self):
        # Title
        title = ctk.CTkLabel(self, text="Dashboard", font=("Arial", 24, "bold"), text_color=ACCENT)
        title.pack(pady=(16,12), anchor="w", padx=20)

        # Stats cards row
        stats_frame = ctk.CTkFrame(self, fg_color="transparent")
        stats_frame.pack(pady=12, padx=20, fill="x")

        def make_card(parent, title_text, value_text):
            card = ctk.CTkFrame(parent, corner_radius=12, fg_color=CARD_BG, border_width=2, border_color=ACCENT)
            card.pack(side="left", padx=8, fill="both", expand=True)
            ctk.CTkLabel(card, text=title_text, font=("Arial", 11, "bold"), text_color=("#555","#aaa")).pack(pady=(12,6), padx=12)
            ctk.CTkLabel(card, text=value_text, font=("Arial", 22, "bold"), text_color=ACCENT).pack(pady=(0,12), padx=12)
            return card

        # Compute totals
        total_clientes = len(self.database.clientes)
        total_emprestado = sum(getattr(e, 'valor_emprestado', 0.0) for e in self.database.emprestimos)
        total_owed = sum(getattr(e, 'saldo_devedor', 0.0) for e in self.database.emprestimos)
        total_paid = sum(
            float(p.get('valor', 0.0))
            for e in self.database.emprestimos
            for p in getattr(e, 'pagamentos', [])
        )

        make_card(stats_frame, "Total de Clientes", str(total_clientes))
        make_card(stats_frame, "Total Emprestado", formatar_moeda(total_emprestado))
        make_card(stats_frame, "Total em Aberto", formatar_moeda(total_owed))
        make_card(stats_frame, "Total Pago", formatar_moeda(total_paid))

        # Chart controls frame
        control_frame = ctk.CTkFrame(self, fg_color="transparent")
        control_frame.pack(pady=12, padx=20, fill="x")

        ctk.CTkLabel(control_frame, text="📊 Gráficos:", font=("Arial", 12, "bold")).pack(side="left", padx=(0, 12))
        
        chart_options = [
            ("🥧 Pizza - Status", "pizza_status"),
            ("🥧 Pizza - Ativos/Inativos", "pizza_ativo"),
            ("📊 Barras - Distribuição de Valores", "barras_valores"),
        ]
        
        for label, chart_type in chart_options:
            btn = ctk.CTkButton(
                control_frame,
                text=label,
                width=150,
                height=32,
                fg_color=ACCENT if self.current_chart == chart_type else ("#e0e0e0", "#333"),
                text_color="white" if self.current_chart == chart_type else "black",
                command=lambda ct=chart_type: self.trocar_grafico(ct)
            )
            btn.pack(side="left", padx=4)
            self.chart_buttons[chart_type] = btn  # Salvar referência do botão

        # Chart frame
        self.chart_frame = ctk.CTkFrame(self, corner_radius=12, fg_color=CARD_BG, border_width=2, border_color=ACCENT)
        self.chart_frame.pack(pady=12, padx=20, fill="both", expand=True)

        # Renderizar gráfico inicial
        self.trocar_grafico(self.current_chart)

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
