from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pathlib import Path
from typing import List, Optional

from models.database_sqlite import DatabaseSQLite
from models.cliente import Cliente
from models.emprestimo import Emprestimo
from models.usuario import Usuario

app = FastAPI(title="FinancePro API")

# CORS: permitir frontend local (Electron carregando arquivos e fetch para localhost)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost", "http://localhost:3000", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inicializar DB (mesmo diretório usado pela app desktop)
data_dir = Path.home() / "Documentos" / "FinancePro"
db_path = data_dir / "financepro.db"
db = DatabaseSQLite(db_path, None)

# Criar usuário admin padrão se não existir nenhum usuário
def ensure_default_user():
    if len(db.usuarios) == 0:
        # Criar usuário admin com senha admin123
        password_hash = Usuario.hash_password("admin123")
        admin_user = Usuario(usuario="admin", password_hash=password_hash, titulo="Administrador")
        db.adicionar_usuario(admin_user)
        print("✓ Usuário admin padrão criado (admin/admin123)")

ensure_default_user()


class LoginIn(BaseModel):
    username: str
    password: str


class ClienteIn(BaseModel):
    nome: str
    cpf_cnpj: str
    telefone: str
    email: str
    endereco: Optional[str] = ""


class EmprestimoIn(BaseModel):
    cliente_id: str
    valor_emprestado: float
    taxa_juros: float
    data_emprestimo: str
    prazo_meses: int
    metodo_calculo: Optional[str] = 'compostos'


class PaymentIn(BaseModel):
    emprestimo_id: str
    valor: float
    data: Optional[str] = None
    tipo: Optional[str] = 'Parcela'


@app.post('/login')
def login(payload: LoginIn):
    for user in db.usuarios:
        # suportar diferentes nomes de atributo (senha / password_hash)
        stored = getattr(user, 'password_hash', None) or getattr(user, 'senha', None)
        if user.usuario == payload.username and stored:
            ok, rehash = Usuario.verify_password(stored, payload.password)
            if ok:
                return {"ok": True, "message": "Autenticado"}

    raise HTTPException(status_code=401, detail="Usuário ou senha inválidos")


@app.get('/clients')
def list_clients():
    return [c.to_dict() for c in db.clientes]


@app.post('/clients')
def create_client(payload: ClienteIn):
    cliente = Cliente(
        nome=payload.nome,
        cpf_cnpj=payload.cpf_cnpj,
        telefone=payload.telefone,
        email=payload.email,
        endereco=payload.endereco
    )
    db.adicionar_cliente(cliente)
    return {'ok': True, 'id': cliente.id}


@app.get('/loans')
def list_loans():
    return [e.to_dict() for e in db.emprestimos]


@app.post('/loans')
def create_loan(payload: EmprestimoIn):
    emprestimo = Emprestimo(
        cliente_id=payload.cliente_id,
        valor_emprestado=payload.valor_emprestado,
        taxa_juros=payload.taxa_juros,
        data_emprestimo=payload.data_emprestimo,
        prazo_meses=payload.prazo_meses,
        metodo_calculo=payload.metodo_calculo
    )
    db.adicionar_emprestimo(emprestimo)
    return {'ok': True, 'id': emprestimo.id}


@app.post('/payments')
def register_payment(payload: PaymentIn):
    # localizar empréstimo
    emprestimo = None
    for e in db.emprestimos:
        if e.id == payload.emprestimo_id:
            emprestimo = e
            break

    if not emprestimo:
        raise HTTPException(status_code=404, detail='Empréstimo não encontrado')

    try:
        emprestimo.registrar_pagamento(payload.valor, payload.data, payload.tipo)
        db.atualizar_emprestimo(emprestimo)
        return {'ok': True}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post('/seed-test-data')
