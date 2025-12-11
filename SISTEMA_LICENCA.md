# 🔐 Sistema de Licença e Proteção - FinancePro

## 📋 Informações de Login

### Credenciais Padrão (mantidas em todas as instalações)
```
Usuário: admin
Senha: admin123
```

**IMPORTANTE:** Essas credenciais são criadas automaticamente na primeira execução e ficam salvas em:
- Linux: `~/Documentos/FinancePro/usuarios.json`
- Windows: `C:\Users\Usuario\Documents\FinancePro\usuarios.json`

---

## 🛡️ Como Funciona a Proteção

### Sistema de Licença Baseado em Hardware

O FinancePro possui proteção básica contra cópias não autorizadas:

1. **ID Único da Máquina**
   - Cada computador gera um ID único baseado no hardware
   - ID combina: MAC Address + Nome do PC + Sistema Operacional
   - Exemplo: `a1b2c3d4e5f6g7h8`

2. **Licença Trial (30 dias)**
   - Na primeira execução, cria licença trial automaticamente
   - Válida por 30 dias
   - Vinculada ao computador específico

3. **Arquivo de Licença**
   - Salvo em: `~/Documentos/FinancePro/.license`
   - Contém: Machine ID, chave criptografada, data de expiração
   - **Não funciona se copiado para outro PC**

### O que a Proteção Faz

✅ **Impede:**
- Copiar executável para outro computador
- Compartilhar licença entre máquinas
- Usar após expiração

✅ **Permite:**
- Atualizações enviando novo executável (mesma máquina)
- Backup dos dados (pasta Documentos/FinancePro)
- Reinstalação no mesmo PC

---

## 🚀 Como Distribuir para Clientes

### 1. Gerar Executável

**Linux:**
```bash
./build_linux.sh
```

**Windows:**
```cmd
build_windows.bat
```

### 2. Enviar Executável

Você envia apenas o executável:
- Linux: `FinancePro` (arquivo único)
- Windows: `FinancePro.exe` (arquivo único)

### 3. Cliente Executa

Na **primeira execução**:
1. Cria automaticamente pasta em Documentos
2. Gera licença trial (30 dias)
3. Mostra ID da máquina
4. Login com `admin` / `admin123`

### 4. Verificar ID da Máquina

Cliente pode ver o ID em:
- Tela "ℹ️ Sobre" (botão na sidebar)
- Ou ao tentar usar após expiração

---

## 🔑 Como Gerar Licença para Cliente

### Quando Cliente Envia o Machine ID

**Exemplo:** Cliente enviou ID `a1b2c3d4e5f6g7h8`

```python
# Execute no seu Python:
from utils.license import generate_license_key_for_machine

machine_id = "a1b2c3d4e5f6g7h8"  # ID que cliente enviou
license_key = generate_license_key_for_machine(machine_id)
print(license_key)

# Resultado:
# 9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08
```

### Enviar Chave para Cliente

Envie a chave gerada. Cliente deve:

1. Abrir o app
2. Clicar em "ℹ️ Sobre"
3. **(TODO: Adicionar botão "Ativar Licença" na tela)**
4. Colar a chave recebida

---

## 🔄 Como Enviar Atualizações

### Processo Simples

1. **Você modifica o código**
2. **Gera novo executável:**
   ```bash
   ./build_linux.sh  # ou build_windows.bat
   ```
3. **Envia novo executável para cliente**
4. **Cliente substitui o arquivo antigo**
5. **Dados são mantidos** (pasta Documentos/FinancePro)

### ✅ O que é Preservado

- Todos os dados (clientes, empréstimos, etc)
- Licença ativa
- Configurações
- Login e senha

### ⚠️ IMPORTANTE

- Cliente deve usar no **mesmo computador**
- Não precisa reativar licença
- Pasta de dados nunca é apagada

---

## 📁 Estrutura de Arquivos no Cliente

```
~/Documentos/FinancePro/  (ou Documents\FinancePro no Windows)
├── .license                  ← Arquivo de licença (oculto)
├── clientes.json
├── emprestimos.json
├── usuarios.json
├── lembretes.json
├── smtp_config.json
└── backups/
    └── (backups manuais)
```

---

## 🧪 Testar Proteção

### Teste 1: Copiar para Outro PC
```bash
# Gere executável
./build_linux.sh

# Copie para outro computador
# Execute
./FinancePro

# Resultado esperado:
# ❌ Erro: "Esta licença está registrada para outro computador"
```

### Teste 2: Expiração
```python
# Modificar data de expiração no arquivo .license
# Executar app
# Resultado: "Licença expirada"
```

### Teste 3: Atualização
```bash
# Modifique algo no código
# Gere novo executável
./build_linux.sh

# Substitua o executável antigo
# Execute
# Resultado: Funciona normalmente, dados preservados
```

---

## 🔧 Configurações Técnicas

### Duração das Licenças

```python
# Em utils/license.py

# Trial (primeira execução):
timedelta(days=30)  # 30 dias

# Licença completa (após ativação):
timedelta(days=365*10)  # 10 anos
```

### Personalizar Duração

Modifique em `utils/license.py`:

```python
def _create_trial_license(self):
    expiry = datetime.now() + timedelta(days=90)  # 90 dias trial
```

---

## 🎯 Fluxo Completo

### Para Você (Desenvolvedor)

1. ✅ Desenvolve/modifica código
2. ✅ Gera executável (`./build_linux.sh`)
3. ✅ Envia executável para cliente
4. ⏳ Cliente usa por 30 dias (trial)
5. 📧 Cliente envia Machine ID
6. 🔑 Você gera chave de licença
7. 📤 Envia chave para cliente
8. ✅ Cliente ativa licença completa

### Para Cliente

1. 📥 Recebe executável
2. ▶️ Executa primeira vez
3. 📁 Pasta criada em Documentos
4. 🔓 Login: `admin` / `admin123`
5. ⏱️ Usa por 30 dias (trial)
6. 📧 Envia Machine ID para você
7. 🔑 Recebe e ativa chave
8. ✅ Licença completa ativada
9. 🔄 Recebe atualizações quando disponíveis

---

## 📝 Notas Importantes

### Vantagens

✅ Cliente não precisa instalar Python
✅ Executável único e simples
✅ Dados salvos em local seguro
✅ Atualizações fáceis (só trocar executável)
✅ Proteção básica contra pirataria
✅ Licença vinculada ao hardware

### Limitações

⚠️ Proteção básica (não é inquebbrável)
⚠️ Se cliente formatar PC, perde licença
⚠️ Alteração de hardware pode invalidar licença
⚠️ Necessário processo manual para ativação

### Melhorias Futuras

💡 Servidor de licenças online
💡 Renovação automática
💡 Portal do cliente
💡 Telemetria e analytics
💡 Auto-update automático

---

## 🆘 Suporte

### Cliente Perdeu Licença

Se cliente formatou PC ou trocou hardware:
1. Solicite novo Machine ID
2. Gere nova chave
3. Cliente ativa novamente

### Cliente Não Consegue Ativar

1. Verifique se Machine ID está correto
2. Confirme que chave foi gerada para aquele ID
3. Verifique arquivo `.license` não foi corrompido
4. Em último caso, delete `.license` e comece trial novamente

---

**Desenvolvido por:** GustavoDanielL  
**Versão:** 1.0.0  
**Licença:** Proprietária
