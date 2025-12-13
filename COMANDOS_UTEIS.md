# 🛠️ Comandos Úteis - FinancePro

## 🚀 Execução

### Desenvolvimento
```bash
# Ativar ambiente virtual
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows

# Executar aplicação
python main.py

# Criar dados de teste
python criar_dados_teste.py
```

### Produção
```bash
# Gerar executável Linux
./build_linux.sh

# Gerar executável Windows
build_windows.bat

# Executável gerado em:
# build_output/FinancePro
```

## 🔍 Debug e Diagnóstico

### Verificar Logs
```bash
# Ver últimos logs (Linux)
tail -f ~/Documentos/FinancePro/logs/financepro_$(date +%Y%m%d).log

# Ver erros apenas
grep "ERROR\|CRITICAL" ~/Documentos/FinancePro/logs/*.log

# Ver últimas 50 linhas
tail -50 ~/Documentos/FinancePro/logs/financepro_*.log
```

### Verificar Banco de Dados
```bash
# Abrir SQLite (se não criptografado)
sqlite3 ~/Documentos/FinancePro/financepro.db

# Ver tabelas
.tables

# Ver schema
.schema clientes

# Contar registros
SELECT COUNT(*) FROM clientes;
SELECT COUNT(*) FROM emprestimos;
```

### Verificar Estado
```bash
# Ver tamanho do banco
du -h ~/Documentos/FinancePro/financepro.db

# Ver backups
ls -lh ~/Documentos/FinancePro/backups/

# Ver arquivos sensíveis
ls -la ~/Documentos/FinancePro/ | grep "^\."
```

## 🧹 Limpeza

### Limpar Cache
```bash
# Remover __pycache__
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null

# Remover .pyc
find . -name "*.pyc" -delete

# Remover logs antigos
rm -f ~/Documentos/FinancePro/logs/*.log.{1..4}
```

### Limpar Testes
```bash
# Remover arquivos de teste
rm -f test_*.py debug_*.log debug_*.txt

# Remover exports de teste
rm -f *.xlsx *.xls
```

### Reset Completo (⚠️ Cuidado!)
```bash
# Backup antes!
cp -r ~/Documentos/FinancePro ~/Documentos/FinancePro_backup_$(date +%Y%m%d)

# Remover banco e recomeçar
rm -f ~/Documentos/FinancePro/financepro.db
rm -f ~/Documentos/FinancePro/.salt

# Próxima execução criará novo banco
python main.py
```

## 📦 Gestão de Dependências

### Instalar Dependências
```bash
# Instalar todas
pip install -r requirements.txt

# Atualizar pip
pip install --upgrade pip

# Verificar instaladas
pip list | grep -E "customtkinter|matplotlib|openpyxl|pycryptodome"
```

### Criar Ambiente Virtual
```bash
# Criar
python -m venv .venv

# Ativar (Linux)
source .venv/bin/activate

# Ativar (Windows)
.venv\Scripts\activate

# Instalar
pip install -r requirements.txt
```

### Atualizar requirements.txt
```bash
# Gerar com versões exatas
pip freeze > requirements.txt

# Ou manualmente manter apenas principais
cat > requirements.txt << EOF
customtkinter==5.2.1
matplotlib==3.7.0
openpyxl==3.10.0
pycryptodome==3.19.0
EOF
```

## 🔐 Segurança

### Verificar Permissões
```bash
# Banco deve ser 600 (só owner pode ler/escrever)
chmod 600 ~/Documentos/FinancePro/financepro.db
chmod 600 ~/Documentos/FinancePro/.salt

# Ver permissões
ls -l ~/Documentos/FinancePro/
```

### Backup Manual
```bash
# Criar backup com timestamp
cp ~/Documentos/FinancePro/financepro.db \
   ~/Documentos/FinancePro/backups/manual_$(date +%Y%m%d_%H%M%S).db

# Criar backup compactado
tar -czf ~/financepro_backup_$(date +%Y%m%d).tar.gz \
    ~/Documentos/FinancePro/
```

### Restaurar Backup
```bash
# Listar backups disponíveis
ls -lth ~/Documentos/FinancePro/backups/

# Restaurar (⚠️ sobrescreve atual!)
cp ~/Documentos/FinancePro/backups/backup_YYYYMMDD_HHMMSS.db \
   ~/Documentos/FinancePro/financepro.db
```