def seed_test_data():
    """Cria dados de teste para diferentes cenários de empréstimos"""
    from datetime import datetime, timedelta
    import time
    
    test_clients = [
        {"nome": "João Silva", "cpf_cnpj": "123.456.789-00", "telefone": "(11) 99999-1111", "email": "joao@email.com", "endereco": "Rua A, 100 - São Paulo"},
        {"nome": "Maria Santos", "cpf_cnpj": "234.567.890-11", "telefone": "(11) 99999-2222", "email": "maria@email.com", "endereco": "Rua B, 200 - São Paulo"},
        {"nome": "Pedro Oliveira", "cpf_cnpj": "345.678.901-22", "telefone": "(11) 99999-3333", "email": "pedro@email.com", "endereco": "Rua C, 300 - São Paulo"},
        {"nome": "Ana Costa", "cpf_cnpj": "456.789.012-33", "telefone": "(11) 99999-4444", "email": "ana@email.com", "endereco": "Rua D, 400 - São Paulo"},
        {"nome": "Carlos Ferreira", "cpf_cnpj": "567.890.123-44", "telefone": "(11) 99999-5555", "email": "carlos@email.com", "endereco": "Rua E, 500 - São Paulo"},
        {"nome": "Lucia Mendes", "cpf_cnpj": "678.901.234-55", "telefone": "(11) 99999-6666", "email": "lucia@email.com", "endereco": "Rua F, 600 - São Paulo"},
        {"nome": "Roberto Lima", "cpf_cnpj": "789.012.345-66", "telefone": "(11) 99999-7777", "email": "roberto@email.com", "endereco": "Rua G, 700 - São Paulo"},
        {"nome": "Fernanda Rocha", "cpf_cnpj": "890.123.456-77", "telefone": "(11) 99999-8888", "email": "fernanda@email.com", "endereco": "Rua H, 800 - São Paulo"},
    ]
    
    created_clients = []
    for c_data in test_clients:
        exists = any(c.cpf_cnpj == c_data["cpf_cnpj"] for c in db.clientes)
        if not exists:
            cliente = Cliente(**c_data)
            db.adicionar_cliente(cliente)
            created_clients.append(cliente)
            time.sleep(0.1)  # Pequeno delay para evitar lock
        else:
            cliente = next(c for c in db.clientes if c.cpf_cnpj == c_data["cpf_cnpj"])
            created_clients.append(cliente)
    
    today = datetime.now()
    scenarios_created = []
    
    def create_loan_with_payments(cliente, valor, taxa, prazo, dias_atras, parcelas_pagas, descricao):
        try:
            data_emprestimo = (today - timedelta(days=dias_atras)).strftime("%Y-%m-%d")
            emp = Emprestimo(
                cliente_id=cliente.id,
                valor_emprestado=valor,
                taxa_juros=taxa,
                data_emprestimo=data_emprestimo,
                prazo_meses=prazo,
                metodo_calculo='compostos'
            )
            db.adicionar_emprestimo(emp)
            time.sleep(0.1)
            
            for i in range(parcelas_pagas):
                data_pag = (today - timedelta(days=dias_atras-30*(i+1))).strftime("%Y-%m-%d")
                emp.registrar_pagamento(emp.valor_parcela, data_pag, "Parcela")
            
            if parcelas_pagas > 0:
                db.atualizar_emprestimo(emp)
                time.sleep(0.1)
            
            scenarios_created.append(descricao)
        except Exception as e:
            scenarios_created.append(f"ERRO: {descricao} - {str(e)}")
    
    # Cenários de teste
    if len(created_clients) > 0:
        create_loan_with_payments(created_clients[0], 5000, 3.0, 6, 180, 6, f"QUITADO - {created_clients[0].nome}: R$ 5.000")
    
    if len(created_clients) > 1:
        create_loan_with_payments(created_clients[1], 10000, 5.0, 12, 90, 3, f"EM DIA - {created_clients[1].nome}: R$ 10.000")
    
    if len(created_clients) > 2:
        create_loan_with_payments(created_clients[2], 8000, 4.0, 10, 60, 1, f"ATRASADO 1 parcela - {created_clients[2].nome}: R$ 8.000")
    
    if len(created_clients) > 3:
        create_loan_with_payments(created_clients[3], 15000, 6.0, 12, 120, 1, f"MUITO ATRASADO - {created_clients[3].nome}: R$ 15.000")
    
    if len(created_clients) > 4:
        create_loan_with_payments(created_clients[4], 3000, 3.5, 6, 35, 0, f"SEM PAGAMENTO - {created_clients[4].nome}: R$ 3.000")
    
    if len(created_clients) > 5:
        create_loan_with_payments(created_clients[5], 20000, 4.5, 24, 0, 0, f"NOVO - {created_clients[5].nome}: R$ 20.000")
    
    if len(created_clients) > 6:
        create_loan_with_payments(created_clients[6], 12000, 5.0, 12, 60, 4, f"ADIANTADO - {created_clients[6].nome}: R$ 12.000")
    
    if len(created_clients) > 7:
        create_loan_with_payments(created_clients[7], 50000, 3.0, 12, 330, 11, f"QUASE QUITADO - {created_clients[7].nome}: R$ 50.000")
    
    return {
        "ok": True,
        "message": f"Dados de teste criados: {len(created_clients)} clientes, {len(scenarios_created)} empréstimos",
        "scenarios": scenarios_created
    }


@app.delete('/clear-test-data')
def clear_test_data():
    """Remove todos os dados (usar com cuidado!)"""
    count_clients = len(db.clientes)
    count_loans = len(db.emprestimos)
    db.clientes.clear()
    db.emprestimos.clear()
    db._salvar_clientes()
    db._salvar_emprestimos()
    return {
        "ok": True,
        "message": f"Dados removidos: {count_clients} clientes, {count_loans} empréstimos"
    }


if __name__ == '__main__':
    import uvicorn
    uvicorn.run('backend.api:app', host='127.0.0.1', port=8000, reload=False)
