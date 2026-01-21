$ErrorActionPreference = "Stop"

# Função para elevar privilégios se necessário
function Invoke-AsAdmin {
    param([string]$Script)
    
    $currentUser = [Security.Principal.WindowsIdentity]::GetCurrent()
    $principal = New-Object Security.Principal.WindowsPrincipal($currentUser)
    $isAdmin = $principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
    
    if (-not $isAdmin) {
        Write-Host "[ELEVANDO] Pedindo privilégios de administrador..."
        $scriptPath = $Profile.CurrentUserCurrentHost
        
        # Criar temp script
        $tempScript = "$env:TEMP\build_electron_temp.ps1"
        Set-Content -Path $tempScript -Value $Script
        
        # Executar como admin
        Start-Process powershell.exe -Verb RunAs -ArgumentList "-NoProfile -File `"$tempScript`""
        exit
    }
}

Write-Host "`n========================================`n  FinancePro - Build Electron`n========================================`n"

# Elevar se necessário
$buildScript = {
    Set-Location "C:\Users\affca\Downloads\Nova-pasta-main\Nova-pasta-main"
    
    Write-Host "[LIMPEZA] Deletando cache electron-builder..."
    Remove-Item -Path $env:LOCALAPPDATA\electron-builder -Recurse -Force -ErrorAction SilentlyContinue
    
    Write-Host "[OK] Cache deletado"
    Write-Host "`n[BUILD] Iniciando compilacao Electron..."
    
    Set-Location frontend
    
    # Desabilitar code signing via env
    $env:CSC_IDENTITY_AUTO_DISCOVERY = "false"
    $env:WIN_SIGNING = ""
    
    # Executar build
    npm run build:win
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "`n========================================`n  [OK] Build concluido!"
        Write-Host "`n  Instaladores em: ..\dist\"
        Write-Host "`n========================================"
    }
}

Invoke-AsAdmin -Script ([System.Convert]::ToBase64String([System.Text.Encoding]::Unicode.GetBytes($buildScript)))
