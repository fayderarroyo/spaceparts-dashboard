import toml
import os

SECRETS_PATH = ".streamlit/secrets.toml"

def update_secrets():
    print("🔧 Actualizando configuración de secretos para usar el Pooler (IPv4)...")
    
    if not os.path.exists(SECRETS_PATH):
        print("❌ No se encontró el archivo secrets.toml")
        return

    try:
        # Leer configuración actual
        with open(SECRETS_PATH, 'r') as f:
            config = toml.load(f)
        
        # Actualizar con los datos del Pooler (tomados de tus capturas)
        if 'database' in config:
            config['database']['host'] = "aws-1-us-east-1.pooler.supabase.com"
            config['database']['port'] = 6543
            config['database']['user'] = "postgres.qctcncvsiwlfznvwpafc"
            # La contraseña se mantiene igual, no la tocamos
            
            # Escribir de vuelta
            with open(SECRETS_PATH, 'w') as f:
                toml.dump(config, f)
            
            print("✅ Configuración actualizada exitosamente:")
            print(f"   Host: {config['database']['host']}")
            print(f"   Port: {config['database']['port']}")
            print(f"   User: {config['database']['user']}")
        else:
            print("⚠️ No se encontró la sección [database] en el archivo.")

    except Exception as e:
        print(f"❌ Error actualizando el archivo: {e}")

if __name__ == "__main__":
    update_secrets()
