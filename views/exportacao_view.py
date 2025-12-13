# -*- coding: utf-8 -*-
"""
Exportação View - Interface para exportar dados em Excel
"""

import customtkinter as ctk
from tkinter import messagebox, filedialog
from utils.excel_export import gerar_excel_relatorio_completo, exportar_apenas_emprestimos
from datetime import datetime
import threading
from pathlib import Path

# Cores
from theme_colors import *
CONTENT_BG = COR_CARD
ACCENT = COR_PRIMARIA


class ExportacaoView:
    def __init__(self, parent, database):
        self.parent = parent
        self.database = database
        self.exportando = False
        self.main_frame = None
        
        self.criar_layout()
    
    def criar_layout(self):
        # Frame principal
        self.main_frame = ctk.CTkFrame(self.parent, fg_color=CONTENT_BG)
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Título
        title = ctk.CTkLabel(
            self.main_frame, 
            text="📥 Exportar Dados",
            font=("Segoe UI", 24, "bold"),
            text_color=COR_TEXTO
        )
        title.pack(pady=(0, 20))
        
        # Descrição
        desc = ctk.CTkLabel(
            self.main_frame,
            text="Exporte seus dados financeiros em formato Excel com múltiplas opções de relatórios",
            font=("Segoe UI", 12),
            text_color=COR_TEXTO_SEC
        )
        desc.pack(pady=(0, 30))
        
        # Frame de opções
        opcoes_frame = ctk.CTkFrame(self.main_frame, corner_radius=8, fg_color=("#f0f0f0", "#1a2332"))
        opcoes_frame.pack(fill="both", expand=True)
        
        # Opção 1: Relatório Completo
        self._criar_opcao_exportacao(
            opcoes_frame,
            "Relatório Completo",
            "Resumo executivo + Clientes + Empréstimos + Histórico de Pagamentos",
            self.exportar_completo,
            0
        )
        
        # Opção 2: Apenas Empréstimos
        self._criar_opcao_exportacao(
            opcoes_frame,
            "Apenas Empréstimos",
            "Dados detalhados de todos os empréstimos com status e percentual de conclusão",
            self.exportar_emprestimos,
            1
        )
        
        # Frame inferior com info
        info_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        info_frame.pack(fill="x", pady=(20, 0))
        
        ctk.CTkLabel(
            info_frame,
            text="ℹ️  Os arquivos serão salvos na pasta do aplicativo com data e hora",
            font=("Arial", 10),
            text_color=("gray70", "gray40")
        ).pack()
        
        ctk.CTkLabel(
            info_frame,
            text="✓ Todos os valores estão em Reais (R$)",
            font=("Arial", 10),
            text_color=("gray70", "gray40")
        ).pack()
        
        # Barra de progresso (oculta inicialmente)
        self.progress_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.progress_frame.pack(fill="x", pady=(20, 0))
        
        ctk.CTkLabel(
            self.progress_frame,
            text="Gerando arquivo...",
            font=("Arial", 11, "bold"),
            text_color=ACCENT
        ).pack(pady=(0, 8))
        
        self.progress_bar = ctk.CTkProgressBar(self.progress_frame)
        self.progress_bar.pack(fill="x")
        self.progress_bar.set(0)
        
        self.progress_frame.pack_forget()
    
    def _criar_opcao_exportacao(self, parent, titulo, descricao, comando, indice):
        """Cria uma opção de exportação com descrição e botão"""
        frame = ctk.CTkFrame(parent, corner_radius=8, fg_color=("#ffffff", "#0f1724"), border_width=1, border_color=ACCENT)
        frame.pack(fill="x", padx=12, pady=12)
        
        # Conteúdo
        content_frame = ctk.CTkFrame(frame, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=16, pady=16)
        
        # Título + Descrição
        info_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        info_frame.pack(fill="both", expand=True, side="left")
        
        ctk.CTkLabel(
            info_frame,
            text=titulo,
            font=("Arial", 14, "bold"),
            text_color=ACCENT
        ).pack(anchor="w")
        
        ctk.CTkLabel(
            info_frame,
            text=descricao,
            font=("Arial", 11),
            text_color=("gray60", "gray50"),
            wraplength=400,
            justify="left"
        ).pack(anchor="w", pady=(4, 0))
        
        # Botão
        ctk.CTkButton(
            content_frame,
            text="Exportar",
            width=120,
            height=36,
            fg_color=ACCENT,
            hover_color=("#16a085", "#0d6656"),
            command=comando
        ).pack(side="right", padx=(12, 0))
    
    def exportar_completo(self):
        """Exporta relatório completo"""
        self._executar_exportacao(
            "Gerando Relatório Completo",
            lambda: gerar_excel_relatorio_completo(self.database)
        )
    
    def exportar_emprestimos(self):
        """Exporta apenas empréstimos"""
        self._executar_exportacao(
            "Exportando Empréstimos",
            lambda: exportar_apenas_emprestimos(self.database)
        )
    
    def _executar_exportacao(self, mensagem, funcao_export):
        """Executa exportação em thread separada"""
        if self.exportando:
            messagebox.showwarning("Aviso", "Uma exportação já está em progresso!")
            return
        
        self.exportando = True
        self.progress_frame.pack(fill="x", pady=(20, 0))
        self.progress_bar.set(0.3)
        
        def thread_export():
            try:
                # Executar export
                caminho = funcao_export()
                
                # Atualizar progresso
                self.main_frame.after(0, lambda: self.progress_bar.set(1.0))
                
                # Sucesso
                tamanho_kb = Path(caminho).stat().st_size / 1024
                
                def mostrar_sucesso():
                    messagebox.showinfo(
                        "✓ Exportação Concluída!",
                        f"Arquivo criado com sucesso!\n\n"
                        f"📁 {Path(caminho).name}\n"
                        f"💾 {tamanho_kb:.1f} KB\n"
                        f"📍 {Path(caminho).parent}"
                    )
                
                self.main_frame.after(0, mostrar_sucesso)
                
            except Exception as e:
                import traceback
                erro_completo = traceback.format_exc()
                print(f"Erro na exportação:\n{erro_completo}")
                
                def mostrar_erro():
                    messagebox.showerror("Erro na Exportação", f"Falha ao exportar:\n{str(e)}")
                
                self.main_frame.after(0, mostrar_erro)
            
            finally:
                def limpar():
                    self.exportando = False
                    self.progress_frame.pack_forget()
                
                self.main_frame.after(0, limpar)
        
        # Executar em thread
        thread = threading.Thread(target=thread_export, daemon=True)
        thread.start()
    
    def exportar_com_dialogo(self):
        """Exporta e permite escolher local do arquivo"""
        try:
            caminho = filedialog.asksaveasfilename(
                defaultextension=".xlsx",
                filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")],
                initialfile=f"relatorio_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
            )
            
            if not caminho:
                return
            
            self.exportando = True
            self.progress_frame.pack(fill="x", pady=(20, 0))
            
            def thread_export():
                try:
                    self.progress_bar.set(0.5)
                    self.parent.update()
                    
                    gerar_excel_relatorio_completo(self.database, caminho)
                    
                    self.progress_bar.set(1.0)
                    self.parent.update()
                    
                    messagebox.showinfo(
                        "✓ Sucesso!",
                        f"Arquivo exportado com sucesso!\n\n{caminho}"
                    )
                    
                except Exception as e:
                    messagebox.showerror("Erro", f"Falha ao exportar:\n{str(e)}")
                
                finally:
                    self.exportando = False
                    self.progress_frame.pack_forget()
            
            # Executar em thread
            thread = threading.Thread(target=thread_export, daemon=True)
            thread.start()
        
        except Exception as e:
            messagebox.showerror("Erro", str(e))
