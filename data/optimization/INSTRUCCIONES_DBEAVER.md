# 🦫 Cómo subir datos con DBeaver

Sigue estos pasos para subir tu archivo `sales_summary.csv` a Supabase usando DBeaver.

## Prerrequisito
Asegúrate de haber ejecutado el SQL `CREATE TABLE` en Supabase (o en DBeaver) para que la tabla `sales_summary` ya exista.

## Pasos de Importación

1.  **Ubica la tabla:** En el panel de navegación de la izquierda, abre tu conexión a Supabase -> `Schemas` -> `public` -> `Tables`. Deberías ver la tabla `sales_summary`.
2.  **Iniciar Importación:** Haz clic derecho sobre `sales_summary` y selecciona **Importar Datos** (Import Data).
3.  **Seleccionar Fuente:** Elige **CSV** como formato de fuente y dale a "Siguiente" (Next).
4.  **Seleccionar Archivo:**
    *   Busca el archivo `sales_summary.csv` que generamos.
    *   Está en la carpeta: `.../cv-website/streamlit-dashboard/data/sales_summary.csv`.
5.  **Configurar CSV:**
    *   Asegúrate de que la codificación (encoding) sea `UTF-8`.
    *   Verifica que el separador sea coma (`,`) (por defecto).
    *   Dale a "Siguiente".
6.  **Mapeo de Columnas (Mapping):**
    *   DBeaver intentará hacer coincidir las columnas del Excel con las de la base de datos automáticamente.
    *   Verifica que `billing_date` vaya con `billing_date`, `total_sales` con `total_sales`, etc.
7.  **Finalizar:** Dale a "Siguiente" y luego a **"Proceder"** (Proceed) o "Start".

### ✅ Verificación
Una vez termine:
1.  Haz clic derecho en la tabla `sales_summary` -> **Ver Datos** (View Data).
2.  Deberías ver las filas allí.
3.  ¡Listo! Ya puedes probar la App.
