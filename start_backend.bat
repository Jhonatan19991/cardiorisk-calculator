@echo off
echo Iniciando Calculadora de Riesgo Cardiovascular...
echo.
echo 1. Navegando al directorio backend...
cd backend

echo 2. Activando entorno virtual...
if exist venv\Scripts\activate.bat (
    call venv\Scripts\activate.bat
    echo Entorno virtual activado.
) else (
    echo Creando entorno virtual...
    python -m venv venv
    call venv\Scripts\activate.bat
    echo Instalando dependencias...
    pip install -r requirements.txt
)

echo 3. Iniciando servidor...
echo.
echo El servidor estara disponible en: http://localhost:5000
echo Presiona Ctrl+C para detener el servidor
echo.
python app.py

pause
