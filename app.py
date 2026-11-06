import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine, text

# --- Configuración de la página ---
st.set_page_config(
    page_title="Dashboard MySQL",
    page_icon="📊",
    layout="wide"
)

# --- Conexión con caché ---
@st.cache_resource
def get_db_engine():
    """Crea y almacena en caché el motor de base de datos MySQL."""
    db_config = st.secrets["mysql"]
    connection_url = (
        f"mysql+pymysql://{db_config['user']}:{db_config['password']}@"
        f"{db_config['host']}:{db_config['port']}/{db_config['database']}"
    )
    return create_engine(connection_url, pool_recycle=3600)

@st.cache_data(ttl=600)  # Actualiza la caché cada 10 minutos
def run_query(query: str):
    """Ejecuta una consulta SQL y retorna un DataFrame de Pandas."""
    engine = get_db_engine()
    with engine.connect() as conn:
        return pd.read_sql(text(query), conn)

# --- Interfaz del Dashboard ---
st.title("📊 Panel de Control y Métricas")
st.caption("Conectado a MySQL en la nube")

# Botón para refrescar datos manualmente
if st.sidebar.button("🔄 Refrescar datos"):
    st.cache_data.clear()
    st.rerun()

try:
    # 1. Ejemplo de consulta de resumen / métricas clave
    # (Adapta estas consultas con los nombres de tus tablas y columnas)
    st.subheader("Métricas Generales")
    col1, col2, col3 = st.columns(3)

    # Nota: Reemplaza "SELECT COUNT(*) FROM mi_tabla" con tu tabla real
    # df_total = run_query("SELECT COUNT(*) AS total FROM mi_tabla")
    col1.metric(label="Total Registros", value="1,250", delta="+12%")
    col2.metric(label="Ventas / Actividad", value="$45,200", delta="+8%")
    col3.metric(label="Clientes / Usuarios Activos", value="320", delta="-2%")

    st.divider()

    # 2. Gráficos interactivos
    col_izq, col_der = st.columns(2)

    with col_izq:
        st.subheader("Distribución por Categoría")
        # Ejemplo: df_cat = run_query("SELECT categoria, COUNT(*) as cantidad FROM productos GROUP BY categoria")
        # Datos de prueba para previsualizar:
        sample_df = pd.DataFrame({
            "Categoría": ["Electrónica", "Ropa", "Hogar", "Alimentos"],
            "Ventas": [12000, 8500, 6400, 4300]
        })
        fig_bar = px.bar(sample_df, x="Categoría", y="Ventas", color="Categoría", title="Ventas por Categoría")
        st.plotly_chart(fig_bar, use_container_width=True)

    with col_der:
        st.subheader("Tendencia Temporal")
        sample_time_df = pd.DataFrame({
            "Fecha": pd.date_range(start="2026-01-01", periods=10, freq="D"),
            "Valor": [10, 15, 13, 17, 22, 28, 25, 30, 32, 38]
        })
        fig_line = px.line(sample_time_df, x="Fecha", y="Valor", markers=True, title="Evolución en el Tiempo")
        st.plotly_chart(fig_line, use_container_width=True)

    # 3. Vista de tabla de datos
    st.subheader("Explorador de Datos")
    # df_tabla = run_query("SELECT * FROM mi_tabla LIMIT 50")
    st.dataframe(sample_df, use_container_width=True)

except Exception as e:
    st.error(f"Error al conectar o consultar la base de datos: {e}")
    st.info("Asegúrate de haber configurado correctamente el archivo `.streamlit/secrets.toml` con los datos de tu servidor MySQL.")
