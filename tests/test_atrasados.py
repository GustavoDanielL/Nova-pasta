"""
Script para testar se os empréstimos atrasados estão sendo detectados corretamente.
Cria dados de teste e mostra quais estão marcados como atrasados.
"""

from models.database import Database
from models.cliente import Cliente
from models.emprestimo import Emprestimo
from datetime import datetime, date, timedelta

# Inicializar banco de dados
db = Database()
db.carregar_dados()

print("=" * 60)
print("TESTE DE EMPRÉSTIMOS ATRASADOS")
print("=" * 60)

# Criar cliente de teste se não existir
cliente_teste = next((c for c in db.clientes if c.nome == "Cliente Teste"), None)
if not cliente_teste:
    cliente_teste = Cliente(
        nome="Cliente Teste", 
        cpf_cnpj="123.456.789-00", 
        telefone="1111111111",
        email="teste@email.com",
        endereco="Rua Teste, 123"
    )
    db.adicionar_cliente(cliente_teste)
    print(f"✓ Cliente criado: {cliente_teste.nome} (ID: {cliente_teste.id})")
else:
    print(f"✓ Cliente encontrado: {cliente_teste.nome} (ID: {cliente_teste.id})")

print("\n" + "=" * 60)
print("CRIANDO EMPRÉSTIMOS DE TESTE")
print("=" * 60)

# Criar empréstimo 1: COM ATRASO (iniciado há 3 meses, 1 pagamento feito)
data_3_meses_atras = (date.today() - timedelta(days=90)).isoformat()
emp_atrasado = Emprestimo(
    cliente_id=cliente_teste.id,
    valor_emprestado=1000.0,
    taxa_juros=0.05,  # 5% ao mês
    data_inicio=data_3_meses_atras,
    prazo_meses=6
)
# Simular 1 pagamento (então 2 parcelas deveriam estar pagas, mas só 1 foi)
emp_atrasado.registrar_pagamento(valor=200.0, data=data_3_meses_atras)
db.emprestimos.append(emp_atrasado)
print(f"✓ Empréstimo ATRASADO criado:")
print(f"  - ID: {emp_atrasado.id}")
print(f"  - Data início: {data_3_meses_atras}")
print(f"  - Valor: R$ 1000.00")
print(f"  - Prazo: 6 meses")
print(f"  - Pagamentos feitos: 1")
print(f"  - Saldo devedor: R$ {emp_atrasado.saldo_devedor:.2f}")

# Criar empréstimo 2: SEM ATRASO (iniciado há 1 mês, parcela paga)
data_1_mes_atras = (date.today() - timedelta(days=30)).isoformat()
emp_em_dia = Emprestimo(
    cliente_id=cliente_teste.id,
    valor_emprestado=2000.0,
    taxa_juros=0.03,  # 3% ao mês
    data_inicio=data_1_mes_atras,
    prazo_meses=12
)
# Simular 1 pagamento (que é esperado para 1 mês)
emp_em_dia.registrar_pagamento(valor=200.0, data=data_1_mes_atras)
db.emprestimos.append(emp_em_dia)
print(f"\n✓ Empréstimo EM DIA criado:")
print(f"  - ID: {emp_em_dia.id}")
print(f"  - Data início: {data_1_mes_atras}")
print(f"  - Valor: R$ 2000.00")
print(f"  - Prazo: 12 meses")
print(f"  - Pagamentos feitos: 1")
print(f"  - Saldo devedor: R$ {emp_em_dia.saldo_devedor:.2f}")

# Criar empréstimo 3: RECÉM-CRIADO (não deve estar atrasado)
emp_novo = Emprestimo(
    cliente_id=cliente_teste.id,
    valor_emprestado=500.0,
    taxa_juros=0.04,  # 4% ao mês
    data_inicio=date.today().isoformat(),
    prazo_meses=3
)
db.emprestimos.append(emp_novo)
print(f"\n✓ Empréstimo NOVO criado:")
print(f"  - ID: {emp_novo.id}")
print(f"  - Data início: {date.today().isoformat()}")
print(f"  - Valor: R$ 500.00")
print(f"  - Prazo: 3 meses")
print(f"  - Pagamentos feitos: 0")
print(f"  - Saldo devedor: R$ {emp_novo.saldo_devedor:.2f}")

# Salvar dados
db.salvar_dados()
print("\n✓ Dados salvos no banco")

# Testar detecção de atrasados
print("\n" + "=" * 60)
print("TESTANDO DETECÇÃO DE ATRASADOS")
print("=" * 60)

atrasados = db.get_overdue_emprestimos()
print(f"\nTotal de empréstimos: {len(db.emprestimos)}")
print(f"Empréstimos atrasados detectados: {len(atrasados)}")

if atrasados:
    print("\n⚠️ EMPRÉSTIMOS ATRASADOS:")
    for emp in atrasados:
        cliente = db.get_cliente_por_id(emp.cliente_id)
        nome_cliente = cliente.nome if cliente else "Desconhecido"
        print(f"\n  ID: {emp.id}")
        print(f"  Cliente: {nome_cliente}")
        print(f"  Data início: {emp.data_inicio}")
        print(f"  Saldo devedor: R$ {emp.saldo_devedor:.2f}")
        print(f"  Ativo: {'Sim' if emp.ativo else 'Não'}")
else:
    print("\n✓ Nenhum empréstimo atrasado detectado!")

print("\n✓ Agora abra a aplicação e vá para 'Empréstimos' para ver os empréstimos coloridos:")
print("  - Verde: Ativo (em dia)")
print("  - Vermelho (negrito): ATRASADO")
print("  - Cinza: Inativo")

print("\n" + "=" * 60)
