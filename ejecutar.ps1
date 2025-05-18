# Script para ejecutar la aplicación Ruteador Perú usando Python
# Este script intenta diferentes métodos para ejecutar la aplicación

Write-Host "Intentando ejecutar Ruteador Perú..." -ForegroundColor Cyan

# Método 1: Python directo
Write-Host "Método 1: Intentando ejecutar con Python directamente..." -ForegroundColor Yellow
try {
    python main.py
    if ($LASTEXITCODE -eq 0) {
        exit 0
    }
}
catch {
    Write-Host "No se pudo ejecutar con Python directamente" -ForegroundColor Red
}

# Método 2: Usando Anaconda si está disponible
Write-Host "Método 2: Intentando ejecutar con Anaconda..." -ForegroundColor Yellow
try {
    & conda activate base
    if ($?) {
        python main.py
        if ($LASTEXITCODE -eq 0) {
            exit 0
        }
    }
}
catch {
    Write-Host "No se pudo ejecutar con Anaconda" -ForegroundColor Red
}

# Método 3: Versión alternativa con PySide2
Write-Host "Método 3: Intentando ejecutar versión alternativa con PySide2..." -ForegroundColor Yellow
try {
    python main_pyside2.py
    if ($LASTEXITCODE -eq 0) {
        exit 0
    }
}
catch {
    Write-Host "No se pudo ejecutar versión alternativa" -ForegroundColor Red
}

Write-Host "No se pudo iniciar la aplicación con ningún método." -ForegroundColor Red
Write-Host "Comprueba que tienes las dependencias instaladas:" -ForegroundColor Yellow
Write-Host "- PyQt5 o PySide2" -ForegroundColor Yellow
Write-Host "- matplotlib" -ForegroundColor Yellow
Write-Host "- networkx" -ForegroundColor Yellow
Write-Host "- pandas" -ForegroundColor Yellow
Write-Host "- geopandas" -ForegroundColor Yellow

Read-Host "Presiona Enter para salir"
