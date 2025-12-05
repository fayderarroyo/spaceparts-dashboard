import pandas as pd
from sqlalchemy import create_engine, text
import streamlit as st
import os

# -----------------------------------------------------------------------------
# Script para cargar los archivos Parquet locales a la base de datos (Neon/Supabase)
# -----------------------------------------------------------------------------
# Prerrequisitos:
# 1. Tener el archivo .streamlit/secrets.toml configurado correctamente
# 2. Los archivos .parquet deben existir en la carpeta data/
# -----------------------------------------------------------------------------

def get_db_connection():
    """Crear conexión a base de datos usando st.secrets"""
    try:
        # Intenta cargar desde secrets.toml
        if "database" in st.secrets:
            db_config = st.secrets["database"]
            # Construir URL de conexión
            # Soporta formato estándar de Postgres
            db_url = f"postgresql://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['database']}"
            engine = create_engine(db_url)
            return engine
        else:
            print("❌ No se encontró la configuración [database] en .streamlit/secrets.toml")
            return None
    except Exception as e:
        print(f"❌ Error al conectar con la base de datos: {str(e)}")
        return None

def upload_table(file_path, table_name, engine):
    """Lee un parquet y lo sube a SQL"""
    if not os.path.exists(file_path):
        print(f"⚠️ Archivo no encontrado: {file_path}")
        return

    print(f"📖 Leyendo {file_path}...")
    try:
        df = pd.read_parquet(file_path)
        rows = len(df)
        print(f"✅ Leído {table_name}: {rows} filas. Subiendo a DB...")
        
        # Usar chunksize para evitar timeouts o problemas de memoria con 500MB+
        # 'replace' borrará la tabla existente y la creará de nuevo
        df.to_sql(table_name, engine, if_exists='replace', index=False, chunksize=5000)
        print(f"🎉 Tabla '{table_name}' actualizada exitosamente.")
        
    except Exception as e:
        print(f"❌ Error subiendo {table_name}: {e}")

def main():
    print("🚀 Iniciando carga de datos a la base de datos...")
    
    engine = get_db_connection()
    
    if engine:
        # Probar conexión simple
        try:
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            print("🔌 Conexión a base de datos exitosa.")
        except Exception as e:
            print(f"❌ Falló la prueba de conexión: {e}")
            return

        # Lista de archivos y tablas destino
        # PRIORIDAD: Usar datos agregados si existen
        files_to_upload = []
        
        if os.path.exists('data/invoices_aggregated.parquet'):
             print("💡 Encontrado archivo optimizado 'invoices_aggregated.parquet'. Usando este en lugar de raw invoices.")
             files_to_upload = [
                ('data/invoices_aggregated.parquet', 'sales_summary') 
             ]
        else:
             print("⚠️ No se encontró 'invoices_aggregated.parquet'. Preparando carga de archivos RAW (¡Cuidado con el límite de 500MB!).")
             files_to_upload = [
                ('data/customers_clean.parquet', 'customers'),
                ('data/products_clean.parquet', 'products'),
                ('data/orders_clean.parquet', 'orders'),
                ('data/invoices_clean.parquet', 'invoices')
            ]
        
        for file_path, table_name in files_to_upload:
            upload_table(file_path, table_name, engine)
            
        print("\n✨ Proceso finalizado.")

if __name__ == "__main__":
    main()
