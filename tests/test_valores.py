"""
Teste completo de validação de valores e pagamentos.
Verifica se os cálculos de juros, saldo devedor e histórico de pagamentos estão consistentes.
"""

from models.database import Database
from models.cliente import Cliente
from models.emprestimo import Emprestimo
from datetime import datetime, date, timedelta

db = Database()
db.carregar_dados()

print("=" * 80)
print("TESTE COMPLETO DE VALIDAÇÃO DE VALORES E PAGAMENTOS")
print("=" * 80)

# Encontrar ou criar cliente
cliente_teste = next((c for c in db.clientes if c.nome == "Cliente Validação"), None)
if not cliente_teste:
    cliente_teste = Cliente(
        nome="Cliente Validação", 
        cpf_cnpj="987.654.321-00", 
        telefone="2222222222",
        email="validacao@email.com",
        endereco="Rua Validação, 456"
    )
    db.adicionar_cliente(cliente_teste)
    print(f"✓ Cliente criado: {cliente_teste.nome}")
else:
    print(f"✓ Cliente encontrado: {cliente_teste.nome}")

print("\n" + "=" * 80)
print("CRIANDO EMPRÉSTIMO DE TESTE COM VALORES ESPECÍFICOS")
print("=" * 80)

# Criar empréstimo com valores controláveis
valor_original = 1000.0
taxa_mensal = 5  # 5% ao mês (em percentual)
prazo = 6  # 6 meses

emp = Emprestimo(
    cliente_id=cliente_teste.id,
    valor_emprestado=valor_original,
    taxa_juros=taxa_mensal,  # Enviar em percentual (5, não 0.05)
    data_inicio=(date.today() - timedelta(days=90)).isoformat(),
    prazo_meses=prazo
)

print(f"\n📊 PARÂMETROS DO EMPRÉSTIMO:")
print(f"  Valor emprestado: R$ {valor_original:.2f}")
print(f"  Taxa mensal: {taxa_mensal}%")
print(f"  Prazo: {prazo} meses")

# Cálculos esperados (taxa já em decimal para função)
taxa_decimal = taxa_mensal / 100
valor_total_esperado = valor_original * ((1 + taxa_decimal) ** prazo)
parcela_mensal = valor_total_esperado / prazo
juros_totais = valor_total_esperado - valor_original

print(f"\n💰 CÁLCULOS DO EMPRÉSTIMO:")
print(f"  Valor total com juros: R$ {valor_total_esperado:.2f}")
print(f"  Juros totais: R$ {juros_totais:.2f}")
print(f"  Parcela mensal: R$ {parcela_mensal:.2f}")

print(f"\n📈 VALORES NO OBJETO EMPRÉSTIMO:")
print(f"  emp.valor_emprestado: R$ {emp.valor_emprestado:.2f}")
print(f"  emp.taxa_juros (armazenada em decimal): {emp.taxa_juros}")
print(f"  emp.valor_total: R$ {emp.valor_total:.2f}")
print(f"  emp.valor_parcela: R$ {emp.valor_parcela:.2f}")
print(f"  emp.saldo_devedor (inicial): R$ {emp.saldo_devedor:.2f}")

# Validação 1: Valores iniciais
print(f"\n✓ VALIDAÇÃO 1: Valores iniciais")
assert abs(emp.valor_total - valor_total_esperado) < 0.01, f"Valor total incorreto: {emp.valor_total} vs {valor_total_esperado}"
assert abs(emp.saldo_devedor - valor_total_esperado) < 0.01, f"Saldo devedor inicial incorreto"
print(f"  ✓ Valores iniciais corretos!")

# Simular pagamentos progressivos
print(f"\n" + "=" * 80)
print("SIMULANDO PAGAMENTOS PROGRESSIVOS")
print("=" * 80)

pagamentos = [
    parcela_mensal * 0.8,      # Pagamento 1: 80% da parcela
    parcela_mensal * 1.0,      # Pagamento 2: 100% da parcela
    parcela_mensal * 1.2,      # Pagamento 3: 120% da parcela
]

