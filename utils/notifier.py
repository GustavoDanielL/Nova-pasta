"""
Background notifier que verifica periodicamente empréstimos atrasados
e adiciona lembretes à database.
"""
import threading
import time
from datetime import datetime, date
import smtplib
import ssl
import json
from pathlib import Path

CHECK_INTERVAL = 3600  # 1 hora em produção; mude para 60 segundos para testes

class Notifier:
    def __init__(self, database):
        self.db = database
        self._stop = threading.Event()
        self.thread = threading.Thread(target=self._run_loop, daemon=True)

    def start(self):
        if not self.thread.is_alive():
            self.thread.start()
            print("[Notifier] Background thread started")

    def stop(self):
        self._stop.set()
        self.thread.join(timeout=1)

    def _run_loop(self):
        while not self._stop.is_set():
            try:
                atrasados = self.db.get_overdue_emprestimos()
                now = datetime.now().isoformat()
                
                # Adicionar lembretes se novo
                for emp in atrasados:
                    cliente = self.db.get_cliente_por_id(emp.cliente_id)
                    nome = cliente.nome if cliente else emp.cliente_id
                    msg = f"Empréstimo {emp.id} de {nome} está em atraso. Saldo: R$ {emp.saldo_devedor:.2f}"
                    
                    # Verificar se já existe lembrete semelhante
                    existe = False
                    for lemb in getattr(self.db, 'lembretes', []):
                        if isinstance(lemb, dict) and lemb.get('emp_id') == emp.id:
                            existe = True
                            break
                    
                    if not existe:
                        lemb = {
                            'tipo': 'Atraso',
                            'mensagem': msg,
                            'data': now[:10],
                            'emp_id': emp.id
                        }
                        self.db.lembretes.append(lemb)
                        self.db.salvar_dados()
                        
                        # Opcional: enviar e-mail se SMTP configurado
                        try:
                            self._send_notification_email(cliente, emp)
                        except Exception as e:
                            print(f"[Notifier] Erro ao enviar email: {e}")
                
                # Aguardar CHECK_INTERVAL segundos
                time.sleep(CHECK_INTERVAL)
            except Exception as e:
                print(f"[Notifier] Erro no loop: {e}")
                time.sleep(60)

    def _send_notification_email(self, cliente, emp):
        """Envia notificação por email de atraso."""
        if not cliente or not cliente.email:
            return
        
        smtp_file = Path("data/smtp_config.json")
        if not smtp_file.exists():
            return
        
        try:
            cfg = json.loads(smtp_file.read_text(encoding='utf-8'))
        except Exception:
            return
        
        try:
            subject = f"Notificação de Atraso - FinancePro (ID: {emp.id})"
            body = (
                f"Prezado {cliente.nome},\n\n"
                f"Este é um lembrete automático de que seu empréstimo está em atraso.\n\n"
                f"ID do Empréstimo: {emp.id}\n"
                f"Saldo Devedor: R$ {emp.saldo_devedor:.2f}\n"
                f"Data de Início: {emp.data_inicio}\n\n"
                f"Por favor, regularize o pagamento assim que possível.\n\n"
                f"Atenciosamente,\nFinancePro"
            )
            
            message = f"From: {cfg.get('from_name')} <{cfg.get('username')}>\r\n"
            message += f"To: {cliente.email}\r\n"
            message += f"Subject: {subject}\r\n\r\n"
            message += body
            
            port = int(cfg.get('port', 587))
            host = cfg.get('host')
            username = cfg.get('username')
            password = cfg.get('password')
            
            if port == 465:
                context = ssl.create_default_context()
                with smtplib.SMTP_SSL(host, port, context=context) as server:
                    server.login(username, password)
                    server.sendmail(username, [cliente.email], message.encode('utf-8'))
            else:
                with smtplib.SMTP(host, port, timeout=10) as server:
                    server.starttls(context=ssl.create_default_context())
                    server.login(username, password)
                    server.sendmail(username, [cliente.email], message.encode('utf-8'))
            
            print(f"[Notifier] Email enviado para {cliente.email}")
        except Exception as e:
            print(f"[Notifier] Erro ao enviar email para {cliente.email}: {e}")
