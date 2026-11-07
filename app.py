import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine, text
from datetime import datetime, timedelta
import random

# --- Configuración visual de la aplicación ---
st.set_page_config(
    page_title="KPI Dashboard - Grupo Farmacias",
    page_icon="💊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Conexión a MySQL en vivo (si existen secretos configurados) ---
@st.cache_resource
def get_db_engine():
    if "mysql" in st.secrets:
        cfg = st.secrets["mysql"]
        url = f"mysql+pymysql://{cfg['user']}:{cfg['password']}@{cfg['host']}:{cfg['port']}/{cfg['database']}"
        return create_engine(url, pool_recycle=3600)
    return None

# --- Generador de Datos Mock de Simulación ---
@st.cache_data
def generar_datos_prueba():
    hoy = datetime.now().date()
    sucursales = [
        {"id_sucursal": 1, "codigo_sucursal": "F001", "nombre": "Farmacia Central", "ciudad": "Caracas"},
        {"id_sucursal": 2, "codigo_sucursal": "F002", "nombre": "Farmacia Las Mercedes", "ciudad": "Caracas"},
        {"id_sucursal": 3, "codigo_sucursal": "F003", "nombre": "Farmacia Bella Vista", "ciudad": "Maracaibo"},
        {"id_sucursal": 4, "codigo_sucursal": "F004", "nombre": "Farmacia Los Sauces", "ciudad": "Valencia"},
        {"id_sucursal": 5, "codigo_sucursal": "F005", "nombre": "Farmacia El Parral", "ciudad": "Valencia"}
    ]
    df_suc = pd.DataFrame(sucursales)

    # Catálogo Maestro: solo datos intrínsecos del producto (sin proveedor fijo)
    productos = [
        (1, "7591001", "Atorvastatina 20mg x 30 Tab", "Pfizer"),
        (2, "7591002", "Losartán Potásico 50mg x 30 Comp", "Calox"),
        (3, "7591003", "Amoxicilina + Ác. Clavulánico 875mg", "Genven"),
        (4, "7591004", "Ibuprofeno 400mg x 20 Cáps", "Bayer"),
        (5, "7591005", "Paracetamol 500mg x 20 Tab", "Calox"),
        (6, "7591006", "Omeprazol 20mg x 28 Cáps", "Leti"),
        (7, "7591007", "Vitamina C 1000mg Efervescente", "Bayer"),
        (8, "7591008", "Metformina 850mg x 30 Tab", "Merck"),
        (9, "7591009", "Loratadina 10mg x 10 Tab", "Leti"),
        (10, "7591010", "Cetirizina 10mg x 10 Tab", "Genven")
    ]
    df_prod = pd.DataFrame(productos, columns=["id_producto", "codigo_barras", "nombre_producto", "laboratorio"])

    fechas = [hoy - timedelta(days=i) for i in range(30, -1, -1)]
    proveedores_lista = ["Cobeca", "Droguería Nena", "Drolanca", "Grupo Farvenca"]

    # 1. Ventas Diarias Globales
    filas_vta = []
    for suc in sucursales:
        for f in fechas:
            tck = random.randint(45, 160)
            fact = round(tck * random.uniform(18.5, 38.0), 2)
            filas_vta.append({
                "id_sucursal": suc["id_sucursal"],
                "fecha": f,
                "total_facturado": fact,
                "cantidad_tickets": tck
            })
    df_vta_dia = pd.DataFrame(filas_vta)

    # 2. Ventas por Producto
    filas_prod_vta = []
    for suc in sucursales:
        for f in fechas:
            for _, p in df_prod.iterrows():
                uds = random.randint(2, 22)
                monto = round(uds * random.uniform(4.5, 18.0), 2)
                filas_prod_vta.append({
                    "id_sucursal": suc["id_sucursal"],
                    "fecha": f,
                    "id_producto": p["id_producto"],
                    "unidades_vendidas": uds,
                    "total_venta_monto": monto
                })
    df_vta_prod = pd.DataFrame(filas_prod_vta)

    # 3. Inventario (por sucursal y producto, con costo unitario para valorización)
    costos_base = {1: 8.50, 2: 4.20, 3: 12.00, 4: 3.80, 5: 2.10, 6: 5.60, 7: 6.90, 8: 4.50, 9: 2.80, 10: 3.10}
    filas_inv = []
    for suc in sucursales:
        for _, p in df_prod.iterrows():
            min_stk = random.randint(15, 40)
            act_stk = random.choice([0, random.randint(1, min_stk - 1), random.randint(min_stk, 120)])
            c_unit = costos_base.get(p["id_producto"], 5.00)
            filas_inv.append({
                "id_sucursal": suc["id_sucursal"],
                "id_producto": p["id_producto"],
                "stock_actual": act_stk,
                "stock_minimo": min_stk,
                "costo_unitario": c_unit,
                "valor_total_inventario": round(act_stk * c_unit, 2)
            })
    df_inv = pd.DataFrame(filas_inv)

    # 4. Compras por Producto y Proveedor (múltiples proveedores por producto)
    filas_comp = []
    for suc in sucursales:
        for f in fechas[::2]:
            for _, p in df_prod.sample(6).iterrows():
                prov = random.choice(proveedores_lista)  # Puede ser comprado a cualquier proveedor
                uds_c = random.randint(20, 90)
                costo = round(uds_c * random.uniform(2.5, 12.0), 2)
                filas_comp.append({
                    "id_sucursal": suc["id_sucursal"],
                    "fecha": f,
                    "id_producto": p["id_producto"],
                    "nombre_proveedor": prov,
                    "unidades_compradas": uds_c,
                    "total_compra_monto": costo
                })
    df_compras = pd.DataFrame(filas_comp)

    # 5. Vendedores
    vendedores = ["María Gómez", "Carlos Pérez", "Ana Rodríguez", "José Morales", "Laura Silva"]
    filas_vend = []
    for suc in sucursales:
        for f in fechas:
            for v in random.sample(vendedores, 3):
                ops = random.randint(15, 50)
                mto = round(ops * random.uniform(15.0, 32.0), 2)
                filas_vend.append({
                    "id_sucursal": suc["id_sucursal"],
                    "fecha": f,
                    "nombre_vendedor": v,
                    "total_vendido": mto,
                    "cantidad_operaciones": ops
                })
    df_vend = pd.DataFrame(filas_vend)

    # 6. Formas de Pago
    formas = ['Efectivo', 'Tarjeta Crédito', 'Tarjeta Débito', 'Pago Móvil', 'Transferencia']
    filas_pago = []
    for suc in sucursales:
        for f in fechas:
            for fp in formas:
                filas_pago.append({
                    "id_sucursal": suc["id_sucursal"],
                    "fecha": f,
                    "forma_pago": fp,
                    "total_ingresado": round(random.uniform(150.0, 950.0), 2)
                })
    df_formas_pago = pd.DataFrame(filas_pago)

    # 7. Bancos y Cajas de Efectivo
    bancos = [("Banesco", "4521"), ("Banco Mercantil", "9012"), ("BBVA Provincial", "3341"), ("Banco de Venezuela", "7890")]
    filas_bancos = []
    for suc in sucursales:
        for b_nom, b_cta in bancos:
            filas_bancos.append({
                "id_sucursal": suc["id_sucursal"],
                "fecha": hoy,
                "nombre_banco": b_nom,
                "numero_cuenta_oculto": b_cta,
                "saldo_disponible": round(random.uniform(2500.0, 18400.0), 2)
            })
    df_bancos = pd.DataFrame(filas_bancos)

    cajas_tipos = [
        ("Caja Principal / Bóveda", "USD", 1200.0, 6500.0),
        ("Caja Principal / Bóveda", "VES", 45000.0, 180000.0),
        ("Caja Chica", "USD", 100.0, 450.0),
        ("Caja Punto de Venta", "USD", 350.0, 1800.0)
    ]
    filas_cajas = []
    for suc in sucursales:
        for tipo_c, mon, min_s, max_s in cajas_tipos:
            filas_cajas.append({
                "id_sucursal": suc["id_sucursal"],
                "fecha": hoy,
                "tipo_caja": tipo_c,
                "moneda": mon,
                "saldo_efectivo": round(random.uniform(min_s, max_s), 2)
            })
    df_cajas = pd.DataFrame(filas_cajas)

    # 8. CxC por Cliente y CxP
    clientes_ejemplo = [
        ("Particular", "V-14.238.901", "Roberto Méndez"),
        ("Particular", "V-18.765.432", "Elena Salazar"),
        ("Seguro / Empresa", "J-30491823-1", "Seguros Caracas"),
        ("Seguro / Empresa", "J-00012345-0", "Mercantil Seguros"),
        ("Convenio", "J-00045678-9", "Empresas Polar (Convenio)"),
        ("Seguro / Empresa", "J-29837192-3", "Banesco Seguros")
    ]
    filas_cxc = []
    for suc in sucursales:
        for tipo_c, ident_c, nom_c in clientes_ejemplo:
            filas_cxc.append({
                "id_sucursal": suc["id_sucursal"],
                "fecha": hoy,
                "tipo_cliente": tipo_c,
                "identificacion_cliente": ident_c,
                "nombre_cliente": nom_c,
                "saldo_pendiente": round(random.uniform(250.0, 5200.0), 2)
            })
    df_cxc = pd.DataFrame(filas_cxc)

    filas_cxp = []
    for suc in sucursales:
        for pr in proveedores_lista:
            filas_cxp.append({
                "id_sucursal": suc["id_sucursal"],
                "fecha": hoy,
                "nombre_proveedor": pr,
                "saldo_por_pagar": round(random.uniform(2200.0, 14500.0), 2)
            })
    df_cxp = pd.DataFrame(filas_cxp)

    return {
        "sucursales": df_suc,
        "productos": df_prod,
        "ventas_diarias": df_vta_dia,
        "ventas_producto": df_vta_prod,
        "inventario": df_inv,
        "compras": df_compras,
        "vendedores": df_vend,
        "formas_pago": df_formas_pago,
        "bancos": df_bancos,
        "cajas": df_cajas,
        "cxc": df_cxc,
        "cxp": df_cxp
    }

# --- Título principal ---
st.title("💊 Cuadro de Mando Integral - Red de Farmacias")
st.caption("Consolidado Centralizado de Rendimiento Operativo, Comercial y Financiero")

# --- Barra lateral de Configuración y Filtros ---
st.sidebar.header("⚙️ Configuración & Filtros")

modo_datos = st.sidebar.radio(
    "Fuente de Datos:",
    ["Simulación (Datos de Prueba)", "Conexión MySQL en Vivo"],
    index=0
)

if st.sidebar.button("🔄 Refrescar Datos", use_container_width=True):
    st.cache_data.clear()
    st.rerun()

# Carga de catálogos base
if modo_datos == "Simulación (Datos de Prueba)":
    datos = generar_datos_prueba()
    df_sucursales = datos["sucursales"]
    df_catalogo_prod = datos["productos"]
    lista_provs = sorted(datos["compras"]["nombre_proveedor"].unique().tolist())
else:
    try:
        engine = get_db_engine()
        with engine.connect() as conn:
            df_sucursales = pd.read_sql(text("SELECT id_sucursal, codigo_sucursal, nombre, ciudad FROM sucursales ORDER BY nombre"), conn)
            df_catalogo_prod = pd.read_sql(text("SELECT DISTINCT laboratorio FROM maestro_productos"), conn)
            df_provs = pd.read_sql(text("SELECT DISTINCT nombre_proveedor FROM kpi_compras_por_producto UNION SELECT DISTINCT nombre_proveedor FROM kpi_cxp_diario"), conn)
            lista_provs = sorted(df_provs["nombre_proveedor"].dropna().unique().tolist())
    except Exception as e:
        st.sidebar.error(f"Error MySQL: {e}")
        st.warning("⚠️ No se pudo conectar a MySQL en vivo. Activando datos de prueba.")
        datos = generar_datos_prueba()
        df_sucursales = datos["sucursales"]
        df_catalogo_prod = datos["productos"]
        lista_provs = sorted(datos["compras"]["nombre_proveedor"].unique().tolist())
        modo_datos = "Simulación (Datos de Prueba)"

# 1. Selector de Sucursal
opciones_sucursales = {"Todas las sucursales": None}
for _, row in df_sucursales.iterrows():
    cod_txt = f"[{row['codigo_sucursal']}] " if "codigo_sucursal" in row and pd.notna(row['codigo_sucursal']) else ""
    ciudad_txt = f" - {row['ciudad']}" if pd.notna(row['ciudad']) else ""
    opciones_sucursales[f"{cod_txt}{row['nombre']}{ciudad_txt}"] = int(row['id_sucursal'])

sucursal_label = st.sidebar.selectbox("Sucursal:", options=list(opciones_sucursales.keys()))
id_sucursal = opciones_sucursales[sucursal_label]

# 2. Selector de Fechas
hoy = datetime.now().date()
hace_30_dias = hoy - timedelta(days=30)
rango_fecha = st.sidebar.date_input("Rango de Fechas:", value=(hace_30_dias, hoy), max_value=hoy)

if isinstance(rango_fecha, (tuple, list)) and len(rango_fecha) == 2:
    f_ini, f_fin = rango_fecha
elif isinstance(rango_fecha, (tuple, list)) and len(rango_fecha) == 1:
    f_ini = f_fin = rango_fecha[0]
else:
    f_ini, f_fin = hace_30_dias, hoy

st.sidebar.divider()
st.sidebar.subheader("🎯 Filtros Específicos")

# 3. Filtro por Laboratorio (Afecta Ventas, Inventario y Compras de esa marca)
labs_disponibles = sorted([lab for lab in df_catalogo_prod["laboratorio"].dropna().unique().tolist() if str(lab).strip()])
lab_seleccionado = st.sidebar.selectbox("Laboratorio (Marca / Fabricante):", options=["Todos"] + labs_disponibles)

# 4. Filtro por Proveedor (Afecta Compras realizadas y CxP/Deudas)
prov_seleccionado = st.sidebar.selectbox("Proveedor (Droguería / Distribuidor):", options=["Todos"] + lista_provs)

# --- Pestañas ---
tab_ventas, tab_compras, tab_inventario, tab_vendedores, tab_finanzas = st.tabs([
    "📊 Ventas & Rendimiento",
    "📥 Compras & Proveedores",
    "📦 Inventario & Quiebres",
    "👨‍💼 Equipo de Ventas",
    "💰 Tesorería & Finanzas"
])

# =========================================================================
# FILTRADO DE DATOS (SIMULACIÓN / MYSQL)
# =========================================================================
filtro_lab_activo = (lab_seleccionado != "Todos")
filtro_prov_activo = (prov_seleccionado != "Todos")

if modo_datos == "Simulación (Datos de Prueba)":
    # 1. Ventas por Producto
    df_v_prod = datos["ventas_producto"].merge(datos["productos"], on="id_producto")
    df_v_prod = df_v_prod[(df_v_prod["fecha"] >= f_ini) & (df_v_prod["fecha"] <= f_fin)]
    if id_sucursal:
        df_v_prod = df_v_prod[df_v_prod["id_sucursal"] == id_sucursal]
    if filtro_lab_activo:
        df_v_prod = df_v_prod[df_v_prod["laboratorio"] == lab_seleccionado]

    # 2. Ventas Diarias Globales
    if filtro_lab_activo:
        df_v_dia = df_v_prod.groupby(["fecha"]).agg(
            total_facturado=("total_venta_monto", "sum"),
            cantidad_tickets=("unidades_vendidas", "count")
        ).reset_index()
    else:
        df_v_dia = datos["ventas_diarias"]
        df_v_dia = df_v_dia[(df_v_dia["fecha"] >= f_ini) & (df_v_dia["fecha"] <= f_fin)]
        if id_sucursal:
            df_v_dia = df_v_dia[df_v_dia["id_sucursal"] == id_sucursal]

    # 3. Compras por Producto y Proveedor (Permite filtrar tanto por lab como por proveedor)
    df_comp = datos["compras"].merge(datos["productos"], on="id_producto")
    df_comp = df_comp[(df_comp["fecha"] >= f_ini) & (df_comp["fecha"] <= f_fin)]
    if id_sucursal:
        df_comp = df_comp[df_comp["id_sucursal"] == id_sucursal]
    if filtro_lab_activo:
        df_comp = df_comp[df_comp["laboratorio"] == lab_seleccionado]
    if filtro_prov_activo:
        df_comp = df_comp[df_comp["nombre_proveedor"] == prov_seleccionado]

    # 4. Inventario
    df_inv = datos["inventario"].merge(datos["productos"], on="id_producto").merge(datos["sucursales"], on="id_sucursal")
    if id_sucursal:
        df_inv = df_inv[df_inv["id_sucursal"] == id_sucursal]
    if filtro_lab_activo:
        df_inv = df_inv[df_inv["laboratorio"] == lab_seleccionado]

    # 5. Vendedores
    df_vend = datos["vendedores"][(datos["vendedores"]["fecha"] >= f_ini) & (datos["vendedores"]["fecha"] <= f_fin)]
    if id_sucursal:
        df_vend = df_vend[df_vend["id_sucursal"] == id_sucursal]

    # 6. Formas de Pago
    df_pagos = datos["formas_pago"][(datos["formas_pago"]["fecha"] >= f_ini) & (datos["formas_pago"]["fecha"] <= f_fin)]
    if id_sucursal:
        df_pagos = df_pagos[df_pagos["id_sucursal"] == id_sucursal]

    # 7. Bancos
    df_bancos = datos["bancos"]
    if id_sucursal:
        df_bancos = df_bancos[df_bancos["id_sucursal"] == id_sucursal]

    df_cajas = datos["cajas"]
    if id_sucursal:
        df_cajas = df_cajas[df_cajas["id_sucursal"] == id_sucursal]

    # 8. CxC y CxP
    df_cxc = datos["cxc"]
    if id_sucursal:
        df_cxc = df_cxc[df_cxc["id_sucursal"] == id_sucursal]

    df_cxp = datos["cxp"]
    if id_sucursal:
        df_cxp = df_cxp[df_cxp["id_sucursal"] == id_sucursal]
    if filtro_prov_activo:
        df_cxp = df_cxp[df_cxp["nombre_proveedor"] == prov_seleccionado]

# =========================================================================
# TAB 1: VENTAS & RENDIMIENTO (Segmentable por Laboratorio)
# =========================================================================
with tab_ventas:
    if filtro_lab_activo:
        st.info(f"🔎 Filtrando ventas del Laboratorio: **{lab_seleccionado}**")

    st.subheader("Resumen Comercial de Ventas")

    tot_facturado = df_v_prod["total_venta_monto"].sum() if filtro_lab_activo else (df_v_dia["total_facturado"].sum() if not df_v_dia.empty else 0)
    tot_unidades = df_v_prod["unidades_vendidas"].sum() if not df_v_prod.empty else 0
    tot_tickets = df_v_dia["cantidad_tickets"].sum() if not df_v_dia.empty else 0
    ticket_prom = (tot_facturado / tot_tickets) if tot_tickets > 0 else 0

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Ventas Totales ($)", f"${tot_facturado:,.2f}")
    c2.metric("Unidades Vendidas", f"{int(tot_unidades):,}")
    c3.metric("Tickets / Clientes", f"{int(tot_tickets):,}")
    c4.metric("Ticket Promedio", f"${ticket_prom:,.2f}")

    st.divider()

    st.markdown("#### 📈 Evolución Diaria de Ventas")
    if not df_v_prod.empty:
        df_dia_agg = df_v_prod.groupby("fecha").agg(
            monto_vendido=("total_venta_monto", "sum"),
            unidades=("unidades_vendidas", "sum")
        ).reset_index()
        fig_evol = px.line(
            df_dia_agg, 
            x="fecha", 
            y="monto_vendido",
            labels={"monto_vendido": "Monto Vendido ($)", "fecha": "Fecha"},
            title="Evolución de Ingresos por Venta",
            markers=True
        )
        st.plotly_chart(fig_evol, use_container_width=True)
    else:
        st.warning("No hay registros de ventas para esta selección.")

    col_prod, col_lab = st.columns(2)
    with col_prod:
        st.markdown("#### 🏆 Top Productos Más Vendidos")
        if not df_v_prod.empty:
            df_top_p = df_v_prod.groupby("nombre_producto")["total_venta_monto"].sum().reset_index()
            df_top_p = df_top_p.sort_values("total_venta_monto", ascending=False).head(10)
            fig_p = px.bar(
                df_top_p, 
                x="total_venta_monto", 
                y="nombre_producto", 
                orientation="h",
                labels={"total_venta_monto": "Monto ($)", "nombre_producto": "Producto"},
                color="total_venta_monto",
                color_continuous_scale="Teal"
            )
            fig_p.update_layout(yaxis={'categoryorder':'total ascending'})
            st.plotly_chart(fig_p, use_container_width=True)
        else:
            st.info("Sin registros de productos.")

    with col_lab:
        st.markdown("#### 🧪 Participación de Laboratorios")
        if not df_v_prod.empty:
            df_lab_agg = df_v_prod.groupby("laboratorio")["total_venta_monto"].sum().reset_index()
            fig_l = px.pie(df_lab_agg, names="laboratorio", values="total_venta_monto", hole=0.4)
            st.plotly_chart(fig_l, use_container_width=True)
        else:
            st.info("Sin registros de laboratorio.")

# =========================================================================
# TAB 2: COMPRAS & PROVEEDORES (Filtros cruzados Lab + Proveedor)
# =========================================================================
with tab_compras:
    msg_comp = []
    if filtro_prov_activo:
        msg_comp.append(f"Proveedor: **{prov_seleccionado}**")
    if filtro_lab_activo:
        msg_comp.append(f"Laboratorio: **{lab_seleccionado}**")
    if msg_comp:
        st.info(f"🔎 Compras filtradas por: {' | '.join(msg_comp)}")

    st.subheader("Gestión de Compras y Abastecimiento de Mercancía")

    tot_comp_monto = df_comp["total_compra_monto"].sum() if not df_comp.empty else 0
    tot_comp_uds = df_comp["unidades_compradas"].sum() if not df_comp.empty else 0
    cant_proveedores_activos = df_comp["nombre_proveedor"].nunique() if not df_comp.empty else 0

    col_cmp1, col_cmp2, col_cmp3 = st.columns(3)
    col_cmp1.metric("Inversión Total en Compras", f"${tot_comp_monto:,.2f}")
    col_cmp2.metric("Unidades Compradas", f"{int(tot_comp_uds):,}")
    col_cmp3.metric("Proveedores Involucrados", f"{cant_proveedores_activos}")

    st.divider()

    col_c_izq, col_c_der = st.columns(2)
    with col_c_izq:
        st.markdown("#### 📅 Inversión en Compras por Fecha")
        if not df_comp.empty:
            df_c_fecha = df_comp.groupby("fecha")["total_compra_monto"].sum().reset_index()
            fig_cf = px.bar(
                df_c_fecha,
                x="fecha",
                y="total_compra_monto",
                labels={"total_compra_monto": "Inversión ($)", "fecha": "Fecha"},
                color_discrete_sequence=["#e67e22"]
            )
            st.plotly_chart(fig_cf, use_container_width=True)
        else:
            st.info("Sin compras registradas para estos filtros.")

    with col_c_der:
        st.markdown("#### 🚚 Distribución de Compras por Proveedor")
        if not df_comp.empty:
            df_c_prov = df_comp.groupby("nombre_proveedor")["total_compra_monto"].sum().reset_index()
            fig_cp = px.pie(
                df_c_prov,
                names="nombre_proveedor",
                values="total_compra_monto",
                hole=0.4,
                title="Participación de Proveedores"
            )
            st.plotly_chart(fig_cp, use_container_width=True)
        else:
            st.info("Sin datos de proveedores.")

    st.markdown("#### 📋 Detalle de Artículos Comprados")
    if not df_comp.empty:
        df_detalle_comp = df_comp.groupby(["nombre_proveedor", "laboratorio", "nombre_producto"]).agg(
            unidades=("unidades_compradas", "sum"),
            inversion_total=("total_compra_monto", "sum")
        ).reset_index().sort_values("inversion_total", ascending=False)

        st.dataframe(
            df_detalle_comp,
            use_container_width=True,
            column_config={
                "nombre_proveedor": "Proveedor / Distribuidor",
                "laboratorio": "Laboratorio",
                "nombre_producto": "Producto",
                "unidades": st.column_config.NumberColumn("Unidades Adquiridas", format="%d"),
                "inversion_total": st.column_config.NumberColumn("Inversión Total ($)", format="$%.2f")
            }
        )

# =========================================================================
# TAB 3: INVENTARIO & VALORIZACIÓN
# =========================================================================
with tab_inventario:
    st.subheader("Valorización de Inventario y Alertas de Stock")

    # Métricas Globales de Inventario
    tot_unidades_stock = df_inv["stock_actual"].sum() if not df_inv.empty else 0
    tot_valor_inventario = df_inv["valor_total_inventario"].sum() if not df_inv.empty else 0

    df_quiebres = df_inv[df_inv["stock_actual"] <= df_inv["stock_minimo"]].copy()
    df_quiebres["faltante"] = df_quiebres["stock_minimo"] - df_quiebres["stock_actual"]
    df_quiebres = df_quiebres.sort_values("faltante", ascending=False)

    col_inv1, col_inv2, col_inv3, col_inv4 = st.columns(4)
    col_inv1.metric("💰 Inventario Valorizado Total", f"${tot_valor_inventario:,.2f}")
    col_inv2.metric("📦 Unidades Físicas en Stock", f"{int(tot_unidades_stock):,}")
    col_inv3.metric("🚨 Artículos en Quiebre / Mínimo", f"{len(df_quiebres):,}")
    col_inv4.metric("❌ Artículos Agotados (Stock 0)", f"{len(df_quiebres[df_quiebres['stock_actual'] == 0]):,}")

    st.divider()

    # Fila 1: Valorización por Laboratorio
    col_v_lab, col_v_top = st.columns([1, 1])

    with col_v_lab:
        st.markdown("#### 🧪 Valorización por Laboratorio / Fabricante")
        if not df_inv.empty:
            df_lab_val = df_inv.groupby("laboratorio").agg(
                stock_uds=("stock_actual", "sum"),
                monto_valorizado=("valor_total_inventario", "sum")
            ).reset_index().sort_values("monto_valorizado", ascending=False)

            fig_vlab = px.bar(
                df_lab_val,
                x="monto_valorizado",
                y="laboratorio",
                orientation="h",
                labels={"monto_valorizado": "Capital Invertido ($)", "laboratorio": "Laboratorio"},
                color="monto_valorizado",
                color_continuous_scale="Blues"
            )
            fig_vlab.update_layout(yaxis={'categoryorder':'total ascending'})
            st.plotly_chart(fig_vlab, use_container_width=True)
        else:
            st.info("Sin registros de inventario.")

    with col_v_top:
        st.markdown("#### 🏆 Top Artículos con Mayor Capital Invertido")
        if not df_inv.empty:
            df_top_val = df_inv.groupby(["nombre_producto", "laboratorio"]).agg(
                stock_uds=("stock_actual", "sum"),
                costo_promedio=("costo_unitario", "mean"),
                monto_valorizado=("valor_total_inventario", "sum")
            ).reset_index().sort_values("monto_valorizado", ascending=False).head(10)

            fig_top_art = px.bar(
                df_top_val,
                x="monto_valorizado",
                y="nombre_producto",
                orientation="h",
                labels={"monto_valorizado": "Monto Total ($)", "nombre_producto": "Producto"},
                color="monto_valorizado",
                color_continuous_scale="Teal"
            )
            fig_top_art.update_layout(yaxis={'categoryorder':'total ascending'})
            st.plotly_chart(fig_top_art, use_container_width=True)
        else:
            st.info("Sin datos de artículos.")

    st.divider()

    # Tabla Detallada de Inventario Valorizado por Artículo
    st.markdown("#### 📋 Detalle de Inventario Valorizado por Artículo")
    if not df_inv.empty:
        df_inv_articulo = df_inv.groupby(["codigo_barras", "nombre_producto", "laboratorio"]).agg(
            stock_actual=("stock_actual", "sum"),
            costo_unitario=("costo_unitario", "mean"),
            monto_valorizado=("valor_total_inventario", "sum")
        ).reset_index().sort_values("monto_valorizado", ascending=False)

        st.dataframe(
            df_inv_articulo,
            use_container_width=True,
            column_config={
                "codigo_barras": "Código Barras",
                "nombre_producto": "Producto",
                "laboratorio": "Laboratorio",
                "stock_actual": st.column_config.NumberColumn("Stock Disponible", format="%d"),
                "costo_unitario": st.column_config.NumberColumn("Costo Unit. Prom.", format="$%.2f"),
                "monto_valorizado": st.column_config.NumberColumn("Total Valorizado ($)", format="$%.2f")
            }
        )

    st.divider()

    st.markdown("#### ⚠️ Reposición Inmediata: Productos Bajo Stock Mínimo")
    if not df_quiebres.empty:
        vista_inv = df_quiebres[["nombre", "codigo_barras", "nombre_producto", "laboratorio", "stock_actual", "stock_minimo", "costo_unitario", "valor_total_inventario", "faltante"]]
        st.dataframe(
            vista_inv.rename(columns={"nombre": "Sucursal"}),
            use_container_width=True,
            column_config={
                "stock_actual": st.column_config.NumberColumn("Stock Actual", format="%d"),
                "stock_minimo": st.column_config.NumberColumn("Stock Mínimo", format="%d"),
                "costo_unitario": st.column_config.NumberColumn("Costo Unit.", format="$%.2f"),
                "valor_total_inventario": st.column_config.NumberColumn("Valor Actual ($)", format="$%.2f"),
                "faltante": st.column_config.NumberColumn("Faltante Sugerido", format="%d")
            }
        )
    else:
        st.success("✅ Todo el inventario está por encima del stock mínimo.")

# =========================================================================
# TAB 4: EQUIPO DE VENTAS
# =========================================================================
with tab_vendedores:
    st.subheader("Desempeño y Productividad por Asesor")

    if not df_vend.empty:
        df_v_agg = df_vend.groupby("nombre_vendedor").agg({
            "total_vendido": "sum",
            "cantidad_operaciones": "sum"
        }).reset_index()
        df_v_agg["ticket_promedio"] = round(df_v_agg["total_vendido"] / df_v_agg["cantidad_operaciones"], 2)
        df_v_agg = df_v_agg.sort_values("total_vendido", ascending=False)

        col_v1, col_v2 = st.columns([3, 2])
        with col_v1:
            fig_v = px.bar(
                df_v_agg,
                x="total_vendido",
                y="nombre_vendedor",
                orientation="h",
                labels={"total_vendido": "Total Vendido ($)", "nombre_vendedor": "Asesor"},
                title="Ranking de Vendedores por Monto",
                color="total_vendido",
                color_continuous_scale="Purples"
            )
            fig_v.update_layout(yaxis={'categoryorder':'total ascending'})
            st.plotly_chart(fig_v, use_container_width=True)

        with col_v2:
            st.markdown("#### Desglose de Productividad")
            st.dataframe(
                df_v_agg,
                use_container_width=True,
                column_config={
                    "total_vendido": st.column_config.NumberColumn("Total Vendido", format="$%.2f"),
                    "cantidad_operaciones": st.column_config.NumberColumn("Operaciones", format="%d"),
                    "ticket_promedio": st.column_config.NumberColumn("Ticket Promedio", format="$%.2f")
                }
            )
    else:
        st.info("Sin datos de vendedores en este período.")

# =========================================================================
# TAB 5: TESORERÍA & FINANZAS
# =========================================================================
with tab_finanzas:
    st.subheader("Gestión Financiera, Tesorería, Cajas y Bancos")

    # Fila Superior: Liquidez Disponible (Cajas de Efectivo + Cuentas Bancarias)
    tot_bancos = df_bancos["saldo_disponible"].sum() if not df_bancos.empty else 0
    tot_cajas_usd = df_cajas[df_cajas["moneda"] == "USD"]["saldo_efectivo"].sum() if not df_cajas.empty else 0
    tot_cajas_ves = df_cajas[df_cajas["moneda"] == "VES"]["saldo_efectivo"].sum() if not df_cajas.empty else 0

    col_t1, col_t2, col_t3, col_t4 = st.columns(4)
    col_t1.metric("🏦 Disponibilidad en Bancos", f"${tot_bancos:,.2f}")
    col_t2.metric("💵 Efectivo en Cajas (USD)", f"${tot_cajas_usd:,.2f}")
    col_t3.metric("🇻🇪 Efectivo en Cajas (VES)", f"Bs. {tot_cajas_ves:,.2f}")
    col_t4.metric("💰 Liquidez Total Estimada (USD)", f"${(tot_bancos + tot_cajas_usd):,.2f}")

    st.divider()

    # Fila 2: Detalle de Cajas de Efectivo y Cuentas Bancarias
    col_cajas_v, col_bancos_v = st.columns(2)

    with col_cajas_v:
        st.markdown("#### 💵 Cajas de Efectivo por Tipo y Moneda")
        if not df_cajas.empty:
            df_cajas_agg = df_cajas.groupby(["tipo_caja", "moneda"])["saldo_efectivo"].sum().reset_index()
            st.dataframe(
                df_cajas_agg,
                use_container_width=True,
                column_config={
                    "tipo_caja": "Tipo de Caja",
                    "moneda": "Moneda",
                    "saldo_efectivo": st.column_config.NumberColumn("Saldo Físico en Caja", format="%.2f")
                }
            )
        else:
            st.info("Sin registros de cajas de efectivo.")

    with col_bancos_v:
        st.markdown("#### 🏦 Cuentas Bancarias")
        if not df_bancos.empty:
            df_b_agg = df_bancos.groupby(["nombre_banco", "numero_cuenta_oculto"])["saldo_disponible"].sum().reset_index()
            st.dataframe(
                df_b_agg,
                use_container_width=True,
                column_config={
                    "nombre_banco": "Banco",
                    "numero_cuenta_oculto": "Cuenta (Últimos 4)",
                    "saldo_disponible": st.column_config.NumberColumn("Saldo Disponible ($)", format="$%.2f")
                }
            )
        else:
            st.info("Sin cuentas bancarias registradas.")

    st.divider()

    # Fila 3: Canales de Cobro (Formas de Pago)
    st.markdown("#### 💳 Participación por Canal de Cobro")
    if not df_pagos.empty:
        df_p_agg = df_pagos.groupby("forma_pago")["total_ingresado"].sum().reset_index()
        fig_p = px.pie(df_p_agg, names="forma_pago", values="total_ingresado", hole=0.45, title="Distribución de Métodos de Pago")
        st.plotly_chart(fig_p, use_container_width=True)
    else:
        st.info("Sin registros de formas de pago.")

    st.divider()

    col_cxc, col_cxp = st.columns(2)
    with col_cxc:
        st.markdown("#### 📑 Cuentas por Cobrar por Cliente (CxC)")
        if not df_cxc.empty:
            df_cxc_agg = df_cxc.groupby(["nombre_cliente", "identificacion_cliente", "tipo_cliente"])["saldo_pendiente"].sum().reset_index()
            tot_cxc_monto = df_cxc_agg['saldo_pendiente'].sum()
            st.metric("Cartera Total por Cobrar", f"${tot_cxc_monto:,.2f}")
            st.dataframe(
                df_cxc_agg.sort_values("saldo_pendiente", ascending=False),
                use_container_width=True,
                column_config={
                    "nombre_cliente": "Cliente / Razón Social",
                    "identificacion_cliente": "Identificación (CI/RIF)",
                    "tipo_cliente": "Tipo",
                    "saldo_pendiente": st.column_config.NumberColumn("Saldo Pendiente", format="$%.2f")
                }
            )
        else:
            st.info("Sin cuentas por cobrar pendientes.")

    with col_cxp:
        st.markdown("#### 🚚 Cuentas por Pagar (CxP Proveedores)")
        if not df_cxp.empty:
            df_cxp_agg = df_cxp.groupby("nombre_proveedor")["saldo_por_pagar"].sum().reset_index()
            st.metric("Deuda Total a Proveedores", f"${df_cxp_agg['saldo_por_pagar'].sum():,.2f}")
            st.dataframe(
                df_cxp_agg.sort_values("saldo_por_pagar", ascending=False),
                use_container_width=True,
                column_config={
                    "nombre_proveedor": "Proveedor / Distribuidor",
                    "saldo_por_pagar": st.column_config.NumberColumn("Saldo por Pagar", format="$%.2f")
                }
            )
        else:
            st.info("Sin deudas pendientes registradas.")
