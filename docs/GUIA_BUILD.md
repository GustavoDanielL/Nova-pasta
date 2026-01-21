# 🚀 Guia - Como Gerar Executável e Instalador

## ⚡ Método Rápido (Recomendado)

### Para Windows:

1. **Clique duas vezes em**: `GERAR_INSTALADOR.bat`
2. **Aguarde o processo completar** (pode levar 2-5 minutos)
3. **Uma pasta será aberta** com os arquivos gerados

Pronto! Agora você tem:
- ✅ Executável portável (pode ser distribuído diretamente)
- ✅ Arquivo compactado ZIP (fácil de enviar por email)

---

## 📋 O Que Será Gerado

### Pasta `releases/`

```
releases/
├── FinancePro_v1.0.0_Portable/        (Pasta portável)
│   ├── FinancePro.exe                 (Executável)
│   ├── EXECUTE_AQUI.bat               (Atalho para iniciar)
│   ├── README.txt                     (Instruções)
│   └── data/                          (Dados do programa)
│
├── FinancePro_v1.0.0_Portable.zip     (Arquivo compactado)
│
├── FinancePro_Setup.exe               (Instalador NSIS - opcional)
│
├── FinancePro.exe                     (Executável simples)
│
└── README.md                          (Documentação)
```

---

## 📦 Distribuição ao Cliente

### Opção 1: Enviar ZIP (Recomendado)
```
✅ Mais compacto
✅ Fácil de enviar por email
✅ Contém tudo que o cliente precisa
✅ Basta extrair e clicar em EXECUTE_AQUI.bat

Arquivo: FinancePro_v1.0.0_Portable.zip
Tamanho: ~50-70 MB
```

### Opção 2: Enviar EXE Direto
```
✅ Executável único
✅ Sem necessidade de extrair
✅ Cliente clica 2x e abre

Arquivo: FinancePro.exe
Tamanho: ~100-150 MB
```

### Opção 3: Usar Instalador NSIS
```
✅ Instalação profissional com assistente
✅ Cria atalhos na área de trabalho
✅ Menu Iniciar automático
✅ Desinstalador incluído

Arquivo: FinancePro_Setup.exe
Tamanho: ~100-150 MB
```

---

## 🔧 Método Manual (Se Preferir)

Se `GERAR_INSTALADOR.bat` não funcionar:

### 1. Abra PowerShell na pasta do projeto:
```powershell
cd "C:\Users\seu_usuario\Nova pasta"
```

### 2. Execute o build Python:
```powershell
python build.py
```

### 3. Verifique a pasta `releases/`

---

## 🐛 Troubleshooting

### ❌ "Python não encontrado"
- Instale Python: https://www.python.org/
- Certifique-se de marcar "Add Python to PATH"
- Reinicie o computador

### ❌ "PyInstaller não instalado"
- O script tenta instalar automaticamente
- Ou instale manualmente:
```powershell
pip install pyinstaller
```

### ❌ "Arquivo muito grande"
- Normal! O executável inclui Python e todas as dependências
- Use a versão ZIP para distribuição

### ❌ "Antivírus bloqueia o EXE"
- Alguns antivírus desconfiam de executáveis empacotados
- Adicione uma exceção ou distribua o ZIP
- Aviso falso - é seguro!

---

## 📝 Para Atualizar o Instalador

Sempre que quiser gerar uma nova versão:

1. Edite o arquivo `build.py` se quiser mudar versão:
   ```python
   self.version = "1.0.0"  # Mude para "1.0.1", etc
   ```

2. Execute novamente `GERAR_INSTALADOR.bat`

3. Pronto! Novos arquivos na pasta `releases/`

---

## 💡 Dicas

### Para Cliente com Problema:
1. Envie o arquivo ZIP
2. Cliente extrai em uma pasta
3. Cliente clica em `EXECUTE_AQUI.bat`
4. FinancePro abre normalmente

### Para Distribuição Profissional:
1. Use o instalador `FinancePro_Setup.exe`
2. Cliente clica e segue o assistente
3. Tudo é instalado automaticamente

### Para Teste:
1. Distribua o `FinancePro.exe` simples
2. Cliente testa
3. Se ok, distribua a versão final

---

## 🎁 O Que o Cliente Recebe

O cliente pode receber um dos seguintes:

| Arquivo | Vantagem | Desvantagem |
|---------|----------|------------|
| **ZIP** | Compacto, fácil enviar | Precisa extrair |
| **EXE** | Pronto pra usar | Arquivo grande |
| **Setup** | Instalação profissional | Mais complexo |

**Recomendação**: Envie o ZIP!

---

## 🔐 Segurança

- ✅ Executável não contém vírus
- ✅ Dados do cliente ficam no computador
- ✅ Sem conexão com servidores externos
- ✅ Tudo funciona offline

---

## 📞 Suporte

Se algo não funcionar:
1. Verifique se Python está instalado
2. Tente executar `build.py` manualmente
3. Verifique pasta `releases/` depois
4. Procure pelo arquivo gerado

---

**Versão**: 1.0.0
**Atualizado**: 17/11/2025
