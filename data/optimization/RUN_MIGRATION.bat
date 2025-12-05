@echo off
echo ===========================================
echo   INICIANDO MIGRACION A SUPABASE
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
pip install -r requirements.txt toml psycopg2-binary sqlalchemy

REM Ejecutar script de migracion
python migrate_to_supabase.py

pause
