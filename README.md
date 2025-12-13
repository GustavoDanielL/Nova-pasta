# 💰 FinancePro - Sistema de Gestão de Empréstimos

Um sistema moderno e profissional para gerenciar empréstimos e clientes, com **segurança de nível empresarial**, recursos avançados de análise, notificações automáticas e exportação de dados.

## 🔐 Segurança e Privacidade (LGPD)

### Criptografia AES-256
- **Banco de Dados Criptografado**: Todos os dados são armazenados em SQLite com criptografia AES-256
- **Senha Mestra**: Acesso protegido por senha mestra definida no primeiro uso
- **Salt Único**: Cada instalação possui salt criptográfico único
- **Dados Sensíveis Protegidos**: CPF, emails, telefones e valores são criptografados

### Conformidade LGPD
- ✅ Criptografia de dados pessoais em repouso
- ✅ Controle de acesso com autenticação
- ✅ Backups automáticos criptografados
- ✅ Logs de auditoria de acesso
- ✅ Destruição segura de dados ao remover

## 🎯 Características Principais

### 📊 Dashboard Interativo
- **Gráficos em Tempo Real**: Visualize seus dados através de 3 tipos de gráficos interativos:
  - **Pizza Status**: Distribuição de empréstimos por status (Ativo/Quitado)
  - **Pizza Ativo/Inativo**: Comparação entre empréstimos ativos e inativos
  - **Barras de Valores**: Distribuição de valores dos empréstimos
- **Atualizações Automáticas**: Os gráficos se atualizam automaticamente quando dados mudam
- **Design Responsivo**: Interface que se adapta ao tamanho da tela

### 👥 Gestão de Clientes
- **Cadastro Completo**: Nome, CPF/CNPJ, Email, Telefone, Endereço, Chave PIX
- **Busca Rápida**: Encontre clientes rapidamente
- **Edição e Exclusão**: Gerencie informações de clientes facilmente
- **Histórico de Transações**: Veja todos os empréstimos de cada cliente

### 💳 Gestão de Empréstimos
- **Cálculo Automático**: Juros compostos calculados automaticamente
- **Rastreamento de Pagamentos**: Registre pagamentos parciais ou totais
- **Status Visual**: Cores diferentes para:
  - 🟢 Verde: Empréstimo Ativo
  - 🔴 Vermelho: Empréstimo Atrasado
  - ⚪ Cinza: Empréstimo Quitado
- **Validações de Segurança**:
  - ❌ Não permite registrar pagamento em empréstimo já quitado
  - ❌ Rejeita valores negativos ou zerados
  - ⚠️ Aviso informativo ao abrir empréstimo quitado

### 🔔 Notificações e Alertas
- **Detecção Automática de Atrasos**: Sistema identifica empréstimos em atraso (baseado em data mensal)
- **Thread de Fundo**: Notifier roda continuamente sem bloquear a aplicação
- **Integração com Sistema**: Cria lembretes automáticos para empréstimos atrasados
- **Opções de Notificação**:
  - 📧 Email via SMTP (configurável)
  - 📬 Email via cliente padrão do sistema

### ⚙️ Configurações SMTP
Configure notificações por email com seus próprios servidores:

