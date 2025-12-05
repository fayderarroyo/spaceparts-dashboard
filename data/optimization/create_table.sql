-- SQL para crear la tabla optimizada en Supabase

CREATE TABLE IF NOT EXISTS sales_summary (
    billing_date DATE,
    station TEXT,
    part_ship_class TEXT,
    sub_brand_name TEXT,
    total_sales NUMERIC, -- Usamos NUMERIC para valores monetarios precisos
    total_cogs NUMERIC,
    otd_successes INTEGER, -- Conteo de éxitos OTD
    total_orders INTEGER   -- Total de órdenes (para calcular porcentajes)
);

-- Opcional: Crear un índice por fecha para agilizar los filtros del dashboard
CREATE INDEX IF NOT EXISTS idx_billing_date ON sales_summary(billing_date);
