import customtkinter as ctk
from tkinter import messagebox
import smtplib
import ssl
import json
from pathlib import Path
from utils import validators
import webbrowser
import urllib.parse
from utils.calculos import formatar_moeda
from models.cliente import Cliente
from theme_colors import *
from config import *

# Theme
CARD_BG = ("#ffffff", "#0b1220")
ACCENT = "#1abc9c"

class ClientesView(ctk.CTkFrame):
    def __init__(self, parent, database):
        super().__init__(parent)
        self.database = database
        self.pack(fill="both", expand=True)
        self._busca_timer = None  # Timer para debounce da busca
        self.criar_widgets()
        # Carregar lista após um pequeno delay para não travar UI
        self.after(100, self.atualizar_lista)
    
    def criar_widgets(self):
        # Frame superior (busca e botões)
        top_frame = ctk.CTkFrame(self, fg_color="transparent")
        top_frame.pack(fill="x", padx=16, pady=12)
        
        # Busca
        ctk.CTkLabel(top_frame, text="Buscar:").pack(side="left", padx=5)
        self.entry_busca = ctk.CTkEntry(top_frame, width=300, placeholder_text="Nome, CPF ou telefone")
        self.entry_busca.pack(side="left", padx=5)
        self.entry_busca.bind("<KeyRelease>", self.buscar_cliente)
        
        # Botão novo cliente
        btn_novo = ctk.CTkButton(top_frame, text="+ Novo Cliente", command=self.criar_cliente, 
                                font=("Segoe UI", 13, "bold"), height=36, corner_radius=8,
                                fg_color=COR_SUCESSO, hover_color=COR_HOVER)
        btn_novo.pack(side="right", padx=5)
        
        # Frame principal
        main_frame = ctk.CTkFrame(self, corner_radius=12, fg_color=CARD_BG)
        main_frame.pack(fill="both", expand=True, padx=12, pady=12)
        
        # Lista de clientes
        self.lista_frame = ctk.CTkScrollableFrame(main_frame, corner_radius=12, fg_color="transparent")
        self.lista_frame.pack(fill="both", expand=True, padx=12, pady=12)
    
    def atualizar_lista(self, clientes=None, forcar=False):
        # Se já foi carregado e não é forçado, não fazer nada
        if hasattr(self, '_lista_carregada') and self._lista_carregada and not forcar:
            return
        
        # Limpar lista atual
        for widget in self.lista_frame.winfo_children():
            widget.destroy()
        
        clientes = clientes or self.database.clientes
        self._lista_carregada = True
        
        if not clientes:
            label = ctk.CTkLabel(self.lista_frame, text="Nenhum cliente cadastrado")
            label.pack(pady=20)
            return
        
        # Cabeçalho profissional
        header_frame = ctk.CTkFrame(self.lista_frame, fg_color=COR_PRIMARIA, corner_radius=8)
        header_frame.pack(fill="x", pady=(0, 8), padx=6)
        
        headers = [
            ("", 0),
            ("Nome", 1),
            ("CPF/CNPJ", 2),
            ("Telefone", 3),
            ("Status", 4)
        ]
        
        for header_text, col in headers:
            # Padx idêntico aos dados dos clientes
            if col == 0:
                padx_val = (12, 8)  # Badge
            elif col == 1:
                padx_val = 8  # Nome
            elif col == 2:
                padx_val = 8  # CPF/CNPJ
            elif col == 3:
                padx_val = 8  # Telefone
            else:
                padx_val = 8  # Status
            
            label = ctk.CTkLabel(header_frame, text=header_text, 
                               font=("Segoe UI", 13, "bold"),
                               text_color="#ffffff")
            label.grid(row=0, column=col, padx=padx_val, pady=10, sticky="w")
        
        # Configurar pesos das colunas do cabeçalho (idêntico aos dados)
        header_frame.grid_columnconfigure(0, weight=0)  # Badge - largura fixa
        header_frame.grid_columnconfigure(1, weight=2)  # Nome - mais espaço
        header_frame.grid_columnconfigure(2, weight=1)  # CPF/CNPJ
        header_frame.grid_columnconfigure(3, weight=1)  # Telefone
        header_frame.grid_columnconfigure(4, weight=1)  # Status
        
        # Label de ações no cabeçalho (alinhado com os botões)
        ctk.CTkLabel(header_frame, text="Ações", 
                    font=("Segoe UI", 13, "bold"),
                    text_color="#ffffff").grid(row=0, column=5, columnspan=4, padx=(3, 8), pady=10, sticky="w")
        
        # Cache de empréstimos por cliente (otimização)
        self.emprestimos_cache = {}
        for emp in self.database.emprestimos:
            if emp.cliente_id not in self.emprestimos_cache:
                self.emprestimos_cache[emp.cliente_id] = []
            self.emprestimos_cache[emp.cliente_id].append(emp)
        
        # Lista de clientes
        for cliente in clientes:
            self.adicionar_cliente_na_lista(cliente)
    
    def adicionar_cliente_na_lista(self, cliente):
        # Calcular status do cliente usando cache
        emprestimos_cliente = self.emprestimos_cache.get(cliente.id, [])
        emprestimos_ativos = [e for e in emprestimos_cliente if e.ativo and e.saldo_devedor > 0]
        
        # Status visual
        if emprestimos_ativos:
            total_devido = sum(e.saldo_devedor for e in emprestimos_ativos)
            badge_color = COR_PERIGO
            badge_icon = "●"
            status_text = f"Devendo {formatar_moeda(total_devido)}"
        elif emprestimos_cliente:
            badge_color = COR_SUCESSO
            badge_icon = "✓"
            status_text = "Em dia"
        else:
            badge_color = COR_BORDA
            badge_icon = "○"
            status_text = "Sem empréstimos"
        
        # Frame do cliente
        frame = ctk.CTkFrame(self.lista_frame, corner_radius=8, fg_color=COR_CARD,
                            border_width=1, border_color=badge_color)
        frame.pack(fill="x", pady=3, padx=6)
        
        # Badge de status
        ctk.CTkLabel(frame, text=badge_icon, text_color=badge_color, 
                    font=("Segoe UI", 16, "bold")).grid(
                    row=0, column=0, padx=(12, 8), pady=10, sticky="w")
        
        # Nome do cliente
        ctk.CTkLabel(frame, text=cliente.nome, text_color=COR_TEXTO, 
                    font=("Segoe UI", 13, "bold")).grid(
                    row=0, column=1, padx=8, pady=10, sticky="w")
        
        # CPF/CNPJ
        ctk.CTkLabel(frame, text=cliente.cpf_cnpj, text_color=COR_TEXTO_SEC,
                    font=("Segoe UI", 12)).grid(row=0, column=2, padx=8, pady=10, sticky="w")
        
        # Telefone
        ctk.CTkLabel(frame, text=cliente.telefone, text_color=COR_TEXTO_SEC,
                    font=("Segoe UI", 12)).grid(row=0, column=3, padx=8, pady=10, sticky="w")
        
        # Status textual
        ctk.CTkLabel(frame, text=status_text, text_color=badge_color,
                    font=("Segoe UI", 11, "bold")).grid(row=0, column=4, padx=8, pady=10, sticky="w")
        
        # Configurar pesos das colunas (idêntico ao cabeçalho)
        frame.grid_columnconfigure(0, weight=0)  # Badge - largura fixa
        frame.grid_columnconfigure(1, weight=2)  # Nome - mais espaço
        frame.grid_columnconfigure(2, weight=1)  # CPF/CNPJ
        frame.grid_columnconfigure(3, weight=1)  # Telefone
        frame.grid_columnconfigure(4, weight=1)  # Status
        
        # Botões de ação compactos (alinhados com cabeçalho 'Ações')
        ctk.CTkButton(frame, text="👁️ Info", width=70, height=32, corner_radius=6,
                     font=("Segoe UI", 11),
                     fg_color=COLOR_BTN_INFO, hover_color=COLOR_BTN_INFO_HOVER,
                     command=lambda: self.mostrar_info_cliente(cliente)).grid(
                     row=0, column=5, padx=(3, 3), pady=10, sticky="w")
        
        ctk.CTkButton(frame, text="✏️ Editar", width=75, height=32, corner_radius=6,
                     font=("Segoe UI", 11),
                     fg_color=COLOR_BTN_PRIMARY, hover_color=COLOR_BTN_PRIMARY_HOVER,
                     command=lambda: self.editar_cliente(cliente)).grid(
                     row=0, column=6, padx=3, pady=10, sticky="w")
        
        ctk.CTkButton(frame, text="🗑️ Excluir", width=80, height=32, corner_radius=6,
                     font=("Segoe UI", 11),
                     fg_color=COLOR_BTN_DANGER, hover_color=COLOR_BTN_DANGER_HOVER,
                     command=lambda: self.excluir_cliente(cliente)).grid(
                     row=0, column=7, padx=3, pady=10, sticky="w")
        
        # Botão de cobrança apenas se há dívida
        if emprestimos_ativos:
            ctk.CTkButton(frame, text="📧 Cobrar", width=85, height=32, corner_radius=6,
                         font=("Segoe UI", 11),
                         fg_color=COLOR_BTN_WARNING, hover_color=COLOR_BTN_WARNING_HOVER,
                         command=lambda: self.enviar_cobranca(cliente)).grid(
                         row=0, column=8, padx=(3, 8), pady=10, sticky="w")
    
    def buscar_cliente(self, event=None):
        # Cancelar timer anterior se existir
        if self._busca_timer:
            self.after_cancel(self._busca_timer)
        
        # Agendar busca após 500ms (debounce)
        self._busca_timer = self.after(500, self._executar_busca)
    
    def _executar_busca(self):
        termo = self.entry_busca.get().strip()
        if termo:
            resultados = self.database.buscar_cliente(termo)
            self.atualizar_lista(resultados, forcar=True)
        else:
            self.atualizar_lista(forcar=True)
    
    def criar_cliente(self):
        self.janela_cliente(None)
    
    def editar_cliente(self, cliente):
        self.janela_cliente(cliente)
    
    def janela_cliente(self, cliente=None):
        from utils.window_utils import configurar_janela_modal
        janela = ctk.CTkToplevel(self)
        titulo = "Novo Cliente" if not cliente else "Editar Cliente"
        configurar_janela_modal(janela, titulo, 650, 550, self)
        janela.configure(fg_color=COLOR_BG_LIGHT)
        
        # Formulário
        form_frame = ctk.CTkFrame(janela, fg_color=FRAME_BG, corner_radius=12,
                                 border_width=1, border_color=FRAME_BORDER)
        form_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        from utils.formatters import formatar_cpf_cnpj, formatar_telefone, limpar_formatacao
        
        campos = [
            ("Nome Completo*", "entry_nome"),
            ("CPF/CNPJ*", "entry_cpf"),
            ("Telefone*", "entry_telefone"),
            ("E-mail*", "entry_email"),
            ("Endereço", "entry_endereco")
        ]

        widgets = {}
        for i, (label, key) in enumerate(campos):
            ctk.CTkLabel(form_frame, text=label, font=("Segoe UI", 12)).grid(
                row=i, column=0, sticky="w", pady=8, padx=(20, 10))
            entry = ctk.CTkEntry(form_frame, width=350, height=36, font=("Segoe UI", 11))
            
            # Adicionar formatação automática
            if key == 'entry_cpf':
                def on_cpf_change(event, e=entry):
                    cursor_pos = e.index("insert")
                    texto = e.get()
                    formatado = formatar_cpf_cnpj(texto)
                    if formatado != texto:
                        e.delete(0, "end")
                        e.insert(0, formatado)
                        e.icursor(min(cursor_pos + (len(formatado) - len(texto)), len(formatado)))
                entry.bind('<KeyRelease>', on_cpf_change)
            
            if key == 'entry_telefone':
                def on_phone_change(event, e=entry):
                    cursor_pos = e.index("insert")
                    texto = e.get()
                    formatado = formatar_telefone(texto)
                    if formatado != texto:
                        e.delete(0, "end")
                        e.insert(0, formatado)
                        e.icursor(min(cursor_pos + (len(formatado) - len(texto)), len(formatado)))
                entry.bind('<KeyRelease>', on_phone_change)
            
            entry.grid(row=i, column=1, padx=(10, 20), pady=8, sticky="ew")
            widgets[key] = entry
        
        # Preencher dados se editando
        if cliente:
            widgets['entry_nome'].insert(0, cliente.nome)
            widgets['entry_cpf'].insert(0, cliente.cpf_cnpj)
            widgets['entry_telefone'].insert(0, cliente.telefone)
            widgets['entry_email'].insert(0, cliente.email)
            widgets['entry_endereco'].insert(0, cliente.endereco)
        
        # Botões
        btn_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        btn_frame.grid(row=len(campos), column=0, columnspan=2, pady=20)
        
        def salvar():
            dados = {
                'nome': widgets['entry_nome'].get().strip(),
                'cpf_cnpj': widgets['entry_cpf'].get().strip(),
                'telefone': widgets['entry_telefone'].get().strip(),
                'email': widgets['entry_email'].get().strip(),
                'endereco': widgets['entry_endereco'].get().strip()
            }
            
            # Validar campos obrigatórios
            if not all([dados['nome'], dados['cpf_cnpj'], dados['telefone'], dados['email']]):
                messagebox.showerror("Erro", "Preencha todos os campos obrigatórios!")
                return
            
            if cliente:
                # Editar cliente existente
                cliente.nome = dados['nome']
                cliente.cpf_cnpj = dados['cpf_cnpj']
                cliente.telefone = dados['telefone']
                cliente.email = dados['email']
                cliente.endereco = dados['endereco']
                messagebox.showinfo("Sucesso", "Cliente atualizado com sucesso!")
            else:
                # Novo cliente
                novo_cliente = Cliente(**dados)
                self.database.adicionar_cliente(novo_cliente)
                messagebox.showinfo("Sucesso", "Cliente cadastrado com sucesso!")
            
            self.database.salvar_dados()
            self.atualizar_lista(forcar=True)
            janela.destroy()
        
        btn_salvar = ctk.CTkButton(btn_frame, text="Salvar", command=salvar)
        btn_salvar.pack(side="left", padx=10)
        
        btn_cancelar = ctk.CTkButton(btn_frame, text="Cancelar", command=janela.destroy)
        btn_cancelar.pack(side="left", padx=10)
    
    def excluir_cliente(self, cliente):
        if messagebox.askyesno("Confirmar", f"Excluir cliente {cliente.nome}?"):
            self.database.clientes.remove(cliente)
            self.database.salvar_dados()
            self.atualizar_lista(forcar=True)
            messagebox.showinfo("Sucesso", "Cliente excluído com sucesso!")

    def mostrar_info_cliente(self, cliente):
        """Abre uma janela mostrando detalhes do cliente, débitos e histórico de empréstimos."""
        from utils.window_utils import configurar_janela_modal
        janela = ctk.CTkToplevel(self)
        configurar_janela_modal(janela, f"Informações - {cliente.nome}", 900, 750, self)
        janela.configure(fg_color=COLOR_BG_LIGHT)

        # Frame principal
        main_frame = ctk.CTkFrame(janela, corner_radius=12, fg_color=FRAME_BG, 
                                 border_width=1, border_color=FRAME_BORDER)
        main_frame.pack(fill="both", expand=True, padx=16, pady=16)

        # Cabeçalho com dados do cliente
        header_frame = ctk.CTkFrame(main_frame, fg_color=COLOR_BG_LIGHT, corner_radius=8)
        header_frame.pack(fill="x", padx=16, pady=16)

        ctk.CTkLabel(header_frame, text=f"👤 {cliente.nome}", 
                    font=FONT_HEADING, text_color=COLOR_TEXT_PRIMARY).pack(anchor="w", padx=12, pady=(12,6))
        ctk.CTkLabel(header_frame, text=f"CPF/CNPJ: {cliente.cpf_cnpj} | Telefone: {cliente.telefone}", 
                    font=FONT_SMALL, text_color=COLOR_TEXT_SECONDARY).pack(anchor="w", padx=12, pady=(0,4))
        ctk.CTkLabel(header_frame, text=f"Email: {cliente.email}", 
                    font=FONT_SMALL, text_color=COLOR_TEXT_SECONDARY).pack(anchor="w", padx=12, pady=(0,4))
        ctk.CTkLabel(header_frame, text=f"Endereço: {cliente.endereco}", 
                    font=FONT_SMALL, text_color=COLOR_TEXT_SECONDARY).pack(anchor="w", padx=12, pady=(0,12))

        # Resumo financeiro em cards
        resumo_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        resumo_frame.pack(fill="x", padx=16, pady=(0, 16))

        # Calcular totais
        emprestimos_cliente = [e for e in self.database.emprestimos if e.cliente_id == cliente.id]
        emprestimos_ativos = [e for e in emprestimos_cliente if e.ativo]
        emprestimos_quitados = [e for e in emprestimos_cliente if not e.ativo]
        
        total_emprestado = sum(getattr(e, 'valor_emprestado', 0.0) for e in emprestimos_cliente)
        total_devido = sum(getattr(e, 'saldo_devedor', 0.0) for e in emprestimos_ativos)
        total_pago = sum(
            sum(float(p.get('valor', 0.0)) for p in getattr(e, 'pagamentos', []))
            for e in emprestimos_cliente
        )

        # Cards de resumo
        def criar_card_resumo(parent, titulo, valor, cor):
            card = ctk.CTkFrame(parent, corner_radius=8, fg_color=FRAME_BG, 
                               border_width=2, border_color=cor)
            card.pack(side="left", fill="both", expand=True, padx=6)
            ctk.CTkLabel(card, text=titulo, font=FONT_SMALL, 
                        text_color=COLOR_TEXT_SECONDARY).pack(pady=(12,4))
            ctk.CTkLabel(card, text=valor, font=FONT_HEADING, 
                        text_color=cor).pack(pady=(0,12))

        criar_card_resumo(resumo_frame, "Total Emprestado", formatar_moeda(total_emprestado), COLOR_BTN_INFO)
        criar_card_resumo(resumo_frame, "Total Devendo", formatar_moeda(total_devido), COLOR_BTN_DANGER)
        criar_card_resumo(resumo_frame, "Total Pago", formatar_moeda(total_pago), COLOR_BTN_SUCCESS)

        # Seção de empréstimos
        hist_label = ctk.CTkLabel(main_frame, text="📋 Empréstimos", font=FONT_HEADING, 
                                 text_color=COLOR_TEXT_PRIMARY)
        hist_label.pack(anchor="w", padx=16, pady=(12,8))

        hist_frame = ctk.CTkFrame(main_frame, corner_radius=8, fg_color=FRAME_BG, 
                                 border_width=1, border_color=FRAME_BORDER)
        hist_frame.pack(fill="both", expand=True, padx=16, pady=(0,12))

        if not emprestimos_cliente:
            ctk.CTkLabel(hist_frame, text="Nenhum empréstimo registrado", 
                        font=FONT_NORMAL, text_color=COLOR_TEXT_SECONDARY).pack(anchor="center", pady=40)
        else:
            # Criar scrollable frame para empréstimos
            scroll_frame = ctk.CTkScrollableFrame(hist_frame, fg_color="transparent")
            scroll_frame.pack(fill="both", expand=True, padx=12, pady=12)

            # Exibir empréstimos ativos primeiro
            if emprestimos_ativos:
                ctk.CTkLabel(scroll_frame, text="🔴 Empréstimos Ativos", 
                            font=FONT_NORMAL, text_color=COLOR_DANGER).pack(anchor="w", pady=(4, 8))
                
                for emp in emprestimos_ativos:
                    emp_frame = ctk.CTkFrame(scroll_frame, corner_radius=8, 
                                            fg_color="#fff5f5",
                                            border_width=1, border_color=COLOR_DANGER)
                    emp_frame.pack(fill="x", pady=6)
                    
                    # Hover effect
                    def on_enter(e, frame=emp_frame):
                        frame.configure(border_width=2)
                    def on_leave(e, frame=emp_frame):
                        frame.configure(border_width=1)
                    
                    emp_frame.bind("<Enter>", on_enter)
                    emp_frame.bind("<Leave>", on_leave)
                    
                    content = ctk.CTkFrame(emp_frame, fg_color="transparent")
                    content.pack(fill="x", padx=12, pady=12)
                    
                    # Info principal
                    ctk.CTkLabel(content, text=f"📄 Empréstimo #{emp.id}", 
                                font=FONT_NORMAL, text_color=COLOR_TEXT_PRIMARY, 
                                anchor="w").pack(anchor="w")
                    
                    # Valores
                    valores_text = (f"Emprestado: {formatar_moeda(emp.valor_emprestado)} | "
                                  f"Total c/ Juros: {formatar_moeda(emp.valor_total)} | "
                                  f"Taxa: {emp.taxa_juros * 100:.1f}%")
                    ctk.CTkLabel(content, text=valores_text, font=FONT_SMALL, 
                                text_color=COLOR_TEXT_SECONDARY, anchor="w").pack(anchor="w", pady=(4,0))
                    
                    # Saldo devedor e pagamentos
                    pagamentos_realizados = len(getattr(emp, 'pagamentos', []))
                    total_pago_emp = sum(float(p.get('valor', 0.0)) for p in getattr(emp, 'pagamentos', []))
                    
                    status_text = (f"💰 Devendo: {formatar_moeda(emp.saldo_devedor)} | "
                                 f"✅ Pago: {formatar_moeda(total_pago_emp)} | "
                                 f"📊 Parcelas pagas: {pagamentos_realizados}")
                    ctk.CTkLabel(content, text=status_text, font=FONT_SMALL, 
                                text_color=COLOR_TEXT_PRIMARY, anchor="w").pack(anchor="w", pady=(4,0))

            # Exibir empréstimos quitados
            if emprestimos_quitados:
                ctk.CTkLabel(scroll_frame, text="✅ Empréstimos Quitados", 
                            font=FONT_NORMAL, text_color=COLOR_SUCCESS).pack(anchor="w", pady=(16, 8))
                
                for emp in emprestimos_quitados:
                    emp_frame = ctk.CTkFrame(scroll_frame, corner_radius=8, 
                                            fg_color="#f0fdf4",
                                            border_width=1, border_color=COLOR_SUCCESS)
                    emp_frame.pack(fill="x", pady=6)
                    
                    # Hover effect
                    def on_enter_q(e, frame=emp_frame):
                        frame.configure(border_width=2)
                    def on_leave_q(e, frame=emp_frame):
                        frame.configure(border_width=1)
                    
                    emp_frame.bind("<Enter>", on_enter_q)
                    emp_frame.bind("<Leave>", on_leave_q)
                    
                    content = ctk.CTkFrame(emp_frame, fg_color="transparent")
                    content.pack(fill="x", padx=12, pady=12)
                    
                    ctk.CTkLabel(content, text=f"📄 Empréstimo #{emp.id} - QUITADO", 
                                font=FONT_NORMAL, text_color=COLOR_TEXT_PRIMARY, 
                                anchor="w").pack(anchor="w")
                    
                    pagamentos_realizados = len(getattr(emp, 'pagamentos', []))
                    info_text = (f"Valor original: {formatar_moeda(emp.valor_emprestado)} | "
                               f"Total pago: {formatar_moeda(emp.valor_total)} | "
                               f"Parcelas: {pagamentos_realizados}")
                    ctk.CTkLabel(content, text=info_text, font=FONT_SMALL, 
                                text_color=COLOR_TEXT_SECONDARY, anchor="w").pack(anchor="w", pady=(4,0))

        # Botão fechar
        btn_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        btn_frame.pack(fill="x", padx=16, pady=12)
        ctk.CTkButton(btn_frame, text="✕ Fechar", height=40, width=120,
                     font=("Segoe UI", 13, "bold"), corner_radius=8,
                     fg_color=COLOR_BTN_SECONDARY, hover_color=COLOR_BTN_SECONDARY_HOVER,
                     command=janela.destroy).pack(pady=8)

    def enviar_cobranca(self, cliente):
        """Abre uma janela com PIX + Email para enviar cobrança ao cliente."""
        # Somar saldo devedor dos empréstimos deste cliente ESPECIFICAMENTE
        total_devido = 0.0
        emprestimos_cliente = []
        for emp in getattr(self.database, 'emprestimos', []):
            if getattr(emp, 'cliente_id', None) == cliente.id and getattr(emp, 'ativo', False):
                saldo = float(getattr(emp, 'saldo_devedor', 0.0))
                if saldo > 0:
                    total_devido += saldo
                    emprestimos_cliente.append(emp)

        # Se não há débitos, avisar
        if total_devido <= 0:
            messagebox.showinfo("Aviso", f"Cliente {cliente.nome} não possui débitos ativos.")
            return

        # Criar janela modal
        from utils.window_utils import configurar_janela_modal
        janela = ctk.CTkToplevel(self)
        configurar_janela_modal(janela, f"Cobrança - {cliente.nome}", 750, 650, self)
        janela.configure(fg_color=COLOR_BG_LIGHT)

        # Frame principal
        main_frame = ctk.CTkFrame(janela, corner_radius=12, fg_color=FRAME_BG,
                                 border_width=1, border_color=FRAME_BORDER)
        main_frame.pack(fill="both", expand=True, padx=12, pady=12)

        # Informações do cliente e valor
        info_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        info_frame.pack(fill="x", padx=16, pady=16)
        
        ctk.CTkLabel(info_frame, text=f"Cliente: {cliente.nome}", font=("Arial", 12, "bold")).pack(anchor="w", pady=(0,6))
        ctk.CTkLabel(info_frame, text=f"Email: {cliente.email}", font=("Arial", 11)).pack(anchor="w", pady=(0,8))
        ctk.CTkLabel(info_frame, text=f"Total em aberto: {formatar_moeda(total_devido)}", 
                     font=("Arial", 14, "bold"), text_color=("#ff6b6b", "#ff9999")).pack(anchor="w")

        # Seção PIX
        pix_label = ctk.CTkLabel(main_frame, text="💳 Código PIX", font=("Arial", 12, "bold"))
        pix_label.pack(anchor="w", padx=16, pady=(16,8))

        pix_frame = ctk.CTkFrame(main_frame, corner_radius=8, fg_color=("#f9f9f9", "#0a1419"), border_width=1, border_color="#1abc9c")
        pix_frame.pack(fill="x", padx=16, pady=(0,16))

        # Campo PIX editável
        entry_pix = ctk.CTkEntry(pix_frame, placeholder_text="Insira aqui o código PIX do seu negócio", height=40, font=("Arial", 11))
        entry_pix.pack(fill="both", expand=True, padx=8, pady=8)
        
        # Se o cliente tiver PIX salvo, preencher
        if hasattr(cliente, 'chave_pix') and cliente.chave_pix:
            entry_pix.insert(0, cliente.chave_pix)

        # Seção Email
        email_label = ctk.CTkLabel(main_frame, text="📧 Mensagem para o Cliente", font=("Arial", 12, "bold"))
        email_label.pack(anchor="w", padx=16, pady=(16,8))

        # Texto padrão
        default_msg = (
            f"Olá {cliente.nome},\n\n"
            f"Segue a cobrança referente aos seus empréstimos.\n"
            f"Total em aberto: {formatar_moeda(total_devido)}\n\n"
            f"Você pode realizar o pagamento via PIX usando o código abaixo:\n"
            f"[CÓDIGO PIX SERÁ INSERIDO AQUI]\n\n"
            f"Qualquer dúvida, entre em contato conosco.\n\n"
            f"Atenciosamente,\nEquipe FinancePro"
        )

        # TextBox para mensagem
        msg_frame = ctk.CTkFrame(main_frame, corner_radius=8, fg_color=("#f9f9f9", "#0a1419"), border_width=1, border_color="#1abc9c")
        msg_frame.pack(fill="both", expand=True, padx=16, pady=(0,16))

        text_msg = ctk.CTkTextbox(msg_frame, font=("Arial", 10))
        text_msg.pack(fill="both", expand=True, padx=8, pady=8)
        text_msg.insert("1.0", default_msg)

        # Botões
        btn_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        btn_frame.pack(fill="x", padx=16, pady=12)

        def enviar_email():
            """Envia o email com PIX e mensagem."""
            email = (cliente.email or '').strip()
            if not email:
                messagebox.showerror("Erro", "Cliente não possui e-mail cadastrado.")
                return

            pix_code = entry_pix.get().strip()
            if not pix_code:
                messagebox.showerror("Erro", "Insira o código PIX.")
                return

            msg_completa = text_msg.get("1.0", "end").strip()
            # Substituir placeholder do PIX pela chave real
            msg_completa = msg_completa.replace("[CÓDIGO PIX SERÁ INSERIDO AQUI]", pix_code)

            # Assunto
            assunto = f"Cobrança FinancePro - {formatar_moeda(total_devido)}"

            # Abrir cliente de email nativo (mailto)
            try:
                mailto_url = f"mailto:{email}?subject={urllib.parse.quote(assunto)}&body={urllib.parse.quote(msg_completa)}"
                webbrowser.open(mailto_url)

                # Salvar PIX no cliente
                if not hasattr(cliente, 'chave_pix'):
                    cliente.chave_pix = ""
                cliente.chave_pix = pix_code
                self.database.salvar_dados()

                messagebox.showinfo("Sucesso", f"✓ Email aberto para {email}\n✓ PIX salvo para futuros contatos.")
                janela.destroy()
            except Exception as e:
                messagebox.showerror("Erro", f"Falha ao abrir email: {e}")

        def enviar_via_smtp():
            """Tenta enviar o e-mail usando configuração SMTP em `data/smtp_config.json`.
            Se não existir, informa e oferece abrir mailto como fallback.
            """
            email = (cliente.email or '').strip()
            if not email:
                messagebox.showerror("Erro", "Cliente não possui e-mail cadastrado.")
                return

            pix_code = entry_pix.get().strip()
            msg_completa = text_msg.get("1.0", "end").strip()
            
            # PIX é opcional - não validar
            if pix_code:
                msg_completa = msg_completa.replace("[CÓDIGO PIX SERÁ INSERIDO AQUI]", pix_code)
            else:
                # Se não houver PIX, remover a linha do placeholder
                msg_completa = msg_completa.replace("[CÓDIGO PIX SERÁ INSERIDO AQUI]\n", "")

            assunto = f"Cobrança FinancePro - {formatar_moeda(total_devido)}"
            
            smtp_file = Path("data/smtp_config.json")
            if not smtp_file.exists():
                if messagebox.askyesno("SMTP não configurado", "Configuração SMTP não encontrada. Deseja abrir o email padrão (mailto)?"):
                    enviar_email()
                return

            try:
                cfg = json.loads(smtp_file.read_text(encoding='utf-8'))
            except Exception as e:
                messagebox.showerror("Erro", f"Falha ao ler config SMTP: {e}")
                return

            required = ['host', 'port', 'username', 'password', 'from_name']
            if not all(k in cfg for k in required):
                messagebox.showerror("Erro", "Arquivo smtp_config.json incompleto. Campos necessários: host, port, username, password, from_name")
                return

            try:
                # Construir mensagem simples
                from_addr = cfg.get('username')
                to_addr = email
                subject = assunto
                body = msg_completa
                message = f"From: {cfg.get('from_name')} <{from_addr}>\r\nTo: {to_addr}\r\nSubject: {subject}\r\n\r\n{body}"

                port = int(cfg.get('port'))
                host = cfg.get('host')

                # Suporta SSL se porta for 465
                if port == 465:
                    context = ssl.create_default_context()
                    with smtplib.SMTP_SSL(host, port, context=context) as server:
                        server.login(cfg.get('username'), cfg.get('password'))
                        server.sendmail(from_addr, [to_addr], message.encode('utf-8'))
                else:
                    server = smtplib.SMTP(host, port, timeout=10)
                    server.starttls(context=ssl.create_default_context())
                    server.login(cfg.get('username'), cfg.get('password'))
                    server.sendmail(from_addr, [to_addr], message.encode('utf-8'))
                    server.quit()

                # Salvar PIX no cliente
                if not hasattr(cliente, 'chave_pix'):
                    cliente.chave_pix = ""
                cliente.chave_pix = pix_code
                self.database.salvar_dados()

                messagebox.showinfo("Sucesso", f"✓ Email enviado via SMTP para {email}\n✓ PIX salvo para futuros contatos.")
                janela.destroy()
            except Exception as e:
                messagebox.showerror("Erro", f"Falha ao enviar via SMTP: {e}")
                # fallback para abrir mailto
                if messagebox.askyesno("Fallback", "Deseja abrir o cliente de e-mail padrão (mailto)?"):
                    enviar_email()

        def copiar_pix():
            """Copia o PIX para a área de transferência."""
            pix_code = entry_pix.get().strip()
            if pix_code:
                import tkinter as tk
                root_temp = tk.Tk()
                root_temp.withdraw()
                root_temp.clipboard_clear()
                root_temp.clipboard_append(pix_code)
                root_temp.update()
                root_temp.destroy()
                messagebox.showinfo("Copiado", "✓ PIX copiado para a área de transferência!")
            else:
                messagebox.showwarning("Aviso", "Nenhum PIX inserido.")

        ctk.CTkButton(btn_frame, text="📋 Copiar PIX", height=36, command=copiar_pix).pack(side="left", padx=6)
        # Abrir no cliente padrão (mailto)
        ctk.CTkButton(btn_frame, text="✉️ Abrir no Email", height=36, font=("Arial", 11, "bold"), 
                 fg_color=("#3498db","#2b7fb4"), command=enviar_email).pack(side="left", padx=6)
        # Envio via SMTP (mais destacado)
        ctk.CTkButton(btn_frame, text="📤 Enviar via SMTP", height=40, font=("Arial", 12, "bold"), 
                 fg_color=("#1abc9c","#16a085"), command=enviar_via_smtp).pack(side="left", padx=6)
        ctk.CTkButton(btn_frame, text="✕ Cancelar", height=36, command=janela.destroy).pack(side="left", padx=6)
        
        # Nota sobre PIX opcional
        ctk.CTkLabel(main_frame, text="🔗 Dica: O código PIX é opcional. Você pode enviar a cobrança sem PIX se desejar.", 
                     font=("Arial", 9), text_color=("#999", "#aaa")).pack(anchor="w", padx=16, pady=(0,8))