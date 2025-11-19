#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test script to verify payment validation on paid-off loans
"""

from models.database import Database
from models.emprestimo import Emprestimo
from datetime import datetime

def test_validation():
    db = Database()
    
    print("=" * 60)
    print("TESTE: Validação de Pagamento em Empréstimos")
    print("=" * 60)
    
    # Teste 1: Verificar empréstimos quitados
    print("\n1. Procurando empréstimos quitados...")
    quitados = [e for e in db.emprestimos if e.saldo_devedor <= 0]
    
    if quitados:
        emp = quitados[0]
        print(f"   ID: {emp.id}")
        print(f"   Saldo devedor: R$ {emp.saldo_devedor:.2f}")
        print(f"   Status: QUITADO")
        
        print("\n2. Tentando registrar pagamento em empréstimo quitado...")
        try:
            emp.registrar_pagamento(100)
            print("   ✗ ERRO: Pagamento foi aceito! (BUG)")
        except ValueError as e:
            print(f"   ✓ Validação funcionou: {e}")
        except Exception as e:
            print(f"   ✗ Erro inesperado: {e}")
    else:
        print("   Nenhum empréstimo quitado encontrado.")
        print("\n   Criando empréstimo de teste...")
        
        # Criar um empréstimo quitado para teste
        emp_teste = Emprestimo(
            cliente_id="cliente-001",
            valor_emprestado=1000.0,
            taxa_juros=0,
            data_inicio="2020-01-01",
            prazo_meses=10,
            id="TEST-001"
        )
        
        # Setar como quitado
        emp_teste.saldo_devedor = 0
        
        print(f"   Criado: {emp_teste.id}")
        print(f"   Saldo: R$ {emp_teste.saldo_devedor:.2f}")
        
        print("\n2. Tentando registrar pagamento...")
        try:
            emp_teste.registrar_pagamento(100)
            print("   ✗ ERRO: Pagamento foi aceito! (BUG)")
        except ValueError as e:
            print(f"   ✓ Validação funcionou: {e}")
        except Exception as e:
            print(f"   ✗ Erro inesperado: {e}")
    
    # Teste 3: Valor negativo
    print("\n3. Tentando registrar pagamento negativo...")
    if db.emprestimos:
        emp = db.emprestimos[0]
        try:
            emp.registrar_pagamento(-50)
            print("   ✗ ERRO: Pagamento negativo foi aceito! (BUG)")
        except ValueError as e:
            print(f"   ✓ Validação funcionou: {e}")
        except Exception as e:
            print(f"   ✗ Erro inesperado: {e}")
    
    print("\n" + "=" * 60)
    print("Testes concluídos!")
    print("=" * 60)

if __name__ == "__main__":
    test_validation()
