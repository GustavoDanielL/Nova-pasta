@echo off
REM Build script para Windows
REM Gera executável standalone do FinancePro

echo ========================================
echo    Build FinancePro para Windows
echo ========================================
echo.

REM Ativar ambiente virtual se existir
if exist ".venv\Scripts\activate.bat" (
    echo Ativando ambiente virtual...
    call .venv\Scripts\activate.bat
)

REM Instalar PyInstaller se necessário
echo Verificando PyInstaller...
pip install pyinstaller --quiet

REM Limpar builds anteriores
echo Limpando builds anteriores...
if exist "build" rmdir /s /q build
if exist "dist" rmdir /s /q dist

REM Criar executável
echo.
echo Gerando executavel...
pyinstaller --clean --noconfirm ^
    --name="FinancePro" ^
    --onefile ^
    --windowed ^
    --icon=icon.ico ^
    --add-data="theme_colors.py;." ^
    --add-data="config.py;." ^
    --hidden-import="PIL._tkinter_finder" ^
    --hidden-import="babel.numbers" ^
    --collect-all="customtkinter" ^
    --collect-all="PIL" ^
    main.py

REM Criar pasta de distribuição
echo.
echo Criando pacote de distribuicao...
if not exist "build_output\FinancePro-Windows" mkdir "build_output\FinancePro-Windows"
copy "dist\FinancePro.exe" "build_output\FinancePro-Windows\"
if exist "README.md" copy "README.md" "build_output\FinancePro-Windows\"

REM Criar instalador simples
echo @echo off > "build_output\FinancePro-Windows\instalar.bat"
echo echo Instalando FinancePro... >> "build_output\FinancePro-Windows\instalar.bat"
echo. >> "build_output\FinancePro-Windows\instalar.bat"
echo REM Copiar executavel para Program Files >> "build_output\FinancePro-Windows\instalar.bat"
echo mkdir "%%ProgramFiles%%\FinancePro" 2^>nul >> "build_output\FinancePro-Windows\instalar.bat"
echo copy "FinancePro.exe" "%%ProgramFiles%%\FinancePro\" >> "build_output\FinancePro-Windows\instalar.bat"
echo. >> "build_output\FinancePro-Windows\instalar.bat"
echo REM Criar atalho na Area de Trabalho >> "build_output\FinancePro-Windows\instalar.bat"
echo powershell "$WshShell = New-Object -ComObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%USERPROFILE%\Desktop\FinancePro.lnk'); $Shortcut.TargetPath = '%ProgramFiles%\FinancePro\FinancePro.exe'; $Shortcut.WorkingDirectory = '%ProgramFiles%\FinancePro'; $Shortcut.Save()" >> "build_output\FinancePro-Windows\instalar.bat"
echo. >> "build_output\FinancePro-Windows\instalar.bat"
echo echo. >> "build_output\FinancePro-Windows\instalar.bat"
echo echo FinancePro instalado com sucesso! >> "build_output\FinancePro-Windows\instalar.bat"
echo echo Atalho criado na area de trabalho >> "build_output\FinancePro-Windows\instalar.bat"
echo pause >> "build_output\FinancePro-Windows\instalar.bat"

echo.
echo ========================================
echo   Build concluido com sucesso!
echo ========================================
echo.
echo Executavel: build_output\FinancePro-Windows\FinancePro.exe
echo.
echo Execute diretamente ou instale com:
echo   cd build_output\FinancePro-Windows
echo   instalar.bat (como Administrador)
echo.
pause
