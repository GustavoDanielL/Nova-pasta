# 🔐 Sistema de Licenças - FinancePro

## Como Funciona (SIMPLES)

### Para Você (Desenvolvedor)

1. **Cadastre chaves** no arquivo `license_manager.py`:
```python
CHAVES_VALIDAS = {
    "FINANCEPRO-2025-PREMIUM": {"usado": False, "maquina_id": None},
    "TRIAL-30DIAS-FREE": {"usado": False, "maquina_id": None},
    "CLIENTE-JOAO-2025": {"usado": False, "maquina_id": None},
}
```

2. **Gere o executável** e envie para o cliente:
```bash
./build_linux.sh    # Linux
build_windows.bat   # Windows
```

3. **Pronto!** O cliente só consegue usar se tiver uma chave válida

---

### Para o Cliente

1. **Recebe o executável** de você
2. **Abre o programa** - aparece tela pedindo chave
3. **Digite a chave** que você passou (ex: `FINANCEPRO-2025-PREMIUM`)
4. **Pronto!** Programa ativado **PARA SEMPRE** naquela máquina
5. Nunca mais pede chave naquela máquina

---

## 🛡️ Proteção

- ✅ Cliente não consegue usar sem chave válida
- ✅ Chave fica embutida no executável (não tem como ver)
- ✅ **UMA CHAVE = UMA MÁQUINA** (chave é "queimada" ao ativar)
- ✅ Se cliente passar a chave pra alguém, não funciona (já foi usada)
- ✅ Após ativar, fica permanente (não expira)
- ✅ Se tentar copiar executável para outro PC, chave não funciona mais

---

## 🔄 Atualizações do App

**Pergunta:** Como atualizo o app para os clientes?

**Resposta:** 
1. Faça suas modificações no código
2. Gere um novo executável
3. Envie o novo executável para o cliente
4. Cliente roda o novo executável - **não pede chave de novo!**
5. Licença já está salva na máquina dele

**A licença é permanente e sobrevive a atualizações!**

---

## 📋 Login e Senha Padrão

**Login:** `admin`  
**Senha:** `admin123`

Sempre vem zerado (cliente precisa digitar).

---

## 📝 Gerenciar Chaves
### Adicionar Nova Chave

Edite `license_manager.py`:
```python
CHAVES_VALIDAS = {
    "FINANCEPRO-2025-PREMIUM": {"usado": False, "maquina_id": None},
    "NOVA-CHAVE-AQUI": {"usado": False, "maquina_id": None},  # ← Adicione aqui
}
```

Gere um novo executável e envie.

### ⚠️ Importante sobre Chaves Usadas

Quando uma chave é ativada, ela fica assim:
```python
"CLIENTE-JOAO": {"usado": True, "maquina_id": "a1b2c3d4..."}
```

**Não consegue usar em outra máquina!** Para dar nova licença ao mesmo cliente, gere uma nova chave.
Gere um novo executável e envie.
