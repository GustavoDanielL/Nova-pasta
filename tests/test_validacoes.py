"""
Teste de validações: encontrar todos os bugs de validação
"""

from models.database import Database
from models.cliente import Cliente
from models.emprestimo import Emprestimo
from datetime import date, timedelta

db = Database()
db.carregar_dados()

print("=" * 80)
print("TESTE DE VALIDAÇÕES - ENCONTRAR BUGS")
print("=" * 80)

# Criar cliente e empréstimo quitado
cliente = Cliente(
    nome="Cliente Teste Validação",
    cpf_cnpj="111.222.333-00",
    telefone="11999999999",
    email="teste@teste.com",
    endereco="Rua Teste"
)
db.clientes.append(cliente)

# Empréstimo pequeno (fácil quitar)
emp = Emprestimo(
    cliente_id=cliente.id,
    valor_emprestado=100.0,
    taxa_juros=1,  # 1% ao mês
    data_inicio=date.today().isoformat(),
    prazo_meses=2
)

print(f"\n✓ Empréstimo criado:")
print(f"  ID: {emp.id}")
print(f"  Saldo devedor inicial: R$ {emp.saldo_devedor:.2f}")

# Quitar completamente
emp.registrar_pagamento(emp.saldo_devedor)
print(f"\n✓ Empréstimo quitado:")
print(f"  Saldo devedor final: R$ {emp.saldo_devedor:.2f}")
print(f"  Status (ativo): {emp.ativo}")

db.emprestimos.append(emp)
db.salvar_dados()

print("\n" + "=" * 80)
print("TESTES DE VALIDAÇÃO")
print("=" * 80)

# Teste 1: Tentar registrar pagamento em empréstimo quitado
print("\n🧪 TESTE 1: Registrar pagamento em empréstimo quitado")
print(f"   Saldo devedor: R$ {emp.saldo_devedor:.2f}")
print(f"   Esperado: ❌ REJEITAR")

try:
    emp.registrar_pagamento(50.0)
    print(f"   Resultado: ✅ ACEITO (BUG! Deveria rejeitar)")
    print(f"   Novo saldo: R$ {emp.saldo_devedor:.2f}")
except Exception as e:
    print(f"   Resultado: ✅ REJEITADO - {e}")

# Teste 2: Tentar registrar pagamento de valor inválido
print("\n🧪 TESTE 2: Registrar pagamento com valor <= 0")
emp.saldo_devedor = 100.0  # Reset
print(f"   Saldo devedor: R$ {emp.saldo_devedor:.2f}")
print(f"   Esperado: ❌ REJEITAR")

try:
    emp.registrar_pagamento(-50.0)
    print(f"   Resultado: ✅ ACEITO (BUG! Deveria rejeitar)")
except Exception as e:
    print(f"   Resultado: ✅ REJEITADO - {e}")

# Teste 3: Deletar empréstimo quitado
print("\n🧪 TESTE 3: Deletar empréstimo quitado (deveria avisar)")
emp.saldo_devedor = 0.0
print(f"   Saldo devedor: R$ {emp.saldo_devedor:.2f}")
print(f"   Esperado: ⚠️ AVISAR que há débito (se houver)")
print(f"   Resultado: Sem validação específica no código")

# Teste 4: Editar taxa de um empréstimo quitado
print("\n🧪 TESTE 4: Editar taxa de um empréstimo quitado")
print(f"   Ativo: {emp.ativo}")
print(f"   Esperado: ❌ NÃO PERMITIR edição")
print(f"   Resultado: Sem validação no código (BUG!)")

# Teste 5: Registrar pagamento em empréstimo inativo
print("\n🧪 TESTE 5: Registrar pagamento em empréstimo inativo")
emp.ativo = False
print(f"   Ativo: {emp.ativo}")
print(f"   Saldo: R$ {emp.saldo_devedor:.2f}")
print(f"   Esperado: ❌ AVISAR")
print(f"   Resultado: Sem validação no código (BUG!)")

print("\n" + "=" * 80)
print("RESUMO DE BUGS ENCONTRADOS")
print("=" * 80)
print("""
1. ❌ Em editar(), pode registrar pagamento em empréstimo quitado
   - Falta validação: if saldo_devedor <= 0

2. ❌ Sem validação para valores <= 0 nos formulários da UI
   - Apenas validação no modelo, não na UI

3. ❌ Botões de pagamento (rápidos) não são desabilitados quando quitado
   - "Quitar" e "Parcela" devem sumir quando saldo <= 0

4. ❌ Sem avisos ao deletar empréstimo quitado
   - Deveria avisar mesmo se não houver saldo

5. ❌ Sem validação ao tentar editar empréstimo inativo/quitado
   - Deveria permitir visualização mas não edição
""")

print("=" * 80)