saldo_acumulado = emp.saldo_devedor

for i, valor_pago in enumerate(pagamentos, 1):
    print(f"\n📌 PAGAMENTO {i}: R$ {valor_pago:.2f}")
    print(f"  Saldo antes: R$ {saldo_acumulado:.2f}")
    
    # Registrar pagamento
    emp.registrar_pagamento(valor_pago)
    
    # Novo saldo
    novo_saldo = emp.saldo_devedor
    desconto = saldo_acumulado - novo_saldo
    
    print(f"  Saldo depois: R$ {novo_saldo:.2f}")
    print(f"  Desconto efetivo: R$ {desconto:.2f}")
    
    # Validação: desconto deve ser igual ao valor pago (ou menor se quitou)
    diferenca = abs(desconto - valor_pago)
    if novo_saldo > 0:
        assert diferenca < 0.01, f"Desconto inconsistente: {desconto:.2f} vs {valor_pago:.2f}"
        print(f"  ✓ Desconto correto!")
    else:
        print(f"  ✓ Empréstimo quitado (crédito de R$ {abs(novo_saldo):.2f})")
    
    saldo_acumulado = novo_saldo
    
    # Mostrar histórico
    print(f"\n  📋 Histórico até agora:")
    for j, pag in enumerate(emp.get_historico_pagamentos(), 1):
        print(f"    {j}. Data: {pag['data'][:10]} | Valor: R$ {pag['valor']:.2f} | Saldo anterior: R$ {pag['saldo_anterior']:.2f}")

# Validação 2: Soma dos pagamentos
print(f"\n" + "=" * 80)
print("VALIDAÇÃO FINAL: SOMA DOS PAGAMENTOS")
print("=" * 80)

historico = emp.get_historico_pagamentos()
total_pago = sum(p['valor'] for p in historico)
saldo_final = emp.saldo_devedor

print(f"\nTotal de pagamentos: R$ {total_pago:.2f}")
print(f"Saldo devedor final: R$ {saldo_final:.2f}")
print(f"Total pago + saldo: R$ {(total_pago + max(0, saldo_final)):.2f}")
print(f"Valor total do empréstimo: R$ {valor_total_esperado:.2f}")

# A soma do pago + saldo deve ser igual ao valor total (ou próximo)
soma_final = total_pago + max(0, saldo_final)
assert abs(soma_final - valor_total_esperado) < 0.01, f"Soma inconsistente: {soma_final:.2f} vs {valor_total_esperado:.2f}"

print(f"\n✅ TESTE PASSOU! Os valores estão se conversando corretamente!")
print(f"   Total pago: R$ {total_pago:.2f}")
print(f"   Saldo devedor: R$ {max(0, saldo_final):.2f}")
print(f"   Soma: R$ {soma_final:.2f} (deve ser ≈ R$ {valor_total_esperado:.2f})")

# Salvar dados
db.emprestimos.append(emp)
db.salvar_dados()

print(f"\n✓ Empréstimo de teste salvo no banco de dados")

print("\n" + "=" * 80)
print("CONCLUSÃO")
print("=" * 80)
print("""
✅ Sistema de cálculo validado com sucesso!

O que foi testado:
1. ✓ Cálculo inicial de valor total com juros compostos
2. ✓ Cálculo de parcela mensal
3. ✓ Subtração correta do saldo devedor após cada pagamento
4. ✓ Registro correto do histórico de pagamentos
5. ✓ Consistência: Total Pago + Saldo = Valor Total

Você pode ter CERTEZA que:
- Quando um atrasado paga, o saldo_devedor é atualizado corretamente
- Os juros compostos são calculados uma única vez no início
- Cada pagamento reduz o saldo devedor pelo valor exato pago
- O histórico de pagamentos é mantido com precisão
""")
print("=" * 80)
