@echo off
REM ============================================
REM   Referência Rápida - Build FinancePro
REM ============================================

echo.
echo ========================================
echo   REFERENCIA RAPIDA - BUILD
echo ========================================
echo.
echo 1. PREPARACAO
echo    ├─ python --version  (deve ser 3.8+)
echo    ├─ pip install -r requirements.txt
echo    └─ python scripts\validar_pre_build.py
echo.
echo 2. BUILD
echo    ├─ GERAR_INSTALADOR.bat  (automático)
echo    └─ OU: build_windows.bat
echo.
echo 3. RESULTADO
echo    ├─ build_output\releases\FinancePro.exe
echo    ├─ build_output\releases\Instalar.bat
echo    └─ build_output\releases\LEIA-ME.txt
echo.
echo 4. TESTAR LOCALMENTE
echo    ├─ Opção A: build_output\releases\FinancePro.exe
echo    └─ Opção B: cd build_output\releases ^& Instalar.bat
echo.
echo 5. DISTRIBUIR
echo    ├─ Copiar pasta releases\ para ZIP
echo    ├─ OU copiar 3 arquivos para folder
echo    └─ Enviar ao cliente
echo.
echo ========================================
echo   ESTRUTURA DE ARQUIVOS
echo ========================================
echo.
echo scripts\
echo ├─ build.py                 (Script principal de build)
echo └─ validar_pre_build.py      (Validação pré-build)
echo.
echo build_windows.bat            (Invoca scripts\build.py)
echo GERAR_INSTALADOR.bat         (Invoca build_windows.bat)
echo.
echo FinancePro.spec              (Configuração PyInstaller)
echo requirements.txt             (Dependências Python)
echo main.py                      (Aplicação principal)
echo.
echo models\                      (Dados da aplicação)
echo views\                       (Interface gráfica)
echo utils\                       (Utilitários)
echo.
echo ========================================
echo   DOCUMENTACAO
echo ========================================
echo.
echo README_BUILD.md              (Este resumo)
echo RELATORIO_PROBLEMAS_BUILD.md (Detalhes técnicos)
echo GUIA_CLIENTE.md              (Instruções para cliente)
echo.
echo ========================================
echo   TROUBLESHOOTING
echo ========================================
echo.
echo ERRO: "Python não encontrado"
echo   Solução: Instale Python 3.8+
echo   https://www.python.org/
echo.
echo ERRO: "ModuleNotFoundError"
echo   Solução: pip install -r requirements.txt
echo.
echo ERRO: "PyInstaller não encontrado"
echo   Solução: pip install pyinstaller
echo.
echo ERRO: "Antivírus bloqueando"
echo   Solução: Adicione exceção no antivírus
echo            ou desabilite temporariamente
echo.
echo ERRO: "Arquivo de ícone não encontrado"
echo   Solução: Não precisa, usa ícone padrão
echo            Se quiser customizar, crie icon.ico
echo.
echo ========================================
echo.
echo Comandos rápidos para copiar:
echo.
echo   1. Validar:
echo      python scripts\validar_pre_build.py
echo.
echo   2. Build:
echo      GERAR_INSTALADOR.bat
echo.
echo   3. Testar executável:
echo      build_output\releases\FinancePro.exe
echo.
echo   4. Testar instalação:
echo      cd build_output\releases
echo      Instalar.bat
echo.
echo ========================================
echo.
pause
