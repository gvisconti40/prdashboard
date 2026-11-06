import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine, text

# --- Configuración visual de la aplicación ---
st.set_page_config(
    page_title="Dashboard Comercial y Ventas",
    page_icon="📈",
    layout="wide"
)

# --- Conexión a MySQL usando st.secrets ---
@st.cache_resource
def get_db_engine():
    """Crea la conexión persistente con MySQL."""
    cfg = st.secrets["mysql"]
    url = f"mysql+pymysql://{cfg['user']}:{cfg['password']}@{cfg['host']}:{cfg['port']}/{cfg['database']}"
    return create_engine(url, pool_recycle=3600)

@st.cache_data(ttl=300)  # Re-consulta cada 5 minutos
def run_query(query: str, params: dict = None):
    """Ejecuta una consulta SQL segura y la convierte en DataFrame."""
    engine = get_db_engine()
    with engine.connect() as conn:
        return pd.read_sql(text(query), conn, params=params or {})

# --- Título principal ---
st.title("📊 Dashboard de Control de Ventas y Sedes")

# --- Barra lateral de filtros ---
st.sidebar.header("🔍 Filtros de Consulta")

if st.sidebar.button("🔄 Refrescar Datos"):
    st.cache_data.clear()
    st.rerun()

try:
    # 1. Cargar catálogo de Sedes
    df_sedes = run_query("SELECT id, nombre FROM sedes ORDER BY nombre")
    opciones_sedes = {"Todas": None}
    for _, row in df_sedes.iterrows():
        opciones_sedes[f"{row['nombre']} ({row['id'].strip()})"] = row['id']
    
    sede_seleccionada = st.sidebar.selectbox("Seleccionar Sede:", options=list(opciones_sedes.keys()))
    id_sede = opciones_sedes[sede_seleccionada]

    # 2. Cargar Años disponibles en ventas
    df_anos = run_query("SELECT DISTINCT ano FROM ventas ORDER BY ano DESC")
    lista_anos = df_anos["ano"].tolist() if not df_anos.empty else [2026]
    ano_seleccionado = st.sidebar.selectbox("Seleccionar Año:", options=lista_anos)

    # 3. Consulta de Métricas Generales (vta_dia)
    filtro_sede_sql = "AND v.id = :id_sede" if id_sede else ""
    params_base = {"id_sede": id_sede} if id_sede else {}

    sql_metricas_dia = f"""
        SELECT 
            COALESCE(SUM(vta), 0) as total_ventas,
            COALESCE(SUM(dev), 0) as total_devoluciones,
            COALESCE(SUM(noper), 0) as total_operaciones,
            COALESCE(AVG(tasa), 0) as tasa_promedio
        FROM vta_dia v
        WHERE 1=1 {filtro_sede_sql}
    """
    df_metricas = run_query(sql_metricas_dia, params_base)

    if not df_metricas.empty:
        total_vta = df_metricas.iloc[0]["total_ventas"]
        total_dev = df_metricas.iloc[0]["total_devoluciones"]
        total_oper = df_metricas.iloc[0]["total_operaciones"]
        tasa_prom = df_metricas.iloc[0]["tasa_promedio"]
        vta_neta = total_vta - total_dev

        # --- Tarjetas de Métricas ---
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Ventas Totales Brutas", f"${total_vta:,.2f}")
        col2.metric("Ventas Netas (menos dev)", f"${vta_neta:,.2f}")
        col3.metric("Número de Operaciones", f"{int(total_oper):,}")
        col4.metric("Tasa Promedio", f"{tasa_prom:,.2f}")

    st.divider()

    # --- Fila 1 de Gráficos: Ventas por Día y Cobros Especiales ---
    col_izq, col_der = st.columns(2)

    with col_izq:
        st.subheader("📅 Evolución de Ventas por Día")
        sql_evolucion = f"""
            SELECT fecha, SUM(vta) as ventas, SUM(dev) as devoluciones
            FROM vta_dia v
            WHERE 1=1 {filtro_sede_sql}
            GROUP BY fecha
            ORDER BY fecha DESC
            LIMIT 30
        """
        df_evolucion = run_query(sql_evolucion, params_base)
        if not df_evolucion.empty:
            df_evolucion = df_evolucion.sort_values("fecha")
            fig_dia = px.line(df_evolucion, x="fecha", y=["ventas", "devoluciones"], 
                              labels={"value": "Monto ($)", "fecha": "Fecha", "variable": "Tipo"},
                              title="Últimos 30 días de actividad",
                              markers=True)
            st.plotly_chart(fig_dia, use_container_width=True)
        else:
            st.info("No hay datos registrados en 'vta_dia' para esta selección.")

    with col_der:
        st.subheader("💳 Cobros por Tipo de Divisa")
        sql_divisas = f"""
            SELECT tipodiv, SUM(mnt) as total_monto
            FROM cob_div c
            WHERE 1=1 {"AND c.id = :id_sede" if id_sede else ""}
            GROUP BY tipodiv
            ORDER BY total_monto DESC
        """
        df_divisas = run_query(sql_divisas, params_base)
        if not df_divisas.empty:
            fig_pie = px.pie(df_divisas, names="tipodiv", values="total_monto", 
                             title="Distribución de Cobros en Divisas",
                             hole=0.4)
            st.plotly_chart(fig_pie, use_container_width=True)
        else:
            st.info("Sin registros en 'cob_div'.")

    st.divider()

    # --- Fila 2: Ventas por Línea de Producto y Top Vendedores ---
    col3, col4 = st.columns(2)

    with col3:
        st.subheader("🏷️ Ventas por Línea de Producto")
        sql_lineas = f"""
            SELECT l.lin_des AS linea, SUM(v.mnt) AS total_monto
            FROM ventas v
            JOIN art a ON v.cod = a.cod
            JOIN linea l ON a.co_lin = l.co_lin
            WHERE v.ano = :ano {"AND v.id = :id_sede" if id_sede else ""}
            GROUP BY l.lin_des
            ORDER BY total_monto DESC
            LIMIT 10
        """
        params_lineas = {"ano": ano_seleccionado}
        if id_sede:
            params_lineas["id_sede"] = id_sede
        df_lineas = run_query(sql_lineas, params_lineas)
        if not df_lineas.empty:
            fig_lin = px.bar(df_lineas, x="linea", y="total_monto", color="linea",
                             labels={"total_monto": "Total ($)", "linea": "Línea"},
                             title=f"Top Líneas - Año {ano_seleccionado}")
            st.plotly_chart(fig_lin, use_container_width=True)
        else:
            st.info("No hay datos de ventas por línea para el año seleccionado.")

    with col4:
        st.subheader("🏆 Top 10 Vendedores")
        sql_vendedores = f"""
            SELECT ven.ven_des AS vendedor, SUM(vv.mnt) AS total_ventas
            FROM vta_vend vv
            JOIN vendedor ven ON vv.co_ven = ven.co_ven
            WHERE vv.ano = :ano {"AND vv.id = :id_sede" if id_sede else ""}
            GROUP BY ven.ven_des
            ORDER BY total_ventas DESC
            LIMIT 10
        """
        df_vendedores = run_query(sql_vendedores, params_lineas)
        if not df_vendedores.empty:
            fig_ven = px.bar(df_vendedores, x="total_ventas", y="vendedor", orientation="h",
                             labels={"total_ventas": "Total Vendido ($)", "vendedor": "Vendedor"},
                             title=f"Ranking de Vendedores - Año {ano_seleccionado}",
                             color="total_ventas", color_continuous_scale="Blues")
            st.plotly_chart(fig_ven, use_container_width=True)
        else:
            st.info("No hay datos registrados en 'vta_vend' para este año.")

    st.divider()

    # --- Fila 3: Top Artículos Más Vendidos ---
    st.subheader("📦 Top 15 Artículos Más Vendidos")
    sql_articulos = f"""
        SELECT 
            a.cod AS Codigo,
            a.desc_art AS Descripcion,
            lb.des_lab AS Laboratorio,
            l.lin_des AS Linea,
            SUM(v.mnt) AS Monto_Total
        FROM ventas v
        JOIN art a ON v.cod = a.cod
        LEFT JOIN lab lb ON a.co_lab = lb.co_lab
        LEFT JOIN linea l ON a.co_lin = l.co_lin
        WHERE v.ano = :ano {"AND v.id = :id_sede" if id_sede else ""}
        GROUP BY a.cod, a.desc_art, lb.des_lab, l.lin_des
        ORDER BY Monto_Total DESC
        LIMIT 15
    """
    df_articulos = run_query(sql_articulos, params_lineas)
    if not df_articulos.empty:
        st.dataframe(df_articulos, use_container_width=True)
    else:
        st.info("No hay registros de artículos vendidos para este período.")

except Exception as e:
    st.error(f"Error consultando la base de datos: {e}")
    st.info("Verifica que las credenciales en 'Secrets' de Streamlit Cloud tengan acceso a las tablas indicadas.")
