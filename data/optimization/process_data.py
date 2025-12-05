import pandas as pd
import os

def aggregate_data():
    print("🚀 Cargando archivos CSV para optimización...")
    
    # Rutas de archivos
    invoices_path = 'data/invoices.csv'
    customers_path = 'data/customers.csv'
    products_path = 'data/products.csv'
    
    if not os.path.exists(invoices_path):
        print(f"❌ No se encontró {invoices_path}")
        return

    print("📖 Leyendo Invoices (esto puede tardar unos segundos)...")
    # Solo cargamos columnas necesarias para ahorrar memoria
    invoices = pd.read_csv(invoices_path, usecols=[
        'billing_date', 'customer_key', 'product_key', 
        'net_invoice_value', 'net_invoice_cogs', 'otd_indicator'
    ])
    
    print("📖 Leyendo Clientes y Productos...")
    customers = pd.read_csv(customers_path, usecols=['customer_key', 'station'])
    products = pd.read_csv(products_path, usecols=['product_key', 'part_ship_class', 'sub_brand_name'])

    print(f"✅ Datos cargados. Filas originales facturas: {len(invoices):,}")

    # Unir con dimensiones
    print("🔄 Uniendo tablas...")
    df = invoices.merge(customers, on='customer_key', how='left')
    df = df.merge(products, on='product_key', how='left')

    # Convertir fecha a solo fecha (día) para agrupar
    # Aseguramos formato fecha ya que en CSV viene como string
    df['billing_date'] = pd.to_datetime(df['billing_date']).dt.date

    # Rellenar nulos para agrupación segura
    df['station'] = df['station'].fillna('Unknown')
    df['part_ship_class'] = df['part_ship_class'].fillna('Unknown')
    df['sub_brand_name'] = df['sub_brand_name'].fillna('Unknown')

    print("📉 Agrupando datos (reduciendo tamaño)...")
    
    # Agrupar
    aggregated = df.groupby(['billing_date', 'station', 'part_ship_class', 'sub_brand_name']).agg({
        'net_invoice_value': 'sum',
        'net_invoice_cogs': 'sum',
        'otd_indicator': ['sum', 'count'] 
    }).reset_index()

    # Aplanar columnas
    aggregated.columns = ['billing_date', 'station', 'part_ship_class', 'sub_brand_name', 
                          'total_sales', 'total_cogs', 'otd_successes', 'total_orders']

    print(f"✅ Agrupación completada. Nuevas filas: {len(aggregated):,}")
    
    # Guardar como CSV para fácil importación en DBeaver
    output_path = 'data/sales_summary.csv'
    aggregated.to_csv(output_path, index=False)
    
    size_mb = os.path.getsize(output_path) / (1024 * 1024)
    print(f"💾 Archivo optimizado guardado en: {output_path}")
    print(f"📉 Tamaño final: {size_mb:.2f} MB")
    
    print("\n⚠️ IMPORTANTE PARA DBEAVER:")
    print("1. Crea una tabla llamada 'sales_summary' en Supabase.")
    print("2. Importa este archivo CSV.")
    print("3. Asegúrate de que los tipos de datos sean correctos (billing_date -> DATE/TIMESTAMP, otros -> NUMERIC/INTEGER).")

    return output_path

if __name__ == "__main__":
    try:
        aggregate_data()
    except Exception as e:
        print(f"❌ Error: {e}")
