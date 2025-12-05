# 🚀 Sugerencias de Optimización y Migración a Supabase

## ⚠️ Problema Crítico de Consumo de Datos

Neon te ha informado que alcanzaste el límite de 5GB de transferencia. Esto ocurre porque tu aplicación descarga **toda la base de datos** cada vez que se recarga (aproximadamente 500MB por carga).

- **Neon Free Tier:** Límite de transferencia (varía, pero 5GB es común en planes bajos/free antiguos o soft limits).
- **Supabase Free Tier:** Límite de transferencia de **2GB mensuales** y base de datos de 500MB.

**Si migras a Supabase sin cambiar el código, alcanzarás el límite en solo 4 recargas de la aplicación.**

## ✅ Solución Recomendada (Migración Inteligente)

Para usar Supabase (o cualquier DB) sin pagar costos excesivos, debemos optimizar cómo la aplicación lee los datos.

### Opción A: Migrar a Supabase (Paso a Paso)

1.  **Crear Proyecto:** Ve a [Supabase](https://supabase.com/), crea una cuenta y un nuevo proyecto.
2.  **Obtener Credenciales:** En Settings -> Database -> Connection parameters, obtén:
    - Host
    - Database Name
    - User
    - Password
    - Port
3.  **Actualizar Secretos:** Edita el archivo `.streamlit/secrets.toml` con los nuevos datos de Supabase.
4.  **Cargar Datos:** He creado un script `upload_data_to_db.py` que tomará tus archivos Parquet locales y los subirá a la nueva base de datos.
    - Ejecuta: `python upload_data_to_db.py`
5.  **Optimizar (CRITICO):** Modificar `app.py` para no hacer `SELECT * FROM invoices`. En su lugar, deberíamos calcular los KPIs directamente en SQL o usar un sistema como DuckDB con archivos Parquet remotos para traer solo lo necesario.

### Opción B: Usar DuckDB local (Sin Base de Datos Externa)

Si tu aplicación corre en Streamlit Cloud y tus datos caben en memoria (parece que sí, pues ya lo haces), podrías empaquetar los archivos `.parquet` junto con la app (si caben en GitHub) o descargarlos desde un bucket S3/Google Drive al iniciar. Esto elimina la necesidad de una base de datos SQL costosa para lectura masiva.

---

### ¿Cómo proceder?

1.  Si ya creaste el proyecto en Supabase, por favor comparte las credenciales (o actualiza `secrets.toml` tú mismo).
2.  Puedo ayudarte a ejecutar el script de carga de datos.
3.  ¿Te gustaría que reescriba la lógica de carga de datos para ahorrar ancho de banda?
