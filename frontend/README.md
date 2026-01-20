# FinancePro - Frontend Electron

Interface moderna e fluida para o sistema FinancePro, construída com Electron.

## 🚀 Características

- **Interface Moderna**: Design clean e profissional com animações suaves
- **Tema Claro/Escuro**: Suporte completo a temas
- **Responsivo**: Adaptável a diferentes tamanhos de tela
- **Dashboard Interativo**: Gráficos e métricas em tempo real
- **UX Otimizado**: Feedback visual, validações inline, loading states

## 📦 Estrutura

```
frontend/
├── electron.js     # Processo principal do Electron
├── preload.js      # Script de preload (segurança)
├── index.html      # Interface principal
├── styles.css      # Estilos modernos
├── app.js          # Lógica da aplicação
├── package.json    # Configurações e dependências
└── assets/         # Ícones e recursos
```

## 🛠️ Requisitos

- Node.js 18+
- npm 9+
- Python 3.8+ (para o backend)
- Dependências Python instaladas (`pip install -r requirements.txt`)

## 📥 Instalação

```bash
# Navegar para o diretório frontend
cd frontend

# Instalar dependências do Electron
npm install
```

## 🎯 Executar em Desenvolvimento

```bash
# Iniciar o backend Python (em um terminal separado)
cd ..
python -m uvicorn backend.api:app --host 127.0.0.1 --port 8000

# Iniciar o Electron
npm start

# Ou com logs de debug
npm run dev
```

## 🔨 Build para Produção

### Linux (AppImage + .deb)

```bash
# Build completo
npm run build:linux

# Apenas AppImage
npm run build:linux:appimage

# Apenas .deb
npm run build:linux:deb
```

### Windows

```bash
npm run build:win
```

### Usando o Script de Build

```bash
# Na raiz do projeto
./scripts/build_electron.sh build

# Comandos disponíveis:
# install  - Instalar dependências
# build    - Build completo para Linux
# appimage - Apenas AppImage
# deb      - Apenas .deb
# run      - Executar o app
# dev      - Modo desenvolvimento
```

## 📁 Arquivos Gerados

Após o build, os executáveis estarão em `../dist/`:

- `FinancePro-2.0.0.AppImage` - Executável universal Linux
- `financepro_2.0.0_amd64.deb` - Pacote Debian/Ubuntu
- `FinancePro Setup 2.0.0.exe` - Instalador Windows

## 🎨 Temas

A interface suporta tema claro e escuro:

- Clique no ícone 🌙/☀️ no header
- Ou acesse Configurações → Aparência

O tema é salvo automaticamente no localStorage.

## 🔐 Credenciais Padrão

- **Usuário**: admin
- **Senha**: admin123

## 🏗️ Arquitetura

```
┌─────────────────────────────────────────────┐
│              Electron (Frontend)             │
│  ┌─────────┐  ┌─────────┐  ┌─────────────┐  │
│  │ index   │  │ app.js  │  │ styles.css  │  │
│  │ .html   │  │         │  │             │  │
│  └────┬────┘  └────┬────┘  └─────────────┘  │
│       └────────────┴────────────────────────┤
│                     │ fetch()               │
│                     ▼                       │
├─────────────────────────────────────────────┤
│              FastAPI (Backend)              │
│  ┌─────────────────────────────────────┐    │
│  │  http://127.0.0.1:8000              │    │
│  │  /login, /clients, /loans, etc      │    │
│  └─────────────────────────────────────┘    │
│                     │                       │
│                     ▼                       │
│  ┌─────────────────────────────────────┐    │
│  │  SQLite Database                    │    │
│  │  ~/Documentos/FinancePro/           │    │
│  └─────────────────────────────────────┘    │
└─────────────────────────────────────────────┘
```

## 📝 Licença

Proprietary - Todos os direitos reservados © 2024-2026 FinancePro

