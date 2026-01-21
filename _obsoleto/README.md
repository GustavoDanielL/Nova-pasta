# 📁 Pasta Obsoleto

Esta pasta contém arquivos antigos que foram substituídos ou não são mais utilizados no projeto.

## 📋 Conteúdo

### docs_antigos/
Documentos de desenvolvimento antigos que foram consolidados:
- `COMO_TESTAR.md` - Instruções antigas de teste
- `DIAGNOSTICO.md` - Diagnósticos antigos
- `ESTRUTURA.md` - Estrutura antiga do projeto
- `GUIA_BUILD.md` - Guia antigo de build
- `LICENCAS_SIMPLES.md` - Sistema de licenças antigo
- `MELHORIAS_IMPLEMENTADAS.md` - Lista antiga de melhorias
- `MUDANCAS_TECNICAS.md` - Mudanças técnicas antigas
- `ORGANIZACAO_CONCLUIDA.txt` - Notas antigas
- `SISTEMA_LICENCA.md` - Documentação antiga de licenças

**Substituído por:**
- `README_COMPLETO.md` - Documentação completa e atualizada
- `docs/IMPLEMENTACOES.md` - Resumo técnico das implementações
- `docs/PREPARAR_DISTRIBUICAO.md` - Guia de distribuição

### scripts_antigos/
Scripts de desenvolvimento e debug antigos:
- `run_safe.py` / `safe_run.sh` - Scripts de execução segura
- `test_login.py` / `test_minimal.py` - Testes mínimos
- `financepro_debug_*.log` - Logs antigos de debug
- `scripts/` - Pasta com scripts diversos de build e debug

**Substituído por:**
- `build_linux.sh` / `build_windows.bat` - Scripts de build atualizados
- Sistema de logging profissional em `utils/logger_config.py`

### testes_antigos/
Pasta `tests/` com testes antigos que não seguem padrão atual:
- Testes de UI individuais
- Testes de validação
- Testes de dados

**Substituído por:**
- Testes integrados no sistema
- Validações nos módulos `utils/validators.py`

### Outros:
- `database.py` - Sistema antigo de banco JSON (sem criptografia)

**Substituído por:**
- `models/database_sqlite.py` - SQLite com criptografia AES

## ⚠️ Importante

Estes arquivos são mantidos apenas para referência histórica.

**NÃO use nada desta pasta no projeto atual!**

Se você precisa de alguma funcionalidade antiga:
1. Consulte a documentação atual em `README_COMPLETO.md`
2. Verifique `docs/IMPLEMENTACOES.md` para ver o que foi implementado
3. Os arquivos aqui podem estar desatualizados ou incompatíveis

## 🗑️ Limpeza

Você pode deletar esta pasta inteira com segurança se:
- ✅ Já fez backup do projeto
- ✅ Tem tudo versionado no Git
- ✅ Não precisa consultar implementações antigas

Para deletar:
```bash
rm -rf _obsoleto/
```

---
**Data de criação:** 12 de dezembro de 2025
**Motivo:** Reorganização após implementação de melhorias de segurança e qualidade
