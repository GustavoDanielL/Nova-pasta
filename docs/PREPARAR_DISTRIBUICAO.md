# 📦 Guia de Preparação para Distribuição

## ⚠️ ANTES DE SUBIR NO GITHUB OU DISTRIBUIR

Siga estes passos para garantir segurança e tamanho adequado do pacote:

## 1. Remover .git (se for rezipar)

Se você já tem um repositório Git e quer criar um ZIP limpo:

```bash
# Linux/Mac
rm -rf .git

# Windows (PowerShell)
Remove-Item -Recurse -Force .git
```

**Quando remover?**
- ✅ Se vai criar um ZIP para distribuir
- ✅ Se vai enviar para cliente
- ❌ NÃO remover se vai fazer push para GitHub

## 2. Remover .venv

A pasta `.venv` contém dependências Python e pode ter **centenas de MB**.

```bash
# Linux/Mac
rm -rf .venv

# Windows (PowerShell)
Remove-Item -Recurse -Force .venv
```

**⚠️ SEMPRE remover antes de:**
- Subir no GitHub
- Criar ZIP para distribuição
- Enviar para cliente

## 3. Limpar arquivos temporários

```bash
# Linux/Mac
rm -rf __pycache__ models/__pycache__ views/__pycache__ utils/__pycache__
rm -rf build/ dist/
rm -rf data/ logs/
rm -f *.db *.db-journal .license .salt .master_password

# Windows (PowerShell)
Remove-Item -Recurse -Force __pycache__, models\__pycache__, views\__pycache__, utils\__pycache__
Remove-Item -Recurse -Force build, dist
Remove-Item -Recurse -Force data, logs
Remove-Item -Force *.db, *.db-journal, .license, .salt, .master_password
```

## 4. Verificar .gitignore

Confirme que o `.gitignore` contém:

```gitignore
.venv/
__pycache__/
*.db
data/
logs/
.env
.master_password
.salt
.license
```

## 5. Criar requirements.txt atualizado

```bash
# Ativar venv primeiro (se ainda existir)
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows

# Gerar requirements.txt
pip freeze > requirements.txt
```

## 6. Preparar para GitHub

```bash
# 1. Verificar status
git status

# 2. Adicionar apenas arquivos necessários
git add .

# 3. Commit
git commit -m "Versão de produção - Segurança implementada"

# 4. Push
git push origin main
```

## 7. Criar Executável para Distribuição

### Windows

```bash
# 1. Instalar dependências (se removeu .venv)
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt

# 2. Instalar PyInstaller
pip install pyinstaller

# 3. Gerar executável
pyinstaller --onefile --windowed --name=FinancePro --icon=icon.ico main.py

# 4. Executável estará em dist/FinancePro.exe
```

### Linux

```bash
# 1. Instalar dependências
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# 2. Instalar PyInstaller
pip install pyinstaller

# 3. Gerar executável
pyinstaller --onefile --windowed --name=FinancePro main.py

# 4. Executável estará em dist/FinancePro
```

## 8. Pacote Final para Distribuição

### Estrutura do ZIP:

```
FinancePro/
├── FinancePro.exe (ou FinancePro)   # Executável
├── README.md                         # Documentação
├── .env.example                      # Exemplo de configuração
└── LICENSE                           # Licença (se aplicável)
```

### Criar ZIP:

```bash
# Linux/Mac
zip -r FinancePro_v1.0.zip FinancePro.exe README.md .env.example

# Windows (PowerShell)
Compress-Archive -Path FinancePro.exe, README.md, .env.example -DestinationPath FinancePro_v1.0.zip
```

## 9. Checklist Final

Antes de distribuir, verifique:

- [ ] `.venv/` removido
- [ ] `.git/` removido (se for ZIP)
- [ ] Arquivos `.db`, `data/`, `logs/` removidos
- [ ] `.env` NÃO incluído (apenas `.env.example`)
- [ ] `__pycache__/` removido
- [ ] Executável testado em máquina limpa
- [ ] README.md atualizado
- [ ] Versão documentada

## 10. Segurança - Verificação Final

**O que NÃO deve estar no pacote:**

❌ `.env` (contém credenciais SMTP)
❌ `.git/` (contém histórico e possíveis credenciais)
❌ `.venv/` (muito grande, desnecessário)
❌ `data/` (dados dos usuários)
❌ `*.db` (banco de dados com dados)
❌ `.license`, `.master_password`, `.salt` (configurações locais)
❌ `logs/` (logs locais)

**O que DEVE estar:**

✅ Executável (`.exe` ou binário Linux)
✅ `README.md` ou `README_COMPLETO.md`
✅ `.env.example` (modelo de configuração)
✅ `LICENSE` (se aplicável)

## 11. Teste de Distribuição

Antes de distribuir para clientes:

1. **Copie** o ZIP para uma máquina limpa (ou VM)
2. **Extraia** o conteúdo
3. **Execute** o FinancePro
4. **Teste**:
   - Configuração de senha mestra
   - Login com admin/admin123
   - Cadastrar cliente
   - Criar empréstimo
   - Configurar SMTP (.env)
   - Enviar cobrança

5. **Verifique tamanho**: Deve ser < 50MB

## 12. Script Automatizado de Limpeza

Crie um arquivo `clean_for_dist.sh` (Linux/Mac):

```bash
#!/bin/bash
echo "🧹 Limpando projeto para distribuição..."

rm -rf .venv
rm -rf .git
rm -rf __pycache__ models/__pycache__ views/__pycache__ utils/__pycache__
rm -rf build/ dist/
rm -rf data/ logs/
rm -f *.db *.db-journal .license .salt .master_password .env

echo "✓ Projeto limpo!"
echo "Tamanho do diretório:"
du -sh .
```

Ou `clean_for_dist.ps1` (Windows PowerShell):

```powershell
Write-Host "🧹 Limpando projeto para distribuição..." -ForegroundColor Green

Remove-Item -Recurse -Force .venv, .git -ErrorAction SilentlyContinue
Remove-Item -Recurse -Force __pycache__, models\__pycache__, views\__pycache__, utils\__pycache__ -ErrorAction SilentlyContinue
Remove-Item -Recurse -Force build, dist -ErrorAction SilentlyContinue
Remove-Item -Recurse -Force data, logs -ErrorAction SilentlyContinue
Remove-Item -Force *.db, *.db-journal, .license, .salt, .master_password, .env -ErrorAction SilentlyContinue

Write-Host "✓ Projeto limpo!" -ForegroundColor Green
```

---

**Desenvolvido com ❤️ - Mantenha a segurança sempre em primeiro lugar!**
