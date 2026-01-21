# 📁 Estrutura do Projeto FinancePro

**Atualizado:** 12 de dezembro de 2025  
**Versão:** 2.0 (com SQLite + Criptografia)

## 📂 Estrutura Atual

```
FinancePro/
│
├── 📄 main.py                          # Entry point do aplicativo
├── 📄 config.py                        # Configurações globais
├── 📄 theme_colors.py                  # Cores do tema light
├── 📄 license_manager.py               # Sistema de licenças
│
├── 📄 requirements.txt                 # Dependências Python (versões fixas)
├── 📄 .env.example                     # Exemplo de configuração SMTP
├── 📄 .gitignore                       # Arquivos ignorados pelo Git
│
├── 🔨 build_linux.sh                   # Script de build para Linux
├── 🔨 build_windows.bat                # Script de build para Windows
├── 🔨 GERAR_INSTALADOR.bat             # Gerador de instalador Windows
│
├── 📖 README.md                        # README básico
├── 📖 README_COMPLETO.md               # Documentação completa e detalhada
│
├── 📁 models/                          # Modelos de dados
│   ├── __init__.py
│   ├── cliente.py                      # Classe Cliente
│   ├── emprestimo.py                   # Classe Empréstimo
│   ├── usuario.py                      # Classe Usuário
│   └── database_sqlite.py              # ⭐ Database SQLite + Criptografia AES
│
├── 📁 views/                           # Interface gráfica (CustomTkinter)
│   ├── __init__.py
│   ├── login_view.py                   # Tela de login
│   ├── main_view.py                    # Tela principal (navegação)
│   ├── dashboard_view.py               # Dashboard com gráficos
│   ├── clientes_view.py                # Gestão de clientes
│   ├── emprestimos_view.py             # Gestão de empréstimos
│   ├── notificacoes_view.py            # Notificações e lembretes
│   ├── settings_view.py                # Configurações
│   └── exportacao_view.py              # Exportação (PDF, Excel)
│
├── 📁 utils/                           # Utilitários
│   ├── calculos.py                     # Cálculos financeiros (juros)
│   ├── validators.py                   # Validações (CPF, email, etc)
│   ├── formatters.py                   # Formatação (CPF, telefone, moeda)
│   ├── excel_export.py                 # Exportação Excel
│   ├── pdf_export.py                   # Exportação PDF
│   ├── qr_generator.py                 # Geração de QR Code PIX
│   ├── notifier.py                     # Notificações automáticas (background)
│   ├── logger_config.py                # ⭐ Sistema de logging profissional
│   ├── master_password.py              # ⭐ Gerenciador de senha mestra
│   └── json_migrator.py                # ⭐ Migração JSON → SQLite
│
├── 📁 docs/                            # Documentação técnica
│   ├── LEIA-ME-PRIMEIRO.txt            # Instruções iniciais
│   ├── README_FINAL.md                 # README final antigo
│   ├── GUIA_BUILD.md                   # Guia de build antigo
│   ├── IMPLEMENTACOES.md               # ⭐ Resumo das implementações
│   └── PREPARAR_DISTRIBUICAO.md        # ⭐ Guia de distribuição
│
├── 📁 _obsoleto/                       # ⚠️ Arquivos antigos (não usar!)
│   ├── README.md                       # Explicação do que tem aqui
│   ├── database.py                     # Database JSON antigo
│   ├── docs_antigos/                   # Documentos antigos
│   ├── scripts_antigos/                # Scripts antigos
│   └── testes_antigos/                 # Testes antigos
│
├── 📁 build_output/                    # Saída do build (ignorado no Git)
└── 📁 .venv/                           # Ambiente virtual Python (ignorado)
```

## 🗂️ Dados do Usuário (Criados Automaticamente)

**Localização:**
- **Linux:** `~/Documentos/FinancePro/`
- **Windows:** `C:\Users\<usuario>\Documents\FinancePro\`

```
~/Documentos/FinancePro/
│
├── 🗄️ financepro.db                    # Banco de dados SQLite (PRINCIPAL)
├── 🔐 .salt                            # Salt para criptografia (NÃO DELETAR!)
│
├── 📁 backups/                         # Backups automáticos do banco
│   ├── backup_20251210_120000.db
│   ├── backup_20251210_140000.db
│   └── ...
│
└── 📁 logs/                            # Logs da aplicação
    ├── financepro_20251210.log
    ├── financepro_20251210.log.1       # Backups rotacionados
    └── ...
