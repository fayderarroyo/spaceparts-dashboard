import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
from sqlalchemy import create_engine

# Page config
st.set_page_config(
    page_title="SpaceParts Analytics | Fayder Arroyo",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for dark theme matching the website
st.markdown("""
<style>
    .main {
        background-color: #0f172a;
    }
    .stMetric {
        background-color: #1e293b;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid rgba(255,255,255,0.1);
    }
    .stMetric label {
        color: #94a3b8 !important;
    }
    .stMetric .metric-value {
        color: #22c55e !important;
    }
    h1, h2, h3 {
        color: #f8fafc !important;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def get_db_connection():
    """Create database connection from Streamlit secrets"""
    try:
        if "database" not in st.secrets:
            st.error("❌ No se encontró la configuración de base de datos en secrets.toml")
            return None
            
        db_config = st.secrets["database"]
        engine = create_engine(
            f"postgresql://{db_config['user']}:{db_config['password']}@"
            f"{db_config['host']}:{db_config['port']}/{db_config['database']}"
        )
        return engine
    except Exception as e:
        st.error(f"Error connecting to database: {str(e)}")
        return None

@st.cache_data(ttl=3600)
def load_data():
    """Load aggregated data from Supabase"""
    engine = get_db_connection()
    
    if engine is None:
        return None
    
    with st.spinner("Cargando datos optimizados desde Supabase..."):
        try:
            # Load only the sales_summary table
            # This table is pre-aggregated and small (<10MB) avoiding the 500MB limit
            df = pd.read_sql("SELECT * FROM sales_summary", engine)
            
            # Convert date
            if 'billing_date' in df.columns:
                df['billing_date'] = pd.to_datetime(df['billing_date'])
                
            return df
            
        except Exception as e:
            st.error(f"Error loading data: {str(e)}")
            st.info("💡 Si acabas de migrar, asegúrate de que la tabla `sales_summary` existe en Supabase.")
            return None

def calculate_kpis(df):
    """Calculate main KPIs from aggregated data"""
    # Summing up pre-aggregated values
    total_sales = df['total_sales'].sum()
    total_cogs = df['total_cogs'].sum()
    gross_margin = total_sales - total_cogs
    margin_pct = (gross_margin / total_sales * 100) if total_sales > 0 else 0
    
    # OTD calculation (Weighted average based on successes/orders)
    total_orders = df['total_orders'].sum()
    total_otd_successes = df['otd_successes'].sum()
    
    otd_pct = (total_otd_successes / total_orders * 100) if total_orders > 0 else 0
    
    return {
        'total_sales': total_sales,
        'margin_pct': margin_pct,
        'otd_pct': otd_pct,
        'total_orders': total_orders
    }

def main():
    # Header
    st.title("🚀 SpaceParts Business Intelligence")
    st.markdown("### Dashboard Interactivo | Fayder Arroyo")
    st.caption("⚡ Versión Optimizada para Supabase")
    st.markdown("---")
    
    # Load data
    df = load_data()
    
    if df is None or df.empty:
        st.warning("⚠️ No hay datos disponibles. Ejecuta la migración de datos primero.")
        return
    
    # --- FILTERS ---
    st.sidebar.markdown("## 🔍 Filtros")
    
    # Date Range filter
    min_date = df['billing_date'].min().date()
    max_date = df['billing_date'].max().date()
    
    date_range = st.sidebar.date_input(
        "📅 Rango de Fechas",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )
    
    if len(date_range) == 2:
        start_date, end_date = date_range
        df = df[
            (df['billing_date'].dt.date >= start_date) & 
            (df['billing_date'].dt.date <= end_date)
        ]
        
    # Ship Class filter
    all_classes = sorted(df['part_ship_class'].unique())
    selected_classes = st.sidebar.multiselect(
        "📦 Part Ship Class",
        all_classes,
        default=all_classes
    )
    if selected_classes:
        df = df[df['part_ship_class'].isin(selected_classes)]
        
    # Station filter
    # To avoid list too long, get top stations by sales
    station_sales = df.groupby('station')['total_sales'].sum().sort_values(ascending=False)
    top_stations = station_sales.head(20).index.tolist()
    
    selected_stations = st.sidebar.multiselect(
        "🏢 Estaciones (Top 20)",
        top_stations,
        default=top_stations[:5]  # Select top 5 by default not to clutter
    )
    
    if selected_stations:
        df = df[df['station'].isin(selected_stations)]

    st.sidebar.markdown("---")
    
    # --- KPIs ---
    kpis = calculate_kpis(df)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("💰 Total Sales", f"${kpis['total_sales']/1e6:.1f}M")
    with col2:
        st.metric("📊 Margin %", f"{kpis['margin_pct']:.1f}%")
    with col3:
        st.metric("🎯 OTD %", f"{kpis['otd_pct']:.1f}%")
    with col4:
        st.metric("📦 Orders", f"{kpis['total_orders']:,}")
    
    st.markdown("---")
    
    # --- CHARTS ---
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("💰 Sales Over Time")
        # Group by month
        monthly = df.groupby(df['billing_date'].dt.to_period('M')).agg({
            'total_sales': 'sum',
            'total_cogs': 'sum'
        }).reset_index()
        monthly['billing_date'] = monthly['billing_date'].astype(str)
        
        fig = go.Figure()
        fig.add_trace(go.Bar(name='Sales', x=monthly['billing_date'], y=monthly['total_sales'], marker_color='#22c55e'))
        fig.add_trace(go.Bar(name='COGS', x=monthly['billing_date'], y=monthly['total_cogs'], marker_color='#3b82f6'))
        fig.update_layout(barmode='group', title="Monthly Sales vs COGS", template="plotly_dark")
        st.plotly_chart(fig, use_container_width=True)
        
    with col2:
        st.subheader("🏆 Top Stations")
        top_st = df.groupby('station')['total_sales'].sum().nlargest(10).reset_index()
        fig = px.bar(
            top_st, x='total_sales', y='station', orientation='h',
            title="Top 10 Stations by Sales", template="plotly_dark", color_discrete_sequence=['#22c55e']
        )
        fig.update_layout(yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig, use_container_width=True)
        
    # Row 2
    col3, col4 = st.columns(2)
    
    with col3:
        st.subheader("🚦 Margin Health")
        fig = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = kpis['margin_pct'],
            title = {'text': "Overall Margin %"},
            gauge = {
                'axis': {'range': [0, 60]},
                'bar': {'color': "white"},
                'steps': [
                    {'range': [0, 40], 'color': "#ef4444"},
                    {'range': [40, 42], 'color': "#eab308"},
                    {'range': [42, 100], 'color': "#22c55e"}
                ]
            }
        ))
        fig.update_layout(template="plotly_dark")
        st.plotly_chart(fig, use_container_width=True)
        
    with col4:
        st.subheader("📊 Product Performance")
        # Aggregate by product
        prod_perf = df.groupby('sub_brand_name').agg({
            'total_sales': 'sum',
            'total_cogs': 'sum'
        }).reset_index()
        
        prod_perf['margin_pct'] = ((prod_perf['total_sales'] - prod_perf['total_cogs']) / prod_perf['total_sales'] * 100).fillna(0)
        prod_perf['sales_millions'] = prod_perf['total_sales'] / 1e6
        
        # Filter top 20
        prod_perf = prod_perf.nlargest(20, 'total_sales')
        
        fig = px.scatter(
            prod_perf, x='sales_millions', y='margin_pct', size='sales_millions',
            color='margin_pct', hover_data=['sub_brand_name'],
            title="Sales vs Margin % (Top 20 Products)",
            template="plotly_dark", color_continuous_scale='RdYlGn'
        )
        st.plotly_chart(fig, use_container_width=True)

    # Footer
    st.markdown("---")
    
    # Calculate summary metrics for footer
    unique_stations = df['station'].nunique()
    unique_products = df['sub_brand_name'].nunique()
    total_records = df['total_orders'].sum()
    
    col1, col2, col3 = st.columns(3)
    with col2:
        st.markdown(f"""
        <div style='text-align: center; color: #64748b; font-size: 0.85rem; padding: 0.5rem;'>
            📊 <strong>Datos Procesados:</strong> {unique_stations} Estaciones | {unique_products} Productos | {total_records:,} Transacciones
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown("""
    <div style='text-align: center; color: #94a3b8; padding: 1.5rem;'>
        <p>Desarrollado por <strong style='color: #22c55e;'>Fayder Arroyo</strong> | Data & BI Analyst</p>
        <p>🔗 <a href='https://fayderarroyo.github.io/CV-Website/' style='color: #22c55e;'>Ver Portafolio</a></p>
        <p style='font-size: 0.8rem; margin-top: 1rem;'>Powered by PostgreSQL & Streamlit (Supabase Optimized)</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
