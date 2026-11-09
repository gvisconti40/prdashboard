import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sqlalchemy import create_engine, text
from datetime import datetime, timedelta
import random
import os

# --- Configuración de Marca y Empresa ---
NOMBRE_EMPRESA = "GRUPO SAN ANSELMO"
SLOGAN_EMPRESA = "Red de Farmacias - Cuadro de Mando Integral y Control Operativo"
ICONO_PAGINA   = "💊"

# Rutas de logotipos (puedes colocar tu archivo logo.png en la carpeta assets/)
RUTA_ASSETS   = os.path.join(os.path.dirname(__file__), "assets")
RUTA_LOGO     = os.path.join(RUTA_ASSETS, "logo.png")

# --- Configuración visual de la aplicación ---
st.set_page_config(
    page_title=f"KPIs - {NOMBRE_EMPRESA}",
    page_icon=ICONO_PAGINA,
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Conexión a MySQL en vivo ---
@st.cache_resource
def get_db_engine():
    if "mysql" in st.secrets:
        cfg = st.secrets["mysql"]
        url = f"mysql+pymysql://{cfg['user']}:{cfg['password']}@{cfg['host']}:{cfg['port']}/{cfg['database']}"
        return create_engine(url, pool_recycle=3600)
    return None

# --- Generador de Datos Mock de Simulación Normalizado ---
@st.cache_data
def generar_datos_prueba():
    hoy = datetime.now().date()
    
    # 1. Maestro Sucursales (con Zona y Código de 4 chars)
    sucursales = [
        {"id_sucursal": 1, "codigo_sucursal": "F001", "nombre": "Farmacia Central", "ciudad": "Caracas", "zona": "Gran Caracas"},
        {"id_sucursal": 2, "codigo_sucursal": "F002", "nombre": "Farmacia Las Mercedes", "ciudad": "Caracas", "zona": "Gran Caracas"},
        {"id_sucursal": 3, "codigo_sucursal": "F003", "nombre": "Farmacia Bella Vista", "ciudad": "Maracaibo", "zona": "Occidente"},
        {"id_sucursal": 4, "codigo_sucursal": "F004", "nombre": "Farmacia Los Sauces", "ciudad": "Valencia", "zona": "Centro"},
        {"id_sucursal": 5, "codigo_sucursal": "F005", "nombre": "Farmacia El Parral", "ciudad": "Valencia", "zona": "Centro"}
    ]
    df_suc = pd.DataFrame(sucursales)

    # 2. Maestro Líneas (Código de 6 chars)
    lineas = [
        {"id_linea": 1, "codigo_linea": "LIN001", "descripcion_linea": "Cardiovascular"},
        {"id_linea": 2, "codigo_linea": "LIN002", "descripcion_linea": "Antibióticos y Antivirales"},
        {"id_linea": 3, "codigo_linea": "LIN003", "descripcion_linea": "Analgésicos y Antiinflamatorios"},
        {"id_linea": 4, "codigo_linea": "LIN004", "descripcion_linea": "Gastrointestinales"},
        {"id_linea": 5, "codigo_linea": "LIN005", "descripcion_linea": "Vitaminas y Suplementos"},
        {"id_linea": 6, "codigo_linea": "LIN006", "descripcion_linea": "Antihistamínicos y Respiratorios"},
        {"id_linea": 7, "codigo_linea": "LIN007", "descripcion_linea": "Endocrinología y Diabetes"}
    ]
    df_lineas = pd.DataFrame(lineas)

    # 3. Maestro Laboratorios (Código de 6 chars)
    laboratorios = [
        {"id_laboratorio": 1, "codigo_laboratorio": "LAB001", "nombre_laboratorio": "Pfizer"},
        {"id_laboratorio": 2, "codigo_laboratorio": "LAB002", "nombre_laboratorio": "Bayer"},
        {"id_laboratorio": 3, "codigo_laboratorio": "LAB003", "nombre_laboratorio": "Calox"},
        {"id_laboratorio": 4, "codigo_laboratorio": "LAB004", "nombre_laboratorio": "Leti"},
        {"id_laboratorio": 5, "codigo_laboratorio": "LAB005", "nombre_laboratorio": "Genven"},
        {"id_laboratorio": 6, "codigo_laboratorio": "LAB006", "nombre_laboratorio": "Merck"},
        {"id_laboratorio": 7, "codigo_laboratorio": "LAB007", "nombre_laboratorio": "Novartis"},
        {"id_laboratorio": 8, "codigo_laboratorio": "LAB008", "nombre_laboratorio": "Sanofi"}
    ]
    df_labs = pd.DataFrame(laboratorios)

    # 4. Maestro Proveedores (Código de 10 chars)
    proveedores = [
        {"id_proveedor": 1, "codigo_proveedor": "PRV0000001", "nombre_proveedor": "Droguería Cobeca", "rif_proveedor": "J-00012345-1"},
        {"id_proveedor": 2, "codigo_proveedor": "PRV0000002", "nombre_proveedor": "Droguería Nena", "rif_proveedor": "J-00045678-2"},
        {"id_proveedor": 3, "codigo_proveedor": "PRV0000003", "nombre_proveedor": "Drolanca", "rif_proveedor": "J-00089123-3"},
        {"id_proveedor": 4, "codigo_proveedor": "PRV0000004", "nombre_proveedor": "Grupo Farvenca", "rif_proveedor": "J-00078945-4"},
        {"id_proveedor": 5, "codigo_proveedor": "PRV0000005", "nombre_proveedor": "Droguería Vitalis", "rif_proveedor": "J-00032165-5"}
    ]
    df_provs = pd.DataFrame(proveedores)

    # 5. Maestro Clientes (Código de 10 chars)
    clientes = [
        {"id_cliente": 1, "codigo_cliente": "CLI0000001", "nombre_cliente": "Roberto Méndez", "tipo_cliente": "Particular", "identificacion": "V-14.238.901"},
        {"id_cliente": 2, "codigo_cliente": "CLI0000002", "nombre_cliente": "Elena Salazar", "tipo_cliente": "Particular", "identificacion": "V-18.765.432"},
        {"id_cliente": 3, "codigo_cliente": "CLI0000003", "nombre_cliente": "Seguros Caracas", "tipo_cliente": "Seguro / Empresa", "identificacion": "J-30491823-1"},
        {"id_cliente": 4, "codigo_cliente": "CLI0000004", "nombre_cliente": "Mercantil Seguros", "tipo_cliente": "Seguro / Empresa", "identificacion": "J-00012345-0"},
        {"id_cliente": 5, "codigo_cliente": "CLI0000005", "nombre_cliente": "Empresas Polar (Convenio)", "tipo_cliente": "Convenio", "identificacion": "J-00045678-9"},
        {"id_cliente": 6, "codigo_cliente": "CLI0000006", "nombre_cliente": "Banesco Seguros", "tipo_cliente": "Seguro / Empresa", "identificacion": "J-29837192-3"}
    ]
    df_clientes = pd.DataFrame(clientes)

    # 6. Maestro Productos (con codigo_articulo de 30 chars, codigo_barras >= 15 chars, id_linea, id_laboratorio)
    productos = [
        (1, "ART-CARDIO-00001", "759100100000015", "Atorvastatina 20mg x 30 Tab", 1, 1),
        (2, "ART-CARDIO-00002", "759100200000025", "Losartán Potásico 50mg x 30 Comp", 1, 3),
        (3, "ART-ANTI-000001",  "759100300000035", "Amoxicilina + Ác. Clavulánico 875mg", 2, 5),
        (4, "ART-ANALG-00001",  "759100400000045", "Ibuprofeno 400mg x 20 Cáps", 3, 2),
        (5, "ART-ANALG-00002",  "759100500000055", "Paracetamol 500mg x 20 Tab", 3, 3),
        (6, "ART-GASTRO-0001",  "759100600000065", "Omeprazol 20mg x 28 Cáps", 4, 4),
        (7, "ART-VITAM-00001",  "759100700000075", "Vitamina C 1000mg Efervescente", 5, 2),
        (8, "ART-ENDOC-00001",  "759100800000085", "Metformina 850mg x 30 Tab", 7, 6),
        (9, "ART-RESP-000001",  "759100900000095", "Loratadina 10mg x 10 Tab", 6, 4),
        (10, "ART-RESP-000002", "759101000000105", "Cetirizina 10mg x 10 Tab", 6, 5),
        (11, "ART-ANALG-00003", "759101100000115", "Diclofenac Sódico 50mg x 20 Tab", 3, 7),
        (12, "ART-CARDIO-00003", "759101200000125", "Enalapril 20mg x 30 Tab", 1, 3),
        (13, "ART-ANTI-000002",  "759101300000135", "Azitromicina 500mg x 3 Tab", 2, 1),
        (14, "ART-VITAM-00002",  "759101400000145", "Complejo B Forte x 30 Grageas", 5, 2),
        (15, "ART-ANTI-000003",  "759101500000155", "Ciprofloxacina 500mg x 10 Tab", 2, 5),
        (16, "ART-GASTRO-0002",  "759101600000165", "Pantoprazol 40mg x 14 Tab", 4, 6),
        (17, "ART-ENDOC-00002",  "759101700000175", "Levotiroxina 100mcg x 50 Tab", 7, 6),
        (18, "ART-RESP-000003",  "759101800000185", "Salbutamol Inhalador 100mcg", 6, 8),
        (19, "ART-CARDIO-00004", "759101900000195", "Clopidogrel 75mg x 28 Tab", 1, 8),
        (20, "ART-ANALG-00004",  "759102000000205", "Ketoprofeno 100mg x 24 Cáps", 3, 4),
        (21, "ART-RESP-000004",  "759102100000215", "Desloratadina 5mg x 10 Tab", 6, 1),
        (22, "ART-VITAM-00003",  "759102200000225", "Ácido Fólico 5mg x 30 Tab", 5, 3),
        (23, "ART-ANTI-000004",  "759102300000235", "Fluconazol 150mg x 2 Cáps", 2, 1),
        (24, "ART-ENDOC-00003",  "759102400000245", "Glimepirida 4mg x 30 Tab", 7, 8),
        (25, "ART-VITAM-00004",  "759102500000255", "Calcio + Vitamina D3 x 60 Tab", 5, 2)
    ]
    df_prod = pd.DataFrame(productos, columns=["id_producto", "codigo_articulo", "codigo_barras", "nombre_producto", "id_linea", "id_laboratorio"])
    df_prod = df_prod.merge(df_lineas[["id_linea", "codigo_linea", "descripcion_linea"]], on="id_linea")
    df_prod = df_prod.merge(df_labs[["id_laboratorio", "codigo_laboratorio", "nombre_laboratorio"]], on="id_laboratorio")

    fechas = [hoy - timedelta(days=i) for i in range(30, -1, -1)]

    # 7. Ventas Diarias Globales por Farmacia (Contado vs Crédito y Operaciones)
    filas_vta = []
    for suc in sucursales:
        for f in fechas:
            ops = random.randint(45, 160)
            fact = round(ops * random.uniform(18.5, 38.0), 2)
            pct_cred = random.uniform(0.15, 0.35) # Entre 15% y 35% en crédito
            v_cred = round(fact * pct_cred, 2)
            v_cont = round(fact - v_cred, 2)
            
            # Reparto de operaciones contado y crédito
            ops_cred = max(1, int(round(ops * random.uniform(0.12, 0.28))))
            ops_cont = ops - ops_cred
            
            filas_vta.append({
                "id_sucursal": suc["id_sucursal"],
                "fecha": f,
                "total_facturado": fact,
                "ventas_contado": v_cont,
                "ventas_credito": v_cred,
                "numero_operaciones": ops,
                "operaciones_contado": ops_cont,
                "operaciones_credito": ops_cred
            })
    df_vta_dia = pd.DataFrame(filas_vta)

    # 8. Ventas por Producto
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

    # 9. Inventario (con costo unitario y precio unitario de venta)
    costos_base = {1: 8.50, 2: 4.20, 3: 12.00, 4: 3.80, 5: 2.10, 6: 5.60, 7: 6.90, 8: 4.50, 9: 2.80, 10: 3.10}
    precios_base = {1: 15.00, 2: 8.00, 3: 25.00, 4: 8.00, 5: 5.00, 6: 12.00, 7: 15.00, 8: 10.00, 9: 6.00, 10: 7.50}
    filas_inv = []
    for suc in sucursales:
        for _, p in df_prod.iterrows():
            min_stk = random.randint(15, 40)
            act_stk = random.choice([0, random.randint(1, min_stk - 1), random.randint(min_stk, 120)])
            c_unit = costos_base.get(p["id_producto"], round(random.uniform(2.5, 11.0), 2))
            p_unit = precios_base.get(p["id_producto"], round(c_unit * random.uniform(1.35, 1.70), 2))
            filas_inv.append({
                "id_sucursal": suc["id_sucursal"],
                "id_producto": p["id_producto"],
                "stock_actual": act_stk,
                "stock_minimo": min_stk,
                "costo_unitario": c_unit,
                "precio_unitario": p_unit,
                "valor_total_inventario": round(act_stk * c_unit, 2),
                "valor_venta_inventario": round(act_stk * p_unit, 2)
            })
    df_inv = pd.DataFrame(filas_inv)

    # 10. Compras (enlace a id_proveedor)
    filas_comp = []
    for suc in sucursales:
        for f in fechas[::2]:
            for _, p in df_prod.sample(6).iterrows():
                prv = random.choice(proveedores)
                uds_c = random.randint(20, 90)
                costo = round(uds_c * random.uniform(2.5, 12.0), 2)
                filas_comp.append({
                    "id_sucursal": suc["id_sucursal"],
                    "fecha": f,
                    "id_producto": p["id_producto"],
                    "id_proveedor": prv["id_proveedor"],
                    "unidades_compradas": uds_c,
                    "total_compra_monto": costo
                })
    df_compras = pd.DataFrame(filas_comp)

    # 11. Vendedores
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

    # 12. Formas de Pago
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

    # 13. Bancos y Cajas
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

    # 14. CxC (enlazadas a maestro_clientes) y CxP (enlazadas a maestro_proveedores)
    filas_cxc = []
    for suc in sucursales:
        for cl in clientes:
            filas_cxc.append({
                "id_sucursal": suc["id_sucursal"],
                "fecha": hoy,
                "id_cliente": cl["id_cliente"],
                "saldo_pendiente": round(random.uniform(250.0, 5200.0), 2)
            })
    df_cxc = pd.DataFrame(filas_cxc)

    filas_cxp = []
    for suc in sucursales:
        for pr in proveedores:
            filas_cxp.append({
                "id_sucursal": suc["id_sucursal"],
                "fecha": hoy,
                "id_proveedor": pr["id_proveedor"],
                "saldo_por_pagar": round(random.uniform(2200.0, 14500.0), 2)
            })
    df_cxp = pd.DataFrame(filas_cxp)

    return {
        "sucursales": df_suc,
        "lineas": df_lineas,
        "laboratorios": df_labs,
        "proveedores": df_provs,
        "clientes": df_clientes,
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

# --- Encabezado Principal y Marca ---
if os.path.exists(RUTA_LOGO):
    # Si existe el logo en assets/logo.png, muestra logo + título alineados
    col_logo, col_titulo = st.columns([1, 6])
    with col_logo:
        st.image(RUTA_LOGO, use_container_width=True)
    with col_titulo:
        st.title(NOMBRE_EMPRESA)
        st.caption(SLOGAN_EMPRESA)
else:
    # Si aún no has pegado el logo, muestra el título con su icono institucional
    st.title(f"{ICONO_PAGINA} {NOMBRE_EMPRESA}")
    st.caption(SLOGAN_EMPRESA)

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
    df_lineas_cat = datos["lineas"]
    df_labs_cat = datos["laboratorios"]
    df_provs_cat = datos["proveedores"]
    df_clientes_cat = datos["clientes"]
    df_catalogo_prod = datos["productos"]
else:
    try:
        engine = get_db_engine()
        with engine.connect() as conn:
            df_sucursales = pd.read_sql(text("SELECT id_sucursal, codigo_sucursal, nombre, ciudad, zona FROM sucursales ORDER BY nombre"), conn)
            df_lineas_cat = pd.read_sql(text("SELECT id_linea, codigo_linea, descripcion_linea FROM maestro_lineas ORDER BY descripcion_linea"), conn)
            df_labs_cat = pd.read_sql(text("SELECT id_laboratorio, codigo_laboratorio, nombre_laboratorio FROM maestro_laboratorios ORDER BY nombre_laboratorio"), conn)
            df_provs_cat = pd.read_sql(text("SELECT id_proveedor, codigo_proveedor, nombre_proveedor, rif_proveedor FROM maestro_proveedores ORDER BY nombre_proveedor"), conn)
            df_clientes_cat = pd.read_sql(text("SELECT id_cliente, codigo_cliente, nombre_cliente, tipo_cliente, identificacion FROM maestro_clientes ORDER BY nombre_cliente"), conn)
            sql_p = """
                SELECT p.id_producto, p.codigo_articulo, p.codigo_barras, p.nombre_producto, 
                       l.codigo_linea, l.descripcion_linea, lb.codigo_laboratorio, lb.nombre_laboratorio
                FROM maestro_productos p
                JOIN maestro_lineas l ON p.id_linea = l.id_linea
                JOIN maestro_laboratorios lb ON p.id_laboratorio = lb.id_laboratorio
            """
            df_catalogo_prod = pd.read_sql(text(sql_p), conn)
    except Exception as e:
        st.sidebar.error(f"Error MySQL: {e}")
        st.warning("⚠️ No se pudo conectar a MySQL en vivo. Activando datos de prueba.")
        datos = generar_datos_prueba()
        df_sucursales = datos["sucursales"]
        df_lineas_cat = datos["lineas"]
        df_labs_cat = datos["laboratorios"]
        df_provs_cat = datos["proveedores"]
        df_clientes_cat = datos["clientes"]
        df_catalogo_prod = datos["productos"]
        modo_datos = "Simulación (Datos de Prueba)"

# 1. Filtro por Zona Geográfica
zonas_disponibles = sorted([z for z in df_sucursales["zona"].dropna().unique().tolist() if str(z).strip()]) if "zona" in df_sucursales else []
zona_seleccionada = st.sidebar.selectbox("Zona Geográfica:", options=["Todas las zonas"] + zonas_disponibles)

# Filtrar sucursales según zona
df_sucursales_filtradas = df_sucursales.copy()
if zona_seleccionada != "Todas las zonas":
    df_sucursales_filtradas = df_sucursales_filtradas[df_sucursales_filtradas["zona"] == zona_seleccionada]

# 2. Selector de Sucursal
opciones_sucursales = {"Todas las sucursales de la zona" if zona_seleccionada != "Todas las zonas" else "Todas las sucursales": None}
for _, row in df_sucursales_filtradas.iterrows():
    cod_txt = f"[{row['codigo_sucursal']}] " if "codigo_sucursal" in row and pd.notna(row['codigo_sucursal']) else ""
    ciudad_txt = f" - {row['ciudad']}" if pd.notna(row['ciudad']) else ""
    zona_txt = f" ({row['zona']})" if pd.notna(row.get('zona')) and zona_seleccionada == "Todas las zonas" else ""
    opciones_sucursales[f"{cod_txt}{row['nombre']}{ciudad_txt}{zona_txt}"] = int(row['id_sucursal'])

sucursal_label = st.sidebar.selectbox("Sucursal:", options=list(opciones_sucursales.keys()))
id_sucursal = opciones_sucursales[sucursal_label]
ids_sucursales_zona = df_sucursales_filtradas["id_sucursal"].tolist()

# 3. Selector de Fechas
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
st.sidebar.subheader("🎯 Filtros Maestros")

# 4. Filtro por Línea de Producto (Categoría)
lineas_opciones = {"Todas las líneas": None}
for _, row in df_lineas_cat.iterrows():
    lineas_opciones[f"[{row['codigo_linea']}] {row['descripcion_linea']}"] = int(row['id_linea'])
linea_label = st.sidebar.selectbox("Línea de Producto:", options=list(lineas_opciones.keys()))
id_linea_sel = lineas_opciones[linea_label]

# 5. Filtro por Laboratorio (Fabricante / Marca)
labs_opciones = {"Todos los laboratorios": None}
for _, row in df_labs_cat.iterrows():
    labs_opciones[f"[{row['codigo_laboratorio']}] {row['nombre_laboratorio']}"] = int(row['id_laboratorio'])
lab_label = st.sidebar.selectbox("Laboratorio (Marca):", options=list(labs_opciones.keys()))
id_lab_sel = labs_opciones[lab_label]

# 6. Filtro por Proveedor / Droguería
provs_opciones = {"Todos los proveedores": None}
for _, row in df_provs_cat.iterrows():
    provs_opciones[f"[{row['codigo_proveedor']}] {row['nombre_proveedor']}"] = int(row['id_proveedor'])
prov_label = st.sidebar.selectbox("Proveedor / Droguería:", options=list(provs_opciones.keys()))
id_prov_sel = provs_opciones[prov_label]

# 7. Filtro por Cliente (Para CxC)
clientes_opciones = {"Todos los clientes": None}
for _, row in df_clientes_cat.iterrows():
    tipo_t = f" ({row['tipo_cliente']})" if pd.notna(row.get('tipo_cliente')) else ""
    clientes_opciones[f"[{row['codigo_cliente']}] {row['nombre_cliente']}{tipo_t}"] = int(row['id_cliente'])
cliente_label = st.sidebar.selectbox("Cliente (CxC):", options=list(clientes_opciones.keys()))
id_cliente_sel = clientes_opciones[cliente_label]

# --- Pestañas ---
tab_ventas, tab_compras, tab_inventario, tab_vendedores, tab_finanzas = st.tabs([
    "📊 Ventas & Rendimiento",
    "📥 Compras & Proveedores",
    "📦 Inventario & Valorización",
    "👨‍💼 Equipo de Ventas",
    "💰 Tesorería & Finanzas"
])

# =========================================================================
# FILTRADO DE DATOS (SIMULACIÓN / MYSQL)
# =========================================================================
filtro_linea_activo = (id_linea_sel is not None)
filtro_lab_activo = (id_lab_sel is not None)
filtro_prov_activo = (id_prov_sel is not None)
filtro_cliente_activo = (id_cliente_sel is not None)

if modo_datos == "Simulación (Datos de Prueba)":
    # 1. Ventas por Producto
    df_v_prod = datos["ventas_producto"].merge(datos["productos"], on="id_producto")
    df_v_prod = df_v_prod[(df_v_prod["fecha"] >= f_ini) & (df_v_prod["fecha"] <= f_fin)]
    if id_sucursal:
        df_v_prod = df_v_prod[df_v_prod["id_sucursal"] == id_sucursal]
    else:
        df_v_prod = df_v_prod[df_v_prod["id_sucursal"].isin(ids_sucursales_zona)]
    if filtro_linea_activo:
        df_v_prod = df_v_prod[df_v_prod["id_linea"] == id_linea_sel]
    if filtro_lab_activo:
        df_v_prod = df_v_prod[df_v_prod["id_laboratorio"] == id_lab_sel]

    # 2. Ventas Diarias Globales
    if filtro_linea_activo or filtro_lab_activo:
        df_v_dia = df_v_prod.groupby(["fecha"]).agg(
            total_facturado=("total_venta_monto", "sum"),
            numero_operaciones=("unidades_vendidas", "count")
        ).reset_index()
        df_v_dia["ventas_contado"] = df_v_dia["total_facturado"] * 0.75
        df_v_dia["ventas_credito"] = df_v_dia["total_facturado"] * 0.25
    else:
        df_v_dia = datos["ventas_diarias"]
        df_v_dia = df_v_dia[(df_v_dia["fecha"] >= f_ini) & (df_v_dia["fecha"] <= f_fin)]
        if id_sucursal:
            df_v_dia = df_v_dia[df_v_dia["id_sucursal"] == id_sucursal]
        else:
            df_v_dia = df_v_dia[df_v_dia["id_sucursal"].isin(ids_sucursales_zona)]

    # 3. Compras por Producto y Proveedor
    df_comp = datos["compras"].merge(datos["productos"], on="id_producto").merge(datos["proveedores"], on="id_proveedor")
    df_comp = df_comp[(df_comp["fecha"] >= f_ini) & (df_comp["fecha"] <= f_fin)]
    if id_sucursal:
        df_comp = df_comp[df_comp["id_sucursal"] == id_sucursal]
    else:
        df_comp = df_comp[df_comp["id_sucursal"].isin(ids_sucursales_zona)]
    if filtro_linea_activo:
        df_comp = df_comp[df_comp["id_linea"] == id_linea_sel]
    if filtro_lab_activo:
        df_comp = df_comp[df_comp["id_laboratorio"] == id_lab_sel]
    if filtro_prov_activo:
        df_comp = df_comp[df_comp["id_proveedor"] == id_prov_sel]

    # 4. Inventario
    df_inv = datos["inventario"].merge(datos["productos"], on="id_producto").merge(datos["sucursales"], on="id_sucursal")
    if id_sucursal:
        df_inv = df_inv[df_inv["id_sucursal"] == id_sucursal]
    else:
        df_inv = df_inv[df_inv["id_sucursal"].isin(ids_sucursales_zona)]
    if filtro_linea_activo:
        df_inv = df_inv[df_inv["id_linea"] == id_linea_sel]
    if filtro_lab_activo:
        df_inv = df_inv[df_inv["id_laboratorio"] == id_lab_sel]

    # 5. Vendedores
    df_vend = datos["vendedores"][(datos["vendedores"]["fecha"] >= f_ini) & (datos["vendedores"]["fecha"] <= f_fin)]
    if id_sucursal:
        df_vend = df_vend[df_vend["id_sucursal"] == id_sucursal]
    else:
        df_vend = df_vend[df_vend["id_sucursal"].isin(ids_sucursales_zona)]

    # 6. Formas de Pago
    df_pagos = datos["formas_pago"][(datos["formas_pago"]["fecha"] >= f_ini) & (datos["formas_pago"]["fecha"] <= f_fin)]
    if id_sucursal:
        df_pagos = df_pagos[df_pagos["id_sucursal"] == id_sucursal]
    else:
        df_pagos = df_pagos[df_pagos["id_sucursal"].isin(ids_sucursales_zona)]

    # 7. Bancos y Cajas
    df_bancos = datos["bancos"]
    if id_sucursal:
        df_bancos = df_bancos[df_bancos["id_sucursal"] == id_sucursal]
    else:
        df_bancos = df_bancos[df_bancos["id_sucursal"].isin(ids_sucursales_zona)]

    df_cajas = datos["cajas"]
    if id_sucursal:
        df_cajas = df_cajas[df_cajas["id_sucursal"] == id_sucursal]
    else:
        df_cajas = df_cajas[df_cajas["id_sucursal"].isin(ids_sucursales_zona)]

    # 8. CxC y CxP
    df_cxc = datos["cxc"].merge(datos["clientes"], on="id_cliente")
    if id_sucursal:
        df_cxc = df_cxc[df_cxc["id_sucursal"] == id_sucursal]
    else:
        df_cxc = df_cxc[df_cxc["id_sucursal"].isin(ids_sucursales_zona)]
    if filtro_cliente_activo:
        df_cxc = df_cxc[df_cxc["id_cliente"] == id_cliente_sel]

    df_cxp = datos["cxp"].merge(datos["proveedores"], on="id_proveedor")
    if id_sucursal:
        df_cxp = df_cxp[df_cxp["id_sucursal"] == id_sucursal]
    else:
        df_cxp = df_cxp[df_cxp["id_sucursal"].isin(ids_sucursales_zona)]
    if filtro_prov_activo:
        df_cxp = df_cxp[df_cxp["id_proveedor"] == id_prov_sel]

# =========================================================================
# TAB 1: VENTAS & RENDIMIENTO
# =========================================================================
with tab_ventas:
    filtro_msg = []
    if filtro_linea_activo:
        filtro_msg.append(f"Línea: **{linea_label}**")
    if filtro_lab_activo:
        filtro_msg.append(f"Laboratorio: **{lab_label}**")
    if filtro_msg:
        st.info(f"🔎 Filtrando ventas por: {' | '.join(filtro_msg)}")

    st.subheader("Resumen Comercial de Ventas")

    tot_facturado = df_v_prod["total_venta_monto"].sum() if (filtro_linea_activo or filtro_lab_activo) else (df_v_dia["total_facturado"].sum() if not df_v_dia.empty else 0)
    tot_contado = df_v_dia["ventas_contado"].sum() if "ventas_contado" in df_v_dia and not df_v_dia.empty else 0
    tot_credito = df_v_dia["ventas_credito"].sum() if "ventas_credito" in df_v_dia and not df_v_dia.empty else 0
    pct_contado = (tot_contado / tot_facturado * 100) if tot_facturado > 0 else 0
    pct_credito = (tot_credito / tot_facturado * 100) if tot_facturado > 0 else 0

    tot_unidades = df_v_prod["unidades_vendidas"].sum() if not df_v_prod.empty else 0
    tot_operaciones = df_v_dia["numero_operaciones"].sum() if not df_v_dia.empty else 0
    tot_ops_contado = df_v_dia["operaciones_contado"].sum() if "operaciones_contado" in df_v_dia and not df_v_dia.empty else 0
    tot_ops_credito = df_v_dia["operaciones_credito"].sum() if "operaciones_credito" in df_v_dia and not df_v_dia.empty else 0
    ticket_prom = (tot_facturado / tot_operaciones) if tot_operaciones > 0 else 0

    col_v1, col_v2, col_v3, col_v4, col_v5, col_v6 = st.columns(6)
    col_v1.metric("Ventas Totales ($)", f"${tot_facturado:,.2f}")
    col_v2.metric("💵 Ventas Contado", f"${tot_contado:,.2f}", f"{pct_contado:.1f}% ({int(tot_ops_contado):,} ops)")
    col_v3.metric("📑 Ventas Crédito", f"${tot_credito:,.2f}", f"{pct_credito:.1f}% ({int(tot_ops_credito):,} ops)")
    col_v4.metric("Nº Operaciones (Tickets)", f"{int(tot_operaciones):,}")
    col_v5.metric("Ticket Promedio", f"${ticket_prom:,.2f}")
    col_v6.metric("Unidades Vendidas", f"{int(tot_unidades):,}")

    st.divider()

    # Evolución Diaria de Ventas (Desglosando Contado y Crédito)
    st.markdown("#### 📈 Evolución Diaria de Ventas: Contado vs Crédito")
    if not df_v_dia.empty:
        # Asegurar columnas si vienen de MySQL antiguo
        if "operaciones_contado" not in df_v_dia:
            df_v_dia["operaciones_contado"] = 0
        if "operaciones_credito" not in df_v_dia:
            df_v_dia["operaciones_credito"] = 0

        df_dia_agg = df_v_dia.groupby("fecha").agg(
            ventas_contado=("ventas_contado", "sum"),
            ventas_credito=("ventas_credito", "sum"),
            total_facturado=("total_facturado", "sum"),
            numero_operaciones=("numero_operaciones", "sum"),
            operaciones_contado=("operaciones_contado", "sum"),
            operaciones_credito=("operaciones_credito", "sum")
        ).reset_index().sort_values("fecha")

        custom_info = list(zip(
            df_dia_agg["total_facturado"],
            df_dia_agg["numero_operaciones"],
            df_dia_agg["ventas_contado"],
            df_dia_agg["operaciones_contado"],
            df_dia_agg["ventas_credito"],
            df_dia_agg["operaciones_credito"]
        ))

        fig_evol = go.Figure()

        # Barra Contado
        fig_evol.add_trace(go.Bar(
            x=df_dia_agg["fecha"],
            y=df_dia_agg["ventas_contado"],
            name="💵 Venta Contado",
            marker_color="#2ecc71",
            customdata=custom_info,
            hovertemplate="💵 <b>Contado:</b> $%{y:,.2f} (%{customdata[3]:,} ops)<extra></extra>"
        ))

        # Barra Crédito
        fig_evol.add_trace(go.Bar(
            x=df_dia_agg["fecha"],
            y=df_dia_agg["ventas_credito"],
            name="📑 Venta Crédito",
            marker_color="#3498db",
            customdata=custom_info,
            hovertemplate="📑 <b>Crédito:</b> $%{y:,.2f} (%{customdata[5]:,} ops)<extra></extra>"
        ))

        # Punto invisible para totalizar el día en el hover unificado
        fig_evol.add_trace(go.Scatter(
            x=df_dia_agg["fecha"],
            y=df_dia_agg["total_facturado"],
            name="Total Facturado",
            mode="markers",
            marker=dict(size=0, opacity=0),
            customdata=custom_info,
            hovertemplate="📊 <b>Total Facturado Día:</b> $%{y:,.2f} (%{customdata[1]:,} ops)<extra></extra>"
        ))

        fig_evol.update_layout(
            title="Facturación Diaria por Modalidad de Cobro",
            barmode="stack",
            hovermode="x unified",
            xaxis_title="Fecha",
            yaxis_title="Monto Facturado ($)",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig_evol, use_container_width=True)
    else:
        st.warning("No hay registros de ventas para esta selección.")

    col_prod, col_lab = st.columns([3, 2])
    with col_prod:
        col_t_top, col_c_crit = st.columns([2, 1])
        with col_t_top:
            st.markdown("#### 🏆 Top 20 Productos Más Vendidos")
        with col_c_crit:
            criterio_orden = st.selectbox(
                "Ordenar Top 20 por:",
                options=["Total Facturado ($)", "Unidades Vendidas"],
                index=0,
                key="criterio_top20_ventas"
            )

        if not df_v_prod.empty:
            df_top_p = df_v_prod.groupby(["codigo_articulo", "nombre_producto"]).agg(
                total_venta_monto=("total_venta_monto", "sum"),
                unidades=("unidades_vendidas", "sum")
            ).reset_index()

            if criterio_orden == "Total Facturado ($)":
                df_top_p = df_top_p.sort_values("total_venta_monto", ascending=False).head(20)
                eje_x = "total_venta_monto"
                etiqueta_x = "Venta Total ($)"
                paleta_color = "Teal"
            else:
                df_top_p = df_top_p.sort_values("unidades", ascending=False).head(20)
                eje_x = "unidades"
                etiqueta_x = "Unidades Vendidas"
                paleta_color = "Blues"

            fig_p = px.bar(
                df_top_p, 
                x=eje_x, 
                y="nombre_producto", 
                orientation="h",
                labels={eje_x: etiqueta_x, "nombre_producto": "Producto"},
                color=eje_x,
                color_continuous_scale=paleta_color,
                custom_data=["codigo_articulo", "unidades", "total_venta_monto"],
                height=650
            )
            fig_p.update_traces(
                hovertemplate="<b>Producto:</b> %{y}<br>" +
                              "<b>Cód. Artículo:</b> %{customdata[0]}<br>" +
                              "<b>Total Facturado:</b> $%{customdata[2]:,.2f}<br>" +
                              "<b>Unidades Vendidas:</b> %{customdata[1]:,}<extra></extra>"
            )
            fig_p.update_layout(yaxis={'categoryorder':'total ascending'})
            st.plotly_chart(fig_p, use_container_width=True)
        else:
            st.info("Sin registros de productos.")

    with col_lab:
        st.markdown("#### 🧪 Participación de Laboratorios")
        if not df_v_prod.empty:
            df_lab_agg = df_v_prod.groupby("nombre_laboratorio").agg(
                total_venta_monto=("total_venta_monto", "sum"),
                unidades_vendidas=("unidades_vendidas", "sum")
            ).reset_index()
            fig_l = px.pie(
                df_lab_agg, 
                names="nombre_laboratorio", 
                values="total_venta_monto", 
                hole=0.4,
                custom_data=["unidades_vendidas"]
            )
            fig_l.update_traces(
                hovertemplate="<b>Laboratorio:</b> %{label}<br>" +
                              "<b>Venta Total:</b> $%{value:,.2f}<br>" +
                              "<b>Participación:</b> %{percent}<br>" +
                              "<b>Unidades Vendidas:</b> %{customdata[0]:,}<extra></extra>"
            )
            st.plotly_chart(fig_l, use_container_width=True)
        else:
            st.info("Sin registros de laboratorio.")

    st.divider()

    # Tabla Detallada de Todos los Artículos Vendidos
    st.markdown("#### 📋 Detalle Completo de Artículos Vendidos")
    if not df_v_prod.empty:
        df_detalle_art = df_v_prod.groupby(["codigo_articulo", "codigo_barras", "nombre_producto", "descripcion_linea", "nombre_laboratorio"]).agg(
            unidades_vendidas=("unidades_vendidas", "sum"),
            total_venta_monto=("total_venta_monto", "sum")
        ).reset_index()

        df_detalle_art["precio_promedio"] = round(df_detalle_art["total_venta_monto"] / df_detalle_art["unidades_vendidas"], 2)
        df_detalle_art = df_detalle_art.sort_values("total_venta_monto", ascending=False)

        st.dataframe(
            df_detalle_art,
            use_container_width=True,
            column_config={
                "codigo_articulo": "Cód. Artículo",
                "codigo_barras": "Código de Barras",
                "nombre_producto": "Descripción del Producto",
                "descripcion_linea": "Línea / Categoría",
                "nombre_laboratorio": "Laboratorio",
                "unidades_vendidas": st.column_config.NumberColumn("Unidades", format="%d"),
                "precio_promedio": st.column_config.NumberColumn("Precio Prom. ($)", format="$%.2f"),
                "total_venta_monto": st.column_config.NumberColumn("Total Facturado ($)", format="$%.2f")
            }
        )
    else:
        st.info("Sin registros de artículos vendidos para este período.")

# =========================================================================
# TAB 2: COMPRAS & PROVEEDORES
# =========================================================================
with tab_compras:
    msg_comp = []
    if filtro_prov_activo:
        msg_comp.append(f"Proveedor: **{prov_label}**")
    if filtro_lab_activo:
        msg_comp.append(f"Laboratorio: **{lab_label}**")
    if filtro_linea_activo:
        msg_comp.append(f"Línea: **{linea_label}**")
    if msg_comp:
        st.info(f"🔎 Compras filtradas por: {' | '.join(msg_comp)}")

    st.subheader("Gestión de Compras y Abastecimiento de Mercancía")

    tot_comp_monto = df_comp["total_compra_monto"].sum() if not df_comp.empty else 0
    tot_comp_uds = df_comp["unidades_compradas"].sum() if not df_comp.empty else 0
    cant_proveedores_activos = df_comp["id_proveedor"].nunique() if not df_comp.empty else 0

    col_cmp1, col_cmp2, col_cmp3 = st.columns(3)
    col_cmp1.metric("Inversión Total en Compras", f"${tot_comp_monto:,.2f}")
    col_cmp2.metric("Unidades Compradas", f"{int(tot_comp_uds):,}")
    col_cmp3.metric("Proveedores Involucrados", f"{cant_proveedores_activos}")

    st.divider()

    col_c_izq, col_c_der = st.columns(2)
    with col_c_izq:
        st.markdown("#### 📅 Inversión en Compras por Fecha")
        if not df_comp.empty:
            df_c_fecha = df_comp.groupby("fecha").agg(
                total_compra_monto=("total_compra_monto", "sum"),
                unidades_compradas=("unidades_compradas", "sum")
            ).reset_index()
            fig_cf = px.bar(
                df_c_fecha,
                x="fecha",
                y="total_compra_monto",
                labels={"total_compra_monto": "Inversión ($)", "fecha": "Fecha"},
                color_discrete_sequence=["#e67e22"],
                custom_data=["unidades_compradas"]
            )
            fig_cf.update_traces(
                hovertemplate="<b>Fecha:</b> %{x}<br>" +
                              "<b>Inversión:</b> $%{y:,.2f}<br>" +
                              "<b>Unidades Compradas:</b> %{customdata[0]:,}<extra></extra>"
            )
            st.plotly_chart(fig_cf, use_container_width=True)
        else:
            st.info("Sin compras registradas para estos filtros.")

    with col_c_der:
        col_t_prov, col_c_crit_prov = st.columns([2, 1])
        with col_t_prov:
            st.markdown("#### 🚚 Top 5 Droguerías")
        with col_c_crit_prov:
            criterio_orden_prov = st.selectbox(
                "Ordenar por:",
                options=["Inversión Total ($)", "Unidades Compradas"],
                index=0,
                key="criterio_prov_compras"
            )

        if not df_comp.empty:
            df_c_prov = df_comp.groupby(["codigo_proveedor", "nombre_proveedor"]).agg(
                total_compra_monto=("total_compra_monto", "sum"),
                unidades_compradas=("unidades_compradas", "sum")
            ).reset_index()

            if criterio_orden_prov == "Inversión Total ($)":
                df_top5_prov = df_c_prov.sort_values("total_compra_monto", ascending=False).head(5)
                eje_x_prov = "total_compra_monto"
                lbl_x_prov = "Inversión ($)"
                paleta_prov = "Oranges"
            else:
                df_top5_prov = df_c_prov.sort_values("unidades_compradas", ascending=False).head(5)
                eje_x_prov = "unidades_compradas"
                lbl_x_prov = "Unidades Compradas"
                paleta_prov = "YlOrBr"

            fig_cp = px.bar(
                df_top5_prov,
                x=eje_x_prov,
                y="nombre_proveedor",
                orientation="h",
                labels={eje_x_prov: lbl_x_prov, "nombre_proveedor": "Droguería"},
                color=eje_x_prov,
                color_continuous_scale=paleta_prov,
                custom_data=["codigo_proveedor", "unidades_compradas", "total_compra_monto"]
            )
            fig_cp.update_traces(
                hovertemplate="<b>Droguería:</b> %{y} [%{customdata[0]}]<br>" +
                              "<b>Inversión Total:</b> $%{customdata[2]:,.2f}<br>" +
                              "<b>Unidades Adquiridas:</b> %{customdata[1]:,}<extra></extra>"
            )
            fig_cp.update_layout(yaxis={'categoryorder':'total ascending'})
            st.plotly_chart(fig_cp, use_container_width=True)
        else:
            st.info("Sin datos de proveedores.")

    st.divider()

    # Compras por Laboratorio (con selector de ordenamiento)
    col_c_lab_bar, col_c_lab_pie = st.columns([3, 2])
    with col_c_lab_bar:
        col_t_lab_c, col_c_crit_lab = st.columns([2, 1])
        with col_t_lab_c:
            st.markdown("#### 🧪 Compras por Laboratorio")
        with col_c_crit_lab:
            criterio_orden_lab = st.selectbox(
                "Ordenar por:",
                options=["Inversión Total ($)", "Unidades Compradas"],
                index=0,
                key="criterio_lab_compras"
            )

        if not df_comp.empty:
            df_c_lab = df_comp.groupby("nombre_laboratorio").agg(
                total_compra_monto=("total_compra_monto", "sum"),
                unidades_compradas=("unidades_compradas", "sum")
            ).reset_index()

            if criterio_orden_lab == "Inversión Total ($)":
                df_c_lab_ordenado = df_c_lab.sort_values("total_compra_monto", ascending=False)
                eje_x_lab = "total_compra_monto"
                lbl_x_lab = "Inversión ($)"
                paleta_lab = "Viridis"
            else:
                df_c_lab_ordenado = df_c_lab.sort_values("unidades_compradas", ascending=False)
                eje_x_lab = "unidades_compradas"
                lbl_x_lab = "Unidades Compradas"
                paleta_lab = "Purples"

            fig_clab = px.bar(
                df_c_lab_ordenado,
                x=eje_x_lab,
                y="nombre_laboratorio",
                orientation="h",
                labels={eje_x_lab: lbl_x_lab, "nombre_laboratorio": "Laboratorio"},
                color=eje_x_lab,
                color_continuous_scale=paleta_lab,
                custom_data=["unidades_compradas", "total_compra_monto"]
            )
            fig_clab.update_traces(
                hovertemplate="<b>Laboratorio:</b> %{y}<br>" +
                              "<b>Inversión Total:</b> $%{customdata[1]:,.2f}<br>" +
                              "<b>Unidades Compradas:</b> %{customdata[0]:,}<extra></extra>"
            )
            fig_clab.update_layout(yaxis={'categoryorder':'total ascending'})
            st.plotly_chart(fig_clab, use_container_width=True)
        else:
            st.info("Sin compras por laboratorio.")

    with col_c_lab_pie:
        st.markdown("#### 🥧 Distribución de Compras por Laboratorio")
        if not df_comp.empty:
            fig_clab_pie = px.pie(
                df_c_lab,
                names="nombre_laboratorio",
                values="total_compra_monto",
                hole=0.4,
                custom_data=["unidades_compradas"]
            )
            fig_clab_pie.update_traces(
                hovertemplate="<b>Laboratorio:</b> %{label}<br>" +
                              "<b>Inversión:</b> $%{value:,.2f}<br>" +
                              "<b>Participación:</b> %{percent}<br>" +
                              "<b>Unidades Compradas:</b> %{customdata[0]:,}<extra></extra>"
            )
            st.plotly_chart(fig_clab_pie, use_container_width=True)
        else:
            st.info("Sin datos para distribución de laboratorios.")

    st.markdown("#### 📋 Detalle de Artículos Comprados")
    if not df_comp.empty:
        df_detalle_comp = df_comp.groupby(["codigo_proveedor", "nombre_proveedor", "descripcion_linea", "nombre_laboratorio", "codigo_articulo", "nombre_producto"]).agg(
            unidades=("unidades_compradas", "sum"),
            inversion_total=("total_compra_monto", "sum")
        ).reset_index().sort_values("inversion_total", ascending=False)

        st.dataframe(
            df_detalle_comp,
            use_container_width=True,
            column_config={
                "codigo_proveedor": "Cód. Prov.",
                "nombre_proveedor": "Proveedor / Droguería",
                "descripcion_linea": "Línea",
                "nombre_laboratorio": "Laboratorio",
                "codigo_articulo": "Cód. Artículo",
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

    tot_unidades_stock = df_inv["stock_actual"].sum() if not df_inv.empty else 0
    tot_valor_inventario = df_inv["valor_total_inventario"].sum() if not df_inv.empty else 0
    tot_valor_pvp = df_inv["valor_venta_inventario"].sum() if "valor_venta_inventario" in df_inv and not df_inv.empty else 0
    margen_potencial = ((tot_valor_pvp - tot_valor_inventario) / tot_valor_pvp * 100) if tot_valor_pvp > 0 else 0

    df_quiebres = df_inv[df_inv["stock_actual"] <= df_inv["stock_minimo"]].copy()
    df_quiebres["faltante"] = df_quiebres["stock_minimo"] - df_quiebres["stock_actual"]
    df_quiebres = df_quiebres.sort_values("faltante", ascending=False)

    col_inv1, col_inv2, col_inv3, col_inv4, col_inv5 = st.columns(5)
    col_inv1.metric("💰 Valor Costo Total", f"${tot_valor_inventario:,.2f}")
    col_inv2.metric("🏷️ Valor a Precio Venta (PVP)", f"${tot_valor_pvp:,.2f}")
    col_inv3.metric("📈 Margen Bruto Potencial", f"{margen_potencial:.1f}%")
    col_inv4.metric("📦 Unidades en Stock", f"{int(tot_unidades_stock):,}")
    col_inv5.metric("🚨 Quiebres de Stock", f"{len(df_quiebres):,}")

    st.divider()

    # Valorización por Laboratorio y por Línea
    col_v_lab, col_v_lin = st.columns(2)

    with col_v_lab:
        st.markdown("#### 🧪 Valorización por Laboratorio / Fabricante")
        if not df_inv.empty:
            df_lab_val = df_inv.groupby("nombre_laboratorio").agg(
                stock_uds=("stock_actual", "sum"),
                monto_valorizado=("valor_total_inventario", "sum")
            ).reset_index().sort_values("monto_valorizado", ascending=False)

            fig_vlab = px.bar(
                df_lab_val,
                x="monto_valorizado",
                y="nombre_laboratorio",
                orientation="h",
                labels={"monto_valorizado": "Capital Invertido ($)", "nombre_laboratorio": "Laboratorio"},
                color="monto_valorizado",
                color_continuous_scale="Blues"
            )
            fig_vlab.update_layout(yaxis={'categoryorder':'total ascending'})
            st.plotly_chart(fig_vlab, use_container_width=True)
        else:
            st.info("Sin registros de inventario.")

    with col_v_lin:
        st.markdown("#### 🏷️ Valorización por Línea de Producto")
        if not df_inv.empty:
            df_lin_val = df_inv.groupby("descripcion_linea").agg(
                stock_uds=("stock_actual", "sum"),
                monto_valorizado=("valor_total_inventario", "sum")
            ).reset_index().sort_values("monto_valorizado", ascending=False)

            fig_vlin = px.pie(
                df_lin_val,
                names="descripcion_linea",
                values="monto_valorizado",
                hole=0.4,
                title="Participación de Capital por Línea"
            )
            st.plotly_chart(fig_vlin, use_container_width=True)
        else:
            st.info("Sin registros de líneas.")

    st.divider()

    # Tabla Detallada de Inventario Valorizado por Artículo
    st.markdown("#### 📋 Detalle de Inventario Valorizado por Artículo")
    if not df_inv.empty:
        df_inv_articulo = df_inv.groupby(["codigo_articulo", "codigo_barras", "nombre_producto", "descripcion_linea", "nombre_laboratorio"]).agg(
            stock_actual=("stock_actual", "sum"),
            costo_unitario=("costo_unitario", "mean"),
            precio_unitario=("precio_unitario", "mean"),
            monto_valorizado=("valor_total_inventario", "sum"),
            monto_pvp=("valor_venta_inventario", "sum")
        ).reset_index().sort_values("monto_valorizado", ascending=False)

        st.dataframe(
            df_inv_articulo,
            use_container_width=True,
            column_config={
                "codigo_articulo": "Cód. Artículo",
                "codigo_barras": "Código Barras",
                "nombre_producto": "Producto",
                "descripcion_linea": "Línea",
                "nombre_laboratorio": "Laboratorio",
                "stock_actual": st.column_config.NumberColumn("Stock Disponible", format="%d"),
                "costo_unitario": st.column_config.NumberColumn("Costo Unit.", format="$%.2f"),
                "precio_unitario": st.column_config.NumberColumn("Precio Venta", format="$%.2f"),
                "monto_valorizado": st.column_config.NumberColumn("Valor Costo ($)", format="$%.2f"),
                "monto_pvp": st.column_config.NumberColumn("Valor PVP ($)", format="$%.2f")
            }
        )

    st.divider()

    # --- NUEVO MÓDULO: COMPARADOR DE PRECIOS Y STOCK ENTRE SUCURSALES ---
    st.markdown("#### 🔍 Comparador de Precios y Stock entre Sucursales")
    st.caption("Auditoría de dispersión de precios, costos, márgenes y disponibilidad física en toda la red de farmacias.")

    if not df_inv.empty:
        # Buscador predictivo optimizado para 40.000 artículos
        col_b_txt, col_b_sel = st.columns([1, 2])
        
        with col_b_txt:
            termino_busqueda = st.text_input(
                "🔎 Buscar por Nombre, Código o Barra:",
                value="",
                placeholder="Ej: Atorvastatina, Losartan, 7591001...",
                key="filtro_busqueda_art_comp",
                help="Escribe parte del nombre del medicamento o su código para filtrar el catálogo rápidamente."
            ).strip().lower()

        # Filtrar el universo de artículos según el término escrito
        df_art_unicos = df_inv[["codigo_articulo", "codigo_barras", "nombre_producto", "nombre_laboratorio"]].drop_duplicates()
        
        if termino_busqueda:
            mask_busqueda = (
                df_art_unicos["nombre_producto"].str.lower().str.contains(termino_busqueda, na=False) |
                df_art_unicos["codigo_articulo"].str.lower().str.contains(termino_busqueda, na=False) |
                df_art_unicos["codigo_barras"].str.lower().str.contains(termino_busqueda, na=False) |
                df_art_unicos["nombre_laboratorio"].str.lower().str.contains(termino_busqueda, na=False)
            )
            df_art_filtrados = df_art_unicos[mask_busqueda].sort_values("nombre_producto").head(50)
        else:
            # Mostrar los primeros 50 ordenados para que no colapse la interfaz si no ha escrito nada
            df_art_filtrados = df_art_unicos.sort_values("nombre_producto").head(50)

        with col_b_sel:
            if not df_art_filtrados.empty:
                dict_articulos = {
                    f"{row['nombre_producto']} [{row['codigo_articulo']}] - {row['nombre_laboratorio']}": row["codigo_articulo"] 
                    for _, row in df_art_filtrados.iterrows()
                }
                art_seleccionado_label = st.selectbox(
                    f"Seleccionar Artículo Coincidente ({len(df_art_filtrados)} encontrados):",
                    options=list(dict_articulos.keys()),
                    key="comparador_art_inv"
                )
                cod_art_comparar = dict_articulos[art_seleccionado_label]
            else:
                st.warning("No se encontraron artículos que coincidan con la búsqueda.")
                cod_art_comparar = None

        # Si hay un artículo seleccionado, procesar comparativa
        if cod_art_comparar:
            df_comp_art = df_inv[df_inv["codigo_articulo"] == cod_art_comparar].copy()

            if not df_comp_art.empty:
                p_min = df_comp_art["precio_unitario"].min()
                p_max = df_comp_art["precio_unitario"].max()
                p_avg = df_comp_art["precio_unitario"].mean()
                stock_red = df_comp_art["stock_actual"].sum()
                suc_con_quiebre = len(df_comp_art[df_comp_art["stock_actual"] <= df_comp_art["stock_minimo"]])

                col_cp1, col_cp2, col_cp3, col_cp4, col_cp5 = st.columns(5)
                col_cp1.metric("Precio Mínimo en Red", f"${p_min:,.2f}")
                col_cp2.metric("Precio Máximo en Red", f"${p_max:,.2f}")
                col_cp3.metric("Precio Promedio", f"${p_avg:,.2f}")
                col_cp4.metric("Stock Total en Red", f"{int(stock_red):,} uds")
                col_cp5.metric("Sucursales en Riesgo/Quiebre", f"{suc_con_quiebre} de {len(df_comp_art)}")

                # Gráfica de barras comparativa de Precios por Sucursal
                col_g_comp, col_t_comp = st.columns([3, 2])
                with col_g_comp:
                    fig_comp_p = px.bar(
                        df_comp_art.sort_values("precio_unitario", ascending=False),
                        x="precio_unitario",
                        y="nombre",
                        orientation="h",
                        labels={"precio_unitario": "Precio Venta ($)", "nombre": "Farmacia / Sucursal"},
                        title=f"Comparativa de PVP por Farmacia - {art_seleccionado_label}",
                        color="precio_unitario",
                        color_continuous_scale="Viridis",
                        custom_data=["costo_unitario", "stock_actual"]
                    )
                    fig_comp_p.update_traces(
                        hovertemplate="<b>Farmacia:</b> %{y}<br>" +
                                      "<b>Precio PVP:</b> $%{x:,.2f}<br>" +
                                      "<b>Costo Reposición:</b> $%{customdata[0]:,.2f}<br>" +
                                      "<b>Stock Disponible:</b> %{customdata[1]} uds<extra></extra>"
                    )
                    fig_comp_p.update_layout(yaxis={'categoryorder':'total ascending'})
                    st.plotly_chart(fig_comp_p, use_container_width=True)

                with col_t_comp:
                    st.markdown("##### Desglose por Farmacia")
                    tabla_comparativa = df_comp_art[["nombre", "zona", "costo_unitario", "precio_unitario", "stock_actual", "stock_minimo"]].copy()
                    tabla_comparativa["margen_pct"] = round((tabla_comparativa["precio_unitario"] - tabla_comparativa["costo_unitario"]) / tabla_comparativa["precio_unitario"] * 100, 1)
                    
                    st.dataframe(
                        tabla_comparativa.rename(columns={"nombre": "Sucursal", "zona": "Zona"}),
                        use_container_width=True,
                        column_config={
                            "costo_unitario": st.column_config.NumberColumn("Costo", format="$%.2f"),
                            "precio_unitario": st.column_config.NumberColumn("PVP", format="$%.2f"),
                            "margen_pct": st.column_config.NumberColumn("Margen %", format="%.1f%%"),
                            "stock_actual": st.column_config.NumberColumn("Stock", format="%d"),
                            "stock_minimo": st.column_config.NumberColumn("Mín.", format="%d")
                        }
                    )

    st.divider()

    st.markdown("#### ⚠️ Reposición Inmediata: Productos Bajo Stock Mínimo")
    if not df_quiebres.empty:
        vista_inv = df_quiebres[["nombre", "codigo_articulo", "codigo_barras", "nombre_producto", "descripcion_linea", "nombre_laboratorio", "stock_actual", "stock_minimo", "costo_unitario", "valor_total_inventario", "faltante"]]
        st.dataframe(
            vista_inv.rename(columns={"nombre": "Sucursal"}),
            use_container_width=True,
            column_config={
                "codigo_articulo": "Cód. Artículo",
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

    tot_bancos = df_bancos["saldo_disponible"].sum() if not df_bancos.empty else 0
    tot_cajas_usd = df_cajas[df_cajas["moneda"] == "USD"]["saldo_efectivo"].sum() if not df_cajas.empty else 0
    tot_cajas_ves = df_cajas[df_cajas["moneda"] == "VES"]["saldo_efectivo"].sum() if not df_cajas.empty else 0

    col_t1, col_t2, col_t3, col_t4 = st.columns(4)
    col_t1.metric("🏦 Disponibilidad en Bancos", f"${tot_bancos:,.2f}")
    col_t2.metric("💵 Efectivo en Cajas (USD)", f"${tot_cajas_usd:,.2f}")
    col_t3.metric("🇻🇪 Efectivo en Cajas (VES)", f"Bs. {tot_cajas_ves:,.2f}")
    col_t4.metric("💰 Liquidez Total Estimada (USD)", f"${(tot_bancos + tot_cajas_usd):,.2f}")

    st.divider()

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
            df_cxc_agg = df_cxc.groupby(["codigo_cliente", "nombre_cliente", "identificacion", "tipo_cliente"])["saldo_pendiente"].sum().reset_index()
            tot_cxc_monto = df_cxc_agg['saldo_pendiente'].sum()
            st.metric("Cartera Total por Cobrar", f"${tot_cxc_monto:,.2f}")
            st.dataframe(
                df_cxc_agg.sort_values("saldo_pendiente", ascending=False),
                use_container_width=True,
                column_config={
                    "codigo_cliente": "Cód. Cliente",
                    "nombre_cliente": "Cliente / Razón Social",
                    "identificacion": "Identificación (CI/RIF)",
                    "tipo_cliente": "Tipo",
                    "saldo_pendiente": st.column_config.NumberColumn("Saldo Pendiente", format="$%.2f")
                }
            )
        else:
            st.info("Sin cuentas por cobrar pendientes.")

    with col_cxp:
        st.markdown("#### 🚚 Cuentas por Pagar (CxP Proveedores)")
        if not df_cxp.empty:
            df_cxp_agg = df_cxp.groupby(["codigo_proveedor", "nombre_proveedor", "rif_proveedor"])["saldo_por_pagar"].sum().reset_index()
            st.metric("Deuda Total a Proveedores", f"${df_cxp_agg['saldo_por_pagar'].sum():,.2f}")
            st.dataframe(
                df_cxp_agg.sort_values("saldo_por_pagar", ascending=False),
                use_container_width=True,
                column_config={
                    "codigo_proveedor": "Cód. Prov.",
                    "nombre_proveedor": "Proveedor / Droguería",
                    "rif_proveedor": "RIF",
                    "saldo_por_pagar": st.column_config.NumberColumn("Saldo por Pagar", format="$%.2f")
                }
            )
        else:
            st.info("Sin deudas pendientes registradas.")
