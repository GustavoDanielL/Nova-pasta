import customtkinter as ctk
from datetime import datetime, timedelta
from utils.calculos import formatar_moeda
from config import *

# Colors
CARD_BG = ("#ffffff", "#0b1220")
ACCENT = "#3b82f6"

class DashboardView(ctk.CTkFrame):
    def __init__(self, parent, database):
        super().__init__(parent, fg_color="transparent")
        self.database = database
        self.filtro_periodo = "todos"
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
                fg_color=ACCENT if self.filtro_periodo == periodo else "#e5e7eb",
                text_color="white" if self.filtro_periodo == periodo else COLOR_TEXT_PRIMARY,
                hover_color="#d1d5db",
                command=lambda p=periodo: self.aplicar_filtro_periodo(p)
            )
            btn.pack(side="left", padx=2)

        # Stats cards row com hover effect
        stats_frame = ctk.CTkFrame(self, fg_color="transparent")
        stats_frame.pack(pady=12, padx=20, fill="x")

        def make_card(parent, icon, title_text, value_text, color):
            card = ctk.CTkFrame(parent, corner_radius=12, fg_color="#ffffff", 
                               border_width=2, border_color="#e5e7eb")
            card.pack(side="left", padx=8, fill="both", expand=True)
            
            # Bind hover effect
            def on_enter(e):
                card.configure(border_color=color, border_width=2)
            def on_leave(e):
                card.configure(border_color="#e5e7eb", border_width=2)
            
            card.bind("<Enter>", on_enter)
            card.bind("<Leave>", on_leave)
            
            ctk.CTkLabel(card, text=icon, font=("Arial", 32)).pack(pady=(16,8), padx=12)
            ctk.CTkLabel(card, text=title_text, font=FONT_SMALL, 
                        text_color=COLOR_TEXT_SECONDARY).pack(pady=(0,4), padx=12)
            ctk.CTkLabel(card, text=value_text, font=FONT_HEADING, 
                        text_color=color).pack(pady=(0,16), padx=12)
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

        # Seção de Resumo Visual (sem gráficos)
        resumo_frame = ctk.CTkFrame(self, corner_radius=12, fg_color="#ffffff",
                                    border_width=2, border_color="#e5e7eb")
        resumo_frame.pack(pady=12, padx=20, fill="both", expand=True)
        
        ctk.CTkLabel(resumo_frame, text="📊 Resumo dos Empréstimos", 
                    font=FONT_HEADING, text_color=COLOR_TEXT_PRIMARY).pack(pady=(20, 16))
        
        # Lista de empréstimos ativos
        scroll = ctk.CTkScrollableFrame(resumo_frame, fg_color="transparent", height=300)
        scroll.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        emprestimos_ativos_lista = [e for e in emprestimos_filtrados if e.ativo]
        
        if not emprestimos_ativos_lista:
            ctk.CTkLabel(scroll, text="✅ Nenhum empréstimo ativo no período selecionado",
                        font=FONT_NORMAL, text_color=COLOR_SUCCESS).pack(pady=40)
        else:
            for emp in emprestimos_ativos_lista[:10]:  # Mostrar top 10
                cliente = self.database.get_cliente_por_id(emp.cliente_id)
                nome = cliente.nome if cliente else emp.cliente_id
                
                emp_card = ctk.CTkFrame(scroll, corner_radius=8, fg_color="#f9fafb",
                                       border_width=1, border_color="#e5e7eb")
                emp_card.pack(fill="x", pady=6, padx=8)
                
                content = ctk.CTkFrame(emp_card, fg_color="transparent")
                content.pack(fill="x", padx=12, pady=12)
                
                # Nome e ID
                ctk.CTkLabel(content, text=f"👤 {nome} (ID: {emp.id})", 
                           font=FONT_NORMAL, text_color=COLOR_TEXT_PRIMARY,
                           anchor="w").pack(anchor="w")
                
                # Valores
                info_text = f"Emprestado: {formatar_moeda(emp.valor_emprestado)} | Saldo: {formatar_moeda(emp.saldo_devedor)}"
                ctk.CTkLabel(content, text=info_text, 
                           font=FONT_SMALL, text_color=COLOR_TEXT_SECONDARY,
                           anchor="w").pack(anchor="w", pady=(4,0))
    
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
