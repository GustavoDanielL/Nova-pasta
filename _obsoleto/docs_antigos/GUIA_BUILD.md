# 🚀 Como Gerar Executável do FinancePro

## 📋 Visão Geral

O FinancePro pode ser compilado em executável standalone para **Linux** e **Windows** usando PyInstaller.

---

## 🐧 Linux

### Método 1: Script Automático (Recomendado)

```bash
./build_linux.sh
```

O script irá:
- ✅ Instalar dependências necessárias
- ✅ Gerar executável standalone
- ✅ Criar instalador opcional
- ✅ Gerar pacote em `build_output/FinancePro-Linux/`

### Método 2: Manual

```bash
pip install pyinstaller
pyinstaller --clean --noconfirm \
    --name="FinancePro" \
    --onefile \
    --windowed \
    --collect-all="customtkinter" \
    main.py
```

### Instalar no Sistema (Opcional)

```bash
cd build_output/FinancePro-Linux
sudo ./instalar.sh
```

Isso irá:
- Copiar executável para `/opt/financepro/`
- Criar atalho na área de trabalho

---

## 🪟 Windows

### Método 1: Script Automático (Recomendado)

```cmd
build_windows.bat
```

O script irá:
- ✅ Instalar dependências necessárias
- ✅ Gerar executável `.exe`
- ✅ Criar instalador opcional
- ✅ Gerar pacote em `build_output\FinancePro-Windows\`

### Método 2: Manual

```cmd
pip install pyinstaller
pyinstaller --clean --noconfirm ^
    --name="FinancePro" ^
    --onefile ^
    --windowed ^
    --collect-all="customtkinter" ^
    main.py
```

### Instalar no Sistema (Opcional)

Execute `instalar.bat` **como Administrador**:
- Copia para `C:\Program Files\FinancePro\`
- Cria atalho na Área de Trabalho

---

## 📁 Localização dos Dados

O FinancePro cria automaticamente uma pasta para armazenar dados:

### Linux
```
~/Documentos/FinancePro/
├── clientes.json
├── emprestimos.json
├── usuarios.json
└── lembretes.json
```

### Windows
```
C:\Users\SeuUsuario\Documents\FinancePro\
├── clientes.json
├── emprestimos.json
├── usuarios.json
└── lembretes.json
```

---

## 🔧 Requisitos

### Dependências Python
```
customtkinter>=5.2.0
Pillow>=10.0.0
matplotlib>=3.7.0
```

### Sistema
- **Linux**: Python 3.8+, Tkinter
- **Windows**: Python 3.8+

---

## ✅ Testar Executável

### Linux
```bash
./build_output/FinancePro-Linux/FinancePro
```

### Windows
```
build_output\FinancePro-Windows\FinancePro.exe
```

---

## 🐛 Solução de Problemas

### Erro: "No module named 'customtkinter'"

Reinstale as dependências:
```bash
pip install -r requirements.txt
```

### Erro: "Failed to execute script"

Verifique se todas as dependências estão incluídas no build:
```bash
pyinstaller --collect-all customtkinter --collect-all PIL main.py
```

### Executável muito grande

Use `--onefile` para gerar um único arquivo compactado.

### Linux: Erro de permissão

Dê permissão de execução:
```bash
chmod +x FinancePro
```

---

## 📦 Distribuição

### Criar ZIP para Distribuição

**Linux:**
```bash
cd build_output
zip -r FinancePro-Linux.zip FinancePro-Linux/
```

**Windows:**
```cmd
cd build_output
powershell Compress-Archive -Path FinancePro-Windows -DestinationPath FinancePro-Windows.zip
```

---

## 🎯 Recursos do Executável

✅ **Standalone** - Não requer Python instalado
✅ **Cross-platform** - Funciona em Linux e Windows
✅ **Auto-configura** - Cria pasta de dados automaticamente
✅ **Portátil** - Pode rodar de qualquer pasta
✅ **Instalador** - Scripts de instalação inclusos

---

## 📝 Notas

- O primeiro executável pode demorar ~30-60 segundos para abrir
- Execuções subsequentes são mais rápidas
- Dados são salvos em `~/Documentos/FinancePro` (Linux) ou `Documents\FinancePro` (Windows)
- Backups podem ser feitos copiando essa pasta

---

**Desenvolvido por:** GustavoDanielL  
**Versão:** 1.0.0  
**Licença:** MIT
