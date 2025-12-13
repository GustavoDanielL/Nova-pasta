# 🔧 Guia de Diagnóstico - FinancePro

## ⚠️ Problema: Sistema reiniciando o computador

**IMPORTANTE**: Um aplicativo Python **NUNCA** pode reiniciar o computador sem privilégios de root. O que pode estar acontecendo:

### Possíveis Causas:

1. **Crash do driver gráfico** (Nobara/Wayland/X11)
2. **Problema de memória/GPU** ao renderizar interface
3. **Conflito com compositor gráfico**
4. **Kernel panic não relacionado ao app**

### Como Diagnosticar:

#### 1. Usar o Modo Seguro (Recomendado)
```bash
python run_safe.py
```
Isso criará um arquivo de log detalhado (`financepro_debug_*.log`) que mostrará exatamente onde o problema ocorre.

#### 2. Verificar Logs do Sistema
```bash
# Ver logs do kernel
sudo journalctl -b -p err

# Ver logs do Xorg/Wayland
journalctl --user -u graphical-session.target
```

#### 3. Testar sem Customtkinter
Se o problema for o CustomTkinter causando crash do driver gráfico:
```bash
# Teste básico do tkinter
python -c "import tkinter; root = tkinter.Tk(); root.mainloop()"
```

#### 4. Modo Conservador (Sem Notifier)
O arquivo `main.py` já foi atualizado para **DESATIVAR** o notifier por padrão. Teste novamente.

### Proteções Adicionadas:

✅ **Try/except em todas as operações críticas**
✅ **Handler de fechamento seguro** 
✅ **Notifier desativado por padrão**
✅ **Salvamento automático de dados**
✅ **Logs detalhados de erros**

### Se o problema persistir:

1. **Execute com o modo seguro** (`python run_safe.py`)
2. **Verifique o arquivo de log** gerado
3. **Verifique logs do sistema** para ver se é crash de driver
4. **Teste no Windows** para confirmar que é específico do Linux

### Compatibilidade:

- ✅ Windows 10/11
- ✅ Linux (Ubuntu, Debian, Fedora)
- ⚠️ Nobara (possível conflito com driver gráfico - use run_safe.py)

### Contato:

Se após usar o `run_safe.py` o problema continuar, envie o arquivo de log gerado para análise.
