# Como Executar o FinancePro

Este guia explica como iniciar a aplicação FinancePro (versão Electron).

---

## 📋 Pré-requisitos

Antes de executar, certifique-se de ter instalado:

- **Python 3.8+** com os pacotes:
  - `fastapi`
  - `uvicorn`
  - `pydantic`
  
- **Node.js 18+** com npm

---

## 🚀 Execução Rápida (2 Terminais)

### Terminal 1 - Backend (API)

```bash
cd /caminho/para/Nova-pasta
PYTHONPATH="$PWD" python3 backend/api.py
```

Você verá:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
```

### Terminal 2 - Frontend (Electron)

```bash
cd /caminho/para/Nova-pasta/frontend
npm start
```

O aplicativo Electron será aberto automaticamente.

---

## 📁 Estrutura Necessária

```
Nova-pasta/
├── backend/
│   └── api.py          # Servidor FastAPI
├── frontend/
│   ├── electron.js     # Processo principal Electron
│   ├── index.html      # Interface
│   ├── app.js          # Lógica do app
│   └── package.json    # Dependências Node
├── models/             # Modelos de dados
└── data/               # Banco de dados SQLite
```

---

## ⚡ Comando Único (Modo Desenvolvimento)

Se preferir executar tudo com um comando:

```bash
cd /caminho/para/Nova-pasta/frontend
npm start
```

O Electron tentará iniciar o backend automaticamente se não estiver rodando.

---

## 🔧 Instalação das Dependências

### Python (uma vez)

```bash
cd /caminho/para/Nova-pasta
pip3 install -r requirements.txt
```

### Node.js (uma vez)

```bash
cd /caminho/para/Nova-pasta/frontend
npm install
```

---

## ❌ Solução de Problemas

### Erro: "address already in use" (porta 8000)

O backend já está rodando. Pode continuar normalmente ou encerrar:

```bash
# Verificar processo
lsof -i :8000

# Encerrar
kill $(lsof -t -i :8000)
```

### Erro: "ModuleNotFoundError: No module named 'models'"

Execute o backend da pasta raiz com PYTHONPATH:

```bash
cd /caminho/para/Nova-pasta
PYTHONPATH="$PWD" python3 backend/api.py
```

### Erro: "Cannot find module 'electron'"

Instale as dependências do Node:

```bash
cd /caminho/para/Nova-pasta/frontend
npm install
```

---

## 🎯 Resumo

| Componente | Comando | Porta |
|------------|---------|-------|
| Backend API | `PYTHONPATH="$PWD" python3 backend/api.py` | 8000 |
| Frontend Electron | `npm start` (na pasta frontend) | - |

---

## 📝 Notas

- O backend deve estar rodando **antes** ou o Electron iniciará automaticamente
- Dados são salvos em `data/financepro.db` (SQLite)
- Para recarregar a interface: `Ctrl+Shift+R` no Electron
- Para DevTools: `Ctrl+Shift+I` no Electron
