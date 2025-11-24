import customtkinter as ctk
from tkinter import messagebox, ttk
import tkinter as tk
from models.emprestimo import Emprestimo
from datetime import datetime
from utils.calculos import formatar_moeda
from utils import validators

CARD_BG = ("#0b1220", "#0b1220")
ACCENT = "#1abc9c"

class EmprestimosView(ctk.CTkFrame):
    def __init__(self, parent, database):
        super().__init__(parent)
        self.database = database
        self.pack(fill="both", expand=True)
        self.criar_widgets()

    def criar_widgets(self):
        title = ctk.CTkLabel(self, text="Empréstimos", font=("Arial", 24, "bold"), text_color=ACCENT)
        title.pack(pady=(16,12), anchor="w", padx=20)

        # Simple filter frame - just search by client name
        filter_frame = ctk.CTkFrame(self, fg_color="transparent")
        filter_frame.pack(padx=20, pady=(0,12), fill="x")

        ctk.CTkLabel(filter_frame, text="Filtrar por cliente:", font=("Arial", 12)).pack(side="left", padx=(0,8))
        self.search_entry = ctk.CTkEntry(filter_frame, placeholder_text="Nome do cliente...", width=300)
        self.search_entry.pack(side="left", padx=(0,8), fill="x", expand=True)
        self.search_entry.bind("<KeyRelease>", lambda e: self.atualizar_tabela())

        # Main card with rounded corners and better styling
        main_card = ctk.CTkFrame(self, corner_radius=16, fg_color=CARD_BG, border_width=2, border_color=ACCENT)
        main_card.pack(padx=20, pady=(0,16), fill="both", expand=True)

        # Card header with title
        card_header = ctk.CTkFrame(main_card, fg_color="transparent")
        card_header.pack(fill="x", padx=16, pady=12, side="top")
        ctk.CTkLabel(card_header, text="Empréstimos Cadastrados", font=("Arial", 14, "bold")).pack(side="left")

        # Table inside the card - SIMPLIFICADA
        table_frame = ctk.CTkFrame(main_card, fg_color="transparent")
        table_frame.pack(padx=12, pady=(0,12), fill="both", expand=True)

        columns = ("ID", "Cliente", "Valor Emprestado", "Saldo Devido", "Status")
        self.tree = ttk.Treeview(table_frame, columns=columns, height=15, show="headings")
        self.tree.column("#0", width=0, stretch=False)
        for col in columns:
            width = 150 if col in ["Cliente", "Saldo Devido"] else 120
            self.tree.column(col, anchor="center", width=width)
            self.tree.heading(col, text=col)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Configure row colors by tag
        style = ttk.Style()
        style.configure("active.Treeview", foreground="#27ae60")  # Green for active
        style.configure("inactive.Treeview", foreground="#95a5a6")  # Gray for inactive
        style.configure("overdue.Treeview", foreground="#e74c3c")  # Red for overdue
        
        # Alternative: Use different font weight or style
        self.tree.tag_configure("active", foreground="#27ae60")  # Green
        self.tree.tag_configure("inactive", foreground="#95a5a6")  # Gray
        self.tree.tag_configure("overdue", foreground="#e74c3c", font=("Arial", 10, "bold"))  # Red and bold

        # Action buttons frame
        button_frame = ctk.CTkFrame(self, fg_color="transparent")
        button_frame.pack(padx=20, pady=12, fill="x")
        ctk.CTkButton(button_frame, text="➕ Novo Empréstimo", fg_color=ACCENT, font=("Arial", 12, "bold"), height=36, command=self.novo_emprestimo).pack(side="left", padx=6)
        ctk.CTkButton(button_frame, text="💵 Registrar Pagamento", font=("Arial", 12), height=36, command=self.registrar_pagamento).pack(side="left", padx=6)
        ctk.CTkButton(button_frame, text="📝 Editar", font=("Arial", 12), height=36, command=self.editar).pack(side="left", padx=6)
        ctk.CTkButton(button_frame, text="🗑 Deletar", fg_color=("#ff6b6b","#8b2a2a"), font=("Arial", 12), height=36, command=self.deletar).pack(side="left", padx=6)

        self.atualizar_tabela()

    def atualizar_tabela(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Get all emprestimos and overdue list
        emps = list(self.database.emprestimos)
        try:
            atrasados = self.database.get_overdue_emprestimos()
            atrasados_ids = [e.id for e in atrasados]
        except Exception:
            atrasados_ids = []
        
        # Filter by client name search
        search_text = self.search_entry.get().strip().lower() if hasattr(self, 'search_entry') else ""
        if search_text:
            filtered_emps = []
            for emp in emps:
                cliente = self.database.get_cliente_por_id(emp.cliente_id)
                if cliente and search_text in cliente.nome.lower():
                    filtered_emps.append(emp)
            emps = filtered_emps
        
        for emp in emps:
            cliente = self.database.get_cliente_por_id(emp.cliente_id)
            cliente_nome = cliente.nome if cliente else "Desconhecido"
            
            valor_emprestado = getattr(emp, 'valor_emprestado', 0.0)
            saldo_devido = getattr(emp, 'saldo_devedor', 0.0)
            
            try:
                valor_emprestado_text = formatar_moeda(valor_emprestado)
                saldo_text = formatar_moeda(saldo_devido)
            except Exception:
                valor_emprestado_text = f"R$ {valor_emprestado:.2f}"
                saldo_text = f"R$ {saldo_devido:.2f}"
            
            # Determine status text and tag (for coloring)
            if emp.id in atrasados_ids:
                status = "⚠️ ATRASADO"
                tag = "overdue"
            elif emp.ativo:
                status = "✓ Ativo"
                tag = "active"
            else:
                status = "✗ Inativo"
                tag = "inactive"
            
            self.tree.insert("", "end", values=(emp.id, cliente_nome, valor_emprestado_text, saldo_text, status), tags=(tag,))

    def buscar(self):
        # placeholder: keep simple
        pass

    def novo_emprestimo(self):
        """Modal simplificado e amigável para novo empréstimo com preview."""
        # Validar se há clientes
        if not self.database.clientes:
            messagebox.showerror("Erro", "Nenhum cliente cadastrado.\nCadastre um cliente primeiro em 👥 Clientes.")
            return

        janela = ctk.CTkToplevel(self)
        janela.title("Novo Empréstimo")
        janela.geometry("620x750")
        janela.transient(self)
        janela.update_idletasks()
        try:
            janela.grab_set()
        except Exception:
            pass

        # Frame principal
        main_frame = ctk.CTkFrame(janela, corner_radius=12, fg_color=("#0b1220", "#0b1220"))
        main_frame.pack(fill="both", expand=True, padx=12, pady=12)

        # Seção 1: Dados básicos
        titulo = ctk.CTkLabel(main_frame, text="📋 Dados do Empréstimo", font=("Arial", 14, "bold"), text_color=ACCENT)
        titulo.pack(anchor="w", padx=16, pady=(16,12))

        # Cliente
        ctk.CTkLabel(main_frame, text="👤 Cliente:", font=("Arial", 11, "bold")).pack(anchor="w", padx=16, pady=(0,6))
        clientes_choices = [f"{c.id} - {c.nome}" for c in self.database.clientes]
        cliente_var = ctk.StringVar(value=clientes_choices[0] if clientes_choices else "")
        cliente_menu = ctk.CTkOptionMenu(main_frame, values=clientes_choices, variable=cliente_var, 
                                         font=("Arial", 11), dropdown_font=("Arial", 10))
        cliente_menu.pack(fill="x", padx=16, pady=(0,12))

        # Valor - com label de exemplo
        ctk.CTkLabel(main_frame, text="💰 Valor do Empréstimo (R$):", font=("Arial", 11, "bold")).pack(anchor="w", padx=16, pady=(0,4))
        ctk.CTkLabel(main_frame, text="Exemplo: 1000 ou 1500,50", font=("Arial", 9), text_color=("#999","#ccc")).pack(anchor="w", padx=16, pady=(0,6))
        vcmd_decimal = (self.register(validators.validate_decimal), '%P')
        entry_valor = ctk.CTkEntry(main_frame, placeholder_text="0.00", validate='key', validatecommand=vcmd_decimal, height=36, font=("Arial", 11))
        entry_valor.pack(fill="x", padx=16, pady=(0,12))

        # Taxa - com slider visual
        ctk.CTkLabel(main_frame, text="📊 Taxa de Juros (% ao mês):", font=("Arial", 11, "bold")).pack(anchor="w", padx=16, pady=(0,4))
        ctk.CTkLabel(main_frame, text="Exemplo: 2% = 2 | 5% = 5", font=("Arial", 9), text_color=("#999","#ccc")).pack(anchor="w", padx=16, pady=(0,6))
        vcmd_int = (self.register(validators.validate_integer), '%P')
        entry_taxa = ctk.CTkEntry(main_frame, placeholder_text="0", validate='key', validatecommand=vcmd_int, height=36, font=("Arial", 11), width=100)
        entry_taxa.pack(anchor="w", padx=16, pady=(0,12))

        # Prazo
        ctk.CTkLabel(main_frame, text="⏱️ Prazo (meses):", font=("Arial", 11, "bold")).pack(anchor="w", padx=16, pady=(0,4))
        ctk.CTkLabel(main_frame, text="Exemplo: 6, 12, 24", font=("Arial", 9), text_color=("#999","#ccc")).pack(anchor="w", padx=16, pady=(0,6))
        entry_prazo = ctk.CTkEntry(main_frame, placeholder_text="0", validate='key', validatecommand=vcmd_int, height=36, font=("Arial", 11), width=100)
        entry_prazo.pack(anchor="w", padx=16, pady=(0,12))

        # Data de Vencimento (nova)
        ctk.CTkLabel(main_frame, text="📅 Data de Vencimento (opcional):", font=("Arial", 11, "bold")).pack(anchor="w", padx=16, pady=(0,4))
        ctk.CTkLabel(main_frame, text="Deixe em branco para calcular automaticamente (prazo em meses)", font=("Arial", 9), text_color=("#999","#ccc")).pack(anchor="w", padx=16, pady=(0,6))
        entry_data_venc = ctk.CTkEntry(main_frame, placeholder_text="YYYY-MM-DD (opcional)", height=36, font=("Arial", 11))
        entry_data_venc.pack(fill="x", padx=16, pady=(0,16))

        # Seção 2: Preview de cálculos
        preview_titulo = ctk.CTkLabel(main_frame, text="📈 Preview do Empréstimo", font=("Arial", 14, "bold"), text_color=ACCENT)
        preview_titulo.pack(anchor="w", padx=16, pady=(0,12))

        preview_frame = ctk.CTkFrame(main_frame, corner_radius=8, fg_color=("#f9f9f9", "#0a1419"), border_width=1, border_color=ACCENT)
        preview_frame.pack(fill="both", padx=16, pady=(0,16))

        preview_label = ctk.CTkLabel(preview_frame, text="", font=("Arial", 10), justify="left", text_color=("#333","#ddd"))
        preview_label.pack(anchor="w", padx=12, pady=12)

        def atualizar_preview(*args):
            """Atualiza preview em tempo real."""
            try:
                valor_str = entry_valor.get().strip()
                taxa_str = entry_taxa.get().strip()
                prazo_str = entry_prazo.get().strip()

                if not valor_str or not taxa_str or not prazo_str:
                    preview_label.configure(text="Preencha os campos para ver o preview")
                    return

                valor = float(valor_str.replace(',', '.'))
                taxa_mensal = float(taxa_str) / 100
                prazo = int(prazo_str)

                # Cálculo com juros compostos
                valor_total = valor * ((1 + taxa_mensal) ** prazo)
                valor_juros = valor_total - valor
                valor_parcela = valor_total / prazo

                preview_text = (
                    f"✓ Valor emprestado: {formatar_moeda(valor)}\n"
                    f"✓ Juros totais ({taxa_str}% x {prazo}m): {formatar_moeda(valor_juros)}\n"
                    f"✓ Valor total a pagar: {formatar_moeda(valor_total)}\n"
                    f"✓ Parcela mensal: {formatar_moeda(valor_parcela)}"
                )
                preview_label.configure(text=preview_text, text_color=("#1abc9c","#1abc9c"))
            except Exception:
                preview_label.configure(text="Valores inválidos", text_color=("#ff6b6b","#ff9999"))

        entry_valor.bind("<KeyRelease>", atualizar_preview)
        entry_taxa.bind("<KeyRelease>", atualizar_preview)
        entry_prazo.bind("<KeyRelease>", atualizar_preview)

        # Botões
        def salvar():
            try:
                if not clientes_choices:
                    messagebox.showerror("Erro", "Nenhum cliente selecionado.")
                    return

                selecionado = cliente_var.get()
                cliente_id = selecionado.split(' - ')[0]

                raw_valor = entry_valor.get().strip()
                raw_taxa = entry_taxa.get().strip()
                raw_prazo = entry_prazo.get().strip()

                # Valor
                if not raw_valor:
                    messagebox.showerror("Erro", "Digite o valor do empréstimo!")
                    return
                valor = float(raw_valor.replace(',', '.'))
                if valor <= 0:
                    messagebox.showerror("Erro", "O valor deve ser maior que zero!")
                    return

                # Taxa
                if not raw_taxa:
                    messagebox.showerror("Erro", "Digite a taxa de juros!")
                    return
                taxa = float(raw_taxa.replace(',', '.')) / 100
                if taxa < 0:
                    messagebox.showerror("Erro", "A taxa não pode ser negativa!")
                    return

                # Prazo
                if not raw_prazo:
                    messagebox.showerror("Erro", "Digite o prazo em meses!")
                    return
                prazo = int(raw_prazo)
                if prazo <= 0:
                    messagebox.showerror("Erro", "O prazo deve ser maior que zero!")
                    return

                data_inicio = datetime.now().date().isoformat()

                # Data de vencimento (opcional)
                data_venc_str = entry_data_venc.get().strip()
                if data_venc_str:
                    try:
                        datetime.strptime(data_venc_str, "%Y-%m-%d")
                        data_vencimento = data_venc_str
                    except:
                        messagebox.showerror("Erro", "Data de vencimento inválida. Use formato YYYY-MM-DD.")
                        return
                else:
                    data_vencimento = None  # Será calculado automaticamente no modelo

                # Criar empréstimo
                novo = Emprestimo(cliente_id=cliente_id, valor_emprestado=valor, taxa_juros=taxa, data_inicio=data_inicio, prazo_meses=prazo, data_vencimento=data_vencimento)
                self.database.adicionar_emprestimo(novo)
                self.database.salvar_dados()
                messagebox.showinfo("Sucesso", f"✓ Empréstimo criado!\n\nValor total: {formatar_moeda(novo.valor_total)}\nParcela: {formatar_moeda(novo.valor_parcela)}")
                janela.destroy()
                self.atualizar_tabela()
            except ValueError as e:
                messagebox.showerror("Erro", f"Valores inválidos: {e}")
            except Exception as e:
                messagebox.showerror("Erro", f"Falha ao criar empréstimo: {e}")

        btn_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        btn_frame.pack(fill="x", padx=16, pady=12)

        ctk.CTkButton(btn_frame, text="✓ Confirmar", fg_color=ACCENT, height=36, font=("Arial", 12, "bold"), command=salvar).pack(side="left", padx=6)
        ctk.CTkButton(btn_frame, text="✕ Cancelar", height=36, command=janela.destroy).pack(side="left", padx=6)

    def registrar_pagamento(self):
        """Abre modal simplificado para registrar pagamento de um empréstimo."""
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror("Erro", "Selecione um empréstimo para registrar pagamento")
            return
        
        item = self.tree.item(selected[0])
        values = item.get('values', [])
        if not values:
            messagebox.showerror("Erro", "Seleção inválida")
            return
        
        emp_id = values[0]
        emprestimo = next((e for e in self.database.emprestimos if e.id == emp_id), None)
        if emprestimo is None:
            messagebox.showerror("Erro", "Empréstimo não encontrado")
            return
        
        if emprestimo.saldo_devedor <= 0:
            messagebox.showinfo("Aviso", "Este empréstimo já foi totalmente quitado!")
            return

        # Modal de pagamento
        janela = ctk.CTkToplevel(self)
        janela.title(f"Registrar Pagamento - {emprestimo.id}")
        janela.geometry("550x400")
        janela.transient(self)
        janela.update_idletasks()
        try:
            janela.grab_set()
        except Exception:
            pass

        main_frame = ctk.CTkFrame(janela, corner_radius=12, fg_color=("#0b1220", "#0b1220"))
        main_frame.pack(fill="both", expand=True, padx=12, pady=12)

        # Informações
        cliente_obj = self.database.get_cliente_por_id(emprestimo.cliente_id)
        cliente_nome = cliente_obj.nome if cliente_obj else "Desconhecido"
        
        ctk.CTkLabel(main_frame, text=f"Empréstimo de {cliente_nome}", font=("Arial", 12, "bold")).pack(anchor="w", padx=16, pady=(16,8))
        ctk.CTkLabel(main_frame, text=f"Saldo devedor: {formatar_moeda(emprestimo.saldo_devedor)}", 
                     font=("Arial", 11), text_color=("#ff6b6b", "#ff9999")).pack(anchor="w", padx=16, pady=(0,16))

        # Campo de valor
        ctk.CTkLabel(main_frame, text="💰 Valor a pagar (R$):", font=("Arial", 11, "bold")).pack(anchor="w", padx=16, pady=(0,6))
        vcmd = (self.register(validators.validate_decimal), '%P')
        entry_valor = ctk.CTkEntry(main_frame, placeholder_text="Digite o valor", validate='key', validatecommand=vcmd, height=36, font=("Arial", 11))
        entry_valor.pack(fill="x", padx=16, pady=(0,12))

        # Botões rápidos
        botoes_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        botoes_frame.pack(fill="x", padx=16, pady=(0,12))

        def preenc_parcela():
            entry_valor.delete(0, 'end')
            entry_valor.insert(0, f"{emprestimo.valor_parcela:.2f}".replace('.', ','))

        def preenc_quitar():
            entry_valor.delete(0, 'end')
            entry_valor.insert(0, f"{emprestimo.saldo_devedor:.2f}".replace('.', ','))

        ctk.CTkButton(botoes_frame, text=f"Parcela\n{formatar_moeda(emprestimo.valor_parcela)}", 
                     height=40, fg_color=ACCENT, command=preenc_parcela).pack(side="left", padx=6)
        ctk.CTkButton(botoes_frame, text=f"Quitar\n{formatar_moeda(emprestimo.saldo_devedor)}", 
                     height=40, fg_color=("#27ae60", "#1e8449"), command=preenc_quitar).pack(side="left", padx=6)

        # Separador
        sep = ctk.CTkFrame(main_frame, fg_color=ACCENT, height=1)
        sep.pack(fill="x", padx=16, pady=(0,12))

        # Campo de data (opcional)
        ctk.CTkLabel(main_frame, text="📅 Data (opcional - deixe em branco para hoje):", font=("Arial", 10)).pack(anchor="w", padx=16, pady=(0,6))
        entry_data = ctk.CTkEntry(main_frame, placeholder_text="YYYY-MM-DD", height=32, font=("Arial", 10))
        entry_data.pack(fill="x", padx=16, pady=(0,12))

        # Botões
        def confirmar():
            try:
                valor_str = entry_valor.get().strip()
                if not valor_str:
                    messagebox.showerror("Erro", "Digite o valor do pagamento!")
                    return
                
                valor = float(valor_str.replace(',', '.'))
                if valor <= 0:
                    messagebox.showerror("Erro", "O valor deve ser maior que zero!")
                    return

                data_str = entry_data.get().strip()
                if data_str:
                    try:
                        datetime.strptime(data_str, "%Y-%m-%d")
                    except:
                        messagebox.showerror("Erro", "Data inválida. Use formato YYYY-MM-DD.")
                        return
                else:
                    data_str = datetime.now().date().isoformat()

                # Registrar pagamento
                emprestimo.registrar_pagamento(valor, data=data_str)
                self.database.salvar_dados()

                # Feedback baseado no saldo resultante
                if emprestimo.saldo_devedor <= 0:
                    messagebox.showinfo("Sucesso", f"✓ Empréstimo quitado com sucesso!\n✓ Valor pago: {formatar_moeda(valor)}")
                else:
                    messagebox.showinfo("Sucesso", f"✓ Pagamento registrado!\n✓ Valor pago: {formatar_moeda(valor)}\n✓ Saldo restante: {formatar_moeda(emprestimo.saldo_devedor)}")

                self.atualizar_tabela()
                janela.destroy()
            except ValueError as e:
                messagebox.showerror("Erro", f"Erro ao processar: {e}")
            except Exception as e:
                messagebox.showerror("Erro", f"Falha: {e}")

        btn_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        btn_frame.pack(fill="x", padx=16, pady=12)

        ctk.CTkButton(btn_frame, text="✓ Confirmar", fg_color=ACCENT, height=36, font=("Arial", 12, "bold"), command=confirmar).pack(side="left", padx=6)
        ctk.CTkButton(btn_frame, text="✕ Cancelar", height=36, command=janela.destroy).pack(side="left", padx=6)

    def editar(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror("Erro", "Selecione um empréstimo")
            return
        item = self.tree.item(selected[0])
        values = item.get('values', [])
        if not values:
            messagebox.showerror("Erro", "Seleção inválida")
            return
        emp_id = values[0]
        emprestimo = next((e for e in self.database.emprestimos if e.id == emp_id), None)
        if emprestimo is None:
            messagebox.showerror("Erro", "Empréstimo não encontrado")
            return
        
        # Avisar se empréstimo já foi quitado
        if emprestimo.saldo_devedor <= 0:
            messagebox.showinfo("Aviso", "Este empréstimo já foi totalmente quitado!\nVocê pode visualizar os detalhes, mas não será possível registrar novos pagamentos.")

        # Modal detalhes do empréstimo
        janela = ctk.CTkToplevel(self)
        janela.title(f"Empréstimo {emprestimo.id}")
        janela.geometry("800x700")
        janela.transient(self)
        janela.update_idletasks()
        try:
            janela.grab_set()
        except Exception:
            pass

        frame = ctk.CTkFrame(janela, corner_radius=12, fg_color=("#0b1220", "#0b1220"))
        frame.pack(fill="both", expand=True, padx=12, pady=12)

        # Informações principais
        cliente_obj = self.database.get_cliente_por_id(emprestimo.cliente_id)
        cliente_nome = cliente_obj.nome if cliente_obj else emprestimo.cliente_id
        info_text = (
            f"Cliente: {cliente_nome}\n"
            f"Valor emprestado: {formatar_moeda(emprestimo.valor_emprestado)}\n"
            f"Valor total (com juros): {formatar_moeda(emprestimo.valor_total)}\n"
            f"Parcela: {formatar_moeda(emprestimo.valor_parcela)}\n"
            f"Saldo devedor: {formatar_moeda(emprestimo.saldo_devedor)}\n"
            f"Taxa (mensal): {emprestimo.taxa_juros * 100:.2f}%\n"
            f"Criado em: {emprestimo.data_criacao[:10]}\n"
            f"Vencimento: {emprestimo.data_vencimento if emprestimo.data_vencimento else 'Não especificado'}"
        )
        ctk.CTkLabel(frame, text=info_text, justify="left", anchor="w").pack(fill="x", padx=12, pady=(6,12))

        # Histórico de Pagamentos
        hist_header = ctk.CTkFrame(frame, fg_color="transparent")
        hist_header.pack(fill="x", padx=12, pady=(12,8))
        ctk.CTkLabel(hist_header, text="📋 Histórico de Pagamentos", font=("Arial", 12, "bold")).pack(side="left")

        # Pagamentos (histórico com scrollbar melhor)
        pagamentos_frame = ctk.CTkFrame(frame, corner_radius=8, fg_color=("#f9f9f9", "#0a1419"), border_width=1, border_color=ACCENT)
        pagamentos_frame.pack(fill="both", expand=True, padx=12, pady=(0,8))

        pagos_cols = ("Valor", "Data", "Saldo Restante")
        pagos_tree = ttk.Treeview(pagamentos_frame, columns=pagos_cols, height=6)
        pagos_tree.column("#0", width=0, stretch=False)
        for col in pagos_cols:
            width = 150 if col == "Valor" else (150 if col == "Data" else 150)
            pagos_tree.column(col, anchor="center", width=width)
            pagos_tree.heading(col, text=col)
        
        scrollbar = ttk.Scrollbar(pagamentos_frame, orient="vertical", command=pagos_tree.yview)
        pagos_tree.configure(yscroll=scrollbar.set)
        pagos_tree.pack(side="left", fill="both", expand=True, padx=6, pady=6)
        scrollbar.pack(side="right", fill="y", padx=(0,6), pady=6)

        def atualizar_pagamentos():
            for it in pagos_tree.get_children():
                pagos_tree.delete(it)
            for p in emprestimo.get_historico_pagamentos():
                try:
                    valor_text = formatar_moeda(p.get('valor', 0.0))
                    saldo_text = formatar_moeda(p.get('saldo_anterior', 0.0) - p.get('valor', 0.0))
                except Exception:
                    valor_text = f"R$ {p.get('valor', 0.0):.2f}"
                    saldo_text = f"R$ {(p.get('saldo_anterior', 0.0) - p.get('valor', 0.0)):.2f}"
                pagos_tree.insert("", "end", values=(valor_text, p.get('data')[:10], saldo_text))

        atualizar_pagamentos()

        # Seção de Pagamento - DESABILITADA SE QUITADO
        pag_header = ctk.CTkFrame(frame, fg_color="transparent")
        pag_header.pack(fill="x", padx=12, pady=(12,8))
        
        if emprestimo.saldo_devedor <= 0:
            ctk.CTkLabel(pag_header, text="✓ Empréstimo Quitado", font=("Arial", 12, "bold"), text_color="#27ae60").pack(side="left")
            ctk.CTkLabel(pag_header, text="Nenhum pagamento adicional necessário", font=("Arial", 10), text_color="#27ae60").pack(side="right")
        else:
            ctk.CTkLabel(pag_header, text="💰 Registrar Pagamento", font=("Arial", 12, "bold")).pack(side="left")
            ctk.CTkLabel(pag_header, text=f"Saldo devedor: {formatar_moeda(emprestimo.saldo_devedor)}", 
                         font=("Arial", 10), text_color=("#ff6b6b", "#ff9999")).pack(side="right")
        
        # Mostrar seção de pagamento apenas se não quitado
        if emprestimo.saldo_devedor > 0:
            pay_frame = ctk.CTkFrame(frame, corner_radius=8, fg_color=("#f0f0f0", "#1a2332"), border_width=1, border_color=ACCENT)
            pay_frame.pack(fill="x", padx=12, pady=(0,8))

            # Valor do pagamento
            valor_frame = ctk.CTkFrame(pay_frame, fg_color="transparent")
            valor_frame.pack(fill="x", padx=12, pady=12)
            
            ctk.CTkLabel(valor_frame, text="Valor a pagar:", font=("Arial", 11, "bold")).pack(side="left", padx=(0,12))
            entry_pay = ctk.CTkEntry(valor_frame, placeholder_text="Ex: 100.50", width=150)
            entry_pay.pack(side="left", padx=(0,8))
            
            # Botões rápidos: parcela, quitação total
            # Handlers to fill the payment entry explicitly
            def preencher_parcela():
                entry_pay.delete(0, tk.END)
                entry_pay.insert(0, f"{emprestimo.valor_parcela:.2f}")

            def preencher_quitar():
                entry_pay.delete(0, tk.END)
                entry_pay.insert(0, f"{emprestimo.saldo_devedor:.2f}")

            def atualizar_botao_quitar():
                """Atualiza o texto do botão Quitar com o saldo devedor atual."""
                btn_quitar.configure(text=f"Quitar ({formatar_moeda(emprestimo.saldo_devedor)})")

            ctk.CTkButton(valor_frame, text=f"Parcela ({formatar_moeda(emprestimo.valor_parcela)})", 
                         width=150, height=32, fg_color=ACCENT,
                         command=preencher_parcela).pack(side="left", padx=4)

            btn_quitar = ctk.CTkButton(valor_frame, text=f"Quitar ({formatar_moeda(emprestimo.saldo_devedor)})", 
                         width=150, height=32, fg_color=("#27ae60", "#1e8449"),
                         command=preencher_quitar)
            btn_quitar.pack(side="left", padx=4)

            # Data (opcional)
            data_frame = ctk.CTkFrame(pay_frame, fg_color="transparent")
            data_frame.pack(fill="x", padx=12, pady=(0,12))
            
            ctk.CTkLabel(data_frame, text="Data (opcional):", font=("Arial", 11)).pack(side="left", padx=(0,12))
            entry_pay_date = ctk.CTkEntry(data_frame, placeholder_text="YYYY-MM-DD (deixe em branco = hoje)", width=250)
            entry_pay_date.pack(side="left", fill="x", expand=True)

            def registrar_pagamento():
                raw = entry_pay.get().strip()
                raw_date = entry_pay_date.get().strip()
                
                # Validar valor
                try:
                    valor = float(raw.replace(',', '.'))
                    if valor <= 0:
                        messagebox.showerror("Erro", "O valor deve ser maior que zero!")
                        return
                except Exception:
                    messagebox.showerror("Erro", "Valor inválido. Informe um número maior que zero.")
                    return
                
                # Validar data se fornecida
                if raw_date:
                    try:
                        datetime.strptime(raw_date, "%Y-%m-%d")
                        data = raw_date
                    except Exception:
                        messagebox.showerror("Erro", "Data inválida. Use formato YYYY-MM-DD.")
                        return
                else:
                    data = None

                # Capturar valores ANTES de registrar
                saldo_antes = emprestimo.saldo_devedor

                # Registrar pagamento
                try:
                    emprestimo.registrar_pagamento(valor, data=data)
                    self.database.salvar_dados()
                    
                    # Saldo DEPOIS do pagamento
                    saldo_depois = emprestimo.saldo_devedor

                    # Mensagem de feedback baseada no saldo DEPOIS
                    if saldo_depois <= 0:  # Quitação total
                        # calcular quanto foi efetivamente pago para quitar
                        pago_para_quitar = min(valor, saldo_antes)
                        excesso = max(0.0, valor - saldo_antes)
                        if excesso > 0:
                            msg = (f"✓ Empréstimo quitado com sucesso!\nTotal pago: {formatar_moeda(pago_para_quitar)}\n"
                                   f"Crédito gerado: {formatar_moeda(excesso)}")
                        else:
                            msg = f"✓ Empréstimo quitado com sucesso!\nTotal pago: {formatar_moeda(pago_para_quitar)}"
                    elif valor > saldo_antes:  # Pagamento acima do saldo original (shouldn't happen here but handle)
                        credito = valor - saldo_antes
                        msg = (f"✓ Pagamento registrado!\nSaldo após pagamento: {formatar_moeda(saldo_depois)}\n"
                               f"Crédito disponível: {formatar_moeda(credito)}")
                    else:  # Pagamento parcial
                        msg = f"✓ Pagamento registrado!\nValor pago: {formatar_moeda(valor)}\nSaldo devedor: {formatar_moeda(saldo_depois)}"
                    
                    messagebox.showinfo("Sucesso", msg)
                    
                    # Limpar entrada
                    entry_pay.delete(0, 'end')
                    entry_pay_date.delete(0, 'end')
                    
                    # Atualizar botão Quitar com novo saldo
                    atualizar_botao_quitar()
                    
                    # Atualizar tabelas e telas
                    atualizar_pagamentos()
                    self.atualizar_tabela()
                except ValueError as ve:
                    messagebox.showerror("Erro", str(ve))
                except Exception as e:
                    messagebox.showerror("Erro", f"Falha ao registrar: {e}")

            # Botões de ação
            btn_frame = ctk.CTkFrame(frame, fg_color="transparent")
            btn_frame.pack(fill="x", padx=12, pady=12)
            
            ctk.CTkButton(btn_frame, text="✓ Registrar Pagamento", height=36, font=("Arial", 12, "bold"), 
                         fg_color=ACCENT, command=registrar_pagamento).pack(side="left", padx=6)
            ctk.CTkButton(btn_frame, text="✕ Fechar", height=36, font=("Arial", 12), 
                         command=janela.destroy).pack(side="left", padx=6)
        else:
            # Se quitado, mostrar apenas botão Fechar
            btn_frame = ctk.CTkFrame(frame, fg_color="transparent")
            btn_frame.pack(fill="x", padx=12, pady=12)
            ctk.CTkButton(btn_frame, text="✕ Fechar", height=36, font=("Arial", 12), 
                         command=janela.destroy).pack(side="left", padx=6)

    def deletar(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror("Erro", "Selecione um empréstimo para deletar")
            return
        item = self.tree.item(selected[0])
        values = item.get('values', [])
        emp_id = values[0] if values else None
        emprestimo = next((e for e in self.database.emprestimos if e.id == emp_id), None)
        if emprestimo is None:
            messagebox.showerror("Erro", "Empréstimo não encontrado")
            return

        # Obter dados para confirmação
        cliente = self.database.get_cliente_por_id(emprestimo.cliente_id)
        cliente_nome = cliente.nome if cliente else "Desconhecido"
        saldo = emprestimo.saldo_devedor

        # Aviso claro se há saldo devedor
        if saldo > 0:
            msg = (f"⚠️ ATENÇÃO - Saldo Pendente!\n\n"
                   f"Cliente: {cliente_nome}\n"
                   f"Saldo devedor: {formatar_moeda(saldo)}\n\n"
                   f"Tem certeza que deseja DELETAR este empréstimo?\n"
                   f"Esta ação não pode ser desfeita!")
        else:
            msg = (f"Confirmar exclusão?\n\n"
                   f"Cliente: {cliente_nome}\n"
                   f"Empréstimo: {emprestimo.id}\n\n"
                   f"Esta ação não pode ser desfeita!")

        if messagebox.askyesno("Confirmar Deleção", msg):
            try:
                self.database.emprestimos.remove(emprestimo)
                self.database.salvar_dados()
                self.atualizar_tabela()
                messagebox.showinfo("Sucesso", "✓ Empréstimo removido com sucesso!")
            except Exception as e:
                messagebox.showerror("Erro", f"Falha ao remover: {e}")
