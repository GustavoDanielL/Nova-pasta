import customtkinter as ctk
from tkinter import messagebox
from pathlib import Path
import csv
from datetime import datetime
from utils.calculos import formatar_moeda
from theme_colors import *

CARD_BG = COR_CARD
ACCENT = COR_PERIGO

class NotificacoesView(ctk.CTkFrame):
    def __init__(self, parent, database):
        super().__init__(parent)
        self.database = database
        self.criar_widgets()

    def criar_widgets(self):
        # Header
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(pady=(16,12), padx=20, fill="x")
        
        title = ctk.CTkLabel(header_frame, text="🔔 Notificações e Alertas", 
                           font=("Segoe UI", 24, "bold"), text_color=COR_TEXTO)
        title.pack(side="left")
        
        # Botões de ação
        btn_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        btn_frame.pack(side="right")
        
        ctk.CTkButton(btn_frame, text="🔄", width=40, height=32,
                     fg_color=COR_INFO, font=("Segoe UI", 11),
                     hover_color=COR_SECUNDARIA,
                     command=self.atualizar_lista).pack(side="left", padx=4)
        
        ctk.CTkButton(btn_frame, text="🗑️", width=40, height=32,
                     fg_color=COR_PERIGO, font=("Segoe UI", 11),
                     command=self.limpar).pack(side="left", padx=4)

        # Frame principal scrollable
        self.scroll_frame = ctk.CTkScrollableFrame(self, corner_radius=12, 
                                                   fg_color=CARD_BG,
                                                   border_width=2,
                                                   border_color=COR_BORDA)
        self.scroll_frame.pack(pady=12, padx=20, fill="both", expand=True)

        # Carregar com delay para não travar
        self.after(100, self.atualizar_lista)

    def atualizar_lista(self):
        # Limpar lista
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()
        
        # Contar notificações
        total_notif = 0
        
        # Empréstimos atrasados
        atrasados = []
        try:
            atrasados = self.database.get_overdue_emprestimos()
        except Exception:
            atrasados = []
        
        if atrasados:
            # Cache de clientes para performance
            clientes_cache = {c.id: c.nome for c in self.database.clientes}
            
            # Seção de atrasados
            secao = ctk.CTkLabel(self.scroll_frame, text="⚠️ Empréstimos Atrasados", 
                               font=("Segoe UI", 16, "bold"), text_color=COR_PERIGO)
            secao.pack(anchor="w", padx=16, pady=(16, 8))
            
            for emp in atrasados:
                total_notif += 1
                nome = clientes_cache.get(emp.cliente_id, str(emp.cliente_id))
                
                # Card de notificação simplificado
                card = ctk.CTkFrame(self.scroll_frame, corner_radius=8, 
                                   fg_color="#fef2f2",
                                   border_width=1, border_color=COR_PERIGO)
                card.pack(fill="x", padx=16, pady=4)
                
                # Conteúdo em um label único (mais rápido)
                data_str = emp.data_emprestimo[:10] if hasattr(emp, 'data_emprestimo') else "---"
                texto_completo = f"🔴 {nome} | ID: {emp.id} | Saldo: {formatar_moeda(emp.saldo_devedor)} | {data_str}"
                
                ctk.CTkLabel(card, text=texto_completo, 
                           font=("Segoe UI", 11), text_color=COR_TEXTO,
                           anchor="w").pack(anchor="w", padx=12, pady=8)
        
        # Lembretes genéricos
        lembretes = self.database.lembretes if hasattr(self.database, 'lembretes') else []
        
        if lembretes:
            secao = ctk.CTkLabel(self.scroll_frame, text="📝 Lembretes", 
                               font=("Segoe UI", 16, "bold"), text_color=COR_INFO)
            secao.pack(anchor="w", padx=16, pady=(16, 8))
            
            for lemb in lembretes:
                total_notif += 1
                tipo = lemb.get('tipo', 'Info')
                msg = lemb.get('mensagem', str(lemb))
                data = lemb.get('data', '---')
                
                # Card simplificado
                card = ctk.CTkFrame(self.scroll_frame, corner_radius=8, 
                                   fg_color="#f0f9ff",
                                   border_width=1, border_color=COR_INFO)
                card.pack(fill="x", padx=16, pady=4)
                
                texto_completo = f"📌 {tipo} | {msg} | {data}"
                ctk.CTkLabel(card, text=texto_completo, 
                           font=("Segoe UI", 11), text_color=COR_TEXTO,
                           anchor="w").pack(anchor="w", padx=12, pady=8)
        
        # Se não há notificações
        if total_notif == 0:
            empty_frame = ctk.CTkFrame(self.scroll_frame, fg_color="transparent")
            empty_frame.pack(expand=True, pady=50)
            
            ctk.CTkLabel(empty_frame, text="✅", font=("Segoe UI", 48)).pack(pady=(0, 16))
            ctk.CTkLabel(empty_frame, text="Nenhuma notificação pendente", 
                        font=("Segoe UI", 16), text_color=COR_TEXTO_SEC).pack()
            ctk.CTkLabel(empty_frame, text="Tudo em ordem!", 
                        font=("Segoe UI", 13), text_color=COR_SUCESSO).pack(pady=(8,0))

    def limpar(self):
        self.database.lembretes = []
        self.database.salvar_dados()
        self.atualizar_lista()

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

    
