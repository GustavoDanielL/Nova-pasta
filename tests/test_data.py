#!/usr/bin/env python3
"""Script para popular dados de teste na aplicação."""

from models.database import Database
from models.cliente import Cliente
from models.emprestimo import Emprestimo
from datetime import datetime

# Inicializar database
db = Database()
db.carregar_dados()

# Limpar dados anteriores
db.clientes = []
db.emprestimos = []

# Criar clientes de teste
clientes_dados = [
    {"nome": "João Silva", "cpf_cnpj": "12345678901", "telefone": "(11)98765-4321", "email": "joao@email.com", "endereco": "Rua A, 123"},
    {"nome": "Maria Santos", "cpf_cnpj": "98765432101", "telefone": "(21)99876-5432", "email": "maria@email.com", "endereco": "Rua B, 456"},
    {"nome": "Pedro Oliveira", "cpf_cnpj": "11122233345", "telefone": "(31)97654-3210", "email": "pedro@email.com", "endereco": "Rua C, 789"},
]

for dados in clientes_dados:
    cliente = Cliente(**dados)
    db.clientes.append(cliente)

print(f"✓ {len(db.clientes)} clientes criados")

# Criar empréstimos de teste
emprestimos_dados = [
    {"cliente_id": db.clientes[0].id, "valor_emprestado": 1000.0, "taxa_juros": 5.0, "data_inicio": "2025-11-01", "prazo_meses": 12},
    {"cliente_id": db.clientes[0].id, "valor_emprestado": 2500.0, "taxa_juros": 3.5, "data_inicio": "2025-10-15", "prazo_meses": 24},
    {"cliente_id": db.clientes[1].id, "valor_emprestado": 5000.0, "taxa_juros": 4.0, "data_inicio": "2025-09-01", "prazo_meses": 36},
    {"cliente_id": db.clientes[2].id, "valor_emprestado": 1500.0, "taxa_juros": 6.0, "data_inicio": "2025-11-05", "prazo_meses": 6},
]

for dados in emprestimos_dados:
    emp = Emprestimo(**dados)
    # Registrar alguns pagamentos para o primeiro empréstimo
    if emp.cliente_id == db.clientes[0].id and emprestimos_dados.index(dados) == 0:
        emp.registrar_pagamento(100.0, data=datetime.now().isoformat(), tipo="Parcela")
    db.emprestimos.append(emp)

print(f"✓ {len(db.emprestimos)} empréstimos criados")

# Salvar dados
db.salvar_dados()
print("✓ Dados salvos com sucesso!")
print("\nDados de teste criados. Você pode abrir a aplicação agora.")
