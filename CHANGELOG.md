# 📋 Changelog - FinancePro

## [2.0.0] - Dezembro 2025 - ATUALIZAÇÃO MAJOR DE SEGURANÇA

### 🔐 Segurança e LGPD
- ✅ **Migração completa para SQLite com criptografia AES-256**
  - Todos os dados sensíveis (CPF, email, telefone, valores) agora são criptografados
  - Banco de dados único: `financepro.db` substituindo múltiplos JSONs
  - PBKDF2 com 100.000 iterações para derivação de chave
  - Salt único por instalação (arquivo `.salt`)

- ✅ **Sistema de Senha Mestra**
  - Obrigatória no primeiro uso
  - Protege todo o banco de dados
  - Hash PBKDF2-HMAC-SHA256 irreversível
  - ⚠️ Perda da senha = perda dos dados (segurança máxima)

- ✅ **Conformidade LGPD (Lei Geral de Proteção de Dados)**
  - Criptografia de dados pessoais em repouso (Art. 46)
  - Controle de acesso com autenticação
  - Logs de auditoria sem dados sensíveis
  - Backups automáticos criptografados

### 🚀 Melhorias de Funcionalidade

- ✅ **Exportações Corrigidas**
  - Excel: Relatório Completo e Apenas Empréstimos funcionando
  - Barra de progresso durante exportação
  - Threading para não travar interface
  - Formatação profissional (cores, valores R$, datas BR)

- ✅ **Indicadores Visuais de Status**
  - ✅ QUITADO (verde) - empréstimo pago
  - ⚠️ ATRASADO (X dias) - com contagem de dias
  - 🔄 EM DIA - dentro do prazo

- ✅ **Validações Aprimoradas**
  - Não permite pagamento em empréstimo quitado
  - Rejeita valores negativos/zero
  - Aviso ao editar empréstimo quitado

- ✅ **Interface Melhorada**
  - Popups sempre no topo (não ficam atrás)
  - Formatação de data inteligente (DD/MM/YYYY)
  - Sem formatação automática durante digitação
  - Modal windows com focus correto

### 🔧 Melhorias Técnicas

- ✅ **Banco de Dados SQLite**
  - Thread-safe com `threading.Lock`
  - Transações ACID completas
  - Índices para performance
  - Schema otimizado com relacionamentos (FOREIGN KEY)
  - Métodos especializados: `get_overdue_emprestimos()`, `get_emprestimos_by_cliente()`

- ✅ **Migração Automática**
  - Detecção de dados JSON antigos
  - Migração transparente na primeira execução
  - Backup dos JSONs originais
  - Preservação completa de dados

- ✅ **Logging Profissional**
  - Níveis: DEBUG, INFO, WARNING, ERROR, CRITICAL
  - Rotação automática (10MB, 5 backups)
  - Logs em `~/Documentos/FinancePro/logs/`
  - Formato estruturado com timestamps

### 🗑️ Arquivos Removidos

- ❌ `data/clientes.json` - substituído por SQLite
- ❌ `data/emprestimos.json` - substituído por SQLite
- ❌ `data/usuarios.json` - substituído por SQLite
- ❌ `data/lembretes.json` - substituído por SQLite
- ❌ `data/smtp_config.json` - substituído por SQLite
- ❌ `models/database.py` - substituído por `database_sqlite.py`

### 📚 Documentação

- ✅ **README.md** - Atualizado com seção de segurança LGPD
- ✅ **IMPLEMENTACOES.md** - Documentação completa das mudanças
- ✅ **CHANGELOG.md** - Este arquivo (novo)
- ✅ **.gitignore** - Atualizado para proteger arquivos sensíveis

### ⚠️ BREAKING CHANGES

**Atenção:** Esta é uma atualização MAJOR que muda a estrutura de dados.

- **Migração automática** na primeira execução
- **Senha mestra obrigatória** para novos bancos
- **JSONs antigos** são migrados e mantidos em `backups/`
- **Não há como voltar** à versão 1.x após migração (por segurança)

### 🔄 Como Atualizar

1. **Backup**: Faça backup da pasta `data/` antes de atualizar
2. **Execute**: `python main.py`
3. **Defina senha**: Crie senha mestra forte (mínimo 8 caracteres)
4. **Migração**: Sistema detecta JSONs e migra automaticamente
5. **Pronto**: Use normalmente com segurança aprimorada

### 📊 Estatísticas

- **Arquivos modificados**: 15+
- **Arquivos novos**: 5
- **Arquivos removidos**: 6
- **Linhas de código adicionadas**: ~2000
- **Nível de segurança**: ⬆️ Básico → Empresarial
- **Conformidade**: ✅ LGPD

---

## [1.0.0] - Novembro 2025 - Release Inicial

### ✨ Funcionalidades Iniciais

- 👥 Gestão de Clientes
- 💰 Gestão de Empréstimos
- 📊 Dashboard com gráficos
- 🔔 Notificações automáticas
- 📧 Configuração SMTP
- 📥 Exportação para Excel
- 🔐 Sistema de login
- 🎨 Interface CustomTkinter

### ⚠️ Limitações da v1.0

- ❌ Dados em JSON (texto plano)
- ❌ Sem criptografia
- ❌ Não conforme LGPD
- ❌ Múltiplos arquivos JSON
- ❌ Sem proteção de senha

---

**Desenvolvido com ❤️ para segurança e conformidade**
