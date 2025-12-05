import os
import toml
import process_data
import upload_data_to_db
import sys
import subprocess

SECRETS_PATH = ".streamlit/secrets.toml"

def install_dependencies():
    print("📦 Verificando dependencias...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt", "toml"])

def setup_secrets():
    print("\n🔐 Configuración de Credenciales de Supabase")
    
    # Datos conocidos
    supabase_host = "db.qctcncvsiwlfznvwpafc.supabase.co"
    supabase_port = 5432
    supabase_db = "postgres"
    supabase_user = "postgres"
    
    print(f"Host detectado: {supabase_host}")
    print(f"User detectado: {supabase_user}")
    
    # Pedir contraseña
    password = input("🔑 Por favor, ingresa tu contraseña de base de datos de Supabase: ").strip()
    
    if not password:
        print("❌ La contraseña no puede estar vacía.")
        return False
    
    secrets_data = {
        "database": {
            "host": supabase_host,
            "port": supabase_port,
            "database": supabase_db,
            "user": supabase_user,
            "password": password
        }
    }
    
    # Asegurar directorio
    os.makedirs(".streamlit", exist_ok=True)
    
    # Escribir archivo (Sobrescribiendo o creando)
    try:
        with open(SECRETS_PATH, "w") as f:
            toml.dump(secrets_data, f)
        print(f"✅ Archivo {SECRETS_PATH} actualizado correctamente.")
        return True
    except Exception as e:
        print(f"❌ Error escribiendo secrets.toml: {e}")
        return False

def main():
    print("🚀 === ASISTENTE DE MIGRACIÓN SUPABASE === 🚀")
    
    # 1. Instalar dependencias (basico)
    try:
        import pandas
        import toml
        import sqlalchemy
        import psycopg2
    except ImportError:
        install_dependencies()

    # 2. Configurar secretos
    if not setup_secrets():
        return

    # 3. Optimizar datos (Agregación)
    print("\n📉 === PASO 1: OPTIMIZACIÓN DE DATOS ===")
    try:
        process_data.aggregate_data()
    except Exception as e:
        print(f"⚠️ Error en optimización (continuando con datos raw si es posible): {e}")

    # 4. Subir a DB
    print("\n☁️ === PASO 2: SUBIDA A SUPABASE ===")
    upload_data_to_db.main()
    
    print("\n✅ === MIGRACIÓN COMPLETADA EXITOSAMENTE ===")
    print("Ahora puedes ejecutar la app: streamlit run app.py")

if __name__ == "__main__":
    main()
