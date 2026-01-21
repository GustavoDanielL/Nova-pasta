# Melhorias, correções e como rodar (Resumo)

Este documento resume as melhorias aplicadas (scaffold inicial) e passos recomendados para transformar o projeto em um produto pronto.

## O que foi adicionado neste commit
- Backend HTTP mínimo com FastAPI em `backend/api.py` expos endpoints: `/login`, `/clients` (GET/POST), `/loans` (GET/POST), `/payments` (POST).
- Frontend mínimo em Electron usando Tailwind (CDN) em `frontend/` com páginas básicas: login, listagem de clientes e empréstimos. Arquivos: `frontend/index.html`, `frontend/renderer.js`, `frontend/electron.js`, `frontend/package.json`.
- Dependências adicionadas em `requirements.txt`: `fastapi`, `uvicorn`.

Essas mudanças têm o objetivo de iniciar a migração da UI de `customtkinter` para uma stack moderna (Electron + Tailwind). O frontend atual é um *prototype* mínimo para validar fluxo e UX.

## Correções e prioridades recomendadas
1. Corrigir inconsitência de armazenamento/verificação de senha (atributos `senha` vs `password_hash`) — PRIORIDADE ALTA.
2. Habilitar/forçar uso de senha mestra para criptografia e proteger arquivos `.salt` e `.master_password` com permissões restritas — PRIORIDADE ALTA.
3. Remover chaves de licença hardcoded e adotar mecanismo de ativação seguro (servidor ou chave assinada) — PRIORIDADE ALTA.
4. Adicionar testes unitários (autenticação, DB, migrator, endpoints) e pipeline CI — PRIORIDADE ALTA.
5. Refatorar `views/` para desacoplar UI das regras de negócio (introduzir `services/`) — PRIORIDADE MÉDIA.

## Melhores práticas de UX/UI a aplicar (parte de Empréstimos, Registro de Pagamentos e Criação de Clientes)
- Formulários com validação inline e mensagens amigáveis.
- Fluxo de criação de cliente: passo único com campos obrigatórios destacados, confirmação visual após salvar e foco no próximo passo (ex: criar empréstimo).
- Criação de empréstimo: pré-seleção de cliente via busca incremental, preview dos cálculos (valor total, parcelas, juros) antes de confirmar.
- Registrar pagamento: modal com sugestão de valor (próxima parcela), validação de excesso e histórico na mesma modal.
- Feedback visual consistente (toasts, badges de status, cores de estado acessíveis).

## Como rodar o backend (desenvolvimento)
1. Criar ambiente Python e instalar requisitos:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Rodar a API FastAPI:

```bash
python -m backend.api
# ou: uvicorn backend.api:app --reload
```

3. Abrir a interface Electron (em outro terminal):

```bash
cd frontend
npm install
npm run start
```

## Como gerar builds (resumo rápido)
- Backend (Linux): rode `./build_linux.sh` na raiz do projeto (usa PyInstaller). Resultado em `build_output/FinancePro-Linux/`.
- Frontend (Electron): entre em `frontend/` e rode `./build_electron.sh`. Resultado em `frontend/dist/`.

Observação: o frontend do Electron espera a API em `http://127.0.0.1:8000`.

## Próximos passos recomendados para migração completa
1. Implementar páginas completas (React/Vue + Tailwind) com rotas e componentes reutilizáveis.
2. Implementar autenticação com tokens (JWT) e sessões seguras entre Electron e backend local.
3. Remover dependência de `customtkinter` aos poucos ou manter o app Python como fallback.
4. Adicionar testes automatizados e GitHub Actions para lint, type-check e testes.
5. Planejar empacotamento: Electron-builder / electron-forge e instruções cross-platform.

---
Se desejar, posso começar agora pela correção da autenticação (P0) e adicionar testes unitários de `Usuario.verify_password` e do endpoint `/login`.
