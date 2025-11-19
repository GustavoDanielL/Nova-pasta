import customtkinter as ctk
from tkinter import ttk, messagebox
from pathlib import Path
import csv
from datetime import datetime
# PDF export disabled by default to avoid hard dependency on reportlab
# (install reportlab or re-enable if you need PDF generation)

CARD_BG = ("#ffffff", "#071018")
ACCENT = "#1abc9c"

class NotificacoesView(ctk.CTkFrame):
    def __init__(self, parent, database):
        super().__init__(parent)
        self.database = database
        self.criar_widgets()

    def criar_widgets(self):
        title = ctk.CTkLabel(self, text="Notificações", font=("Arial", 20, "bold"))
        title.pack(pady=(12,8), anchor="w", padx=20)

        table_frame = ctk.CTkFrame(self, corner_radius=12, fg_color=CARD_BG)
        table_frame.pack(pady=12, padx=20, fill="both", expand=True)

        columns = ("Tipo", "Mensagem", "Data")
        self.tree = ttk.Treeview(table_frame, columns=columns, height=12)
        self.tree.column("#0", width=0, stretch=False)
        for col in columns:
            self.tree.column(col, anchor="center", width=180)
            self.tree.heading(col, text=col)
        self.tree.pack(fill="both", expand=True, padx=8, pady=8)

        button_frame = ctk.CTkFrame(self, fg_color="transparent")
        button_frame.pack(pady=8, padx=20, fill="x")
        ctk.CTkButton(button_frame, text="Limpar Notificações", fg_color=("#ff6b6b","#8b2a2a"), command=self.limpar).pack(side="left", padx=8)
        ctk.CTkButton(button_frame, text="Exportar CSV", fg_color=ACCENT, command=self.exportar_csv).pack(side="left", padx=8)
        ctk.CTkButton(button_frame, text="Atualizar", fg_color=ACCENT, command=self.atualizar_tabela).pack(side="left", padx=8)

        self.atualizar_tabela()

    def atualizar_tabela(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        # Primeiro, inserir lembretes genéricos
        notificacoes = self.database.lembretes if hasattr(self.database, 'lembretes') else []
        if not notificacoes:
            self.tree.insert("", "end", values=("Info", "Nenhuma notificação", "---"))
        else:
            for lemb in notificacoes:
                tipo = lemb.get('tipo', 'Info')
                msg = lemb.get('mensagem', str(lemb))
                data = lemb.get('data', '---')
                self.tree.insert("", "end", values=(tipo, msg, data))

        # Em seguida, adicionar empréstimos em atraso
        atrasados = []
        try:
            atrasados = self.database.get_overdue_emprestimos()
        except Exception:
            atrasados = []

        if atrasados:
            # separador visual
            self.tree.insert("", "end", values=("---", "--- Empréstimos Atrasados ---", "---"))
            for emp in atrasados:
                cliente = self.database.get_cliente_por_id(emp.cliente_id)
                nome = cliente.nome if cliente else emp.cliente_id
                msg = f"ID {emp.id} - {nome} - Saldo: {emp.saldo_devedor:.2f}"
                data = emp.data_inicio if hasattr(emp, 'data_inicio') else emp.data_criacao[:10]
                self.tree.insert("", "end", values=("Atraso", msg, data))

    def limpar(self):
        self.database.lembretes = []
        self.database.salvar_dados()
        self.atualizar_tabela()

    def exportar_csv(self):
        try:
            export_dir = Path("data/exports")
            export_dir.mkdir(parents=True, exist_ok=True)
        except Exception:
            import os
            os.makedirs("data/exports", exist_ok=True)

        filename = f"data/exports/notificacoes_{datetime.now().strftime('%Y%m%d%H%M%S')}.csv"
        try:
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(["Tipo", "Mensagem", "Data"])
                # lembretes
                for lemb in (self.database.lembretes or []):
                    writer.writerow([lemb.get('tipo', 'Info'), lemb.get('mensagem', ''), lemb.get('data', '')])
                # atrasados
                for emp in self.database.get_overdue_emprestimos():
                    cliente = self.database.get_cliente_por_id(emp.cliente_id)
                    nome = cliente.nome if cliente else emp.cliente_id
                    writer.writerow(["Atraso", f"ID {emp.id} - {nome}", emp.data_inicio])

            message = f"Exportado: {filename}"
            ctk.CTkLabel(self, text=message, font=("Arial", 10)).pack(padx=20, pady=(4,8))
        except Exception as e:
            from tkinter import messagebox
            messagebox.showerror("Erro", f"Falha ao exportar CSV: {e}")

    
