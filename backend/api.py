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
                return {"ok": True, "message": "Authenticated"}

    raise HTTPException(status_code=401, detail="Invalid credentials")


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


if __name__ == '__main__':
    import uvicorn
    uvicorn.run('backend.api:app', host='127.0.0.1', port=8000, reload=False)
