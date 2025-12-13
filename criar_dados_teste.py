#!/usr/bin/env python3
"""
Script para popular o banco com dados de teste
Cria clientes e empréstimos em diferentes estados: ativo, atrasado e quitado
"""
from pathlib import Path
from datetime import datetime, timedelta
from models.database_sqlite import DatabaseSQLite
from models.cliente import Cliente
from models.emprestimo import Emprestimo
import time

def criar_dados_teste():
    """Cria dados de teste variados"""
    
    print("=" * 70)
    print("CRIANDO DADOS DE TESTE")
    print("=" * 70)
    
    # Conectar ao banco
    data_dir = Path.home() / "Documentos" / "FinancePro"
    db_path = data_dir / "financepro.db"
    db = DatabaseSQLite(db_path, senha_mestra=None)
    
    print(f"\n📂 Banco de dados: {db_path}")
    print(f"   Clientes atuais: {len(db.clientes)}")
    print(f"   Empréstimos atuais: {len(db.emprestimos)}")
    
    # Criar clientes de teste
    print("\n1️⃣ Criando clientes de teste...")
    clientes_teste = [
        {
            "nome": "João Silva Santos",
            "cpf_cnpj": "123.456.789-00",
            "telefone": "(11) 98765-4321",
            "email": "joao.silva@email.com",
            "endereco": "Rua das Flores, 123 - São Paulo/SP"
        },
        {
            "nome": "Maria Oliveira Costa",
            "cpf_cnpj": "987.654.321-00",
            "telefone": "(21) 91234-5678",
            "email": "maria.oliveira@email.com",
            "endereco": "Av. Principal, 456 - Rio de Janeiro/RJ"
        },
        {
            "nome": "Pedro Almeida Souza",
            "cpf_cnpj": "456.789.123-00",
            "telefone": "(31) 99876-5432",
            "email": "pedro.almeida@email.com",
            "endereco": "Rua do Comércio, 789 - Belo Horizonte/MG"
        },
        {
            "nome": "Ana Carolina Ferreira",
            "cpf_cnpj": "321.654.987-00",
            "telefone": "(41) 97654-3210",
            "email": "ana.ferreira@email.com",
            "endereco": "Travessa das Palmeiras, 321 - Curitiba/PR"
        }
    ]
    
    clientes_criados = []
    for dados in clientes_teste:
        # Verificar se já existe
        existe = any(c.cpf_cnpj == dados["cpf_cnpj"] for c in db.clientes)
        if existe:
            print(f"   ⚠️  {dados['nome'][:20]:20s} - Já existe")
            cliente = next(c for c in db.clientes if c.cpf_cnpj == dados["cpf_cnpj"])
            clientes_criados.append(cliente)
        else:
            cliente = Cliente(**dados)
            db.adicionar_cliente(cliente)
            clientes_criados.append(cliente)
            print(f"   ✅ {cliente.nome[:20]:20s} - Criado com sucesso")
    
    # Criar empréstimos de teste em diferentes estados
    print("\n2️⃣ Criando empréstimos de teste...")
    
    hoje = datetime.now().date()
    
    emprestimos_teste = [
        # EMPRÉSTIMO EM DIA - João
        {
            "cliente": clientes_criados[0],
            "descricao": "Em dia (10 meses restantes)",
            "valor_emprestado": 5000.0,
            "taxa_juros": 3.5,
            "data_emprestimo": (hoje - timedelta(days=60)).isoformat(),  # 2 meses atrás
            "prazo_meses": 12,
            "data_vencimento": (hoje + timedelta(days=300)).isoformat(),  # 10 meses à frente
            "pagamentos": [
                {"valor": 458.33, "data": (hoje - timedelta(days=30)).isoformat()},
                {"valor": 458.33, "data": hoje.isoformat()}
            ]
        },
        # EMPRÉSTIMO ATRASADO - Maria
        {
            "cliente": clientes_criados[1],
            "descricao": "Atrasado (venceu há 45 dias)",
            "valor_emprestado": 3000.0,
            "taxa_juros": 4.0,
            "data_emprestimo": (hoje - timedelta(days=200)).isoformat(),
            "prazo_meses": 6,
            "data_vencimento": (hoje - timedelta(days=45)).isoformat(),  # Venceu há 45 dias
            "pagamentos": []  # Sem pagamentos
        },
        # EMPRÉSTIMO QUITADO - Pedro
        {
            "cliente": clientes_criados[2],
            "descricao": "Quitado (pago integralmente)",
            "valor_emprestado": 2000.0,
            "taxa_juros": 2.5,
            "data_emprestimo": (hoje - timedelta(days=180)).isoformat(),
            "prazo_meses": 6,
            "data_vencimento": hoje.isoformat(),
            "pagamentos": [
                {"valor": 500.0, "data": (hoje - timedelta(days=150)).isoformat()},
                {"valor": 500.0, "data": (hoje - timedelta(days=120)).isoformat()},
                {"valor": 500.0, "data": (hoje - timedelta(days=90)).isoformat()},
                {"valor": 500.0, "data": (hoje - timedelta(days=60)).isoformat()},
                {"valor": 500.0, "data": (hoje - timedelta(days=30)).isoformat()},
                {"valor": 500.0, "data": hoje.isoformat()}
            ]
        },
        # EMPRÉSTIMO EM DIA (CURTO PRAZO) - Ana
        {
            "cliente": clientes_criados[3],
            "descricao": "Em dia (curto prazo - 2 meses)",
            "valor_emprestado": 1500.0,
            "taxa_juros": 5.0,
            "data_emprestimo": (hoje - timedelta(days=15)).isoformat(),
            "prazo_meses": 3,
            "data_vencimento": (hoje + timedelta(days=75)).isoformat(),
            "pagamentos": []
        },
        # EMPRÉSTIMO ATRASADO (GRAVE) - João (segundo empréstimo)
        {
            "cliente": clientes_criados[0],
            "descricao": "Atrasado grave (venceu há 90 dias)",
            "valor_emprestado": 4000.0,
            "taxa_juros": 4.5,
            "data_emprestimo": (hoje - timedelta(days=270)).isoformat(),
            "prazo_meses": 6,
            "data_vencimento": (hoje - timedelta(days=90)).isoformat(),  # Venceu há 90 dias
            "pagamentos": [
                {"valor": 700.0, "data": (hoje - timedelta(days=240)).isoformat()},
            ]
        },
        # EMPRÉSTIMO EM DIA (LONGO PRAZO) - Maria (segundo empréstimo)
        {
            "cliente": clientes_criados[1],
            "descricao": "Em dia (longo prazo - 24 meses)",
            "valor_emprestado": 10000.0,
            "taxa_juros": 3.0,
            "data_emprestimo": (hoje - timedelta(days=90)).isoformat(),
            "prazo_meses": 24,
            "data_vencimento": (hoje + timedelta(days=630)).isoformat(),
            "pagamentos": [
                {"valor": 500.0, "data": (hoje - timedelta(days=60)).isoformat()},
                {"valor": 500.0, "data": (hoje - timedelta(days=30)).isoformat()},
                {"valor": 500.0, "data": hoje.isoformat()}
            ]
        }
    ]
    
    for dados in emprestimos_teste:
        cliente = dados["cliente"]
        
        # Criar empréstimo
        emp = Emprestimo(
            cliente_id=cliente.id,
            valor_emprestado=dados["valor_emprestado"],
            taxa_juros=dados["taxa_juros"],
            data_emprestimo=dados["data_emprestimo"],
            prazo_meses=dados["prazo_meses"],
            data_vencimento=dados["data_vencimento"]
        )
        
        # Adicionar pagamentos
        for pag in dados.get("pagamentos", []):
            try:
                emp.registrar_pagamento(pag["valor"], pag["data"])
            except ValueError as e:
                # Se já estiver quitado, ignorar
                pass
        
        db.adicionar_emprestimo(emp)
        
        # Status visual
        status_badge = emp.get_status_badge()
        print(f"   ✅ {cliente.nome[:20]:20s} - {dados['descricao']:35s} - {status_badge}")
    
    # Salvar
    print("\n3️⃣ Salvando dados...")
    db.salvar_dados()
    
    print("\n" + "=" * 70)
    print("✅ DADOS DE TESTE CRIADOS COM SUCESSO!")
    print("=" * 70)
    print(f"\n📊 Resumo:")
    print(f"   • Total de clientes: {len(db.clientes)}")
    print(f"   • Total de empréstimos: {len(db.emprestimos)}")
    
    # Estatísticas dos empréstimos
    quitados = sum(1 for e in db.emprestimos if e.esta_quitado())
    atrasados = sum(1 for e in db.emprestimos if e.esta_atrasado())
    em_dia = sum(1 for e in db.emprestimos if not e.esta_quitado() and not e.esta_atrasado())
    
    print(f"\n   Status dos empréstimos:")
    print(f"   • ✅ Quitados: {quitados}")
    print(f"   • 🔄 Em dia: {em_dia}")
    print(f"   • ⚠️  Atrasados: {atrasados}")
    print(f"\n{'=' * 70}\n")

if __name__ == "__main__":
    try:
        criar_dados_teste()
    except Exception as e:
        print(f"\n❌ ERRO: {e}")
        import traceback
        traceback.print_exc()
