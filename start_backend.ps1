# Script de inicio para la Calculadora de Riesgo Cardiovascular
Write-Host "Iniciando Calculadora de Riesgo Cardiovascular..." -ForegroundColor Green
Write-Host ""

Write-Host "1. Navegando al directorio backend..." -ForegroundColor Yellow
Set-Location backend

Write-Host "2. Activando entorno virtual..." -ForegroundColor Yellow
if (Test-Path "venv\Scripts\Activate.ps1") {
    & "venv\Scripts\Activate.ps1"
    Write-Host "Entorno virtual activado." -ForegroundColor Green
} else {
    Write-Host "Creando entorno virtual..." -ForegroundColor Yellow
    python -m venv venv
    & "venv\Scripts\Activate.ps1"
    Write-Host "Instalando dependencias..." -ForegroundColor Yellow
    pip install -r requirements.txt
}

Write-Host "3. Iniciando servidor..." -ForegroundColor Yellow
Write-Host ""
Write-Host "El servidor estará disponible en: http://localhost:5000" -ForegroundColor Cyan
Write-Host "Presiona Ctrl+C para detener el servidor" -ForegroundColor Cyan
Write-Host ""

python app.py

Read-Host "Presiona Enter para continuar..."
