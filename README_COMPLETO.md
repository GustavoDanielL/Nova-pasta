# 📊 FinancePro - Sistema de Gestão Financeira

Sistema profissional para controle de clientes, empréstimos e cobranças, com criptografia de dados sensíveis e proteção por senha mestra.

## 🔒 Segurança e Privacidade

- ✅ **Criptografia AES**: Dados sensíveis (CPF/CNPJ, email, telefone) criptografados
- ✅ **Senha Mestra**: Proteção por senha no primeiro uso
- ✅ **Banco SQLite**: Dados locais, sem servidor externo
- ✅ **Backups Automáticos**: Sistema de backup integrado
- ✅ **Thread-Safe**: Operações protegidas contra concorrência
- ✅ **Logs Rotacionados**: Sistema de logs profissional com rotação automática

## 📥 Instalação e Primeiro Uso

### Windows

#### Opção 1: Executável (Recomendado)
1. **Baixe** o arquivo `FinancePro.exe`
2. **Extraia** se estiver em ZIP
3. **Execute** clicando duas vezes
4. **Aguarde** a tela de senha mestra aparecer

#### Opção 2: Python (Desenvolvimento)
```bash
# 1. Clone ou baixe o repositório
git clone https://github.com/seu-usuario/financepro.git
cd financepro

# 2. Crie ambiente virtual
python -m venv .venv
.venv\Scripts\activate

# 3. Instale dependências
pip install -r requirements.txt

# 4. Execute
python main.py
```

### Linux

#### Opção 1: Executável
```bash
# 1. Baixe e dê permissão
chmod +x FinancePro
./FinancePro
```

#### Opção 2: Python (Desenvolvimento)
```bash
# 1. Clone ou baixe
git clone https://github.com/seu-usuario/financepro.git
cd financepro

# 2. Crie ambiente virtual
python3 -m venv .venv
source .venv/bin/activate

# 3. Instale dependências
pip install -r requirements.txt

# 4. Execute
python main.py
```

## 🔐 Configuração Inicial

### 1. Senha Mestra (Primeira Execução)

Na primeira vez que você executar o FinancePro, aparecerá uma tela para configurar a **Senha Mestra**:

**⚠️ IMPORTANTE:**
- Esta senha protege todos os seus dados sensíveis
- **NÃO HÁ RECUPERAÇÃO** se você esquecer
- Escolha uma senha forte (mínimo 6 caracteres)
- **Anote em local seguro!**

**Opções:**
- **Configurar senha**: Seus dados serão criptografados (recomendado)
- **Continuar sem senha**: Dados NÃO serão criptografados (apenas para testes)

### 2. Login Padrão

Após configurar a senha mestra, use as credenciais padrão:

```
Usuário: admin
Senha: admin123
```

**⚠️ RECOMENDADO**: Altere a senha padrão imediatamente em **Configurações → Usuários**

### 3. Configuração de E-mail (Opcional)

Para enviar cobranças por e-mail, configure o SMTP:

#### Passo 1: Criar arquivo `.env`
Copie o arquivo `.env.example` para `.env` na raiz do projeto:
```bash
cp .env.example .env
```

#### Passo 2: Configurar Gmail (Recomendado)
1. Ative **Verificação em 2 etapas** na sua conta Google
2. Acesse: https://myaccount.google.com/apppasswords
3. Gere uma "Senha de app" para "Outro"
4. Edite o arquivo `.env`:

```env
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=seu_email@gmail.com
SMTP_PASSWORD=sua_senha_de_app_16_caracteres
SMTP_FROM_NAME=Sua Empresa
SMTP_FROM_EMAIL=seu_email@gmail.com
```

**⚠️ IMPORTANTE**: Use a **Senha de App** gerada, NÃO sua senha normal do Gmail!

#### Passo 3: Alternativas

**Outlook/Hotmail:**
```env
SMTP_HOST=smtp-mail.outlook.com
SMTP_PORT=587
SMTP_USERNAME=seu_email@outlook.com
SMTP_PASSWORD=sua_senha_normal
```

**Outros provedores:** Consulte a documentação do seu provedor de e-mail.

## 📖 Guia de Uso

### 1. Dashboard
- **Visão geral** do negócio
- Total emprestado, recebido e saldo
- Gráficos de desempenho
- Alertas de atrasos

### 2. Cadastrar Cliente

**Passo a passo:**
1. Clique em **"Clientes"** no menu lateral
2. Clique no botão **"+ Novo Cliente"**
3. Preencha os campos:
   - **Nome Completo** (obrigatório)
   - **CPF/CNPJ** (formata automaticamente enquanto digita)
   - **Telefone** (formata automaticamente)
   - **E-mail** (obrigatório)
   - **Endereço** (opcional)
