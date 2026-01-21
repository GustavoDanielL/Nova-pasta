# 🧪 Como Testar as Melhorias - FinancePro

## ✅ Lista de Verificação

### 1️⃣ Testar Formatação Automática de Campos

#### CPF/CNPJ
1. Abra o app: `python main.py`
2. Clique em **"+ Novo Cliente"**
3. No campo **CPF/CNPJ**, digite apenas números:
   - Digite: `12345678901`
   - Deve formatar para: `123.456.789-01` (CPF)
   - Digite: `12345678901234`
   - Deve formatar para: `12.345.678/9012-34` (CNPJ)

#### Telefone
1. No campo **Telefone**, digite apenas números:
   - Digite: `11987654321`
   - Deve formatar para: `(11) 98765-4321` (Celular)
   - Digite: `1140028922`
   - Deve formatar para: `(11) 4002-8922` (Fixo)

#### Data de Vencimento (Empréstimo)
1. Clique em **"Novo Empréstimo"** no menu
2. No campo **Data de Vencimento**, digite apenas números:
   - Digite: `31122025`
   - Deve formatar para: `31/12/2025`

---

### 2️⃣ Testar Cabeçalho Alinhado

1. Vá para a aba **Clientes**
2. Verifique se o cabeçalho está alinhado com os dados:
   - Coluna **Status** alinhada com ícones ●/✓/○
   - Coluna **Nome** alinhada com nomes dos clientes
   - Coluna **CPF/CNPJ** alinhada com documentos
   - Coluna **Telefone** alinhada com telefones
   - Coluna **Ações** alinhada com botões

---

### 3️⃣ Testar Pasta em Documentos

#### Linux
```bash
# Verificar se a pasta foi criada
ls -la ~/Documentos/FinancePro/

# Deve mostrar:
# - clientes.json
# - emprestimos.json
# - usuarios.json
# - lembretes.json
# - backups/
```

#### Windows
```cmd
# Verificar se a pasta foi criada
dir %USERPROFILE%\Documents\FinancePro

# Deve mostrar os mesmos arquivos
```

---

### 4️⃣ Testar Cache de Performance

1. Abra o terminal onde rodou `python main.py`
2. Navegue entre as abas: Dashboard → Clientes → Empréstimos → Notificações
3. No console, deve aparecer:
   ```
   [CACHE] Reutilizando clientes do cache (instantâneo)
   [CACHE] Reutilizando emprestimos do cache (instantâneo)
   [CACHE] Reutilizando notificacoes do cache (instantâneo)
   ```
4. A navegação deve ser **instantânea** (sem delay)

---

### 5️⃣ Testar Build do Executável

#### Linux
```bash
# Dar permissão ao script
chmod +x build_linux.sh

# Executar build (demora ~2-5 minutos)
./build_linux.sh

# Testar executável gerado
./build_output/FinancePro-Linux/FinancePro
```

#### Windows
```cmd
REM Executar build (demora ~2-5 minutos)
build_windows.bat

REM Testar executável gerado
build_output\FinancePro-Windows\FinancePro.exe
```

---

## 🐛 Problemas Comuns e Soluções

### Problema: Formatação não está funcionando

**Solução:**
```bash
# Limpar cache do Python
rm -rf __pycache__ models/__pycache__ views/__pycache__ utils/__pycache__

# Executar novamente
python main.py
```

### Problema: Pasta não foi criada em Documentos

**Solução:**
- Faça login no app (primeira vez)
- A pasta é criada na primeira execução
- Verifique se tem permissão de escrita em `~/Documentos`

### Problema: Build falha com "PyInstaller not found"

**Solução:**
```bash
# Instalar PyInstaller
pip install pyinstaller

# Tentar build novamente
./build_linux.sh  # ou build_windows.bat
```

### Problema: Executável não abre

**Solução Linux:**
```bash
# Dar permissão de execução
chmod +x build_output/FinancePro-Linux/FinancePro

# Verificar dependências
ldd build_output/FinancePro-Linux/FinancePro
```

**Solução Windows:**
- Execute como Administrador
- Desabilite antivírus temporariamente (pode bloquear)
- Verifique se não está em quarentena

---

## 📊 Checklist Completo

- [ ] Formatação de CPF funciona (###.###.###-##)
- [ ] Formatação de CNPJ funciona (##.###.###/####-##)
- [ ] Formatação de telefone celular funciona ((##) #####-####)
- [ ] Formatação de telefone fixo funciona ((##) ####-####)
- [ ] Formatação de data funciona (DD/MM/AAAA)
- [ ] Cabeçalho de clientes está alinhado
- [ ] Pasta FinancePro foi criada em Documentos
- [ ] Dados foram migrados da pasta `data/` antiga
- [ ] Cache está funcionando (mensagens no console)
- [ ] Navegação entre abas é instantânea
- [ ] Build Linux gera executável
- [ ] Build Windows gera executável
- [ ] Executável funciona sem Python instalado

---

## 🎯 Teste Completo em 5 Minutos

```bash
# 1. Limpar cache
rm -rf __pycache__ models/__pycache__ views/__pycache__ utils/__pycache__

# 2. Executar app
python main.py

# 3. Testar formatação
# - Criar novo cliente com CPF e telefone
# - Criar novo empréstimo com data

# 4. Verificar cache
# - Navegar entre abas e ver mensagens [CACHE] no terminal

# 5. Verificar pasta
ls ~/Documentos/FinancePro/

# 6. (Opcional) Testar build
./build_linux.sh
./build_output/FinancePro-Linux/FinancePro
```

---

## 📝 Relatório de Teste

Após testar, preencha:

```
Data: ___/___/___
Sistema: [ ] Linux  [ ] Windows
Versão Python: _______

Funcionalidades Testadas:
[ ] Formatação CPF/CNPJ - Status: ___
[ ] Formatação Telefone - Status: ___
[ ] Formatação Data - Status: ___
[ ] Cabeçalho Alinhado - Status: ___
[ ] Pasta em Documentos - Status: ___
[ ] Cache Performance - Status: ___
[ ] Build Executável - Status: ___

Observações:
_________________________________
_________________________________
```

---

**Boa sorte com os testes!** 🚀