#### Como Configurar:
1. **Acesse Configurações** → Menu ⚙️
2. **Preencha os Campos SMTP**:
   - **Servidor SMTP**: ex: `smtp.gmail.com` ou `smtp.office365.com`
   - **Porta**: geralmente `587` (TLS) ou `465` (SSL)
   - **Email Remetente**: seu email corporativo
   - **Senha**: senha do email ou [senha de app](https://support.google.com/accounts/answer/185833) (Gmail)
   - **Email Destinatário**: onde receberá as notificações
   - **Usar TLS**: ✓ (recomendado para porta 587)
3. **Teste a Conexão**: Clique em "Testar Conexão"
4. **Salve**: As configurações são armazenadas automaticamente

#### Exemplos de Servidores Populares:
- **Gmail**: `smtp.gmail.com:587` (TLS)
- **Outlook/Office365**: `smtp.office365.com:587` (TLS)
- **Yahoo Mail**: `smtp.mail.yahoo.com:465` (SSL)
- **Empresa/Corporativo**: Entre em contato com seu administrador

### 📥 Exportação de Dados
Exporte todos seus dados em planilhas Excel bem formatadas:

#### Opção 1: Relatório Completo (4 abas)
- **Resumo Executivo**: Estatísticas gerais
  - Total de clientes e empréstimos
  - Valores totais emprestados e recebidos
  - Total de juros
- **Clientes**: Lista completa com dados de contato
- **Empréstimos**: Detalhes de cada empréstimo
  - Valor, taxa, parcelas
  - Saldo devedor e percentual pago
  - Status (Ativo/Quitado)
- **Pagamentos**: Histórico completo de transações

#### Opção 2: Apenas Empréstimos
- Relatório detalhado de empréstimos
- Próximas parcelas a pagar
- Campo de observações editável

#### Formatação Profissional:
- ✅ Cabeçalhos azuis com texto branco
- ✅ Bordas em todas as células
- ✅ Valores formatados em Reais (R$)
- ✅ Datas em formato DD/MM/YYYY
- ✅ Percentuais com símbolo %
- ✅ Cores por status (verde/amarelo/vermelho)
- ✅ Colunas automaticamente ajustadas

### 🔐 Autenticação e Segurança
- **Senha Mestra**: Proteção do banco de dados com criptografia AES-256
- **Login de Usuários**: Autenticação para múltiplos usuários
- **Dados Criptografados**: Todos os dados sensíveis são criptografados
- **Backups Automáticos**: Sistema de backup automático com criptografia

## 🚀 Instalação

### Pré-requisitos
- Python 3.8+
- pip (gerenciador de pacotes Python)

### Passos de Instalação

1. **Clone ou faça download do projeto**
```bash
cd "c:\Users\user\Nova pasta"
```

2. **Instale as dependências**
```bash
pip install -r requirements.txt
```

3. **Execute a aplicação**
```bash
python main.py
```

## 📦 Dependências

```
customtkinter==5.2.1
matplotlib==3.7.0
openpyxl==3.10.0
pycryptodome==3.19.0
```

### Descrição das Dependências:
- **customtkinter**: Interface gráfica moderna e responsiva
- **matplotlib**: Gráficos profissionais e interativos
- **openpyxl**: Criação de planilhas Excel formatadas
- **pycryptodome**: Criptografia AES-256 para proteção de dados

## 📂 Estrutura do Projeto

```
FinancePro/
├── main.py                 # Ponto de entrada da aplicação
├── requirements.txt        # Dependências do projeto
├── README.md              # Este arquivo
│
├── models/
│   ├── database_sqlite.py # Banco SQLite com criptografia AES-256
│   ├── cliente.py         # Modelo de Cliente
│   ├── emprestimo.py      # Modelo de Empréstimo
│   └── usuario.py         # Modelo de Usuário
│
├── views/
│   ├── main_view.py       # Menu principal e navegação
│   ├── login_view.py      # Tela de login
│   ├── dashboard_view.py  # Dashboard com gráficos
│   ├── clientes_view.py   # Gestão de clientes
│   ├── emprestimos_view.py # Gestão de empréstimos
│   ├── notificacoes_view.py # Alertas e notificações
│   ├── exportacao_view.py  # Exportação de dados
│   └── settings_view.py   # Configurações SMTP
│
├── utils/
│   ├── calculos.py        # Cálculos de juros compostos
│   ├── validators.py      # Validações de dados
│   ├── excel_export.py    # Exportação para Excel
│   ├── notifier.py        # Thread de notificações
│   ├── pdf_export.py      # Exportação para TXT
│   └── qr_generator.py    # Geração de QR codes
│
└── data/
    ├── financepro.db      # Banco de dados SQLite criptografado
    ├── .salt              # Salt para criptografia (único por instalação)
    └── backups/           # Backups automáticos criptografados
```

## 💡 Como Usar

### Primeiro Acesso
1. Execute `python main.py`
2. **Defina uma Senha Mestra**: Esta senha protegerá todos os seus dados
   - ⚠️ **IMPORTANTE**: Guarde esta senha em local seguro!
   - Sem a senha, não será possível acessar os dados
3. Crie um usuário administrador
4. Você será redirecionado ao Dashboard

### Fluxo Básico

#### 1. **Cadastrar um Cliente**
- Clique em "👥 Clientes"
- Clique em "➕ Novo Cliente"
- Preencha os dados: Nome, CPF/CNPJ, Email, Telefone, Endereço
- Opcionalmente, adicione uma Chave PIX para recebimentos
- Clique em "✓ Salvar"

#### 2. **Criar um Empréstimo**
- Clique em "💰 Empréstimos"
- Clique em "➕ Novo Empréstimo"
- Selecione o cliente
- Informe:
  - **Valor Emprestado**: Valor inicial sem juros
  - **Taxa de Juros**: Percentual mensal (ex: 2.5%)
  - **Prazo**: Quantidade de meses
- O sistema calcula automaticamente:
  - Valor Total (com juros)
  - Valor da Parcela Mensal
- Clique em "✓ Criar"

#### 3. **Registrar Pagamento**
- Clique em "💰 Empréstimos"
- Clique em "✏️ Editar" no empréstimo desejado
- Na seção "💰 Registrar Pagamento":
  - Escolha "Parcela" para pagamento mensal padrão
  - Ou "Quitar" para pagar o saldo total
  - Opcionalmente, altere a data do pagamento
- Clique em "✓ Registrar Pagamento"
- Sistema confirma e atualiza o saldo

#### 4. **Visualizar Dashboard**
- Clique em "📊 Dashboard"
- Observe os 3 gráficos:
  - Status dos empréstimos (Ativo/Quitado)
  - Proporção entre empréstimos ativos e inativos
  - Distribuição de valores

#### 5. **Verificar Notificações**
- Clique em "🔔 Notificações"
- Visualize alertas de empréstimos atrasados
- Veja lembretes criados automaticamente

#### 6. **Exportar Dados**
- Clique em "📥 Exportar"
- Escolha o tipo de relatório:
  - **Relatório Completo**: 4 abas com todos os dados
  - **Apenas Empréstimos**: Foco em detalhes dos empréstimos
- O arquivo será criado e a pasta será aberta automaticamente
- Você pode abrir no Excel e personalizar conforme necessário

#### 7. **Configurar SMTP**
- Clique em "⚙️ Configurações"
- Preencha os dados SMTP:
  ```
  Servidor SMTP: smtp.gmail.com
  Porta: 587
  Email: seu.email@gmail.com
  Senha: sua.senha.app
  Email Destinatário: notificacoes@seu.dominio.com
  Usar TLS: ✓
  ```
- Clique em "Testar Conexão" para verificar
- Clique em "💾 Salvar Configurações"
- Sistema usará esse servidor para enviar notificações

## 🔧 Validações de Segurança

O sistema implementa várias validações para proteger seus dados:

### Pagamentos
- ✅ Aceita apenas valores positivos
- ✅ Rejeita pagamentos em empréstimos já quitados
- ❌ **Não permite**: Inserir valor zerado ou negativo
- ❌ **Não permite**: Pagar um empréstimo já 100% quitado
- ⚠️ **Avisa**: Ao abrir um empréstimo quitado

### Clientes
- ✅ Validação de formato de CPF/CNPJ
- ✅ Validação de email
- ✅ Validação de telefone
- ❌ **Não permite**: Duplicar cliente com mesmo CPF/CNPJ

### Empréstimos
- ✅ Valor mínimo obrigatório
- ✅ Taxa de juros não-negativa
- ✅ Prazo mínimo de 1 mês
- ✅ Cálculo preciso de juros compostos

## 📊 Cálculos Implementados

### Juros Compostos
A fórmula utilizada é:
```
Valor Total = Valor Inicial × (1 + Taxa)^Meses
```

**Exemplo:**
- Valor: R$ 1.000,00
- Taxa: 2.5% ao mês
- Prazo: 12 meses
- **Resultado**: R$ 1.344,89 (com R$ 344,89 de juros)

### Detecção de Atraso
- Sistema verifica automaticamente empréstimos vencidos
- Usa heurística mensal: compara data vs parcelas pagas
- Cria alertas para clientes atrasados

## 🗄️ Backup de Dados

O sistema faz backup automático dos dados:
- **Localização**: `data/backups/`
- **Formato**: JSON com timestamp
- **Frequência**: A cada operação que modifica dados
- **Retenção**: Todos os backups são mantidos para auditoria

Arquivo de backup exemplo:
```
clientes_20251117170424.json
emprestimos_20251117170424.json
```

## 🎨 Interface

### Design Moderno
- **Tema Escuro**: Interface profissional e confortável para os olhos
- **Cores Intuitivas**:
  - 🟢 Verde: Ativo/Sucesso
  - 🔴 Vermelho: Atrasado/Erro
  - ⚪ Cinza: Inativo/Concluído
  - 🔵 Azul: Destaque/Ação primária

### Responsividade
- Janelas adaptáveis a diferentes tamanhos
- Scrollbars automáticos quando necessário
- Textos com wrap automático

## 🐛 Troubleshooting

### Erro: "Servidor SMTP não responde"
- Verifique credenciais (email e senha)
- Confirme servidor e porta (Gmail: smtp.gmail.com:587)
- Se usar Gmail, gere [senha de app](https://support.google.com/accounts/answer/185833)
- Desabilite "Menos aplicativos seguro" se necessário

### Erro: "Arquivo Excel não foi criado"
- Verifique se há espaço em disco
- Confirme permissões de escrita na pasta
- Feche arquivo Excel anterior (não pode estar aberto)

### Notificações não chegam
- Verifique se o notifier está em background (ver console)
- Confirme configurações SMTP
- Teste a conexão no painel de configurações

### Aplicação lenta
- Limite número de registros (considere arquivar dados antigos)
- Aumente RAM disponível
- Feche outras aplicações

## 📝 Licença

Desenvolvido com ❤️ para gerenciamento profissional de empréstimos.

## 🤝 Suporte

Para dúvidas ou sugestões:
1. Verifique este README
2. Consulte a documentação inline no código
3. Verifique arquivos de teste (`test_*.py`)

## 🎓 Exemplos de Uso

### Exemplo 1: Criar Empréstimo com Juros
```
Cliente: João Silva
Valor: R$ 5.000,00
Taxa: 2.5% ao mês
Prazo: 12 meses

Resultado:
- Valor Total: R$ 6.724,44
- Parcela Mensal: R$ 560,37
- Juros Totais: R$ 1.724,44
```

### Exemplo 2: Registrar Pagamentos
```
Empréstimo: 12 parcelas de R$ 560,37
Mês 1: Paga R$ 560,37 (parcela normal) ✓
Mês 2: Paga R$ 1.120,74 (2 parcelas) ✓
Mês 3-12: Pagas automaticamente ✓
Resultado: Empréstimo Quitado! 🎉
```

### Exemplo 3: Exportar Relatório
```
Clique: 📥 Exportar → Relatório Completo
Sistema cria: relatorio_financeiro_20251117_212503.xlsx
Abre automaticamente no Excel
Você pode: Editar, formatar, imprimir, enviar
```

---

**Versão**: 1.0.0  
**Última Atualização**: 17/11/2025  
**Status**: ✅ Production Ready