4. Clique em **"Salvar"**

**Dica**: Os campos CPF/CNPJ e Telefone são formatados automaticamente enquanto você digita!

### 3. Criar Empréstimo

**Passo a passo:**
1. Clique em **"Empréstimos"** no menu lateral
2. Clique no botão **"+ Novo Empréstimo"**
3. Selecione o **Cliente** (use o dropdown)
4. Preencha:
   - **Valor Emprestado**
   - **Taxa de Juros (%)** por mês
   - **Data de Empréstimo** (clique no calendário)
   - **Data de Vencimento**
   - **Método de Cálculo**: Juros Simples ou Compostos
   - **Observações** (opcional)
5. Clique em **"Calcular"** para ver o total
6. Clique em **"Salvar Empréstimo"**

### 4. Registrar Pagamento

**Passo a passo:**
1. Na aba **"Empréstimos"**, localize o empréstimo
2. Clique no botão **"💰 Pagar"**
3. Digite o **valor do pagamento**
4. Selecione a **data** (padrão: hoje)
5. Escolha o **método** (Dinheiro, PIX, Transferência, etc.)
6. Clique em **"Registrar Pagamento"**

**Automático**: O saldo devedor é atualizado automaticamente!

### 5. Ver Devedores

**Passo a passo:**
1. Clique em **"Empréstimos"** no menu lateral
2. Use o filtro **"Status"** e selecione **"Ativos"**
3. Os empréstimos em atraso aparecem com tag **"⚠️ ATRASADO"** em vermelho

**Dica**: Clique em **"👁️ Ver"** para ver todos os detalhes e histórico de pagamentos!

### 6. Enviar Cobrança

**Via WhatsApp (direto):**
1. Na aba **"Clientes"**, clique no ícone **"📱"** ao lado do cliente
2. Sua cobrança será formatada automaticamente
3. WhatsApp abrirá com a mensagem pronta
4. Clique em **"Enviar"**

**Via E-mail:**
1. Na aba **"Clientes"**, clique no botão **"📧 Enviar Cobrança"**
2. Revise a mensagem
3. Clique em **"Enviar"**

**Pré-requisito email**: Configure o SMTP no arquivo `.env` (veja seção "Configuração de E-mail")

### 7. Notificações Automáticas

O sistema verifica automaticamente **a cada hora** se há empréstimos atrasados e:
- Adiciona **lembretes** na aba de Notificações
- Envia **e-mails automáticos** (se SMTP configurado)

**Ver notificações:**
1. Clique em **"Notificações"** no menu lateral
2. Veja todos os alertas de atraso

### 8. Editar/Excluir

**Editar Cliente:**
1. Na aba **"Clientes"**, clique no botão **"✏️ Editar"**
2. Altere os dados
3. Clique em **"Salvar"**

**Excluir Cliente:**
1. Clique no botão **"🗑️ Excluir"**
2. Confirme a exclusão

**⚠️ ATENÇÃO**: Excluir um cliente **NÃO exclui** os empréstimos dele!

**Editar Empréstimo:**
- Não é possível editar diretamente
- Registre pagamentos para atualizar o saldo

**Quitar Empréstimo:**
1. Registre um pagamento com o **valor total do saldo devedor**
2. O empréstimo será automaticamente marcado como **"QUITADO"**

### 9. Backup dos Dados

**Backup Automático:**
- O sistema salva automaticamente a cada alteração
- Backups ficam em: `~/Documentos/FinancePro/backups/`

**Backup Manual:**
1. Clique em **"Configurações"** no menu lateral
2. Clique em **"Fazer Backup Agora"**
3. Arquivo será salvo em: `~/Documentos/FinancePro/backups/backup_AAAAMMDD_HHMMSS.db`

**Restaurar Backup:**
1. Feche o FinancePro
2. Localize o arquivo `financepro.db` em `~/Documentos/FinancePro/`
3. Substitua por um arquivo de backup (renomeie para `financepro.db`)
4. Abra o FinancePro novamente

### 10. Trocar Login e Senha

**Passo a passo:**
1. Clique em **"Configurações"** no menu lateral
2. Clique em **"Gerenciar Usuários"**
3. Clique em **"+ Adicionar Usuário"**
4. Digite novo **usuário** e **senha**
5. Clique em **"Salvar"**

**Trocar senha do admin:**
1. Exclua o usuário **"admin"**
2. Crie novo usuário com as credenciais desejadas

## 🔍 Problemas Comuns

