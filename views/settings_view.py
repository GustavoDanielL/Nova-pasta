import customtkinter as ctk
from tkinter import messagebox
import json
from pathlib import Path

CARD_BG = ("#ffffff", "#0b1220")
ACCENT = "#1abc9c"

class SettingsView(ctk.CTkFrame):
    def __init__(self, parent, database):
        super().__init__(parent)
        self.database = database
        self.smtp_config_file = Path("data/smtp_config.json")
        self.pack(fill="both", expand=True)
        self.criar_widgets()
        self.carregar_config()

    def criar_widgets(self):
        # Título
        title = ctk.CTkLabel(self, text="⚙️ Configurações", font=("Arial", 24, "bold"), text_color=ACCENT)
        title.pack(pady=(16, 12), anchor="w", padx=20)

        # Frame principal com scroll
        scroll_frame = ctk.CTkScrollableFrame(self, fg_color="transparent")
        scroll_frame.pack(fill="both", expand=True, padx=20, pady=12)

        # Seção SMTP
        self.criar_secao_smtp(scroll_frame)

        # Seção Backup
        self.criar_secao_backup(scroll_frame)

        # Seção Sobre
        self.criar_secao_sobre(scroll_frame)

        # Botões inferiores
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(fill="x", padx=20, pady=12)
        ctk.CTkButton(btn_frame, text="💾 Salvar Configurações", fg_color=ACCENT, height=36, 
                     font=("Arial", 12, "bold"), command=self.salvar_config).pack(side="left", padx=6)
        ctk.CTkButton(btn_frame, text="🔄 Carregar Padrões", height=36, command=self.carregar_config).pack(side="left", padx=6)

    def criar_secao_smtp(self, parent):
        """Seção de configuração SMTP."""
        # Cabeçalho
        header = ctk.CTkLabel(parent, text="📧 Configuração SMTP para Enviar Emails", 
                             font=("Arial", 14, "bold"), text_color=ACCENT)
        header.pack(anchor="w", pady=(12, 8))

        # Frame da seção
        frame = ctk.CTkFrame(parent, corner_radius=12, fg_color=CARD_BG, border_width=1, border_color=ACCENT)
        frame.pack(fill="x", pady=(0, 16))

        # Campos SMTP
        campos = [
            ("Host (ex: smtp.gmail.com)", "host", "SMTP host"),
            ("Porta (ex: 587 ou 465)", "port", "587"),
            ("Usuário / Email", "username", "seu_email@gmail.com"),
            ("Senha / Token", "password", "(oculta)"),
            ("Nome do Remetente", "from_name", "FinancePro"),
        ]

        self.smtp_entries = {}
        for label_text, key, placeholder in campos:
            ctk.CTkLabel(frame, text=label_text, font=("Arial", 11, "bold")).pack(anchor="w", padx=16, pady=(8, 4))
            
            if key == "password":
                entry = ctk.CTkEntry(frame, placeholder_text=placeholder, show="•", height=32, font=("Arial", 10))
            else:
                entry = ctk.CTkEntry(frame, placeholder_text=placeholder, height=32, font=("Arial", 10))
            
            entry.pack(fill="x", padx=16, pady=(0, 8))
            self.smtp_entries[key] = entry

        # Info
        info_text = (
            "ℹ️ Dicas:\n"
            "• Gmail: host=smtp.gmail.com, porta=587, username=seu_email@gmail.com, password=SUA_APP_PASSWORD\n"
            "• Gere APP PASSWORD em https://myaccount.google.com/apppasswords\n"
            "• Outlook: host=smtp-mail.outlook.com, porta=587\n"
            "• Porta 587 = TLS, 465 = SSL"
        )
        ctk.CTkLabel(frame, text=info_text, font=("Arial", 9), text_color=("#666", "#aaa"), justify="left").pack(anchor="w", padx=16, pady=(8, 16))

    def criar_secao_backup(self, parent):
        """Seção de backup e restauração."""
        header = ctk.CTkLabel(parent, text="💾 Backup e Dados", font=("Arial", 14, "bold"), text_color=ACCENT)
        header.pack(anchor="w", pady=(12, 8))

        frame = ctk.CTkFrame(parent, corner_radius=12, fg_color=CARD_BG, border_width=1, border_color=ACCENT)
        frame.pack(fill="x", pady=(0, 16))

        info = (
            "Backups automáticos são salvos em: data/backups/\n"
            "Todos os backups incluem timestamp (data/hora).\n"
            "\n"
            "Para restaurar:\n"
            "1. Copie um arquivo de backup (ex: clientes_20251117170424.json)\n"
            "2. Renomeie para remover timestamp (ex: clientes.json)\n"
            "3. Copie para data/ e reinicie a aplicação."
        )
        ctk.CTkLabel(frame, text=info, font=("Arial", 10), justify="left").pack(anchor="w", padx=16, pady=16)

    def criar_secao_sobre(self, parent):
        """Seção sobre."""
        header = ctk.CTkLabel(parent, text="ℹ️ Sobre", font=("Arial", 14, "bold"), text_color=ACCENT)
        header.pack(anchor="w", pady=(12, 8))

        frame = ctk.CTkFrame(parent, corner_radius=12, fg_color=CARD_BG, border_width=1, border_color=ACCENT)
        frame.pack(fill="x", pady=(0, 16))

        info = (
            "FinancePro v1.0\n"
            "Sistema de Gestão de Empréstimos\n"
            "\n"
            "Funcionalidades:\n"
            "✓ Cadastro de clientes e empréstimos\n"
            "✓ Cálculo de juros compostos\n"
            "✓ Registro de pagamentos\n"
            "✓ Notificações de atrasos\n"
            "✓ Envio de cobranças por email\n"
            "✓ Relatórios e exportação\n"
            "✓ Backup automático"
        )
        ctk.CTkLabel(frame, text=info, font=("Arial", 10), justify="left").pack(anchor="w", padx=16, pady=16)

    def carregar_config(self):
        """Carrega config SMTP do arquivo."""
        if self.smtp_config_file.exists():
            try:
                cfg = json.loads(self.smtp_config_file.read_text(encoding='utf-8'))
                self.smtp_entries['host'].delete(0, 'end')
                self.smtp_entries['host'].insert(0, cfg.get('host', ''))
                self.smtp_entries['port'].delete(0, 'end')
                self.smtp_entries['port'].insert(0, str(cfg.get('port', '')))
                self.smtp_entries['username'].delete(0, 'end')
                self.smtp_entries['username'].insert(0, cfg.get('username', ''))
                self.smtp_entries['password'].delete(0, 'end')
                self.smtp_entries['password'].insert(0, cfg.get('password', ''))
                self.smtp_entries['from_name'].delete(0, 'end')
                self.smtp_entries['from_name'].insert(0, cfg.get('from_name', ''))
                messagebox.showinfo("Sucesso", "Configurações SMTP carregadas!")
            except Exception as e:
                messagebox.showerror("Erro", f"Falha ao carregar config: {e}")
        else:
            messagebox.showinfo("Info", "Nenhuma configuração SMTP salva ainda. Preencha e clique 'Salvar'.")

    def salvar_config(self):
        """Salva config SMTP no arquivo."""
        try:
            cfg = {
                'host': self.smtp_entries['host'].get().strip(),
                'port': int(self.smtp_entries['port'].get().strip() or 587),
                'username': self.smtp_entries['username'].get().strip(),
                'password': self.smtp_entries['password'].get().strip(),
                'from_name': self.smtp_entries['from_name'].get().strip(),
            }

            if not all([cfg['host'], cfg['username'], cfg['password']]):
                messagebox.showerror("Erro", "Preencha pelo menos: Host, Usuário e Senha!")
                return

            # Salvar arquivo
            self.smtp_config_file.parent.mkdir(parents=True, exist_ok=True)
            self.smtp_config_file.write_text(json.dumps(cfg, indent=2, ensure_ascii=False), encoding='utf-8')
            
            messagebox.showinfo("Sucesso", "✓ Configurações SMTP salvas com sucesso!")
        except ValueError:
            messagebox.showerror("Erro", "Porta deve ser um número (ex: 587)")
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao salvar: {e}")
