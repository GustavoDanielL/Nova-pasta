# BUILDING — Gerar builds para testes

Este arquivo descreve como gerar builds para o frontend Electron e para o backend Python (PyInstaller).

## Requisitos
- Node.js + npm (para frontend Electron)
- Python 3.10+ e `pip` (para backend)
- PyInstaller (para empacotar o backend)
- `electron-builder` (para empacotar o frontend)

## Backend (Standalone Linux via PyInstaller)

1. Crie e ative um virtualenv:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install pyinstaller
```

2. Use o script já presente `build_linux.sh` que gera executável em `build_output/FinancePro-Linux/`:

```bash
chmod +x build_linux.sh
./build_linux.sh
```

O script gera um executável `FinancePro` e um instalador simples `instalar.sh` dentro de `build_output/FinancePro-Linux/`.

## Frontend (Electron + Tailwind)

1. Entre na pasta `frontend` e rode o script de build:

```bash
cd frontend
chmod +x build_electron.sh
./build_electron.sh
```

2. O build usará `electron-builder` e criará pacotes em `frontend/dist/` (AppImage, .deb conforme configuração).

Observações:
- Se desejar apenas testar localmente sem empacotar, rode `npm install` e `npm run start` dentro de `frontend/`.
- Estes scripts fornecem um ponto de partida; adapte `electron-builder` config em `frontend/package.json` conforme necessário.

## Notas de integração
- O frontend Electron no protótipo faz chamadas para a API local (FastAPI) em `http://127.0.0.1:8000`. Assegure que a API esteja rodando antes de iniciar o app.
- Para produção, recomendo empacotar a API Python junto ao Electron e iniciar a API como subprocesso no `main` do Electron, ou migrar a API para um serviço local rodando em background.