```

**Configuração:**
- **Linux:** `~/.config/FinancePro/`
- **Windows:** `C:\Users\<usuario>\AppData\Local\FinancePro\`

```
~/.config/FinancePro/
│
├── 🔐 .master_password                 # Hash da senha mestra (NÃO DELETAR!)
└── 🔐 .license                         # Informações de licença
```

## 📊 Fluxo de Dados

```
┌─────────────────┐
│   main.py       │  ← Entry Point
└────────┬────────┘
         │
         ├──► Configura logging (logger_config.py)
         ├──► Solicita senha mestra (master_password.py)
         ├──► Verifica migração JSON → SQLite (json_migrator.py)
         ├──► Inicializa DatabaseSQLite (database_sqlite.py)
         │
         └──► LoginView (login_view.py)
                    │
                    └──► MainView (main_view.py)
                            │
                            ├──► Dashboard (dashboard_view.py)
                            ├──► Clientes (clientes_view.py)
                            ├──► Empréstimos (emprestimos_view.py)
                            ├──► Notificações (notificacoes_view.py)
                            ├──► Exportação (exportacao_view.py)
                            └──► Configurações (settings_view.py)
```

## 🔐 Segurança

### Dados Criptografados (AES-256):
- ✅ CPF/CNPJ dos clientes
- ✅ E-mails dos clientes
- ✅ Telefones dos clientes

### Dados em Hash (PBKDF2):
- ✅ Senha mestra (100.000 iterações SHA-256)
- ✅ Senhas de usuários do sistema

### Dados Protegidos (não versionados):
- ✅ `.env` - Credenciais SMTP
- ✅ `financepro.db` - Banco de dados
- ✅ `.master_password` - Hash da senha
- ✅ `.salt` - Salt da criptografia
- ✅ `logs/` - Logs da aplicação

## 📦 Dependências Principais

```
customtkinter==5.2.2          # Interface gráfica moderna
pillow==10.4.0                 # Manipulação de imagens
qrcode[pil]==7.4.2            # Geração de QR Code
fpdf2==2.8.1                   # Geração de PDF
reportlab==4.2.5               # Relatórios PDF
openpyxl==3.1.5                # Exportação Excel
cryptography==43.0.3           # ⭐ Criptografia AES
python-dotenv==1.0.1           # ⭐ Variáveis de ambiente
```

## 🚀 Como Executar

### Desenvolvimento:
```bash
# 1. Ativar ambiente virtual
source .venv/bin/activate        # Linux/Mac
.venv\Scripts\activate           # Windows

# 2. Instalar dependências
pip install -r requirements.txt

# 3. Executar
python main.py
```

### Produção (Executável):
```bash
# Linux
./build_linux.sh
./dist/FinancePro

# Windows
build_windows.bat
dist\FinancePro.exe
```

## 📝 Arquivos Principais

### Core:
- `main.py` - Inicialização, integração com senha mestra e migração
- `models/database_sqlite.py` - Banco de dados com criptografia
- `utils/logger_config.py` - Sistema de logging

### Interface:
- `views/main_view.py` - Navegação principal
- `views/clientes_view.py` - CRUD de clientes
- `views/emprestimos_view.py` - CRUD de empréstimos

### Segurança:
- `utils/master_password.py` - Tela de senha mestra
- `utils/json_migrator.py` - Migração segura de dados
- `license_manager.py` - Sistema de licenças

### Documentação:
- `README_COMPLETO.md` - Guia completo de uso
- `docs/IMPLEMENTACOES.md` - Resumo técnico
- `docs/PREPARAR_DISTRIBUICAO.md` - Guia de distribuição

## ⚠️ Arquivos Obsoletos

A pasta `_obsoleto/` contém:
- Database JSON antigo (sem criptografia)
- Documentos de desenvolvimento antigos
- Scripts de teste antigos
- Testes unitários antigos

**NÃO USE nada da pasta `_obsoleto/`!**

Todos foram substituídos por versões melhores e mais seguras.

## 🔄 Changelog

### Versão 2.0 (12/12/2025):
- ✅ Migração JSON → SQLite
- ✅ Criptografia AES-256 para dados sensíveis
- ✅ Sistema de senha mestra
- ✅ Logging profissional com rotação
- ✅ Proteção SMTP com .env
- ✅ Thread-safe com locks
- ✅ Documentação completa

### Versão 1.0:
- Interface CustomTkinter
- CRUD de clientes e empréstimos
- Cálculos financeiros
- Exportação PDF/Excel
- Sistema de notificações

---

**Desenvolvido com ❤️ para gestão financeira profissional e segura**
