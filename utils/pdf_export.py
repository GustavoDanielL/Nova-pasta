"""
Fallback exporters for report generation.

These functions provide lightweight plain-text exports so the app can run
even when `reportlab` is not installed. If you need full PDF output, install
`reportlab` and re-enable the original PDF module.
"""
from datetime import datetime
from pathlib import Path


def _ensure_export_dir():
    Path("data/exports").mkdir(parents=True, exist_ok=True)


def gerar_pdf_notificacoes(database, filename=None):
    """Fallback: gera um arquivo de texto com as notificações e retorna o caminho."""
    _ensure_export_dir()
    if not filename:
        filename = f"data/exports/notificacoes_{datetime.now().strftime('%Y%m%d%H%M%S')}.txt"

    with open(filename, 'w', encoding='utf-8') as f:
        f.write("Relatório de Notificações\n")
        f.write(f"Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n\n")

        f.write("Lembretes:\n")
        for lemb in (getattr(database, 'lembretes', []) or []):
            f.write(f"- [{lemb.get('data','')}] {lemb.get('tipo','')} - {lemb.get('mensagem','')}\n")
        f.write("\nEmpréstimos em atraso:\n")
        for emp in getattr(database, 'get_overdue_emprestimos', lambda: [])() or []:
            cliente = database.get_cliente_por_id(emp.cliente_id)
            nome = cliente.nome if cliente else emp.cliente_id
            f.write(f"- ID {emp.id} - {nome} - Saldo: {getattr(emp,'saldo_devedor',0):.2f}\n")

    return filename


def gerar_pdf_emprestimos(database, filename=None):
    """Fallback: gera um arquivo de texto com a lista de empréstimos."""
    _ensure_export_dir()
    if not filename:
        filename = f"data/exports/emprestimos_{datetime.now().strftime('%Y%m%d%H%M%S')}.txt"

    with open(filename, 'w', encoding='utf-8') as f:
        f.write("Relatório de Empréstimos\n")
        f.write(f"Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n\n")
        for emp in getattr(database, 'emprestimos', []) or []:
            cliente = database.get_cliente_por_id(emp.cliente_id)
            nome = cliente.nome if cliente else 'Desconhecido'
            f.write(f"ID: {getattr(emp,'id','?')} | Cliente: {nome} | Saldo: {getattr(emp,'saldo_devedor',0):.2f}\n")

    return filename
