# 📁 Estrutura do Projeto - FinancePro

## 🗂️ Organização dos Arquivos

```
FinancePro/
│
├── 📄 main.py                    ← INICIE AQUI (Execute este arquivo)
├── 📄 requirements.txt            ← Dependências do projeto
├── 📄 README.md                   ← Documentação completa
│
├── 📁 models/                     ← Modelos de dados
│   ├── __init__.py
│   ├── cliente.py
│   ├── emprestimo.py
│   ├── database.py
│   └── usuario.py
│
├── 📁 views/                      ← Interfaces gráficas
│   ├── __init__.py
│   ├── main_view.py
│   ├── login_view.py
│   ├── dashboard_view.py
│   ├── clientes_view.py
│   ├── emprestimos_view.py
│   ├── notificacoes_view.py
│   ├── exportacao_view.py
│   └── settings_view.py
│
├── 📁 utils/                      ← Funções utilitárias
│   ├── calculos.py
│   ├── validators.py
│   ├── excel_export.py
│   ├── pdf_export.py
│   ├── notifier.py
│   └── qr_generator.py
│
├── 📁 data/                       ← Dados do programa (JSON)
│   ├── clientes.json
│   ├── emprestimos.json
│   ├── usuarios.json
│   ├── lembretes.json
│   └── backups/                   ← Backups automáticos
│
├── 📁 docs/                       ← Documentação
│   ├── LEIA-ME-PRIMEIRO.txt      ← Instruções rápidas
│   ├── GUIA_BUILD.md              ← Como gerar executável
│   └── README_FINAL.md
│
├── 📁 scripts/                    ← Scripts de utilidade
│   ├── build.py                   ← Gera executável
│   ├── GERAR_INSTALADOR.bat       ← Clique para gerar instalador
│   ├── run_app_debug.py
│   └── debug_imports.py
│
├── 📁 tests/                      ← Testes automatizados
│   ├── test_*.py                  ← Vários testes
│   └── ...
│
├── 📁 build_output/               ← Saída de builds
│   ├── releases/                  ← Executáveis e instaladores
│   ├── *_relatorio*.xlsx          ← Arquivos Excel gerados
│   └── teste_*.xlsx               ← Testes de exportação
│
└── 📁 venv/                       ← Ambiente virtual Python (ignorado)
```

---

## 🚀 Como Usar

### 1️⃣ **Primeira Vez - Instalação**

```bash
# 1. Abra PowerShell na pasta do projeto
cd "c:\Users\seu_usuario\Nova pasta"

# 2. Instale as dependências
pip install -r requirements.txt

# 3. Execute o programa
python main.py
```

### 2️⃣ **Próximas Vezes - Apenas Execute**

```bash
python main.py
```

### 3️⃣ **Gerar Executável para Distribuição**

```bash
# Opção A: Clique duplo em GERAR_INSTALADOR.bat
GERAR_INSTALADOR.bat

# Opção B: Via PowerShell
python scripts/build.py
```

---

## 📋 Descrição das Pastas

### `models/` - Modelos de Dados
- Define as classes: Cliente, Empréstimo, Usuário
- Lógica de negócio e cálculos
- Persistência em JSON

### `views/` - Interface Gráfica
- Telas do programa
- Interação com usuário
- CustomTkinter para UI moderna

### `utils/` - Utilitários
- Funções compartilhadas
- Cálculos de juros
- Validações
- Exportação para Excel
- Notificações por email

### `data/` - Armazenamento
- Arquivos JSON com dados
- Backups automáticos
- Versionamento de dados

### `docs/` - Documentação
- Guias de uso
- Instruções de build
- README e FAQ

### `scripts/` - Automação
- Build script (gera executável)
- Teste e debug
- Utilitários

### `tests/` - Testes
- Testes unitários
- Testes de integração
- Validação de funcionalidades

### `build_output/` - Saída de Compilação
- Executáveis gerados
- Instaladores
- Arquivos Excel de teste

---

## ✨ Arquivos Importantes na Raiz

| Arquivo | Descrição |
|---------|-----------|
| `main.py` | 🚀 Ponto de entrada do programa |
| `requirements.txt` | 📦 Dependências a instalar |
| `README.md` | 📖 Documentação completa |
| `GERAR_INSTALADOR.bat` | 📦 Gera executável/instalador |

---

## 🔧 Estrutura de Dados (JSON)

Os dados são armazenados em `data/` como JSON:

```json
// clientes.json
[
  {
    "id": "CLI20251117...",
    "nome": "João Silva",
    "cpf_cnpj": "123.456.789-00",
    "email": "joao@email.com",
    ...
  }
]

// emprestimos.json
[
  {
    "id": "EMP20251117...",
    "cliente_id": "CLI20251117...",
    "valor_emprestado": 5000.00,
    "taxa_juros": 2.5,
    "pagamentos": [...]
    ...
  }
]
```

---

## 🔄 Fluxo de Dados

```
main.py (Inicialização)
   ↓
LoginView (Autenticação)
   ↓
MainView (Menu Principal)
   ↓
Database (models/database.py)
   ↓
JSON files (data/*.json)
   ↓
Backups (data/backups/)
```

---

## 📊 Dependências

```
customtkinter==5.2.1    → Interface gráfica moderna
matplotlib==3.7.0       → Gráficos
openpyxl==3.10.0        → Exportação Excel
```

Instale com: `pip install -r requirements.txt`

---

## 🐛 Troubleshooting

### Erro ao executar `python main.py`
```
1. Verifique se Python está no PATH
2. Instale dependências: pip install -r requirements.txt
3. Verifique pasta data/ existe
```

### Erro ao gerar executável
```
1. Instale PyInstaller: pip install pyinstaller
2. Execute: python scripts/build.py
3. Verifique se há espaço em disco
```

### Dados não salvam
```
1. Verifique permissões na pasta data/
2. Verifique espaço em disco
3. Consulte data/backups/ para recuperar dados
```

---

## 💡 Dicas

- **Backup de dados**: Sempre presente em `data/backups/`
- **Testes**: Execute `python tests/test_*.py` para testar funcionalidades
- **Debug**: Use `scripts/debug_imports.py` para diagnosticar problemas
- **Build**: Gere executável com `GERAR_INSTALADOR.bat`

---

## 📞 Versão

**FinancePro v1.0.0**
Última atualização: 17/11/2025

---

**👉 Comece aqui**: Execute `python main.py`