## 📊 Análise

### Contar Linhas de Código
```bash
# Python files (sem .venv e _obsoleto)
find . -name "*.py" -not -path "./.venv/*" -not -path "./_obsoleto/*" \
    -exec wc -l {} + | tail -1

# Por diretório
wc -l models/*.py views/*.py utils/*.py
```

### Estatísticas
```bash
# Tamanho por diretório
du -sh models/ views/ utils/ data/

# Total de arquivos Python
find . -name "*.py" -not -path "./.venv/*" | wc -l

# Arquivos modificados hoje
find . -name "*.py" -mtime 0 -not -path "./.venv/*"
```

## 🐛 Troubleshooting

### App não inicia
```bash
# Verificar Python
python --version  # deve ser 3.8+

# Verificar dependências
pip list

# Verificar erros no log
tail -20 ~/Documentos/FinancePro/logs/financepro_*.log

# Tentar em modo debug
python main.py --debug  # (se implementado)
```

### Erro de criptografia
```bash
# Verificar se .salt existe
ls -la ~/Documentos/FinancePro/.salt

# Se perdeu a senha, não tem como recuperar dados
# Única opção: resetar banco (perde tudo)
rm ~/Documentos/FinancePro/financepro.db
rm ~/Documentos/FinancePro/.salt
```

### Exportação não funciona
```bash
# Verificar openpyxl
pip show openpyxl

# Reinstalar se necessário
pip uninstall openpyxl -y
pip install openpyxl==3.10.0

# Testar manualmente
python -c "from utils.excel_export import gerar_excel_relatorio_completo; print('OK')"
```

### Interface não aparece
```bash
# Verificar CustomTkinter
pip show customtkinter

# Reinstalar
pip uninstall customtkinter -y
pip install customtkinter==5.2.1

# No Linux, pode precisar de:
sudo apt install python3-tk  # Debian/Ubuntu
sudo dnf install python3-tkinter  # Fedora
```

## 🔄 Git

### Commit Safe
```bash
# Ver o que vai commitar
git status

# Verificar .gitignore está funcionando
git check-ignore data/* .venv/* *.db

# Commit apenas código
git add models/ views/ utils/ *.py requirements.txt README.md
git commit -m "feat: implementação SQLite com AES-256"
git push
```

### Ignorar arquivos sensíveis
```bash
# Se acidentalmente commitou .db
git rm --cached data/financepro.db
git commit -m "remove: arquivo sensível"

# Se commitou .env
git rm --cached .env
git commit -m "remove: credenciais"
```

## 📈 Performance

### Otimizar Banco
```bash
sqlite3 ~/Documentos/FinancePro/financepro.db << EOF
VACUUM;
ANALYZE;
.quit
EOF
```

### Limpar Cache Python
```bash
# Remover cache compilado
python -m py_compile models/*.py views/*.py utils/*.py
rm -rf __pycache__ models/__pycache__ views/__pycache__ utils/__pycache__
```

## 🎯 Testes Rápidos

### Teste Completo
```bash
# 1. Limpar dados antigos
rm -f ~/Documentos/FinancePro/financepro.db

# 2. Criar dados de teste
python criar_dados_teste.py

# 3. Executar app
python main.py

# 4. Verificar logs
tail -f ~/Documentos/FinancePro/logs/financepro_*.log
```

### Teste de Exportação
```bash
python -c "
from models.database_sqlite import DatabaseSQLite
from utils.excel_export import gerar_excel_relatorio_completo
from pathlib import Path

db = DatabaseSQLite(Path('~/Documentos/FinancePro/financepro.db').expanduser(), 'senha123')
print(f'Clientes: {len(db.clientes)}')
print(f'Empréstimos: {len(db.emprestimos)}')

if len(db.emprestimos) > 0:
    arquivo = gerar_excel_relatorio_completo(db)
    print(f'Excel gerado: {arquivo}')
else:
    print('Sem dados para exportar')
"
```

---

**💡 Dica**: Salve este arquivo como referência rápida!

**📚 Mais informações**: Consulte `docs/IMPLEMENTACOES.md`
