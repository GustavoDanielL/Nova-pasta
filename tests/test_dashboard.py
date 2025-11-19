"""
Teste de visualização dos novos gráficos do dashboard.
Cria dados de teste e mostra uma prévia dos gráficos gerados.
"""

import customtkinter as ctk
from models.database import Database
from views.dashboard_view import DashboardView
from models.cliente import Cliente
from models.emprestimo import Emprestimo
from datetime import date, timedelta

# Configurar modo dark
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

# Carregar banco de dados
db = Database()
db.carregar_dados()

print("=" * 80)
print("TESTE DO DASHBOARD COM GRÁFICOS")
print("=" * 80)

# Garantir dados de teste
if len(db.clientes) < 3:
    print("\n✓ Criando clientes de teste...")
    for i in range(5):
        cliente = Cliente(
            nome=f"Cliente Teste {i+1}",
            cpf_cnpj=f"123.456.{i:03d}-00",
            telefone=f"11999{i:05d}",
            email=f"cliente{i}@test.com",
            endereco=f"Rua Teste {i+1}"
        )
        db.clientes.append(cliente)

if len(db.emprestimos) < 5:
    print("✓ Criando empréstimos de teste...")
    for i, cliente in enumerate(db.clientes[:5]):
        for j in range(2):
            valor = 1000 + (i * j * 500)
            taxa = 3 + (i % 5)
            prazo = 6 + (i % 6)
            data = (date.today() - timedelta(days=30 * (j + 1))).isoformat()
            
            emp = Emprestimo(
                cliente_id=cliente.id,
                valor_emprestado=valor,
                taxa_juros=taxa,
                data_inicio=data,
                prazo_meses=prazo
            )
            
            # Alguns pagamentos aleatórios
            if j > 0:
                emp.registrar_pagamento(valor * 0.3)
            
            db.emprestimos.append(emp)

db.salvar_dados()

print(f"\n✓ Total de clientes: {len(db.clientes)}")
print(f"✓ Total de empréstimos: {len(db.emprestimos)}")

# Criar janela teste
print("\n✓ Abrindo janela de teste do dashboard...")
print("   - Você pode clicar nos botões para alternar entre gráficos")
print("   - Disponíveis: Pizza (Status), Pizza (Ativo/Inativo), Barras (Clientes), Barras (Valores)")

root = ctk.CTk()
root.title("FinancePro - Dashboard Teste")
root.geometry("1200x700")

# Criar dashboard
dashboard = DashboardView(root, db)

root.mainloop()
