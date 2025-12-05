@echo off
echo ===========================================
echo   OPTIMIZANDO DATOS CSV PARA SUPABASE
echo ===========================================

REM Buscar Python
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] Python no encontrado. Por favor instala Python.
    pause
    exit /b
)

REM Crear entorno virtual si no existe
if not exist .venv (
    echo [INFO] Creando entorno virtual...
    python -m venv .venv
)

REM Activar entorno
call .venv\Scripts\activate

REM Instalar dependencias
echo [INFO] Instalando librerias necesarias...
pip install pandas toml sqlalchemy psycopg2-binary

REM Ejecutar script de optimizacion
python process_data.py

echo.
echo ===========================================
echo   PROCESO COMPLETADO
echo ===========================================
echo Si todo salio bien, veras 'sales_summary.csv' en la carpeta data/
echo Ahora abre DBeaver y sube ese archivo a Supabase.
echo.
pause