### "Senha mestra incorreta"
- **Causa**: Você digitou a senha errada
- **Solução**: Digite a senha correta que você configurou na primeira vez
- **Esqueceu?**: Sem recuperação possível. Você precisará reinstalar e perder os dados criptografados.

### "Erro ao enviar e-mail"
- **Causa 1**: Arquivo `.env` não configurado ou incompleto
  - **Solução**: Siga a seção "Configuração de E-mail"
- **Causa 2**: Senha de app inválida (Gmail)
  - **Solução**: Gere nova senha de app em https://myaccount.google.com/apppasswords
- **Causa 3**: Verificação em 2 etapas não ativada (Gmail)
  - **Solução**: Ative a verificação em 2 etapas primeiro

### "Cliente não aparece após cadastrar"
- **Causa**: Bug já corrigido na versão mais recente
- **Solução**: Atualize para a última versão

### "Aplicativo fecha ao abrir janela"
- **Causa**: Problema de compatibilidade com Linux
- **Solução**: Bug já corrigido, atualize para última versão

### "Dados não aparecem"
- **Causa**: Primeira execução ou migração de JSON para SQLite
- **Solução**: Se você tinha dados antigos em JSON, eles foram migrados automaticamente para `financepro.db`

## 📂 Estrutura de Arquivos

```
~/Documentos/FinancePro/          # Diretório de dados (Windows e Linux)
├── financepro.db                 # Banco de dados SQLite (PRINCIPAL)
├── .salt                          # Salt para criptografia (NÃO DELETAR!)
├── backups/                       # Backups automáticos
│   ├── backup_20251210_120000.db
│   └── ...
└── logs/                          # Logs da aplicação
    ├── financepro_20251210.log
    └── ...

~/.config/FinancePro/              # Configurações (Linux) ou AppData\Local (Windows)
└── .master_password               # Hash da senha mestra (NÃO DELETAR!)
```

## ⚠️ Avisos Importantes

1. **Senha Mestra**: Não há recuperação. Anote em local seguro!
2. **Backup**: Faça backups regulares (automáticos em `backups/`)
3. **Arquivo .env**: Nunca compartilhe ou faça commit no Git
4. **Dados Sensíveis**: Todos criptografados com sua senha mestra
5. **SQLite**: Cliente NÃO precisa instalar nada, o `.db` já é o banco

## 🚀 Distribuição

### Gerar Executável

**Windows:**
```bash
# Instalar PyInstaller
pip install pyinstaller

# Gerar executável
pyinstaller --onefile --windowed --name=FinancePro main.py
```

**Linux:**
```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name=FinancePro main.py
```

O executável estará em `dist/FinancePro.exe` (Windows) ou `dist/FinancePro` (Linux).

### Distribuir para Clientes

**O que enviar:**
1. ✅ Executável (`FinancePro.exe` ou `FinancePro`)
2. ✅ Arquivo `.env.example` (renomear para `.env` e configurar)
3. ✅ Este README.md

**O que NÃO enviar:**
- ❌ Pasta `.venv/`
- ❌ Pasta `.git/`
- ❌ Arquivos `.db` (dados)
- ❌ Arquivo `.env` configurado (tem suas credenciais!)
- ❌ Pasta `__pycache__/`
- ❌ Logs e backups

## 🛠️ Desenvolvimento

### Tecnologias
- **Python 3.14+**
- **CustomTkinter 5.2.2**: Interface gráfica moderna
- **SQLite3**: Banco de dados local
- **Cryptography**: Criptografia AES para dados sensíveis
- **python-dotenv**: Gerenciamento de variáveis de ambiente

### Estrutura do Código
```
financepro/
├── main.py                       # Entry point
├── models/
│   ├── database_sqlite.py        # Banco de dados com criptografia
│   ├── cliente.py                # Modelo Cliente
│   ├── emprestimo.py             # Modelo Empréstimo
│   └── usuario.py                # Modelo Usuário
├── views/
│   ├── login_view.py             # Tela de login
│   ├── main_view.py              # Tela principal
│   ├── clientes_view.py          # Gestão de clientes
│   ├── emprestimos_view.py       # Gestão de empréstimos
│   └── notificacoes_view.py      # Notificações
└── utils/
    ├── logger_config.py          # Sistema de logging
    ├── master_password.py        # Gerenciador de senha mestra
    ├── json_migrator.py          # Migração JSON → SQLite
    ├── notifier.py               # Notificações automáticas
    └── validators.py             # Validações
```

## 📄 Licença

Este projeto é proprietário. Uso comercial requer licença.

## 📞 Suporte

Para dúvidas ou problemas:
- **GitHub Issues**: [link para issues]
- **E-mail**: seu_email@exemplo.com

---

**Desenvolvido com ❤️ para gestão financeira profissional**
