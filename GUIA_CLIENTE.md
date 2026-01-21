# FinancePro - Guia do Cliente

## Como Instalar e Usar

### Opção 1: Instalação Recomendada (com Atalho)

1. **Abra a pasta** que você recebeu com os arquivos do FinancePro
   
2. **Clique com botão direito** em `Instalar.bat`

3. **Selecione "Executar como administrador"**
   - Pode aparecer uma janela de confirmação do Windows → Clique em "Sim"

4. **Aguarde a instalação concluir**
   - Uma janela preta mostrará o progresso
   - Quando terminar, pressione uma tecla

5. **Verifique a Desktop**
   - Um atalho "FinancePro" será criado automaticamente

6. **Abra o FinancePro clicando no atalho**
   - Na primeira execução, pode levar um pouco para iniciar

### Opção 2: Execução Direta (sem instalação)

Simplesmente **execute `FinancePro.exe`** diretamente sem rodar o instalador.

---

## ⚠️ Se Tiver Problemas

### "O antivírus bloqueou o arquivo"
- Arquivos .exe gerados com PyInstaller às vezes disparam falsos positivos
- **Solução:** Adicione `FinancePro.exe` à lista de exceções do seu antivírus
  
### "FinancePro não abre"
1. Tente executar como Administrador:
   - Clique com botão direito em `FinancePro.exe` → "Executar como administrador"

2. Se ainda não funcionar:
   - Certifique-se de que você tem pelo menos 500 MB livres
   - Tente desabilitar o antivírus temporariamente durante a instalação

### "Erro de permissão ao instalar"
- O script precisa de direitos de administrador
- Execute `Instalar.bat` como administrador (clique direito → "Executar como administrador")

### "Erro de arquivo não encontrado"
- Certifique-se que todos os arquivos estão na mesma pasta:
  - `FinancePro.exe`
  - `Instalar.bat`
  - `LEIA-ME.txt`

---

## 📋 Requisitos

- **Windows 7** ou superior
- **Conectividade com internet** (opcional, apenas para primeira execução)
- **500 MB** de espaço em disco

Nenhuma instalação adicional é necessária!

---

## 🔄 Desinstalação

1. Abra **Painel de Controle** → **Programas** → **Desinstalar um programa**

2. Localize **"FinancePro"** na lista

3. Clique em **Desinstalar**

4. (Opcional) Delete a pasta `C:\Program Files\FinancePro` se ela existir

---

## 📝 Notas

- Os dados do FinancePro são salvos em: `%USERPROFILE%\Documentos\FinancePro`
- A aplicação cria configurações em: `%USERPROFILE%\.config\FinancePro`
- Para resetar tudo, delete essas pastas e reinstale

---

**Versão:** 2.0.0  
**Data:** {datetime.now().strftime('%d/%m/%Y')}  

Se continuar com problemas, envie:
- Uma captura de tela da mensagem de erro
- Uma descrição do que estava tentando fazer
- Seu sistema operacional e versão do Windows
