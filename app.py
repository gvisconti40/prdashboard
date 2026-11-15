import streamlit as st
import streamlit.components.v1 as components
import json
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio

# --- Configuración de Plantilla Visual Global para Gráficos (Paleta Oficial de la Maqueta) ---
tema_farma = go.layout.Template()
tema_farma.layout.plot_bgcolor = "#5a6876"
tema_farma.layout.paper_bgcolor = "#475564"
tema_farma.layout.font = dict(color="#f1f5f9", family="Inter, sans-serif")
tema_farma.layout.xaxis = dict(gridcolor="rgba(255, 255, 255, 0.08)", linecolor="rgba(255, 255, 255, 0.15)")
tema_farma.layout.yaxis = dict(gridcolor="rgba(255, 255, 255, 0.08)", linecolor="rgba(255, 255, 255, 0.15)")
tema_farma.layout.hoverlabel = dict(
    bgcolor="rgba(15, 23, 42, 0.95)",
    bordercolor="#0d9488",
    font=dict(color="#ffffff", size=13, family="Inter, sans-serif")
)

pio.templates["farma_center_theme"] = tema_farma
pio.templates.default = "farma_center_theme"

def aplicar_estilo_farma(fig):
    if fig is None:
        return fig
    fig.update_layout(
        plot_bgcolor="#5a6876",
        paper_bgcolor="#475564",
        font=dict(color="#f1f5f9", family="Inter, sans-serif"),
        hoverlabel=dict(
            bgcolor="rgba(15, 23, 42, 0.95)",
            bordercolor="#0d9488",
            font=dict(color="#ffffff", size=13, family="Inter, sans-serif")
        )
    )
    fig.update_xaxes(gridcolor="rgba(255, 255, 255, 0.08)", linecolor="rgba(255, 255, 255, 0.15)")
    fig.update_yaxes(gridcolor="rgba(255, 255, 255, 0.08)", linecolor="rgba(255, 255, 255, 0.15)")
    return fig

from sqlalchemy import create_engine, text
from datetime import datetime, timedelta
import random
import os

# --- Configuración de Marca y Empresa ---
NOMBRE_EMPRESA = "GRUPO FARMA CENTER"
SLOGAN_EMPRESA = "Cuadro de Mando Integral y Control Operativo MIVO 7.1"
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

# --- Inyección de Estilos de Diseño Avanzados: Glassmorphism, Paleta Marina y Grilla ---
st.markdown("""
<style>
/* 1. Fondo base degradado azul-pizarra y marina intermedio (#101726 a #1A223B) */
.stApp {
    background: linear-gradient(135deg, #101726 0%, #151d30 50%, #1a223b 100%) !important;
    color: #e2e8f0;
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

/* 2. Ancho fijo optimizado de Sidebar (280px - 300px) */
[data-testid="stSidebar"] {
    background: rgba(16, 23, 38, 0.75) !important;
    backdrop-filter: blur(16px) !important;
    -webkit-backdrop-filter: blur(16px) !important;
    border-right: 1px solid rgba(255, 255, 255, 0.06) !important;
    min-width: 280px !important;
    max-width: 300px !important;
}

/* 3. Tarjetas KPI Blancas / Clean Glassmorphism idénticas a la maqueta */
.kpi-card-white {
    background: #ffffff !important;
    border-radius: 14px !important;
    padding: 16px 18px !important;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15), 0 1px 3px rgba(0, 0, 0, 0.1) !important;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    min-height: 110px;
    position: relative;
    overflow: hidden;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.kpi-card-white:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.2) !important;
}

.kpi-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 6px;
}

.kpi-title {
    font-size: 0.82rem;
    font-weight: 600;
    color: #475569;
    letter-spacing: 0.02em;
}

.kpi-icon-badge {
    width: 28px;
    height: 28px;
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.95rem;
}

.kpi-value {
    font-size: 1.65rem;
    font-weight: 800;
    color: #0f172a;
    line-height: 1.2;
}

.kpi-subtext {
    font-size: 0.74rem;
    font-weight: 600;
    margin-top: 4px;
    display: flex;
    align-items: center;
    gap: 4px;
}

.kpi-sparkline {
    position: absolute;
    bottom: 8px;
    right: 12px;
    opacity: 0.7;
}

/* 4. Paneles y Contenedores Glassmorphism Oscuros */
.panel-dark-glass {
    background: rgba(22, 31, 48, 0.7) !important;
    backdrop-filter: blur(14px) !important;
    -webkit-backdrop-filter: blur(14px) !important;
    border: 1px solid rgba(255, 255, 255, 0.07) !important;
    border-radius: 16px !important;
    padding: 18px 20px !important;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.25) !important;
    margin-bottom: 20px;
}

/* 5. Estilos de Pestañas y Navegación */
.stTabs [data-baseweb="tab-list"] {
    background: rgba(15, 23, 42, 0.4) !important;
    backdrop-filter: blur(10px) !important;
    border-radius: 12px !important;
    padding: 4px !important;
    gap: 8px !important;
    border: 1px solid rgba(255, 255, 255, 0.05) !important;
}

.stTabs [data-baseweb="tab"] {
    color: #94a3b8 !important;
    border-radius: 8px !important;
    padding: 8px 16px !important;
    font-weight: 500 !important;
    border: none !important;
    transition: all 0.2s ease !important;
}

.stTabs [aria-selected="true"] {
    background: rgba(16, 185, 129, 0.15) !important;
    color: #34d399 !important;
    border: 1px solid rgba(16, 185, 129, 0.3) !important;
}

/* 6. Tablas de Datos Estilizadas y Efecto Hover Teal */
[data-testid="stDataFrame"] {
    background: rgba(30, 41, 59, 0.35) !important;
    backdrop-filter: blur(12px) !important;
    border: 1px solid rgba(255, 255, 255, 0.06) !important;
    border-radius: 14px !important;
    overflow: hidden !important;
}

/* 7. Chips / Badges Personalizados */
.badge-lab {
    display: inline-block;
    padding: 3px 10px;
    border-radius: 9999px;
    font-size: 0.78rem;
    font-weight: 600;
    letter-spacing: 0.02em;
}
.badge-pfizer { background: rgba(59, 130, 246, 0.18); color: #60a5fa; border: 1px solid rgba(59, 130, 246, 0.3); }
.badge-novartis { background: rgba(139, 92, 246, 0.18); color: #a78bfa; border: 1px solid rgba(139, 92, 246, 0.3); }
.badge-leti { background: rgba(16, 185, 129, 0.18); color: #34d399; border: 1px solid rgba(16, 185, 129, 0.3); }
.badge-calox { background: rgba(249, 115, 22, 0.18); color: #fb923c; border: 1px solid rgba(249, 115, 22, 0.3); }
.badge-other { background: rgba(148, 163, 184, 0.15); color: #cbd5e1; border: 1px solid rgba(148, 163, 184, 0.25); }

/* Fila interactiva con resplandor teal */
.table-glass-row:hover {
    background: rgba(13, 148, 136, 0.15) !important;
    box-shadow: inset 0px 0px 8px rgba(13, 148, 136, 0.3) !important;
    cursor: pointer;
}

/* 8. ADAPTACIONES RESPONSIVAS EXCLUSIVAS PARA TELÉFONO / MÓVIL (< 768px) */
@media (max-width: 768px) {
    /* En móviles, transformar las 6 columnas en una cuadrícula flexible de 2 columnas */
    [data-testid="stHorizontalBlock"] {
        flex-wrap: wrap !important;
        gap: 12px !important;
    }
    
    [data-testid="column"] {
        flex: 1 1 calc(50% - 12px) !important;
        min-width: calc(50% - 12px) !important;
    }

    /* Calibrar el tamaño de la tarjeta KPI en pantallas estrechas */
    .kpi-card-white {
        padding: 12px 14px !important;
        min-height: 95px !important;
    }

    .kpi-value {
        font-size: 1.35rem !important;
    }

    .kpi-title {
        font-size: 0.74rem !important;
    }

    .kpi-sparkline {
        width: 50px !important;
        height: 18px !important;
        bottom: 6px !important;
        right: 8px !important;
    }

    /* Pestañas con desplazamiento táctil horizontal cómodo */
    .stTabs [data-baseweb="tab-list"] {
        overflow-x: auto !important;
        white-space: nowrap !important;
        padding-bottom: 6px !important;
    }

    /* Ajuste de márgenes en móviles */
    .panel-dark-glass {
        padding: 12px 14px !important;
        border-radius: 12px !important;
    }
}
</style>
""", unsafe_allow_html=True)

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
    
    # 1. Maestro Sucursales (con Zona y Código de 4 chars) - Grupo Farma Center / Farmacia La Corina
    sucursales = [
        {"id_sucursal": 1, "codigo_sucursal": "F001", "nombre": "Farmacia La Corina (Sede Principal)", "ciudad": "Puerto Cabello", "zona": "Carabobo"},
        {"id_sucursal": 2, "codigo_sucursal": "F002", "nombre": "Farmacia La corina 2", "ciudad": "Puerto Cabello", "zona": "Carabobo"},
        {"id_sucursal": 3, "codigo_sucursal": "F003", "nombre": "Farmacia Morillo", "ciudad": "Valencia", "zona": "Carabobo"},
        {"id_sucursal": 4, "codigo_sucursal": "F004", "nombre": "Farmacia farmavital", "ciudad": "Guacara", "zona": "Carabobo"},
        {"id_sucursal": 5, "codigo_sucursal": "F005", "nombre": "Farmacia Descuento a su salud", "ciudad": "San Diego", "zona": "Carabobo"}
    ]
    df_suc = pd.DataFrame(sucursales)

    # 2. Maestro Líneas Homologadas MIVO 7.1 (13 Líneas Maestras Oficiales)
    lineas = [
        {"id_linea": 1, "codigo_linea": "LIN001", "descripcion_linea": "01 Especialidades farmacéuticas"},
        {"id_linea": 2, "codigo_linea": "LIN002", "descripcion_linea": "02 Sueros y soluciones"},
        {"id_linea": 3, "codigo_linea": "LIN003", "descripcion_linea": "03 Productos naturales y bienestar"},
        {"id_linea": 4, "codigo_linea": "LIN004", "descripcion_linea": "04 Cuidado personal e higiene"},
        {"id_linea": 5, "codigo_linea": "LIN005", "descripcion_linea": "05 Dermocosmética y belleza"},
        {"id_linea": 6, "codigo_linea": "LIN006", "descripcion_linea": "06 Productos infantiles y maternidad"},
        {"id_linea": 7, "codigo_linea": "LIN007", "descripcion_linea": "07 Dispositivos médicos y rehabilitación"},
        {"id_linea": 8, "codigo_linea": "LIN008", "descripcion_linea": "08 Material médico y primeros auxilios"},
        {"id_linea": 9, "codigo_linea": "LIN009", "descripcion_linea": "09 Alimentos y bebidas"},
        {"id_linea": 10, "codigo_linea": "LIN010", "descripcion_linea": "10 Productos veterinarios"},
        {"id_linea": 11, "codigo_linea": "LIN011", "descripcion_linea": "11 Hogar y uso doméstico"},
        {"id_linea": 12, "codigo_linea": "LIN012", "descripcion_linea": "12 Accesorios y otros productos"},
        {"id_linea": 13, "codigo_linea": "LIN013", "descripcion_linea": "13 Servicios"}
    ]
    df_lineas = pd.DataFrame(lineas)

    # 3. Maestro Sublíneas Homologadas MIVO 7.1 (Catálogo Estándar Farma Center)
    sublineas = [
        # Línea 01: Especialidades Farmacéuticas
        {"id_sublinea": 1, "codigo_sublinea": "0101", "descripcion_sublinea": "Analgésicos y antipiréticos", "id_linea": 1},
        {"id_sublinea": 2, "codigo_sublinea": "0102", "descripcion_sublinea": "Antiinflamatorios", "id_linea": 1},
        {"id_sublinea": 3, "codigo_sublinea": "0103", "descripcion_sublinea": "Cardiovasculares", "id_linea": 1},
        {"id_sublinea": 4, "codigo_sublinea": "0104", "descripcion_sublinea": "Respiratorios", "id_linea": 1},
        {"id_sublinea": 5, "codigo_sublinea": "0105", "descripcion_sublinea": "Gastrointestinales", "id_linea": 1},
        {"id_sublinea": 6, "codigo_sublinea": "0106", "descripcion_sublinea": "Antialérgicos", "id_linea": 1},
        {"id_sublinea": 7, "codigo_sublinea": "0107", "descripcion_sublinea": "Dermatológicos", "id_linea": 1},
        {"id_sublinea": 8, "codigo_sublinea": "0108", "descripcion_sublinea": "Oftálmicos y óticos", "id_linea": 1},
        {"id_sublinea": 9, "codigo_sublinea": "0109", "descripcion_sublinea": "Preparados hormonales", "id_linea": 1},
        {"id_sublinea": 10, "codigo_sublinea": "0110", "descripcion_sublinea": "Antidiabéticos", "id_linea": 1},
        {"id_sublinea": 11, "codigo_sublinea": "0111", "descripcion_sublinea": "Vitaminas y minerales", "id_linea": 1},
        {"id_sublinea": 12, "codigo_sublinea": "0112", "descripcion_sublinea": "Sistema nervioso", "id_linea": 1},
        {"id_sublinea": 13, "codigo_sublinea": "0113", "descripcion_sublinea": "Antifúngicos", "id_linea": 1},
        {"id_sublinea": 14, "codigo_sublinea": "0114", "descripcion_sublinea": "Otros preparados farmacéuticos", "id_linea": 1},
        # Línea 02: Sueros y soluciones
        {"id_sublinea": 15, "codigo_sublinea": "0201", "descripcion_sublinea": "Soluciones fisiológicas", "id_linea": 2},
        {"id_sublinea": 16, "codigo_sublinea": "0202", "descripcion_sublinea": "Soluciones intravenosas", "id_linea": 2},
        {"id_sublinea": 17, "codigo_sublinea": "0203", "descripcion_sublinea": "Soluciones de rehidratación", "id_linea": 2},
        {"id_sublinea": 18, "codigo_sublinea": "0204", "descripcion_sublinea": "Otras soluciones", "id_linea": 2},
        # Línea 03: Productos naturales y bienestar
        {"id_sublinea": 19, "codigo_sublinea": "0301", "descripcion_sublinea": "Productos naturales", "id_linea": 3},
        {"id_sublinea": 20, "codigo_sublinea": "0302", "descripcion_sublinea": "Suplementos y complementos nutricionales", "id_linea": 3},
        {"id_sublinea": 21, "codigo_sublinea": "0303", "descripcion_sublinea": "Productos de bienestar", "id_linea": 3},
        # Línea 04: Cuidado personal e higiene
        {"id_sublinea": 22, "codigo_sublinea": "0401", "descripcion_sublinea": "Cuidado del cabello", "id_linea": 4},
        {"id_sublinea": 23, "codigo_sublinea": "0402", "descripcion_sublinea": "Higiene bucal", "id_linea": 4},
        {"id_sublinea": 24, "codigo_sublinea": "0403", "descripcion_sublinea": "Jabones y limpieza personal", "id_linea": 4},
        {"id_sublinea": 25, "codigo_sublinea": "0404", "descripcion_sublinea": "Desodorantes", "id_linea": 4},
        {"id_sublinea": 26, "codigo_sublinea": "0405", "descripcion_sublinea": "Cuidado femenino", "id_linea": 4},
        {"id_sublinea": 27, "codigo_sublinea": "0406", "descripcion_sublinea": "Higiene íntima y preservativos", "id_linea": 4},
        {"id_sublinea": 28, "codigo_sublinea": "0407", "descripcion_sublinea": "Repelentes", "id_linea": 4},
        {"id_sublinea": 29, "codigo_sublinea": "0408", "descripcion_sublinea": "Cuidado de las uñas", "id_linea": 4},
        # Línea 05: Dermocosmética y belleza
        {"id_sublinea": 30, "codigo_sublinea": "0501", "descripcion_sublinea": "Cuidado de la piel", "id_linea": 5},
        {"id_sublinea": 31, "codigo_sublinea": "0502", "descripcion_sublinea": "Cosmética dermatológica", "id_linea": 5},
        {"id_sublinea": 32, "codigo_sublinea": "0503", "descripcion_sublinea": "Maquillaje", "id_linea": 5},
        {"id_sublinea": 33, "codigo_sublinea": "0504", "descripcion_sublinea": "Tratamientos cosméticos", "id_linea": 5},
        # Línea 06: Productos infantiles y maternidad
        {"id_sublinea": 34, "codigo_sublinea": "0601", "descripcion_sublinea": "Pañales", "id_linea": 6},
        {"id_sublinea": 35, "codigo_sublinea": "0602", "descripcion_sublinea": "Higiene infantil", "id_linea": 6},
        {"id_sublinea": 36, "codigo_sublinea": "0603", "descripcion_sublinea": "Accesorios infantiles", "id_linea": 6},
        {"id_sublinea": 37, "codigo_sublinea": "0604", "descripcion_sublinea": "Leches infantiles", "id_linea": 6},
        {"id_sublinea": 38, "codigo_sublinea": "0605", "descripcion_sublinea": "Productos de maternidad", "id_linea": 6},
        # Línea 07: Dispositivos médicos y rehabilitación
        {"id_sublinea": 39, "codigo_sublinea": "0701", "descripcion_sublinea": "Accesorios de rehabilitación", "id_linea": 7},
        {"id_sublinea": 40, "codigo_sublinea": "0702", "descripcion_sublinea": "Productos para incontinencia", "id_linea": 7},
        {"id_sublinea": 41, "codigo_sublinea": "0703", "descripcion_sublinea": "Dispositivos de medición y diagnóstico", "id_linea": 7},
        {"id_sublinea": 42, "codigo_sublinea": "0704", "descripcion_sublinea": "Accesorios médicos", "id_linea": 7},
        {"id_sublinea": 43, "codigo_sublinea": "0705", "descripcion_sublinea": "Productos oftálmicos no medicinales", "id_linea": 7},
        # Línea 08: Material médico y primeros auxilios
        {"id_sublinea": 44, "codigo_sublinea": "0801", "descripcion_sublinea": "Material de curación", "id_linea": 8},
        {"id_sublinea": 45, "codigo_sublinea": "0802", "descripcion_sublinea": "Primeros auxilios", "id_linea": 8},
        {"id_sublinea": 46, "codigo_sublinea": "0803", "descripcion_sublinea": "Material médico desechable", "id_linea": 8},
        {"id_sublinea": 47, "codigo_sublinea": "0804", "descripcion_sublinea": "Envases y frascos de uso médico", "id_linea": 8},
        # Línea 09: Alimentos y bebidas
        {"id_sublinea": 48, "codigo_sublinea": "0901", "descripcion_sublinea": "Alimentos", "id_linea": 9},
        {"id_sublinea": 49, "codigo_sublinea": "0902", "descripcion_sublinea": "Leches y productos nutricionales", "id_linea": 9},
        {"id_sublinea": 50, "codigo_sublinea": "0903", "descripcion_sublinea": "Bebidas", "id_linea": 9},
        {"id_sublinea": 51, "codigo_sublinea": "0904", "descripcion_sublinea": "Bebidas energéticas y nutritivas", "id_linea": 9},
        {"id_sublinea": 52, "codigo_sublinea": "0905", "descripcion_sublinea": "Golosinas", "id_linea": 9},
        {"id_sublinea": 53, "codigo_sublinea": "0906", "descripcion_sublinea": "Helados", "id_linea": 9},
        # Línea 10: Productos veterinarios
        {"id_sublinea": 54, "codigo_sublinea": "1001", "descripcion_sublinea": "Productos para mascotas", "id_linea": 10},
        {"id_sublinea": 55, "codigo_sublinea": "1002", "descripcion_sublinea": "Productos veterinarios", "id_linea": 10},
        # Línea 11: Hogar y uso doméstico
        {"id_sublinea": 56, "codigo_sublinea": "1101", "descripcion_sublinea": "Productos para el hogar", "id_linea": 11},
        {"id_sublinea": 57, "codigo_sublinea": "1102", "descripcion_sublinea": "Productos para el calzado", "id_linea": 11},
        # Línea 12: Accesorios y otros productos
        {"id_sublinea": 58, "codigo_sublinea": "1201", "descripcion_sublinea": "Pilas y baterías", "id_linea": 12},
        {"id_sublinea": 59, "codigo_sublinea": "1202", "descripcion_sublinea": "Útiles escolares", "id_linea": 12},
        {"id_sublinea": 60, "codigo_sublinea": "1203", "descripcion_sublinea": "Cámaras y rollos", "id_linea": 12},
        {"id_sublinea": 61, "codigo_sublinea": "1204", "descripcion_sublinea": "Tarjetas y papeletas", "id_linea": 12},
        {"id_sublinea": 62, "codigo_sublinea": "1205", "descripcion_sublinea": "Accesorios diversos", "id_linea": 12},
        # Línea 13: Servicios
        {"id_sublinea": 63, "codigo_sublinea": "1301", "descripcion_sublinea": "Servicios telefónicos", "id_linea": 13},
        {"id_sublinea": 64, "codigo_sublinea": "1302", "descripcion_sublinea": "Otros servicios", "id_linea": 13}
    ]
    df_sublineas = pd.DataFrame(sublineas)

    # 4. Maestro Laboratorios (Código de 6 chars)
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

    # 4. Maestro Tipos de Proveedor Oficial MIVO 7.1 (Naturaleza Principal)
    tipos_proveedor = [
        {"id_tipo_proveedor": 1, "codigo_tipo_proveedor": "01", "descripcion": "Mercancía"},
        {"id_tipo_proveedor": 2, "codigo_tipo_proveedor": "02", "descripcion": "Servicios"},
        {"id_tipo_proveedor": 3, "codigo_tipo_proveedor": "03", "descripcion": "Activos y Equipos"},
        {"id_tipo_proveedor": 4, "codigo_tipo_proveedor": "04", "descripcion": "Tecnología"},
        {"id_tipo_proveedor": 5, "codigo_tipo_proveedor": "05", "descripcion": "Logística y Transporte"},
        {"id_tipo_proveedor": 6, "codigo_tipo_proveedor": "06", "descripcion": "Servicios Profesionales"},
        {"id_tipo_proveedor": 7, "codigo_tipo_proveedor": "07", "descripcion": "Servicios Públicos"},
        {"id_tipo_proveedor": 8, "codigo_tipo_proveedor": "08", "descripcion": "Arrendamiento"},
        {"id_tipo_proveedor": 9, "codigo_tipo_proveedor": "09", "descripcion": "Seguros"},
        {"id_tipo_proveedor": 10, "codigo_tipo_proveedor": "10", "descripcion": "Telecomunicaciones"},
        {"id_tipo_proveedor": 99, "codigo_tipo_proveedor": "99", "descripcion": "Otros Proveedores"}
    ]
    df_tipos_prov = pd.DataFrame(tipos_proveedor)

    # 5. Maestro Segmentos de Proveedor Oficial MIVO 7.1 (Especialización Comercial)
    segmentos_proveedor = [
        # Comercialización y Distribución
        {"id_segmento": 1, "codigo_segmento": "P0101", "descripcion": "Droguerías Estratégicas"},
        {"id_segmento": 2, "codigo_segmento": "P0102", "descripcion": "Droguerías Habituales"},
        {"id_segmento": 3, "codigo_segmento": "P0103", "descripcion": "Droguerías Ocasionales"},
        {"id_segmento": 4, "codigo_segmento": "P0104", "descripcion": "Laboratorios Farmacéuticos"},
        {"id_segmento": 5, "codigo_segmento": "P0105", "descripcion": "Farmacia Intercompañía"},
        {"id_segmento": 6, "codigo_segmento": "P0106", "descripcion": "Otros Distribuidores de Mercancía"},
        # Insumos, Bienes y Mantenimiento
        {"id_segmento": 7, "codigo_segmento": "P0107", "descripcion": "Alimentos y Bebidas"},
        {"id_segmento": 8, "codigo_segmento": "P0108", "descripcion": "Higiene y Cuidado Personal"},
        {"id_segmento": 9, "codigo_segmento": "P0109", "descripcion": "Productos de Limpieza"},
        {"id_segmento": 10, "codigo_segmento": "P0110", "descripcion": "Material Médico y Sanitario"},
        {"id_segmento": 11, "codigo_segmento": "P0111", "descripcion": "Papelería y Suministros"},
        {"id_segmento": 12, "codigo_segmento": "P0201", "descripcion": "Mantenimiento"},
        {"id_segmento": 13, "codigo_segmento": "P0202", "descripcion": "Limpieza"},
        {"id_segmento": 14, "codigo_segmento": "P0203", "descripcion": "Vigilancia y Seguridad"},
        # Corporativo, Servicios y Tecnología
        {"id_segmento": 15, "codigo_segmento": "P0204", "descripcion": "Reparaciones"},
        {"id_segmento": 16, "codigo_segmento": "P0205", "descripcion": "Servicios Generales"},
        {"id_segmento": 17, "codigo_segmento": "P0301", "descripcion": "Equipos Computación"},
        {"id_segmento": 18, "codigo_segmento": "P0401", "descripcion": "Software y Licencias"},
        {"id_segmento": 19, "codigo_segmento": "P0501", "descripcion": "Transporte Mercancías"},
        {"id_segmento": 20, "codigo_segmento": "P0601", "descripcion": "Contabilidad / Auditoría"},
        {"id_segmento": 21, "codigo_segmento": "P0801", "descripcion": "Alquiler Locales"},
        {"id_segmento": 99, "codigo_segmento": "P9999", "descripcion": "Otros Proveedores"}
    ]
    df_segmentos_prov = pd.DataFrame(segmentos_proveedor)

    # 6. Maestro Proveedores (Código correlativo de 6 dígitos según estándar MIVO 7.1)
    proveedores = [
        {"id_proveedor": 1, "codigo_proveedor": "000001", "nombre_proveedor": "Droguería Cobeca", "rif_proveedor": "J-00012345-1", "tipo_proveedor": "01", "segmento": "P0101"},
        {"id_proveedor": 2, "codigo_proveedor": "000002", "nombre_proveedor": "Droguería Nena", "rif_proveedor": "J-00045678-2", "tipo_proveedor": "01", "segmento": "P0101"},
        {"id_proveedor": 3, "codigo_proveedor": "000003", "nombre_proveedor": "Drolanca", "rif_proveedor": "J-00089123-3", "tipo_proveedor": "01", "segmento": "P0102"},
        {"id_proveedor": 4, "codigo_proveedor": "000004", "nombre_proveedor": "Grupo Farvenca", "rif_proveedor": "J-00078945-4", "tipo_proveedor": "01", "segmento": "P0102"},
        {"id_proveedor": 5, "codigo_proveedor": "000005", "nombre_proveedor": "Laboratorios Leti Directo", "rif_proveedor": "J-00032165-5", "tipo_proveedor": "01", "segmento": "P0104"},
        {"id_proveedor": 6, "codigo_proveedor": "000006", "nombre_proveedor": "Mervis Technology C.A. (MIVO)", "rif_proveedor": "J-40981234-9", "tipo_proveedor": "04", "segmento": "P0401"},
        {"id_proveedor": 7, "codigo_proveedor": "000007", "nombre_proveedor": "Transfarma Logística Express", "rif_proveedor": "J-31456789-2", "tipo_proveedor": "05", "segmento": "P0501"}
    ]
    df_provs = pd.DataFrame(proveedores)

    # 7. Maestro Clientes (Cédula de 10 dígitos o RIF, Tipos A01/A02 y Segmentos C01-C05 según MIVO 7.1)
    clientes = [
        {"id_cliente": 1, "codigo_cliente": "0014238901", "nombre_cliente": "Roberto Méndez", "tipo_cliente": "A01", "segmento_cliente": "C01", "identificacion": "V-14238901"},
        {"id_cliente": 2, "codigo_cliente": "0018765432", "nombre_cliente": "Elena Salazar", "tipo_cliente": "A01", "segmento_cliente": "C01", "identificacion": "V-18765432"},
        {"id_cliente": 3, "codigo_cliente": "J304918231", "nombre_cliente": "Seguros Caracas", "tipo_cliente": "A02", "segmento_cliente": "C02", "identificacion": "J-30491823-1"},
        {"id_cliente": 4, "codigo_cliente": "J000123450", "nombre_cliente": "Mercantil Seguros", "tipo_cliente": "A02", "segmento_cliente": "C02", "identificacion": "J-00012345-0"},
        {"id_cliente": 5, "codigo_cliente": "J000456789", "nombre_cliente": "Empresas Polar (Convenio)", "tipo_cliente": "A02", "segmento_cliente": "C04", "identificacion": "J-00045678-9"},
        {"id_cliente": 6, "codigo_cliente": "0025987654", "nombre_cliente": "Carlos Martínez (Empleado)", "tipo_cliente": "A01", "segmento_cliente": "C05", "identificacion": "V-25987654"}
    ]
    df_clientes = pd.DataFrame(clientes)

    # 8. Maestro Productos (SKU de 6 dígitos según estándar MIVO 7.1 y atributos regulatorios)
    # Formato: (id, sku_6d, codigo_barras, nombre, id_linea, id_sublinea, id_lab, categoria_mivo, es_regulado)
    productos = [
        # Línea 01: Especialidades Farmacéuticas
        (1, "000101", "759100100000015", "Atorvastatina 20mg x 30 Tab", 1, 3, 1, "Medicinas", False),
        (2, "000102", "759100200000025", "Losartán Potásico 50mg x 30 Comp", 1, 3, 3, "Medicinas", True),
        (3, "000103", "759100300000035", "Amoxicilina + Ác. Clavulánico 875mg", 1, 14, 5, "Antibióticos", True),
        (4, "000104", "759100400000045", "Ibuprofeno 400mg x 20 Cáps", 1, 2, 2, "Medicinas", False),
        (5, "000105", "759100500000055", "Paracetamol 500mg x 20 Tab", 1, 1, 3, "Medicinas", False),
        (6, "000106", "759100600000065", "Omeprazol 20mg x 28 Cáps", 1, 5, 4, "Medicinas", True),
        (7, "000107", "759100700000075", "Vitamina C 1000mg Efervescente", 1, 11, 2, "Medicinas", False),
        (8, "000108", "759100800000085", "Metformina 850mg x 30 Tab", 1, 10, 6, "Medicinas", True),
        (9, "000109", "759100900000095", "Loratadina 10mg x 10 Tab", 1, 6, 4, "Medicinas", False),
        (10, "000110", "759101000000105", "Cetirizina 10mg x 10 Tab", 1, 6, 5, "Medicinas", False),
        (11, "000111", "759101100000115", "Diclofenac Sódico 50mg x 20 Tab", 1, 2, 7, "Medicinas", False),
        (12, "000112", "759101200000125", "Enalapril 20mg x 30 Tab", 1, 3, 3, "Medicinas", True),
        (13, "000113", "759101300000135", "Azitromicina 500mg x 3 Tab", 1, 14, 1, "Antibióticos", True),
        (14, "000114", "759101400000145", "Clonazepam 2mg x 30 Tab", 1, 12, 6, "Psicotrópicos controlados", True),
        (15, "000115", "759101500000155", "Ciprofloxacina 500mg x 10 Tab", 1, 14, 5, "Antibióticos", True),
        (16, "000116", "759101600000165", "Alprazolam 0.5mg x 30 Tab", 1, 12, 7, "Psicotrópicos controlados", True),
        (17, "000117", "759101700000175", "Levotiroxina 100mcg x 50 Tab", 1, 9, 6, "Medicinas", True),
        (18, "000118", "759101800000185", "Salbutamol Inhalador 100mcg", 1, 4, 8, "Medicinas", True),
        (19, "000119", "759101900000195", "Clopidogrel 75mg x 28 Tab", 1, 3, 8, "Medicinas", False),
        (20, "000120", "759102000000205", "Ketoprofeno 100mg x 24 Cáps", 1, 2, 4, "Medicinas", False),
        # Línea 02: Sueros y Soluciones
        (21, "000201", "759102100000215", "Solución Fisiológica 0.9% 500ml", 2, 15, 5, "Medicinas", True),
        (22, "000202", "759102200000225", "Solución Ringer Lactato 500ml", 2, 16, 5, "Medicinas", True),
        (23, "000203", "759102300000235", "Suero Oral Rehidratante Polvo", 2, 17, 3, "Medicinas", False),
        # Línea 04: Cuidado personal e higiene
        (24, "000401", "759102400000245", "Jabón Antibacterial Dermocuidado 120g", 4, 24, 2, "Misceláneos", False),
        (25, "000402", "759102500000255", "Crema Dental Protección Total 100ml", 4, 23, 2, "Misceláneos", False),
        (26, "000403", "759102600000265", "Desodorante Antitranspirante Roll-On", 4, 25, 4, "Misceláneos", False),
        # Línea 06: Productos infantiles y maternidad
        (27, "000601", "759102700000275", "Pañales Desechables Etapa 3 x 40", 6, 34, 2, "Misceláneos", False),
        (28, "000602", "759102800000285", "Fórmula Infantil Nan Pro 1 400g", 6, 37, 8, "Misceláneos", True),
        # Línea 07: Dispositivos médicos y rehabilitación
        (29, "000701", "759102900000295", "Tensiómetro Digital de Brazo", 7, 41, 1, "Misceláneos", False),
        (30, "000702", "759103000000305", "Glucómetro Digital + 10 Tiras", 7, 41, 6, "Misceláneos", False),
        # Línea 08: Material médico y primeros auxilios
        (31, "000801", "759103100000315", "Alcohol Antiséptico 70% 500ml", 8, 45, 3, "Misceláneos", False),
        (32, "000802", "759103200000325", "Gasa Estéril 10x10cm x 10 Uds", 8, 44, 4, "Misceláneos", False),
        # Línea 09: Alimentos y bebidas
        (33, "000901", "759103300000335", "Agua Mineral sin Gas 500ml", 9, 50, 7, "Misceláneos", False),
        (34, "000902", "759103400000345", "Bebida Hidratante Gatorade 500ml", 9, 51, 7, "Misceláneos", False)
    ]
    df_prod = pd.DataFrame(productos, columns=[
        "id_producto", "codigo_articulo", "codigo_barras", "nombre_producto", 
        "id_linea", "id_sublinea", "id_laboratorio", "categoria_mivo", "es_regulado"
    ])
    df_prod = df_prod.merge(df_lineas[["id_linea", "codigo_linea", "descripcion_linea"]], on="id_linea")
    df_prod = df_prod.merge(df_sublineas[["id_sublinea", "codigo_sublinea", "descripcion_sublinea"]], on="id_sublinea")
    df_prod = df_prod.merge(df_labs[["id_laboratorio", "codigo_laboratorio", "nombre_laboratorio"]], on="id_laboratorio")

    # Generar histórico de 6 meses (aprox 180 días) para análisis mensual
    fechas = [hoy - timedelta(days=i) for i in range(180, -1, -1)]

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

    # 9.1. Histórico Mensual de Inventario (Últimos 6 meses)
    meses_hist = [
        (hoy - timedelta(days=30*i)).strftime("%Y-%m")
        for i in range(5, -1, -1)
    ]
    filas_inv_mes = []
    for suc in sucursales:
        base_cst = random.uniform(85000.0, 160000.0)
        for idx_m, m in enumerate(meses_hist):
            # Tendencia de evolución
            cst_mes = round(base_cst * (1 + (idx_m * 0.035) + random.uniform(-0.02, 0.02)), 2)
            pvp_mes = round(cst_mes * random.uniform(1.60, 1.72), 2)
            uds_mes = int(round(cst_mes / random.uniform(4.5, 5.5)))
            filas_inv_mes.append({
                "id_sucursal": suc["id_sucursal"],
                "periodo_mes": m,
                "fecha_cierre": f"{m}-28",
                "total_unidades": uds_mes,
                "valor_total_costo": cst_mes,
                "valor_total_pvp": pvp_mes,
                "margen_potencial_pct": round((pvp_mes - cst_mes) / pvp_mes * 100, 2)
            })
    df_inv_mes = pd.DataFrame(filas_inv_mes)

    # 10. Compras (enlace a id_proveedor)
    filas_comp = []
    filas_comp_dia = []
    for suc in sucursales:
        for f in fechas[::2]:
            uds_tot_dia = 0
            mto_tot_dia = 0.0
            for _, p in df_prod.sample(6).iterrows():
                prv = random.choice(proveedores)
                uds_c = random.randint(20, 90)
                costo = round(uds_c * random.uniform(2.5, 12.0), 2)
                uds_tot_dia += uds_c
                mto_tot_dia += costo
                filas_comp.append({
                    "id_sucursal": suc["id_sucursal"],
                    "fecha": f,
                    "id_producto": p["id_producto"],
                    "id_proveedor": prv["id_proveedor"],
                    "unidades_compradas": uds_c,
                    "total_compra_monto": costo
                })
            facs = random.randint(2, 6)
            c_cred = round(mto_tot_dia * random.uniform(0.60, 0.85), 2)
            c_cont = round(mto_tot_dia - c_cred, 2)
            filas_comp_dia.append({
                "id_sucursal": suc["id_sucursal"],
                "fecha": f,
                "total_comprado": mto_tot_dia,
                "unidades_compradas": uds_tot_dia,
                "numero_facturas_compra": facs,
                "compras_contado": c_cont,
                "compras_credito": c_cred
            })
    df_compras = pd.DataFrame(filas_comp)
    df_compras_dia = pd.DataFrame(filas_comp_dia)

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
        "sublineas": df_sublineas,
        "laboratorios": df_labs,
        "tipos_proveedor": df_tipos_prov,
        "segmentos_proveedor": df_segmentos_prov,
        "proveedores": df_provs,
        "clientes": df_clientes,
        "productos": df_prod,
        "ventas_diarias": df_vta_dia,
        "ventas_producto": df_vta_prod,
        "inventario": df_inv,
        "inventario_mensual": df_inv_mes,
        "compras": df_compras,
        "compras_diarias": df_compras_dia,
        "vendedores": df_vend,
        "formas_pago": df_formas_pago,
        "bancos": df_bancos,
        "cajas": df_cajas,
        "cxc": df_cxc,
        "cxp": df_cxp
    }

# --- Encabezado Principal y Marca ---
col_logo, col_titulo = st.columns([1, 8])
with col_logo:
    if os.path.exists(RUTA_LOGO):
        st.image(RUTA_LOGO, use_container_width=True)
    else:
        st.markdown("""
        <div style="background: rgba(16, 185, 129, 0.15); border: 2px solid #10b981; border-radius: 14px; width: 60px; height: 60px; display: flex; align-items: center; justify-content: center; font-size: 2rem; box-shadow: 0 0 15px rgba(16,185,129,0.3);">
            ➕
        </div>
        """, unsafe_allow_html=True)
with col_titulo:
    st.markdown(f"""
    <div style="display: flex; flex-direction: column; justify-content: center;">
        <h1 style="margin: 0; padding: 0; font-size: 2rem; font-weight: 800; letter-spacing: -0.02em; color: #ffffff;">
            {NOMBRE_EMPRESA}
        </h1>
        <p style="margin: 2px 0 0 0; padding: 0; font-size: 0.88rem; color: #94a3b8; font-weight: 500;">
            {SLOGAN_EMPRESA}
        </p>
    </div>
    """, unsafe_allow_html=True)

# --- Barra lateral de Configuración y Filtros ---
st.sidebar.header("⚙️ Configuración & Filtros")

modo_datos = st.sidebar.radio(
    "Fuente de Datos:",
    ["Simulación (Datos de Prueba)", "Conexión MySQL en Vivo"],
    index=0
)

if st.sidebar.button("🔄 Refrescar Datos", use_container_width=True):
    st.cache_data.clear()
    st.cache_resource.clear()
    st.rerun()

# Carga de catálogos base
if modo_datos == "Simulación (Datos de Prueba)":
    datos = generar_datos_prueba()
    df_sucursales = datos["sucursales"]
    df_lineas_cat = datos["lineas"]
    df_sublineas_cat = datos["sublineas"]
    df_labs_cat = datos["laboratorios"]
    df_tipos_prov_cat = datos["tipos_proveedor"]
    df_segs_prov_cat = datos["segmentos_proveedor"]
    df_provs_cat = datos["proveedores"]
    df_clientes_cat = datos["clientes"]
    df_catalogo_prod = datos["productos"]
else:
    try:
        engine = get_db_engine()
        with engine.connect() as conn:
            df_sucursales = pd.read_sql(text("SELECT id_sucursal, codigo_sucursal, nombre, ciudad, zona FROM sucursales ORDER BY nombre"), conn)
            df_lineas_cat = pd.read_sql(text("SELECT id_linea, codigo_linea, descripcion_linea FROM maestro_lineas ORDER BY descripcion_linea"), conn)
            try:
                df_sublineas_cat = pd.read_sql(text("SELECT id_sublinea, codigo_sublinea, descripcion_sublinea, id_linea FROM maestro_sublineas ORDER BY descripcion_sublinea"), conn)
            except Exception:
                df_sublineas_cat = pd.DataFrame(columns=["id_sublinea", "codigo_sublinea", "descripcion_sublinea", "id_linea"])
            df_labs_cat = pd.read_sql(text("SELECT id_laboratorio, codigo_laboratorio, nombre_laboratorio FROM maestro_laboratorios ORDER BY nombre_laboratorio"), conn)
            try:
                df_tipos_prov_cat = pd.read_sql(text("SELECT id_tipo_proveedor, codigo_tipo_proveedor, descripcion FROM maestro_tipos_proveedor ORDER BY codigo_tipo_proveedor"), conn)
            except Exception:
                df_tipos_prov_cat = pd.DataFrame(columns=["id_tipo_proveedor", "codigo_tipo_proveedor", "descripcion"])
            try:
                df_segs_prov_cat = pd.read_sql(text("SELECT id_segmento, codigo_segmento, descripcion FROM maestro_segmentos_proveedor ORDER BY codigo_segmento"), conn)
            except Exception:
                df_segs_prov_cat = pd.DataFrame(columns=["id_segmento", "codigo_segmento", "descripcion"])
            df_provs_cat = pd.read_sql(text("SELECT id_proveedor, codigo_proveedor, nombre_proveedor, rif_proveedor, COALESCE(tipo_proveedor, 'DROGUE') AS tipo_proveedor, COALESCE(segmento, 'MEDICA') AS segmento FROM maestro_proveedores ORDER BY nombre_proveedor"), conn)
            df_clientes_cat = pd.read_sql(text("SELECT id_cliente, codigo_cliente, nombre_cliente, tipo_cliente, identificacion FROM maestro_clientes ORDER BY nombre_cliente"), conn)
            sql_p = """
                SELECT p.id_producto, p.codigo_articulo, p.codigo_barras, p.nombre_producto, 
                       l.codigo_linea, l.descripcion_linea,
                       COALESCE(sl.codigo_sublinea, 'SL000') AS codigo_sublinea,
                       COALESCE(sl.descripcion_sublinea, 'Sublínea General') AS descripcion_sublinea,
                       lb.codigo_laboratorio, lb.nombre_laboratorio
                FROM maestro_productos p
                JOIN maestro_lineas l ON p.id_linea = l.id_linea
                LEFT JOIN maestro_sublineas sl ON p.id_sublinea = sl.id_sublinea
                JOIN maestro_laboratorios lb ON p.id_laboratorio = lb.id_laboratorio
            """
            df_catalogo_prod = pd.read_sql(text(sql_p), conn)
    except Exception as e:
        st.sidebar.error(f"Error MySQL: {e}")
        st.warning("⚠️ No se pudo conectar a MySQL en vivo. Activando datos de prueba.")
        datos = generar_datos_prueba()
        df_sucursales = datos["sucursales"]
        df_lineas_cat = datos["lineas"]
        df_sublineas_cat = datos["sublineas"]
        df_labs_cat = datos["laboratorios"]
        df_tipos_prov_cat = datos["tipos_proveedor"]
        df_segs_prov_cat = datos["segmentos_proveedor"]
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
hace_6_meses = hoy - timedelta(days=180)
rango_fecha = st.sidebar.date_input("Rango de Fechas:", value=(hace_6_meses, hoy), max_value=hoy)

if isinstance(rango_fecha, (tuple, list)) and len(rango_fecha) == 2:
    f_ini, f_fin = rango_fecha
elif isinstance(rango_fecha, (tuple, list)) and len(rango_fecha) == 1:
    f_ini = f_fin = rango_fecha[0]
else:
    f_ini, f_fin = hace_6_meses, hoy

st.sidebar.divider()
st.sidebar.subheader("🎯 Filtros Maestros")

# 4. Filtro por Línea de Producto (Categoría)
lineas_opciones = {"Todas las líneas": None}
for _, row in df_lineas_cat.iterrows():
    lineas_opciones[f"[{row['codigo_linea']}] {row['descripcion_linea']}"] = int(row['id_linea'])
linea_label = st.sidebar.selectbox("Línea de Producto:", options=list(lineas_opciones.keys()))
id_linea_sel = lineas_opciones[linea_label]

# 5. Filtro por Sublínea de Producto
df_sublineas_filtradas = df_sublineas_cat.copy()
if id_linea_sel is not None and "id_linea" in df_sublineas_filtradas.columns:
    df_sublineas_filtradas = df_sublineas_filtradas[(df_sublineas_filtradas["id_linea"] == id_linea_sel) | (df_sublineas_filtradas["id_linea"].isna())]

sublineas_opciones = {"Todas las sublíneas": None}
for _, row in df_sublineas_filtradas.iterrows():
    sublineas_opciones[f"[{row['codigo_sublinea']}] {row['descripcion_sublinea']}"] = int(row['id_sublinea'])
sublinea_label = st.sidebar.selectbox("Sublínea de Producto:", options=list(sublineas_opciones.keys()))
id_sublinea_sel = sublineas_opciones[sublinea_label]

# 6. Filtro por Laboratorio (Fabricante / Marca)
labs_opciones = {"Todos los laboratorios": None}
for _, row in df_labs_cat.iterrows():
    labs_opciones[f"[{row['codigo_laboratorio']}] {row['nombre_laboratorio']}"] = int(row['id_laboratorio'])
lab_label = st.sidebar.selectbox("Laboratorio (Marca):", options=list(labs_opciones.keys()))
id_lab_sel = labs_opciones[lab_label]

# 6.1 Filtro por Artículo / Producto
df_articulos_disponibles = df_catalogo_prod.copy()
if id_linea_sel is not None and "id_linea" in df_articulos_disponibles.columns:
    df_articulos_disponibles = df_articulos_disponibles[df_articulos_disponibles["id_linea"] == id_linea_sel]
if id_sublinea_sel is not None and "id_sublinea" in df_articulos_disponibles.columns:
    df_articulos_disponibles = df_articulos_disponibles[df_articulos_disponibles["id_sublinea"] == id_sublinea_sel]
if id_lab_sel is not None and "id_laboratorio" in df_articulos_disponibles.columns:
    df_articulos_disponibles = df_articulos_disponibles[df_articulos_disponibles["id_laboratorio"] == id_lab_sel]

articulos_opciones = {"Todos los artículos": None}
for _, row in df_articulos_disponibles.iterrows():
    sku_txt = f"[{row['codigo_articulo']}] " if pd.notna(row.get('codigo_articulo')) else ""
    articulos_opciones[f"{sku_txt}{row['nombre_producto']}"] = int(row['id_producto'])

articulo_label = st.sidebar.selectbox("Artículo / Producto:", options=list(articulos_opciones.keys()))
id_articulo_sel = articulos_opciones[articulo_label]

# 7. Filtro por Tipo de Proveedor (Alfanumérico 6 caracteres desde maestro_tipos_proveedor)
map_desc_tipo = {}
if "df_tipos_prov_cat" in locals() and not df_tipos_prov_cat.empty:
    for _, r_tp in df_tipos_prov_cat.iterrows():
        map_desc_tipo[r_tp["codigo_tipo_proveedor"]] = r_tp["descripcion"]

tipos_prov_disponibles = sorted([str(t).strip().upper() for t in df_provs_cat["tipo_proveedor"].dropna().unique().tolist() if str(t).strip()]) if "tipo_proveedor" in df_provs_cat else []
opciones_tipo_prov_dict = {"Todos los tipos": "Todos los tipos"}
for t_cod in tipos_prov_disponibles:
    desc_t = f" - {map_desc_tipo[t_cod]}" if t_cod in map_desc_tipo else ""
    opciones_tipo_prov_dict[f"[{t_cod}]{desc_t}"] = t_cod

tipo_prov_label = st.sidebar.selectbox("Tipo de Proveedor:", options=list(opciones_tipo_prov_dict.keys()))
tipo_prov_sel = opciones_tipo_prov_dict[tipo_prov_label]

# 7. Filtro por Segmento de Proveedor (Alfanumérico 6 caracteres desde maestro_segmentos_proveedor)
map_desc_seg = {}
if "df_segs_prov_cat" in locals() and not df_segs_prov_cat.empty:
    for _, r_sg in df_segs_prov_cat.iterrows():
        map_desc_seg[r_sg["codigo_segmento"]] = r_sg["descripcion"]

segs_prov_disponibles = sorted([str(s).strip().upper() for s in df_provs_cat["segmento"].dropna().unique().tolist() if str(s).strip()]) if "segmento" in df_provs_cat else []
opciones_seg_prov_dict = {"Todos los segmentos": "Todos los segmentos"}
for s_cod in segs_prov_disponibles:
    desc_s = f" - {map_desc_seg[s_cod]}" if s_cod in map_desc_seg else ""
    opciones_seg_prov_dict[f"[{s_cod}]{desc_s}"] = s_cod

seg_prov_label = st.sidebar.selectbox("Segmento de Proveedor:", options=list(opciones_seg_prov_dict.keys()))
seg_prov_sel = opciones_seg_prov_dict[seg_prov_label]

# Filtrar catálogo de proveedores por Tipo y Segmento si están seleccionados
df_provs_filtrados = df_provs_cat.copy()
if tipo_prov_sel != "Todos los tipos":
    df_provs_filtrados = df_provs_filtrados[df_provs_filtrados["tipo_proveedor"].str.upper() == tipo_prov_sel]
if seg_prov_sel != "Todos los segmentos":
    df_provs_filtrados = df_provs_filtrados[df_provs_filtrados["segmento"].str.upper() == seg_prov_sel]

# 8. Filtro por Proveedor / Droguería
provs_opciones = {"Todos los proveedores": None}
for _, row in df_provs_filtrados.iterrows():
    tipo_tag = f" ({row['tipo_proveedor']})" if pd.notna(row.get('tipo_proveedor')) else ""
    seg_tag = f" [{row['segmento']}]" if pd.notna(row.get('segmento')) else ""
    provs_opciones[f"[{row['codigo_proveedor']}] {row['nombre_proveedor']}{tipo_tag}{seg_tag}"] = int(row['id_proveedor'])
prov_label = st.sidebar.selectbox("Proveedor / Droguería:", options=list(provs_opciones.keys()))
id_prov_sel = provs_opciones[prov_label]

# 9. Filtro por Cliente (Para CxC)
clientes_opciones = {"Todos los clientes": None}
for _, row in df_clientes_cat.iterrows():
    tipo_t = f" ({row['tipo_cliente']})" if pd.notna(row.get('tipo_cliente')) else ""
    clientes_opciones[f"[{row['codigo_cliente']}] {row['nombre_cliente']}{tipo_t}"] = int(row['id_cliente'])
cliente_label = st.sidebar.selectbox("Cliente (CxC):", options=list(clientes_opciones.keys()))
id_cliente_sel = clientes_opciones[cliente_label]

# --- Pestañas ---
tab_ventas, tab_compras, tab_inventario, tab_vendedores, tab_finanzas, tab_sugerencias = st.tabs([
    "📊 Ventas & Rendimiento",
    "📥 Compras & Proveedores",
    "📦 Inventario & Valorización",
    "👨‍💼 Equipo de Ventas",
    "💰 Tesorería & Finanzas",
    "🧠 Diagnóstico & Sugerencias IA"
])

# =========================================================================
# FILTRADO DE DATOS (SIMULACIÓN / MYSQL)
# =========================================================================
filtro_linea_activo = (id_linea_sel is not None)
filtro_sublinea_activo = (id_sublinea_sel is not None)
filtro_lab_activo = (id_lab_sel is not None)
filtro_articulo_activo = (id_articulo_sel is not None)
filtro_prov_activo = (id_prov_sel is not None)
filtro_tipo_prov_activo = (tipo_prov_sel != "Todos los tipos")
filtro_seg_prov_activo = (seg_prov_sel != "Todos los segmentos")
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
    if filtro_sublinea_activo:
        df_v_prod = df_v_prod[df_v_prod["id_sublinea"] == id_sublinea_sel]
    if filtro_lab_activo:
        df_v_prod = df_v_prod[df_v_prod["id_laboratorio"] == id_lab_sel]
    if filtro_articulo_activo:
        df_v_prod = df_v_prod[df_v_prod["id_producto"] == id_articulo_sel]

    # 2. Ventas Diarias Globales
    if filtro_linea_activo or filtro_sublinea_activo or filtro_lab_activo or filtro_articulo_activo:
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
    if filtro_sublinea_activo:
        df_comp = df_comp[df_comp["id_sublinea"] == id_sublinea_sel]
    if filtro_lab_activo:
        df_comp = df_comp[df_comp["id_laboratorio"] == id_lab_sel]
    if filtro_articulo_activo:
        df_comp = df_comp[df_comp["id_producto"] == id_articulo_sel]
    if filtro_tipo_prov_activo:
        df_comp = df_comp[df_comp["tipo_proveedor"].astype(str).str.upper() == tipo_prov_sel]
    if filtro_seg_prov_activo:
        df_comp = df_comp[df_comp["segmento"].astype(str).str.upper() == seg_prov_sel]
    if filtro_prov_activo:
        df_comp = df_comp[df_comp["id_proveedor"] == id_prov_sel]

    # Compras Diarias Globales
    if filtro_linea_activo or filtro_sublinea_activo or filtro_lab_activo or filtro_articulo_activo or filtro_prov_activo or filtro_tipo_prov_activo or filtro_seg_prov_activo:
        if not df_comp.empty:
            df_c_dia = df_comp.groupby(["fecha"]).agg(
                total_comprado=("total_compra_monto", "sum"),
                unidades_compradas=("unidades_compradas", "sum")
            ).reset_index()
            df_c_dia["numero_facturas_compra"] = df_c_dia["unidades_compradas"].apply(lambda x: max(1, x // 40))
            df_c_dia["compras_contado"] = df_c_dia["total_comprado"] * 0.25
            df_c_dia["compras_credito"] = df_c_dia["total_comprado"] * 0.75
        else:
            df_c_dia = pd.DataFrame(columns=["fecha", "total_comprado", "unidades_compradas", "numero_facturas_compra", "compras_contado", "compras_credito"])
    else:
        df_c_dia = datos["compras_diarias"]
        df_c_dia = df_c_dia[(df_c_dia["fecha"] >= f_ini) & (df_c_dia["fecha"] <= f_fin)]
        if id_sucursal:
            df_c_dia = df_c_dia[df_c_dia["id_sucursal"] == id_sucursal]
        else:
            df_c_dia = df_c_dia[df_c_dia["id_sucursal"].isin(ids_sucursales_zona)]

    # 4. Inventario
    df_inv = datos["inventario"].merge(datos["productos"], on="id_producto").merge(datos["sucursales"], on="id_sucursal")
    if id_sucursal:
        df_inv = df_inv[df_inv["id_sucursal"] == id_sucursal]
    else:
        df_inv = df_inv[df_inv["id_sucursal"].isin(ids_sucursales_zona)]
    if filtro_linea_activo:
        df_inv = df_inv[df_inv["id_linea"] == id_linea_sel]
    if filtro_sublinea_activo:
        df_inv = df_inv[df_inv["id_sublinea"] == id_sublinea_sel]
    if filtro_lab_activo:
        df_inv = df_inv[df_inv["id_laboratorio"] == id_lab_sel]
    if filtro_articulo_activo:
        df_inv = df_inv[df_inv["id_producto"] == id_articulo_sel]

    # Histórico de Inventario Mensual
    df_inv_mes = datos["inventario_mensual"].merge(datos["sucursales"], on="id_sucursal")
    if id_sucursal:
        df_inv_mes = df_inv_mes[df_inv_mes["id_sucursal"] == id_sucursal]
    else:
        df_inv_mes = df_inv_mes[df_inv_mes["id_sucursal"].isin(ids_sucursales_zona)]

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

else:
    # MODO CONEXIÓN MYSQL EN VIVO
    engine = get_db_engine()
    with engine.connect() as conn:
        # Construcción de cláusula de sucursales
        if id_sucursal:
            cond_suc = f"= {id_sucursal}"
        else:
            suc_str = ",".join(map(str, ids_sucursales_zona)) if ids_sucursales_zona else "0"
            cond_suc = f"IN ({suc_str})"

        f_ini_str = str(f_ini)
        f_fin_str = str(f_fin)

        # 1. Ventas por Producto
        q_v_prod = f"""
            SELECT vp.id_sucursal, vp.fecha, vp.id_producto, vp.unidades_vendidas, vp.total_venta_monto,
                   p.codigo_articulo, p.codigo_barras, p.nombre_producto,
                   l.id_linea, l.codigo_linea, l.descripcion_linea,
                   COALESCE(sl.id_sublinea, 0) AS id_sublinea,
                   COALESCE(sl.codigo_sublinea, 'SL000') AS codigo_sublinea,
                   COALESCE(sl.descripcion_sublinea, 'Sublínea General') AS descripcion_sublinea,
                   lb.id_laboratorio, lb.codigo_laboratorio, lb.nombre_laboratorio
            FROM kpi_ventas_por_producto vp
            JOIN maestro_productos p ON vp.id_producto = p.id_producto
            JOIN maestro_lineas l ON p.id_linea = l.id_linea
            LEFT JOIN maestro_sublineas sl ON p.id_sublinea = sl.id_sublinea
            JOIN maestro_laboratorios lb ON p.id_laboratorio = lb.id_laboratorio
            WHERE vp.id_sucursal {cond_suc}
              AND vp.fecha BETWEEN '{f_ini_str}' AND '{f_fin_str}'
        """
        if filtro_linea_activo:
            q_v_prod += f" AND p.id_linea = {id_linea_sel}"
        if filtro_sublinea_activo:
            q_v_prod += f" AND p.id_sublinea = {id_sublinea_sel}"
        if filtro_lab_activo:
            q_v_prod += f" AND p.id_laboratorio = {id_lab_sel}"
        if filtro_articulo_activo:
            q_v_prod += f" AND p.id_producto = {id_articulo_sel}"

        df_v_prod = pd.read_sql(text(q_v_prod), conn)

        # 2. Ventas Diarias Globales
        if filtro_linea_activo or filtro_sublinea_activo or filtro_lab_activo or filtro_articulo_activo:
            if not df_v_prod.empty:
                df_v_dia = df_v_prod.groupby(["fecha"]).agg(
                    total_facturado=("total_venta_monto", "sum"),
                    numero_operaciones=("unidades_vendidas", "count")
                ).reset_index()
                df_v_dia["ventas_contado"] = df_v_dia["total_facturado"] * 0.75
                df_v_dia["ventas_credito"] = df_v_dia["total_facturado"] * 0.25
                df_v_dia["operaciones_contado"] = (df_v_dia["numero_operaciones"] * 0.8).astype(int)
                df_v_dia["operaciones_credito"] = df_v_dia["numero_operaciones"] - df_v_dia["operaciones_contado"]
            else:
                df_v_dia = pd.DataFrame(columns=["fecha", "total_facturado", "numero_operaciones", "ventas_contado", "ventas_credito", "operaciones_contado", "operaciones_credito"])
        else:
            q_v_dia = f"""
                SELECT id_sucursal, fecha, total_facturado,
                       COALESCE(ventas_contado, 0.00) AS ventas_contado,
                       COALESCE(ventas_credito, 0.00) AS ventas_credito,
                       numero_operaciones,
                       COALESCE(operaciones_contado, 0) AS operaciones_contado,
                       COALESCE(operaciones_credito, 0) AS operaciones_credito
                FROM kpi_ventas_diarias
                WHERE id_sucursal {cond_suc}
                  AND fecha BETWEEN '{f_ini_str}' AND '{f_fin_str}'
                ORDER BY fecha
            """
            df_v_dia = pd.read_sql(text(q_v_dia), conn)

        # 3. Compras por Producto y Proveedor
        q_comp = f"""
            SELECT cp.id_sucursal, cp.fecha, cp.id_producto, cp.id_proveedor, cp.unidades_compradas, cp.total_compra_monto,
                   p.codigo_articulo, p.codigo_barras, p.nombre_producto,
                   l.id_linea, l.codigo_linea, l.descripcion_linea,
                   COALESCE(sl.id_sublinea, 0) AS id_sublinea,
                   COALESCE(sl.codigo_sublinea, 'SL000') AS codigo_sublinea,
                   COALESCE(sl.descripcion_sublinea, 'Sublínea General') AS descripcion_sublinea,
                   lb.id_laboratorio, lb.codigo_laboratorio, lb.nombre_laboratorio,
                   pr.codigo_proveedor, pr.nombre_proveedor,
                   COALESCE(pr.tipo_proveedor, 'DROGUE') AS tipo_proveedor,
                   COALESCE(pr.segmento, 'MEDICA') AS segmento
            FROM kpi_compras_por_producto cp
            JOIN maestro_productos p ON cp.id_producto = p.id_producto
            JOIN maestro_lineas l ON p.id_linea = l.id_linea
            LEFT JOIN maestro_sublineas sl ON p.id_sublinea = sl.id_sublinea
            JOIN maestro_laboratorios lb ON p.id_laboratorio = lb.id_laboratorio
            JOIN maestro_proveedores pr ON cp.id_proveedor = pr.id_proveedor
            WHERE cp.id_sucursal {cond_suc}
              AND cp.fecha BETWEEN '{f_ini_str}' AND '{f_fin_str}'
        """
        if filtro_linea_activo:
            q_comp += f" AND p.id_linea = {id_linea_sel}"
        if filtro_sublinea_activo:
            q_comp += f" AND p.id_sublinea = {id_sublinea_sel}"
        if filtro_lab_activo:
            q_comp += f" AND p.id_laboratorio = {id_lab_sel}"
        if filtro_articulo_activo:
            q_comp += f" AND p.id_producto = {id_articulo_sel}"
        if filtro_tipo_prov_activo:
            q_comp += f" AND UPPER(pr.tipo_proveedor) = '{tipo_prov_sel}'"
        if filtro_seg_prov_activo:
            q_comp += f" AND UPPER(pr.segmento) = '{seg_prov_sel}'"
        if filtro_prov_activo:
            q_comp += f" AND cp.id_proveedor = {id_prov_sel}"

        df_comp = pd.read_sql(text(q_comp), conn)

        # Compras Diarias Globales
        if filtro_linea_activo or filtro_sublinea_activo or filtro_lab_activo or filtro_articulo_activo or filtro_prov_activo or filtro_tipo_prov_activo or filtro_seg_prov_activo:
            if not df_comp.empty:
                df_c_dia = df_comp.groupby(["fecha"]).agg(
                    total_comprado=("total_compra_monto", "sum"),
                    unidades_compradas=("unidades_compradas", "sum")
                ).reset_index()
                df_c_dia["numero_facturas_compra"] = df_c_dia["unidades_compradas"].apply(lambda x: max(1, x // 40))
                df_c_dia["compras_contado"] = df_c_dia["total_comprado"] * 0.25
                df_c_dia["compras_credito"] = df_c_dia["total_comprado"] * 0.75
            else:
                df_c_dia = pd.DataFrame(columns=["fecha", "total_comprado", "unidades_compradas", "numero_facturas_compra", "compras_contado", "compras_credito"])
        else:
            try:
                q_c_dia = f"""
                    SELECT id_sucursal, fecha, total_comprado, unidades_compradas,
                           COALESCE(numero_facturas_compra, 0) AS numero_facturas_compra,
                           COALESCE(compras_contado, 0.00) AS compras_contado,
                           COALESCE(compras_credito, 0.00) AS compras_credito
                    FROM kpi_compras_diarias
                    WHERE id_sucursal {cond_suc}
                      AND fecha BETWEEN '{f_ini_str}' AND '{f_fin_str}'
                    ORDER BY fecha
                """
                df_c_dia = pd.read_sql(text(q_c_dia), conn)
            except Exception:
                # Si la tabla kpi_compras_diarias aún no fue creada en MySQL, agrupar desde df_comp
                if not df_comp.empty:
                    df_c_dia = df_comp.groupby(["fecha"]).agg(
                        total_comprado=("total_compra_monto", "sum"),
                        unidades_compradas=("unidades_compradas", "sum")
                    ).reset_index()
                    df_c_dia["numero_facturas_compra"] = df_c_dia["unidades_compradas"].apply(lambda x: max(1, x // 40))
                    df_c_dia["compras_contado"] = df_c_dia["total_comprado"] * 0.25
                    df_c_dia["compras_credito"] = df_c_dia["total_comprado"] * 0.75
                else:
                    df_c_dia = pd.DataFrame(columns=["fecha", "total_comprado", "unidades_compradas", "numero_facturas_compra", "compras_contado", "compras_credito"])

        # 4. Inventario
        q_inv = f"""
            SELECT inv.id_inventario, inv.id_sucursal, inv.id_producto, inv.stock_actual, inv.stock_minimo,
                   inv.costo_unitario, inv.precio_unitario, inv.valor_total_inventario, inv.valor_venta_inventario,
                   s.codigo_sucursal, s.nombre, s.ciudad, s.zona,
                   p.codigo_articulo, p.codigo_barras, p.nombre_producto,
                   l.id_linea, l.codigo_linea, l.descripcion_linea,
                   COALESCE(sl.id_sublinea, 0) AS id_sublinea,
                   COALESCE(sl.codigo_sublinea, 'SL000') AS codigo_sublinea,
                   COALESCE(sl.descripcion_sublinea, 'Sublínea General') AS descripcion_sublinea,
                   lb.id_laboratorio, lb.codigo_laboratorio, lb.nombre_laboratorio
            FROM kpi_inventario_sucursal inv
            JOIN sucursales s ON inv.id_sucursal = s.id_sucursal
            JOIN maestro_productos p ON inv.id_producto = p.id_producto
            JOIN maestro_lineas l ON p.id_linea = l.id_linea
            LEFT JOIN maestro_sublineas sl ON p.id_sublinea = sl.id_sublinea
            JOIN maestro_laboratorios lb ON p.id_laboratorio = lb.id_laboratorio
            WHERE inv.id_sucursal {cond_suc}
        """
        if filtro_linea_activo:
            q_inv += f" AND p.id_linea = {id_linea_sel}"
        if filtro_sublinea_activo:
            q_inv += f" AND p.id_sublinea = {id_sublinea_sel}"
        if filtro_lab_activo:
            q_inv += f" AND p.id_laboratorio = {id_lab_sel}"
        if filtro_articulo_activo:
            q_inv += f" AND p.id_producto = {id_articulo_sel}"

        df_inv = pd.read_sql(text(q_inv), conn)

        # Histórico de Inventario Mensual
        try:
            q_inv_mes = f"""
                SELECT im.id_sucursal, im.periodo_mes, im.fecha_cierre, im.total_unidades,
                       im.valor_total_costo, im.valor_total_pvp, im.margen_potencial_pct,
                       s.codigo_sucursal, s.nombre, s.ciudad, s.zona
                FROM kpi_inventario_mensual im
                JOIN sucursales s ON im.id_sucursal = s.id_sucursal
                WHERE im.id_sucursal {cond_suc}
                ORDER BY im.periodo_mes
            """
            df_inv_mes = pd.read_sql(text(q_inv_mes), conn)
        except Exception:
            # Fallback en caso de que la tabla aún no exista en el MySQL en vivo
            df_inv_mes = pd.DataFrame(columns=["id_sucursal", "periodo_mes", "fecha_cierre", "total_unidades", "valor_total_costo", "valor_total_pvp", "margen_potencial_pct", "codigo_sucursal", "nombre", "ciudad", "zona"])

        # 5. Vendedores
        q_vend = f"""
            SELECT id_sucursal, fecha, nombre_vendedor, total_vendido, cantidad_operaciones
            FROM kpi_ventas_vendedor
            WHERE id_sucursal {cond_suc}
              AND fecha BETWEEN '{f_ini_str}' AND '{f_fin_str}'
        """
        df_vend = pd.read_sql(text(q_vend), conn)

        # 6. Formas de Pago
        q_pagos = f"""
            SELECT id_sucursal, fecha, forma_pago, total_ingresado
            FROM kpi_formas_pago
            WHERE id_sucursal {cond_suc}
              AND fecha BETWEEN '{f_ini_str}' AND '{f_fin_str}'
        """
        df_pagos = pd.read_sql(text(q_pagos), conn)

        # 7. Bancos y Cajas
        q_bancos = f"""
            SELECT id_sucursal, fecha, nombre_banco, numero_cuenta_oculto, saldo_disponible
            FROM kpi_saldos_bancos
            WHERE id_sucursal {cond_suc}
        """
        df_bancos = pd.read_sql(text(q_bancos), conn)

        q_cajas = f"""
            SELECT id_sucursal, fecha, tipo_caja, moneda, saldo_efectivo
            FROM kpi_cajas_efectivo
            WHERE id_sucursal {cond_suc}
        """
        df_cajas = pd.read_sql(text(q_cajas), conn)

        # 8. CxC y CxP
        q_cxc = f"""
            SELECT cxc.id_sucursal, cxc.fecha, cxc.id_cliente, cxc.saldo_pendiente,
                   cxc.monto_otorgado_hoy, cxc.monto_recuperado_hoy,
                   cl.codigo_cliente, cl.nombre_cliente, cl.tipo_cliente, cl.identificacion
            FROM kpi_cxc_diario cxc
            JOIN maestro_clientes cl ON cxc.id_cliente = cl.id_cliente
            WHERE cxc.id_sucursal {cond_suc}
        """
        if filtro_cliente_activo:
            q_cxc += f" AND cxc.id_cliente = {id_cliente_sel}"
        df_cxc = pd.read_sql(text(q_cxc), conn)

        q_cxp = f"""
            SELECT cxp.id_sucursal, cxp.fecha, cxp.id_proveedor, cxp.saldo_por_pagar,
                   pr.codigo_proveedor, pr.nombre_proveedor, pr.rif_proveedor
            FROM kpi_cxp_diario cxp
            JOIN maestro_proveedores pr ON cxp.id_proveedor = pr.id_proveedor
            WHERE cxp.id_sucursal {cond_suc}
        """
        if filtro_prov_activo:
            q_cxp += f" AND cxp.id_proveedor = {id_prov_sel}"
        df_cxp = pd.read_sql(text(q_cxp), conn)

# =========================================================================
# TAB 1: VENTAS & RENDIMIENTO
# =========================================================================
with tab_ventas:
    filtro_msg = []
    if filtro_linea_activo:
        filtro_msg.append(f"Línea: **{linea_label}**")
    if filtro_sublinea_activo:
        filtro_msg.append(f"Sublínea: **{sublinea_label}**")
    if filtro_lab_activo:
        filtro_msg.append(f"Laboratorio: **{lab_label}**")
    if filtro_msg:
        st.info(f"🔎 Filtrando ventas por: {' | '.join(filtro_msg)}")

    st.subheader("Resumen Comercial de Ventas")

    tot_facturado = df_v_prod["total_venta_monto"].sum() if (filtro_linea_activo or filtro_sublinea_activo or filtro_lab_activo) else (df_v_dia["total_facturado"].sum() if not df_v_dia.empty else 0)
    tot_contado = df_v_dia["ventas_contado"].sum() if "ventas_contado" in df_v_dia and not df_v_dia.empty else 0
    tot_credito = df_v_dia["ventas_credito"].sum() if "ventas_credito" in df_v_dia and not df_v_dia.empty else 0
    pct_contado = (tot_contado / tot_facturado * 100) if tot_facturado > 0 else 0
    pct_credito = (tot_credito / tot_facturado * 100) if tot_facturado > 0 else 0

    tot_unidades = df_v_prod["unidades_vendidas"].sum() if not df_v_prod.empty else 0
    tot_operaciones = df_v_dia["numero_operaciones"].sum() if not df_v_dia.empty else 0
    tot_ops_contado = df_v_dia["operaciones_contado"].sum() if "operaciones_contado" in df_v_dia and not df_v_dia.empty else 0
    tot_ops_credito = df_v_dia["operaciones_credito"].sum() if "operaciones_credito" in df_v_dia and not df_v_dia.empty else 0
    ticket_prom = (tot_facturado / tot_operaciones) if tot_operaciones > 0 else 0

    # Helper para renderizar tarjetas KPI blancas con formato idéntico a la imagen
    def format_kpi_num(val):
        if val >= 1_000_000:
            return f"${val/1_000_000:.2f}M"
        elif val >= 1_000:
            return f"${val/1_000:.0f}K"
        return f"${val:,.2f}"

    col_v1, col_v2, col_v3, col_v4, col_v5, col_v6 = st.columns(6)
    
    with col_v1:
        st.markdown(f"""
        <div class="kpi-card-white">
            <div class="kpi-header">
                <span class="kpi-title">Ventas Totales</span>
                <span class="kpi-icon-badge" style="background: rgba(234, 179, 8, 0.15); color: #ca8a04;">💰</span>
            </div>
            <div class="kpi-value">{format_kpi_num(tot_facturado)}</div>
            <svg class="kpi-sparkline" width="70" height="24" viewBox="0 0 70 24" fill="none">
                <path d="M2 18 L18 14 L34 16 L50 8 L68 4" stroke="#10b981" stroke-width="2.5" stroke-linecap="round"/>
            </svg>
        </div>
        """, unsafe_allow_html=True)

    with col_v2:
        st.markdown(f"""
        <div class="kpi-card-white">
            <div class="kpi-header">
                <span class="kpi-title">💵 Ventas Contado</span>
                <span class="kpi-icon-badge" style="background: rgba(16, 185, 129, 0.15); color: #059669;">💲</span>
            </div>
            <div class="kpi-value">{format_kpi_num(tot_contado)}</div>
            <div class="kpi-subtext" style="color: #059669;">
                <span>▲ {pct_contado:.1f}%</span>
                <span style="color: #94a3b8; font-weight: 400;">({int(tot_ops_contado):,})</span>
            </div>
            <svg class="kpi-sparkline" width="70" height="24" viewBox="0 0 70 24" fill="none">
                <path d="M2 20 L20 15 L36 17 L52 9 L68 5" stroke="#059669" stroke-width="2.5" stroke-linecap="round"/>
            </svg>
        </div>
        """, unsafe_allow_html=True)

    with col_v3:
        st.markdown(f"""
        <div class="kpi-card-white">
            <div class="kpi-header">
                <span class="kpi-title">📑 Ventas Crédito</span>
                <span class="kpi-icon-badge" style="background: rgba(59, 130, 246, 0.15); color: #2563eb;">📑</span>
            </div>
            <div class="kpi-value">{format_kpi_num(tot_credito)}</div>
            <div class="kpi-subtext" style="color: #2563eb;">
                <span>▲ {pct_credito:.1f}%</span>
                <span style="color: #94a3b8; font-weight: 400;">({int(tot_ops_credito):,})</span>
            </div>
            <svg class="kpi-sparkline" width="70" height="24" viewBox="0 0 70 24" fill="none">
                <path d="M2 12 L20 16 L38 10 L54 14 L68 8" stroke="#3b82f6" stroke-width="2.5" stroke-linecap="round"/>
            </svg>
        </div>
        """, unsafe_allow_html=True)

    with col_v4:
        st.markdown(f"""
        <div class="kpi-card-white">
            <div class="kpi-header">
                <span class="kpi-title">Nº Operaciones</span>
                <span class="kpi-icon-badge" style="background: rgba(139, 92, 246, 0.15); color: #7c3aed;">📊</span>
            </div>
            <div class="kpi-value">{int(tot_operaciones):,}</div>
            <svg class="kpi-sparkline" width="70" height="24" viewBox="0 0 70 24" fill="none">
                <path d="M2 19 L22 13 L38 15 L52 7 L68 3" stroke="#8b5cf6" stroke-width="2.5" stroke-linecap="round"/>
            </svg>
        </div>
        """, unsafe_allow_html=True)

    with col_v5:
        st.markdown(f"""
        <div class="kpi-card-white">
            <div class="kpi-header">
                <span class="kpi-title">Ticket Promedio</span>
                <span class="kpi-icon-badge" style="background: rgba(249, 115, 22, 0.15); color: #ea580c;">🎟️</span>
            </div>
            <div class="kpi-value">${ticket_prom:.2f}</div>
            <svg class="kpi-sparkline" width="70" height="24" viewBox="0 0 70 24" fill="none">
                <path d="M2 16 L18 10 L36 14 L52 8 L68 12" stroke="#f97316" stroke-width="2.5" stroke-linecap="round"/>
            </svg>
        </div>
        """, unsafe_allow_html=True)

    with col_v6:
        st.markdown(f"""
        <div class="kpi-card-white">
            <div class="kpi-header">
                <span class="kpi-title">Unidades Vendidas</span>
                <span class="kpi-icon-badge" style="background: rgba(234, 179, 8, 0.15); color: #ca8a04;">🏆</span>
            </div>
            <div class="kpi-value">{int(tot_unidades):,}</div>
            <svg class="kpi-sparkline" width="70" height="24" viewBox="0 0 70 24" fill="none">
                <path d="M2 18 L20 12 L38 15 L54 6 L68 2" stroke="#eab308" stroke-width="2.5" stroke-linecap="round"/>
            </svg>
        </div>
        """, unsafe_allow_html=True)

    st.write("")

    # Evolución Diaria de Ventas (Desglosando Contado y Crédito - Últimos 30 Días)
    st.markdown("#### 📈 Evolución Diaria de Ventas: Contado vs Crédito (Últimos 30 Días)")
    if not df_v_dia.empty:
        # Asegurar columnas si vienen de MySQL antiguo
        if "operaciones_contado" not in df_v_dia:
            df_v_dia["operaciones_contado"] = 0
        if "operaciones_credito" not in df_v_dia:
            df_v_dia["operaciones_credito"] = 0

        # Filtrar únicamente los últimos 30 días con respecto a la fecha final seleccionada
        fecha_maxima = pd.to_datetime(df_v_dia["fecha"]).max()
        fecha_corte_30d = fecha_maxima - pd.Timedelta(days=29)
        df_v_dia_30d = df_v_dia[pd.to_datetime(df_v_dia["fecha"]) >= fecha_corte_30d]

        # Calcular unidades vendidas por día desde df_v_prod si no viene en df_v_dia
        if "unidades_vendidas" not in df_v_dia_30d.columns:
            if not df_v_prod.empty:
                df_uds_dia = df_v_prod[pd.to_datetime(df_v_prod["fecha"]) >= fecha_corte_30d].groupby("fecha")["unidades_vendidas"].sum().reset_index()
                df_v_dia_30d = df_v_dia_30d.merge(df_uds_dia, on="fecha", how="left")
                df_v_dia_30d["unidades_vendidas"] = df_v_dia_30d["unidades_vendidas"].fillna(0)
            else:
                df_v_dia_30d["unidades_vendidas"] = 0

        df_dia_agg = df_v_dia_30d.groupby("fecha").agg(
            ventas_contado=("ventas_contado", "sum"),
            ventas_credito=("ventas_credito", "sum"),
            total_facturado=("total_facturado", "sum"),
            numero_operaciones=("numero_operaciones", "sum"),
            operaciones_contado=("operaciones_contado", "sum"),
            operaciones_credito=("operaciones_credito", "sum"),
            unidades_vendidas=("unidades_vendidas", "sum")
        ).reset_index().sort_values("fecha")

        custom_info = list(zip(
            df_dia_agg["total_facturado"],
            df_dia_agg["numero_operaciones"],
            df_dia_agg["ventas_contado"],
            df_dia_agg["operaciones_contado"],
            df_dia_agg["ventas_credito"],
            df_dia_agg["operaciones_credito"],
            df_dia_agg["unidades_vendidas"]
        ))

        fig_evol = go.Figure()

        # Barra Contado (#10B981)
        fig_evol.add_trace(go.Bar(
            x=df_dia_agg["fecha"],
            y=df_dia_agg["ventas_contado"],
            name="💵 Venta Contado",
            marker=dict(
                color="#10B981",
                line=dict(color="#059669", width=1)
            ),
            customdata=custom_info,
            hovertemplate="💵 <b>Contado:</b> $%{y:,.2f} (%{customdata[3]:,} ops)<extra></extra>"
        ))

        # Barra Crédito (#3B82F6)
        fig_evol.add_trace(go.Bar(
            x=df_dia_agg["fecha"],
            y=df_dia_agg["ventas_credito"],
            name="📑 Venta Crédito",
            marker=dict(
                color="#3B82F6",
                line=dict(color="#1E3A8A", width=1)
            ),
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
            hovertemplate="📊 <b>Total Facturado Día:</b> $%{y:,.2f} (%{customdata[1]:,} ops)<br>📦 <b>Unidades Vendidas Día:</b> %{customdata[6]:,} uds<extra></extra>"
        ))

        fig_evol.update_layout(
            title="Facturación Diaria por Modalidad de Cobro (Últimos 30 Días)",
            barmode="stack",
            hovermode="x unified",
            xaxis_title="Fecha",
            yaxis_title="Monto Facturado ($)",
            plot_bgcolor="#5a6876",
            paper_bgcolor="#475564",
            font=dict(color="#f1f5f9"),
            margin=dict(l=40, r=20, t=50, b=40),
            hoverlabel=dict(
                bgcolor="rgba(15, 23, 42, 0.95)",
                bordercolor="#0d9488",
                font_size=13,
                font_family="Inter, sans-serif"
            ),
            xaxis=dict(gridcolor="rgba(255, 255, 255, 0.08)", linecolor="rgba(255, 255, 255, 0.15)"),
            yaxis=dict(gridcolor="rgba(255, 255, 255, 0.08)", linecolor="rgba(255, 255, 255, 0.15)"),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(aplicar_estilo_farma(fig_evol), use_container_width=True)

        # --- Nueva Sección: Evolución Mes a Mes de Ventas, Ticket Promedio y Operaciones ---
        st.markdown("#### 📅 Evolución Mes a Mes: Facturación, Ticket Promedio y Operaciones")
        df_v_mes = df_v_dia.copy()
        df_v_mes["periodo_mes"] = pd.to_datetime(df_v_mes["fecha"]).dt.to_period("M").astype(str)

        # Vincular unidades vendidas por mes desde df_v_prod si no están en df_v_mes
        if "unidades_vendidas" not in df_v_mes.columns:
            if not df_v_prod.empty:
                df_v_prod_copy = df_v_prod.copy()
                df_v_prod_copy["periodo_mes"] = pd.to_datetime(df_v_prod_copy["fecha"]).dt.to_period("M").astype(str)
                df_uds_mes = df_v_prod_copy.groupby("periodo_mes")["unidades_vendidas"].sum().reset_index()
            else:
                df_uds_mes = pd.DataFrame(columns=["periodo_mes", "unidades_vendidas"])
        else:
            df_uds_mes = df_v_mes.groupby("periodo_mes")["unidades_vendidas"].sum().reset_index()

        df_mes_agg = df_v_mes.groupby("periodo_mes").agg(
            total_facturado=("total_facturado", "sum"),
            ventas_contado=("ventas_contado", "sum"),
            ventas_credito=("ventas_credito", "sum"),
            numero_operaciones=("numero_operaciones", "sum"),
            operaciones_contado=("operaciones_contado", "sum"),
            operaciones_credito=("operaciones_credito", "sum")
        ).reset_index().sort_values("periodo_mes")

        if not df_uds_mes.empty:
            df_mes_agg = df_mes_agg.merge(df_uds_mes, on="periodo_mes", how="left")
            df_mes_agg["unidades_vendidas"] = df_mes_agg["unidades_vendidas"].fillna(0).astype(int)
        else:
            df_mes_agg["unidades_vendidas"] = 0

        if not df_mes_agg.empty:
            df_mes_agg["ticket_promedio"] = df_mes_agg["total_facturado"] / df_mes_agg["numero_operaciones"].replace(0, 1)

            col_m_graf, col_m_metr = st.columns([3, 1])

            with col_m_graf:
                from plotly.subplots import make_subplots
                fig_mes = make_subplots(
                    rows=1, cols=1,
                    specs=[[{"secondary_y": True}]]
                )

                # Barras de Facturación
                fig_mes.add_trace(
                    go.Bar(
                        x=df_mes_agg["periodo_mes"],
                        y=df_mes_agg["total_facturado"],
                        name="Facturación Total ($)",
                        marker_color="#2b5876",
                        customdata=df_mes_agg["unidades_vendidas"],
                        hovertemplate="<b>Mes:</b> %{x}<br><b>Venta Total:</b> $%{y:,.2f}<br><b>Unidades:</b> %{customdata:,} uds<extra></extra>"
                    ),
                    secondary_y=False
                )

                # Línea de Ticket Promedio
                fig_mes.add_trace(
                    go.Scatter(
                        x=df_mes_agg["periodo_mes"],
                        y=df_mes_agg["ticket_promedio"],
                        name="Ticket Promedio ($)",
                        mode="lines+markers+text",
                        text=[f"${v:.2f}" for v in df_mes_agg["ticket_promedio"]],
                        textposition="top center",
                        line=dict(color="#e67e22", width=3),
                        marker=dict(size=8),
                        hovertemplate="<b>Ticket Promedio:</b> $%{y:,.2f}<extra></extra>"
                    ),
                    secondary_y=True
                )

                # Línea de Operaciones
                fig_mes.add_trace(
                    go.Scatter(
                        x=df_mes_agg["periodo_mes"],
                        y=df_mes_agg["numero_operaciones"],
                        name="Nº Operaciones",
                        mode="lines+markers",
                        line=dict(color="#9b59b6", width=2, dash="dot"),
                        marker=dict(size=7, symbol="square"),
                        hovertemplate="<b>Operaciones:</b> %{y:,}<extra></extra>"
                    ),
                    secondary_y=False
                )

                fig_mes.update_layout(
                    title="Tendencia Mensual: Facturación vs Ticket Promedio y Operaciones",
                    hovermode="x unified",
                    xaxis_title="Mes (Año-Mes)",
                    plot_bgcolor="#5a6876",
                    paper_bgcolor="#475564",
                    font=dict(color="#f1f5f9"),
                    margin=dict(l=40, r=40, t=50, b=40),
                    legend=dict(orientation="h", yanchor="bottom", y=1.05, xanchor="center", x=0.5),
                    xaxis=dict(gridcolor="rgba(255, 255, 255, 0.08)", linecolor="rgba(255, 255, 255, 0.15)"),
                    yaxis=dict(title="Monto Facturado ($) / Operaciones", gridcolor="rgba(255, 255, 255, 0.08)", linecolor="rgba(255, 255, 255, 0.15)"),
                    yaxis2=dict(title="Ticket Promedio ($)", overlaying="y", side="right", showgrid=False)
                )
                st.plotly_chart(aplicar_estilo_farma(fig_mes), use_container_width=True)

            with col_m_metr:
                st.markdown("##### 📌 Desglose Mensual")
                st.dataframe(
                    df_mes_agg[["periodo_mes", "total_facturado", "ticket_promedio", "numero_operaciones", "unidades_vendidas"]],
                    use_container_width=True,
                    hide_index=True,
                    column_config={
                        "periodo_mes": "Mes",
                        "total_facturado": st.column_config.NumberColumn("Ventas ($)", format="$%.2f"),
                        "ticket_promedio": st.column_config.NumberColumn("Ticket Prom.", format="$%.2f"),
                        "numero_operaciones": st.column_config.NumberColumn("Tickets", format="%d"),
                        "unidades_vendidas": st.column_config.NumberColumn("Unidades", format="%d")
                    }
                )
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
            fig_p.update_layout(
                yaxis={'categoryorder':'total ascending'},
                plot_bgcolor="#5a6876",
                paper_bgcolor="#475564",
                font=dict(color="#f1f5f9"),
                margin=dict(l=40, r=20, t=30, b=40),
                xaxis=dict(gridcolor="rgba(255, 255, 255, 0.08)", linecolor="rgba(255, 255, 255, 0.15)")
            )
            st.plotly_chart(aplicar_estilo_farma(fig_p), use_container_width=True)
        else:
            st.info("Sin registros de productos.")

    with col_lab:
        col_t_l_sub1, col_t_l_sub2 = st.tabs(["🧪 Laboratorios", "🌿 Sublíneas"])
        with col_t_l_sub1:
            st.markdown("#### Participación de Laboratorios (3D Interactive Donut)")
            if not df_v_prod.empty:
                df_lab_agg = df_v_prod.groupby("nombre_laboratorio").agg(
                    total_venta_monto=("total_venta_monto", "sum"),
                    unidades_vendidas=("unidades_vendidas", "sum")
                ).reset_index().sort_values("total_venta_monto", ascending=False)

                # Si hay más de 10 laboratorios, tomar Top 10 y agrupar el resto en "Otros"
                if len(df_lab_agg) > 10:
                    top10_labs = df_lab_agg.head(10)
                    otros_labs = df_lab_agg.iloc[10:]
                    fila_otros = pd.DataFrame([{
                        "nombre_laboratorio": "Otros",
                        "total_venta_monto": otros_labs["total_venta_monto"].sum(),
                        "unidades_vendidas": otros_labs["unidades_vendidas"].sum()
                    }])
                    df_lab_agg = pd.concat([top10_labs, fila_otros], ignore_index=True)

                # Preparar datos JSON para Highcharts 3D Donut
                total_monto_labs = df_lab_agg["total_venta_monto"].sum()
                colores_3d = ["#38bdf8", "#fb7185", "#34d399", "#fb923c", "#a78bfa", "#facc15", "#818cf8", "#f43f5e", "#2dd4bf", "#c084fc", "#94a3b8"]
                
                datos_3d_json = []
                for idx, r_lab in df_lab_agg.iterrows():
                    pct = (r_lab["total_venta_monto"] / total_monto_labs * 100) if total_monto_labs > 0 else 0
                    color_item = colores_3d[idx % len(colores_3d)]
                    datos_3d_json.append({
                        "name": r_lab["nombre_laboratorio"],
                        "y": round(float(r_lab["total_venta_monto"]), 2),
                        "color": color_item,
                        "pct": f"{pct:.1f}%",
                        "uds": int(r_lab["unidades_vendidas"])
                    })

                html_highcharts_3d = f"""
                <!DOCTYPE html>
                <html>
                <head>
                    <meta charset="utf-8">
                    <script src="https://code.highcharts.com/highcharts.js"></script>
                    <script src="https://code.highcharts.com/highcharts-3d.js"></script>
                    <style>
                        body {{
                            background: linear-gradient(135deg, #475564 0%, #5a6876 100%);
                            border-radius: 14px;
                            margin: 0;
                            padding: 0;
                            font-family: 'Inter', sans-serif;
                            overflow: hidden;
                        }}
                        #container3d {{
                            width: 100%;
                            height: 380px;
                        }}
                    </style>
                </head>
                <body>
                    <div id="container3d"></div>
                    <script>
                        Highcharts.chart('container3d', {{
                            chart: {{
                                type: 'pie',
                                backgroundColor: 'transparent',
                                options3d: {{
                                    enabled: true,
                                    alpha: 58,
                                    beta: 0,
                                    depth: 42
                                }}
                            }},
                            title: {{
                                text: null
                            }},
                            tooltip: {{
                                backgroundColor: 'rgba(15, 23, 42, 0.95)',
                                borderColor: '#38bdf8',
                                borderRadius: 10,
                                style: {{
                                    color: '#f8fafc',
                                    fontSize: '13px'
                                }},
                                formatter: function () {{
                                    return '<b>' + this.point.name + '</b><br/>' +
                                           'Venta Total: <b>$' + Highcharts.numberFormat(this.y, 2) + '</b><br/>' +
                                           'Participación: <b>' + this.point.pct + '</b><br/>' +
                                           'Unidades: <b>' + Highcharts.numberFormat(this.point.uds, 0) + ' uds</b>';
                                }}
                            }},
                            plotOptions: {{
                                pie: {{
                                    innerSize: '55%',
                                    depth: 42,
                                    allowPointSelect: true,
                                    cursor: 'pointer',
                                    dataLabels: {{
                                        enabled: true,
                                        format: '<span style="color:#e2e8f0; font-weight:600;">{{point.name}}</span>: {{point.pct}}',
                                        connectorColor: 'rgba(255,255,255,0.2)',
                                        style: {{
                                            textOutline: 'none',
                                            fontSize: '11px'
                                        }}
                                    }}
                                }}
                            }},
                            series: [{{
                                name: 'Ventas',
                                data: {json.dumps(datos_3d_json)}
                            }}],
                            credits: {{
                                enabled: false
                            }}
                        }});
                    </script>
                </body>
                </html>
                """
                components.html(html_highcharts_3d, height=390)
            else:
                st.info("Sin registros de laboratorio.")

        with col_t_l_sub2:
            st.markdown("#### Ventas por Sublínea de Producto")
            if not df_v_prod.empty and "descripcion_sublinea" in df_v_prod.columns:
                df_sublin_agg = df_v_prod.groupby("descripcion_sublinea").agg(
                    total_venta_monto=("total_venta_monto", "sum"),
                    unidades_vendidas=("unidades_vendidas", "sum")
                ).reset_index().sort_values("total_venta_monto", ascending=False)

                fig_subl_v = px.pie(
                    df_sublin_agg,
                    names="descripcion_sublinea",
                    values="total_venta_monto",
                    hole=0.4,
                    color_discrete_sequence=px.colors.qualitative.Safe,
                    custom_data=["unidades_vendidas"]
                )
                fig_subl_v.update_traces(
                    hovertemplate="<b>Sublínea:</b> %{label}<br>" +
                                  "<b>Venta Total:</b> $%{value:,.2f}<br>" +
                                  "<b>Participación:</b> %{percent}<br>" +
                                  "<b>Unidades Vendidas:</b> %{customdata[0]:,}<extra></extra>"
                )
                st.plotly_chart(aplicar_estilo_farma(fig_subl_v), use_container_width=True)
            else:
                st.info("Sin registros de sublínea.")

    st.divider()

    # --- COMPARATIVA DE VENTAS ENTRE SUCURSALES ---
    st.markdown("#### 🏢 Comparativa de Rendimiento Comercial entre Sucursales")
    if not df_v_prod.empty:
        df_v_suc_comp = df_v_prod.copy()
        if "codigo_sucursal" not in df_v_suc_comp.columns or "nombre_sucursal" not in df_v_suc_comp.columns:
            cols_merge_s = [c for c in ["id_sucursal", "codigo_sucursal", "nombre"] if c in df_sucursales.columns]
            df_v_suc_comp = df_v_suc_comp.merge(
                df_sucursales[cols_merge_s].rename(columns={"nombre": "nombre_sucursal"}),
                on="id_sucursal",
                how="left"
            )
        if "nombre_sucursal" not in df_v_suc_comp.columns and "nombre" in df_v_suc_comp.columns:
            df_v_suc_comp["nombre_sucursal"] = df_v_suc_comp["nombre"]

        cols_grp_vsuc = [c for c in ["codigo_sucursal", "nombre_sucursal"] if c in df_v_suc_comp.columns]
        if not cols_grp_vsuc:
            cols_grp_vsuc = ["id_sucursal"]

        df_suc_v_agg = df_v_suc_comp.groupby(cols_grp_vsuc).agg(
            total_facturado=("total_venta_monto", "sum"),
            unidades_vendidas=("unidades_vendidas", "sum"),
            variedad_articulos=("id_producto", "nunique")
        ).reset_index().sort_values("total_facturado", ascending=False)

        col_g_vsuc, col_t_vsuc = st.columns([3, 2])
        with col_g_vsuc:
            fig_vsuc = px.bar(
                df_suc_v_agg,
                x="total_facturado",
                y="nombre_sucursal",
                orientation="h",
                labels={"total_facturado": "Facturación Total ($)", "nombre_sucursal": "Sucursal"},
                title="Ventas Totales por Farmacia ($)",
                color="total_facturado",
                color_continuous_scale="Teal",
                custom_data=["codigo_sucursal", "unidades_vendidas", "variedad_articulos"]
            )
            fig_vsuc.update_traces(
                hovertemplate="<b>%{y}</b> [%{customdata[0]}]<br><b>Facturación:</b> $%{x:,.2f}<br><b>Unidades:</b> %{customdata[1]:,} uds<br><b>Artículos Activos:</b> %{customdata[2]}<extra></extra>"
            )
            fig_vsuc.update_layout(yaxis={'categoryorder':'total ascending'}, height=340)
            st.plotly_chart(aplicar_estilo_farma(fig_vsuc), use_container_width=True)

        with col_t_vsuc:
            tot_gral_v = df_suc_v_agg["total_facturado"].sum()
            df_suc_v_agg["participacion"] = (df_suc_v_agg["total_facturado"] / tot_gral_v * 100) if tot_gral_v > 0 else 0
            st.markdown("##### 📌 Ranking de Sucursales")
            st.dataframe(
                df_suc_v_agg[["codigo_sucursal", "nombre_sucursal", "total_facturado", "unidades_vendidas", "participacion"]],
                use_container_width=True,
                hide_index=True,
                column_config={
                    "codigo_sucursal": "Cód.",
                    "nombre_sucursal": "Farmacia",
                    "total_facturado": st.column_config.NumberColumn("Ventas ($)", format="$%.2f"),
                    "unidades_vendidas": st.column_config.NumberColumn("Unidades", format="%d"),
                    "participacion": st.column_config.NumberColumn("% Part.", format="%.1f%%")
                }
            )

    st.divider()

    # Tabla Resumen de Ventas por Laboratorio
    st.markdown("#### 🧪 Resumen de Ventas por Laboratorio")
    if not df_v_prod.empty:
        df_resumen_lab = df_v_prod.groupby(["codigo_laboratorio", "nombre_laboratorio"]).agg(
            total_articulos=("id_producto", "nunique"),
            unidades_vendidas=("unidades_vendidas", "sum"),
            total_venta_monto=("total_venta_monto", "sum")
        ).reset_index()

        total_general_ventas = df_resumen_lab["total_venta_monto"].sum()
        df_resumen_lab["participacion"] = (df_resumen_lab["total_venta_monto"] / total_general_ventas * 100) if total_general_ventas > 0 else 0
        df_resumen_lab["precio_promedio"] = round(df_resumen_lab["total_venta_monto"] / df_resumen_lab["unidades_vendidas"], 2)
        df_resumen_lab = df_resumen_lab.sort_values("total_venta_monto", ascending=False)

        st.dataframe(
            df_resumen_lab,
            use_container_width=True,
            column_config={
                "codigo_laboratorio": "Cód. Lab",
                "nombre_laboratorio": "Laboratorio / Marca",
                "total_articulos": st.column_config.NumberColumn("Cant. Artículos", format="%d"),
                "unidades_vendidas": st.column_config.NumberColumn("Unidades Vendidas", format="%d"),
                "precio_promedio": st.column_config.NumberColumn("Precio Prom. Unit. ($)", format="$%.2f"),
                "total_venta_monto": st.column_config.NumberColumn("Total Facturado ($)", format="$%.2f"),
                "participacion": st.column_config.NumberColumn("% Participación", format="%.2f%%")
            }
        )
    else:
        st.info("Sin registros de laboratorios para este período.")

    st.divider()

    # Tabla Detallada de Todos los Artículos Vendidos
    st.markdown("#### 📋 Detalle Completo de Artículos Vendidos")
    if not df_v_prod.empty:
        cols_art_v = ["codigo_articulo", "codigo_barras", "nombre_producto", "descripcion_linea"]
        if "descripcion_sublinea" in df_v_prod.columns:
            cols_art_v.append("descripcion_sublinea")
        cols_art_v.append("nombre_laboratorio")

        df_detalle_art = df_v_prod.groupby(cols_art_v).agg(
            unidades_vendidas=("unidades_vendidas", "sum"),
            total_venta_monto=("total_venta_monto", "sum")
        ).reset_index()

        df_detalle_art["precio_promedio"] = round(df_detalle_art["total_venta_monto"] / df_detalle_art["unidades_vendidas"], 2)
        df_detalle_art = df_detalle_art.sort_values("total_venta_monto", ascending=False)

        cfg_art_v = {
            "codigo_articulo": "Cód. Artículo",
            "codigo_barras": "Código de Barras",
            "nombre_producto": "Descripción del Producto",
            "descripcion_linea": "Línea / Categoría",
            "nombre_laboratorio": "Laboratorio",
            "unidades_vendidas": st.column_config.NumberColumn("Unidades", format="%d"),
            "precio_promedio": st.column_config.NumberColumn("Precio Prom. ($)", format="$%.2f"),
            "total_venta_monto": st.column_config.NumberColumn("Total Facturado ($)", format="$%.2f")
        }
        if "descripcion_sublinea" in df_v_prod.columns:
            cfg_art_v["descripcion_sublinea"] = "Sublínea"

        st.dataframe(
            df_detalle_art,
            use_container_width=True,
            column_config=cfg_art_v
        )
    else:
        st.info("Sin registros de artículos vendidos para este período.")

    st.divider()

    # Tabla: Ventas por Producto por Sucursal con Filtro Dinámico de Producto
    st.markdown("#### 🏢 Ventas por Producto por Sucursal")
    if not df_v_prod.empty:
        # Enriquecer con nombre de sucursal si aún no está presente
        df_vp_suc = df_v_prod.copy()
        if "nombre_sucursal" not in df_vp_suc.columns:
            df_vp_suc = df_vp_suc.merge(
                df_sucursales[["id_sucursal", "codigo_sucursal", "nombre"]].rename(columns={"nombre": "nombre_sucursal"}),
                on="id_sucursal",
                how="left"
            )

        # Buscador / selector de producto para filtrar la tabla
        # Construir opciones de productos disponibles en el set filtrado
        prods_unicos = df_vp_suc[["id_producto", "codigo_articulo", "nombre_producto"]].drop_duplicates().sort_values("nombre_producto")
        opciones_prod_filtro = {"Todos los productos": None}
        for _, r_p in prods_unicos.iterrows():
            opciones_prod_filtro[f"[{r_p['codigo_articulo']}] {r_p['nombre_producto']}"] = r_p["id_producto"]

        col_f_prod, col_f_info = st.columns([2, 1])
        with col_f_prod:
            sel_prod_label = st.selectbox(
                "🔍 Filtrar por Producto (opcional):",
                options=list(opciones_prod_filtro.keys()),
                key="filtro_prod_sucursal"
            )
        sel_prod_id = opciones_prod_filtro[sel_prod_label]

        df_vp_suc_filtrado = df_vp_suc if sel_prod_id is None else df_vp_suc[df_vp_suc["id_producto"] == sel_prod_id]

        with col_f_info:
            tot_uds_f = df_vp_suc_filtrado["unidades_vendidas"].sum()
            tot_mnt_f = df_vp_suc_filtrado["total_venta_monto"].sum()
            st.metric("Total Unidades", f"{tot_uds_f:,.0f}")
            st.caption(f"Monto Total: **${tot_mnt_f:,.2f}**")

        df_tabla_prod_suc = df_vp_suc_filtrado.groupby(
            ["codigo_sucursal", "nombre_sucursal", "codigo_articulo", "nombre_producto", "nombre_laboratorio"]
        ).agg(
            unidades_vendidas=("unidades_vendidas", "sum"),
            total_venta_monto=("total_venta_monto", "sum")
        ).reset_index()

        df_tabla_prod_suc["precio_promedio"] = round(
            df_tabla_prod_suc["total_venta_monto"] / df_tabla_prod_suc["unidades_vendidas"], 2
        )
        df_tabla_prod_suc = df_tabla_prod_suc.sort_values(
            ["nombre_sucursal", "total_venta_monto"],
            ascending=[True, False]
        )

        st.dataframe(
            df_tabla_prod_suc,
            use_container_width=True,
            height=420,
            column_config={
                "codigo_sucursal": "Cód. Sucursal",
                "nombre_sucursal": "Sucursal / Farmacia",
                "codigo_articulo": "Cód. Artículo",
                "nombre_producto": "Producto",
                "nombre_laboratorio": "Laboratorio",
                "unidades_vendidas": st.column_config.NumberColumn("Unidades Vendidas", format="%d"),
                "precio_promedio": st.column_config.NumberColumn("Precio Prom. ($)", format="$%.2f"),
                "total_venta_monto": st.column_config.NumberColumn("Total Facturado ($)", format="$%.2f")
            }
        )

        # Resumen Visual con Badges de Laboratorios (Muestra destacada Top 10)
        with st.expander("✨ Vista Rápida Estilizada con Badges de Laboratorio", expanded=False):
            def badge_lab_html(nombre_lab):
                n_lower = str(nombre_lab).lower()
                if "pfizer" in n_lower:
                    cls = "badge-pfizer"
                elif "novartis" in n_lower:
                    cls = "badge-novartis"
                elif "leti" in n_lower:
                    cls = "badge-leti"
                elif "calox" in n_lower:
                    cls = "badge-calox"
                else:
                    cls = "badge-other"
                return f'<span class="badge-lab {cls}">{nombre_lab}</span>'

            filas_html = ""
            for _, r_b in df_tabla_prod_suc.head(15).iterrows():
                b_html = badge_lab_html(r_b["nombre_laboratorio"])
                filas_html += f"""
                <tr class="table-glass-row" style="border-bottom: 1px solid rgba(255,255,255,0.04); transition: background 0.15s ease;">
                    <td style="padding: 10px 14px; font-weight: 600; color: #38bdf8;">[{r_b['codigo_sucursal']}] {r_b['nombre_sucursal']}</td>
                    <td style="padding: 10px 14px; color: #94a3b8; font-family: monospace;">{r_b['codigo_articulo']}</td>
                    <td style="padding: 10px 14px; color: #f1f5f9; font-weight: 500;">{r_b['nombre_producto']}</td>
                    <td style="padding: 10px 14px;">{b_html}</td>
                    <td style="padding: 10px 14px; text-align: right; color: #e2e8f0;">{int(r_b['unidades_vendidas']):,}</td>
                    <td style="padding: 10px 14px; text-align: right; color: #34d399; font-weight: 600;">${r_b['total_venta_monto']:,.2f}</td>
                </tr>
                """

            tabla_estilizada = f"""
            <div style="background: rgba(15, 23, 42, 0.45); backdrop-filter: blur(12px); border-radius: 12px; border: 1px solid rgba(255,255,255,0.06); overflow: hidden;">
                <table style="width: 100%; border-collapse: collapse; font-size: 0.88rem;">
                    <thead>
                        <tr style="background: rgba(15, 23, 42, 0.7); border-bottom: 1px solid rgba(255,255,255,0.08); text-transform: uppercase; font-size: 0.75rem; letter-spacing: 0.05em; color: #94a3b8;">
                            <th style="padding: 10px 14px; text-align: left;">Sucursal</th>
                            <th style="padding: 10px 14px; text-align: left;">Cód. Artículo</th>
                            <th style="padding: 10px 14px; text-align: left;">Producto</th>
                            <th style="padding: 10px 14px; text-align: left;">Laboratorio</th>
                            <th style="padding: 10px 14px; text-align: right;">Unidades</th>
                            <th style="padding: 10px 14px; text-align: right;">Total Facturado</th>
                        </tr>
                    </thead>
                    <tbody>
                        {filas_html}
                    </tbody>
                </table>
            </div>
            """
            st.markdown(tabla_estilizada, unsafe_allow_html=True)
    else:
        st.info("Sin registros de productos por sucursal para este período.")

# =========================================================================
# TAB 2: COMPRAS & PROVEEDORES
# =========================================================================
with tab_compras:
    msg_comp = []
    if filtro_tipo_prov_activo:
        msg_comp.append(f"Tipo Prov: **{tipo_prov_sel}**")
    if filtro_seg_prov_activo:
        msg_comp.append(f"Segmento: **{seg_prov_sel}**")
    if filtro_prov_activo:
        msg_comp.append(f"Proveedor: **{prov_label}**")
    if filtro_lab_activo:
        msg_comp.append(f"Laboratorio: **{lab_label}**")
    if filtro_linea_activo:
        msg_comp.append(f"Línea: **{linea_label}**")
    if filtro_sublinea_activo:
        msg_comp.append(f"Sublínea: **{sublinea_label}**")
    if msg_comp:
        st.info(f"🔎 Compras filtradas por: {' | '.join(msg_comp)}")

    st.subheader("Gestión de Compras y Abastecimiento de Mercancía")

    tot_comp_monto = df_comp["total_compra_monto"].sum() if not df_comp.empty else (df_c_dia["total_comprado"].sum() if not df_c_dia.empty else 0)
    tot_comp_uds = df_comp["unidades_compradas"].sum() if not df_comp.empty else (df_c_dia["unidades_compradas"].sum() if not df_c_dia.empty else 0)
    cant_proveedores_activos = df_comp["id_proveedor"].nunique() if not df_comp.empty else 0
    tot_cmp_contado = df_c_dia["compras_contado"].sum() if "compras_contado" in df_c_dia and not df_c_dia.empty else 0
    tot_cmp_credito = df_c_dia["compras_credito"].sum() if "compras_credito" in df_c_dia and not df_c_dia.empty else 0
    tot_facturas_compra = df_c_dia["numero_facturas_compra"].sum() if "numero_facturas_compra" in df_c_dia and not df_c_dia.empty else 0

    col_cmp1, col_cmp2, col_cmp3, col_cmp4, col_cmp5 = st.columns(5)
    col_cmp1.metric("Inversión Total en Compras", f"${tot_comp_monto:,.2f}")
    col_cmp2.metric("💵 Compras Contado", f"${tot_cmp_contado:,.2f}")
    col_cmp3.metric("📑 Compras Crédito", f"${tot_cmp_credito:,.2f}")
    col_cmp4.metric("Unidades Ingresadas", f"{int(tot_comp_uds):,}")
    col_cmp5.metric("Nº Facturas de Compra", f"{int(tot_facturas_compra):,}")

    st.divider()

    col_c_izq, col_c_der = st.columns(2)
    with col_c_izq:
        st.markdown("#### 📅 Compras Diarias: Contado vs Crédito (Últimos 30 Días)")
        if not df_c_dia.empty:
            fecha_max_comp = pd.to_datetime(df_c_dia["fecha"]).max()
            fecha_corte_comp_30d = fecha_max_comp - pd.Timedelta(days=29)
            df_c_dia_30d = df_c_dia[pd.to_datetime(df_c_dia["fecha"]) >= fecha_corte_comp_30d]

            df_c_dia_agg = df_c_dia_30d.groupby("fecha").agg(
                compras_contado=("compras_contado", "sum"),
                compras_credito=("compras_credito", "sum"),
                total_comprado=("total_comprado", "sum"),
                unidades_compradas=("unidades_compradas", "sum"),
                numero_facturas_compra=("numero_facturas_compra", "sum")
            ).reset_index().sort_values("fecha")

            custom_info_cmp = list(zip(
                df_c_dia_agg["total_comprado"],
                df_c_dia_agg["unidades_compradas"],
                df_c_dia_agg["numero_facturas_compra"],
                df_c_dia_agg["compras_contado"],
                df_c_dia_agg["compras_credito"]
            ))

            fig_cf = go.Figure()

            # Barra Compras Contado
            fig_cf.add_trace(go.Bar(
                x=df_c_dia_agg["fecha"],
                y=df_c_dia_agg["compras_contado"],
                name="💵 Compra Contado",
                marker_color="#27ae60",
                customdata=custom_info_cmp,
                hovertemplate="💵 <b>Contado:</b> $%{y:,.2f}<extra></extra>"
            ))

            # Barra Compras Crédito
            fig_cf.add_trace(go.Bar(
                x=df_c_dia_agg["fecha"],
                y=df_c_dia_agg["compras_credito"],
                name="📑 Compra Crédito",
                marker_color="#e67e22",
                customdata=custom_info_cmp,
                hovertemplate="📑 <b>Crédito:</b> $%{y:,.2f}<extra></extra>"
            ))

            # Marcador totalizador para hover unificado
            fig_cf.add_trace(go.Scatter(
                x=df_c_dia_agg["fecha"],
                y=df_c_dia_agg["total_comprado"],
                name="Total Comprado",
                mode="markers",
                marker=dict(size=0, opacity=0),
                customdata=custom_info_cmp,
                hovertemplate="📦 <b>Total Compras Día:</b> $%{y:,.2f}<br><b>Unidades:</b> %{customdata[1]:,} | <b>Facturas:</b> %{customdata[2]}<extra></extra>"
            ))

            fig_cf.update_layout(
                title="Compras Diarias por Modalidad de Pago (Últimos 30 Días)",
                barmode="stack",
                hovermode="x unified",
                xaxis_title="Fecha",
                yaxis_title="Monto Inversión ($)",
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
            )
            st.plotly_chart(aplicar_estilo_farma(fig_cf), use_container_width=True)
        else:
            st.info("Sin compras registradas para estos filtros.")

    # --- Sección: Compras por Tipo de Proveedor, Segmento y Proveedores ---
    col_c_tipo_prv, col_c_seg_prv, col_c_der = st.columns([1, 1, 1.2])

    with col_c_tipo_prv:
        col_t_tprv, col_c_crit_tprv = st.columns([2, 1])
        with col_t_tprv:
            st.markdown("#### 🏷️ Por Tipo")
        with col_c_crit_tprv:
            criterio_orden_tprv = st.selectbox(
                "Ordenar por:",
                options=["Inversión Total ($)", "Unidades Compradas"],
                index=0,
                key="criterio_tprv_compras"
            )

        if not df_comp.empty and "tipo_proveedor" in df_comp.columns:
            df_c_tprov = df_comp.groupby("tipo_proveedor").agg(
                total_compra_monto=("total_compra_monto", "sum"),
                unidades_compradas=("unidades_compradas", "sum")
            ).reset_index()

            col_ord_t = "total_compra_monto" if criterio_orden_tprv == "Inversión Total ($)" else "unidades_compradas"
            df_c_tprov = df_c_tprov.sort_values(col_ord_t, ascending=False)

            if criterio_orden_tprv == "Inversión Total ($)":
                eje_x_tprv = "total_compra_monto"
                lbl_x_tprv = "Inversión ($)"
                paleta_tprv = "Teal"
            else:
                eje_x_tprv = "unidades_compradas"
                lbl_x_tprv = "Unidades Compradas"
                paleta_tprv = "GnBu"

            fig_tprv = px.bar(
                df_c_tprov,
                x=eje_x_tprv,
                y="tipo_proveedor",
                orientation="h",
                labels={eje_x_tprv: lbl_x_tprv, "tipo_proveedor": "Tipo"},
                color=eje_x_tprv,
                color_continuous_scale=paleta_tprv,
                custom_data=["tipo_proveedor", "unidades_compradas", "total_compra_monto"]
            )
            fig_tprv.update_traces(
                hovertemplate="<b>Tipo:</b> %{y}<br>" +
                              "<b>Inversión Total:</b> $%{customdata[2]:,.2f}<br>" +
                              "<b>Unidades Compradas:</b> %{customdata[1]:,}<extra></extra>"
            )
            fig_tprv.update_layout(yaxis={'categoryorder':'total ascending'})
            st.plotly_chart(aplicar_estilo_farma(fig_tprv), use_container_width=True)
        else:
            st.info("Sin datos para tipos de proveedor.")

    with col_c_seg_prv:
        col_t_seg, col_c_crit_seg = st.columns([2, 1])
        with col_t_seg:
            st.markdown("#### 🗂️ Por Segmento")
        with col_c_crit_seg:
            criterio_orden_seg = st.selectbox(
                "Ordenar por:",
                options=["Inversión Total ($)", "Unidades Compradas"],
                index=0,
                key="criterio_seg_compras"
            )

        if not df_comp.empty and "segmento" in df_comp.columns:
            df_c_seg = df_comp.groupby("segmento").agg(
                total_compra_monto=("total_compra_monto", "sum"),
                unidades_compradas=("unidades_compradas", "sum")
            ).reset_index()

            col_ord_s = "total_compra_monto" if criterio_orden_seg == "Inversión Total ($)" else "unidades_compradas"
            df_c_seg = df_c_seg.sort_values(col_ord_s, ascending=False)

            if criterio_orden_seg == "Inversión Total ($)":
                eje_x_seg = "total_compra_monto"
                lbl_x_seg = "Inversión ($)"
                paleta_seg = "Purples"
            else:
                eje_x_seg = "unidades_compradas"
                lbl_x_seg = "Unidades Compradas"
                paleta_seg = "BuPu"

            fig_seg = px.bar(
                df_c_seg,
                x=eje_x_seg,
                y="segmento",
                orientation="h",
                labels={eje_x_seg: lbl_x_seg, "segmento": "Segmento"},
                color=eje_x_seg,
                color_continuous_scale=paleta_seg,
                custom_data=["segmento", "unidades_compradas", "total_compra_monto"]
            )
            fig_seg.update_traces(
                hovertemplate="<b>Segmento:</b> %{y}<br>" +
                              "<b>Inversión Total:</b> $%{customdata[2]:,.2f}<br>" +
                              "<b>Unidades Compradas:</b> %{customdata[1]:,}<extra></extra>"
            )
            fig_seg.update_layout(yaxis={'categoryorder':'total ascending'})
            st.plotly_chart(aplicar_estilo_farma(fig_seg), use_container_width=True)
        else:
            st.info("Sin datos para segmentos de proveedor.")

    with col_c_der:
        col_t_prov, col_c_crit_prov = st.columns([2, 1])
        with col_t_prov:
            st.markdown("#### 🚚 Top 10 Droguerías / Provs")
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
                df_top_prov = df_c_prov.sort_values("total_compra_monto", ascending=False).head(10)
                eje_x_prov = "total_compra_monto"
                lbl_x_prov = "Inversión ($)"
                paleta_prov = "Oranges"
            else:
                df_top_prov = df_c_prov.sort_values("unidades_compradas", ascending=False).head(10)
                eje_x_prov = "unidades_compradas"
                lbl_x_prov = "Unidades Compradas"
                paleta_prov = "YlOrBr"

            fig_cp = px.bar(
                df_top_prov,
                x=eje_x_prov,
                y="nombre_proveedor",
                orientation="h",
                labels={eje_x_prov: lbl_x_prov, "nombre_proveedor": "Proveedor"},
                color=eje_x_prov,
                color_continuous_scale=paleta_prov,
                custom_data=["codigo_proveedor", "unidades_compradas", "total_compra_monto"]
            )
            fig_cp.update_traces(
                hovertemplate="<b>Proveedor:</b> %{y} [%{customdata[0]}]<br>" +
                              "<b>Inversión Total:</b> $%{customdata[2]:,.2f}<br>" +
                              "<b>Unidades Adquiridas:</b> %{customdata[1]:,}<extra></extra>"
            )
            fig_cp.update_layout(yaxis={'categoryorder':'total ascending'})
            st.plotly_chart(aplicar_estilo_farma(fig_cp), use_container_width=True)
        else:
            st.info("Sin datos de proveedores.")

    st.divider()

    # Compras por Laboratorio (Top 10 + Otros con selector de ordenamiento)
    col_c_lab_bar, col_c_lab_pie = st.columns([3, 2])
    with col_c_lab_bar:
        col_t_lab_c, col_c_crit_lab = st.columns([2, 1])
        with col_t_lab_c:
            st.markdown("#### 🧪 Top 10 Compras por Laboratorio")
        with col_c_crit_lab:
            criterio_orden_lab = st.selectbox(
                "Ordenar por:",
                options=["Inversión Total ($)", "Unidades Compradas"],
                index=0,
                key="criterio_lab_compras"
            )

        if not df_comp.empty:
            df_c_lab_raw = df_comp.groupby("nombre_laboratorio").agg(
                total_compra_monto=("total_compra_monto", "sum"),
                unidades_compradas=("unidades_compradas", "sum")
            ).reset_index()

            # Ordenar según criterio seleccionado
            col_orden = "total_compra_monto" if criterio_orden_lab == "Inversión Total ($)" else "unidades_compradas"
            df_c_lab_sorted = df_c_lab_raw.sort_values(col_orden, ascending=False)

            # Separar Top 10 y agrupar el resto en "Otros"
            if len(df_c_lab_sorted) > 10:
                df_top10 = df_c_lab_sorted.head(10).copy()
                df_resto = df_c_lab_sorted.iloc[10:]

                fila_otros = pd.DataFrame([{
                    "nombre_laboratorio": "Otros Laboratorios",
                    "total_compra_monto": df_resto["total_compra_monto"].sum(),
                    "unidades_compradas": df_resto["unidades_compradas"].sum()
                }])
                df_c_lab_ordenado = pd.concat([df_top10, fila_otros], ignore_index=True)
            else:
                df_c_lab_ordenado = df_c_lab_sorted.copy()

            if criterio_orden_lab == "Inversión Total ($)":
                eje_x_lab = "total_compra_monto"
                lbl_x_lab = "Inversión ($)"
                paleta_lab = "Viridis"
            else:
                eje_x_lab = "unidades_compradas"
                lbl_x_lab = "Unidades Compradas"
                paleta_lab = "Purples"

            fig_clab = px.bar(
                df_c_lab_ordenado,
                x=eje_x_lab,
                y="nombre_laboratorio",
                orientation="h",
                labels={eje_x_lab: lbl_x_lab, "nombre_laboratorio": "Laboratorio"},
                title="Top 10 Laboratorios + Otros",
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
            st.plotly_chart(aplicar_estilo_farma(fig_clab), use_container_width=True)
        else:
            st.info("Sin compras por laboratorio.")

    with col_c_lab_pie:
        st.markdown("#### 🥧 Distribución de Compras por Laboratorio")
        if not df_comp.empty:
            fig_clab_pie = px.pie(
                df_c_lab_ordenado,
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
            st.plotly_chart(aplicar_estilo_farma(fig_clab_pie), use_container_width=True)
        else:
            st.info("Sin datos para distribución de laboratorios.")

    # --- Nueva Sección: Evolución Mes a Mes de Compras por Laboratorio y por Proveedor ---
    st.markdown("#### 📅 Evolución Mes a Mes de Compras: Por Laboratorio y por Proveedor")
    if not df_comp.empty:
        df_comp_mes = df_comp.copy()
        df_comp_mes["periodo_mes"] = pd.to_datetime(df_comp_mes["fecha"]).dt.to_period("M").astype(str)

        col_cmes_lab, col_cmes_prv = st.columns(2)

        with col_cmes_lab:
            st.markdown("##### 🧪 Compras Mensuales por Laboratorio ($) [Top 10 + Otros]")
            # Identificar Top 10 laboratorios globales en el período
            top10_labs_globales = df_comp.groupby("nombre_laboratorio")["total_compra_monto"].sum().nlargest(10).index.tolist()
            df_comp_mes_lab = df_comp_mes.copy()
            df_comp_mes_lab["lab_display"] = df_comp_mes_lab["nombre_laboratorio"].apply(
                lambda x: x if x in top10_labs_globales else "Otros Laboratorios"
            )

            # Orden alfabético: los nombres de laboratorios de A a Z y "Otros Laboratorios" al final
            labs_alfabeticos = sorted([l for l in df_comp_mes_lab["lab_display"].unique() if l != "Otros Laboratorios"])
            if "Otros Laboratorios" in df_comp_mes_lab["lab_display"].values:
                labs_alfabeticos.append("Otros Laboratorios")

            df_mes_lab = df_comp_mes_lab.groupby(["periodo_mes", "lab_display"]).agg(
                total_compra_monto=("total_compra_monto", "sum"),
                unidades_compradas=("unidades_compradas", "sum")
            ).reset_index().sort_values("periodo_mes")

            fig_mes_lab = px.bar(
                df_mes_lab,
                x="periodo_mes",
                y="total_compra_monto",
                color="lab_display",
                category_orders={"lab_display": labs_alfabeticos},
                labels={"periodo_mes": "Mes", "total_compra_monto": "Inversión ($)", "lab_display": "Laboratorio"},
                barmode="stack",
                custom_data=["lab_display", "unidades_compradas"]
            )
            fig_mes_lab.update_traces(
                hovertemplate="<b>Mes:</b> %{x}<br><b>Laboratorio:</b> %{customdata[0]}<br><b>Inversión:</b> $%{y:,.2f}<br><b>Unidades:</b> %{customdata[1]:,}<extra></extra>"
            )
            fig_mes_lab.update_layout(
                hovermode="x unified",
                legend=dict(
                    orientation="h",
                    yanchor="top",
                    y=-0.22,
                    xanchor="center",
                    x=0.5,
                    title_text=""
                ),
                margin=dict(t=20, b=80)
            )
            st.plotly_chart(aplicar_estilo_farma(fig_mes_lab), use_container_width=True)

        with col_cmes_prv:
            st.markdown("##### 🚚 Compras Mensuales por Proveedor / Droguería ($) [Top 10 + Otros]")
            # Identificar Top 10 proveedores globales en el período
            top10_prvs_globales = df_comp.groupby("nombre_proveedor")["total_compra_monto"].sum().nlargest(10).index.tolist()
            df_comp_mes_prv = df_comp_mes.copy()
            df_comp_mes_prv["prv_display"] = df_comp_mes_prv["nombre_proveedor"].apply(
                lambda x: x if x in top10_prvs_globales else "Otros Proveedores"
            )

            # Orden alfabético: los nombres de droguerías de A a Z y "Otros Proveedores" al final
            prvs_alfabeticos = sorted([p for p in df_comp_mes_prv["prv_display"].unique() if p != "Otros Proveedores"])
            if "Otros Proveedores" in df_comp_mes_prv["prv_display"].values:
                prvs_alfabeticos.append("Otros Proveedores")

            df_mes_prv = df_comp_mes_prv.groupby(["periodo_mes", "prv_display"]).agg(
                total_compra_monto=("total_compra_monto", "sum"),
                unidades_compradas=("unidades_compradas", "sum")
            ).reset_index().sort_values("periodo_mes")

            fig_mes_prv = px.bar(
                df_mes_prv,
                x="periodo_mes",
                y="total_compra_monto",
                color="prv_display",
                category_orders={"prv_display": prvs_alfabeticos},
                labels={"periodo_mes": "Mes", "total_compra_monto": "Inversión ($)", "prv_display": "Droguería"},
                barmode="stack",
                custom_data=["prv_display", "unidades_compradas"]
            )
            fig_mes_prv.update_traces(
                hovertemplate="<b>Mes:</b> %{x}<br><b>Droguería:</b> %{customdata[0]}<br><b>Inversión:</b> $%{y:,.2f}<br><b>Unidades:</b> %{customdata[1]:,}<extra></extra>"
            )
            fig_mes_prv.update_layout(
                hovermode="x unified",
                legend=dict(
                    orientation="h",
                    yanchor="top",
                    y=-0.22,
                    xanchor="center",
                    x=0.5,
                    title_text=""
                ),
                margin=dict(t=20, b=80)
            )
            st.plotly_chart(aplicar_estilo_farma(fig_mes_prv), use_container_width=True)
    else:
        st.info("Sin registros de compras para la evolución mensual.")

    st.divider()

    # Tabla Resumen de Compras por Laboratorio
    st.markdown("#### 🧪 Resumen de Compras por Laboratorio")
    if not df_comp.empty:
        df_resumen_comp_lab = df_comp.groupby(["codigo_laboratorio", "nombre_laboratorio"]).agg(
            total_articulos=("id_producto", "nunique"),
            unidades_compradas=("unidades_compradas", "sum"),
            total_compra_monto=("total_compra_monto", "sum")
        ).reset_index()

        total_general_compras = df_resumen_comp_lab["total_compra_monto"].sum()
        df_resumen_comp_lab["participacion"] = (df_resumen_comp_lab["total_compra_monto"] / total_general_compras * 100) if total_general_compras > 0 else 0
        df_resumen_comp_lab["costo_promedio"] = round(df_resumen_comp_lab["total_compra_monto"] / df_resumen_comp_lab["unidades_compradas"], 2)
        df_resumen_comp_lab = df_resumen_comp_lab.sort_values("total_compra_monto", ascending=False)

        st.dataframe(
            df_resumen_comp_lab,
            use_container_width=True,
            column_config={
                "codigo_laboratorio": "Cód. Lab",
                "nombre_laboratorio": "Laboratorio / Marca",
                "total_articulos": st.column_config.NumberColumn("Cant. Artículos", format="%d"),
                "unidades_compradas": st.column_config.NumberColumn("Unidades Compradas", format="%d"),
                "costo_promedio": st.column_config.NumberColumn("Costo Prom. Unit. ($)", format="$%.2f"),
                "total_compra_monto": st.column_config.NumberColumn("Inversión Total ($)", format="$%.2f"),
                "participacion": st.column_config.NumberColumn("% Participación", format="%.2f%%")
            }
        )
    else:
        st.info("Sin registros de compras por laboratorios para este período.")

    st.divider()

    # Tabla Resumen de Compras por Tipo de Proveedor, por Segmento, por Proveedor y por Sublínea
    col_t_res_tprv, col_t_res_seg, col_t_res_prv, col_t_res_subl = st.columns([1, 1, 1.2, 1])

    with col_t_res_tprv:
        st.markdown("#### 🏷️ Resumen por Tipo")
        if not df_comp.empty and "tipo_proveedor" in df_comp.columns:
            df_resumen_tprv = df_comp.groupby("tipo_proveedor").agg(
                total_proveedores=("id_proveedor", "nunique"),
                unidades_compradas=("unidades_compradas", "sum"),
                total_compra_monto=("total_compra_monto", "sum")
            ).reset_index()

            tot_gen_tprv = df_resumen_tprv["total_compra_monto"].sum()
            df_resumen_tprv["participacion"] = (df_resumen_tprv["total_compra_monto"] / tot_gen_tprv * 100) if tot_gen_tprv > 0 else 0
            df_resumen_tprv = df_resumen_tprv.sort_values("total_compra_monto", ascending=False)

            st.dataframe(
                df_resumen_tprv,
                use_container_width=True,
                column_config={
                    "tipo_proveedor": "Tipo de Proveedor",
                    "total_proveedores": st.column_config.NumberColumn("Cant. Provs", format="%d"),
                    "unidades_compradas": st.column_config.NumberColumn("Unidades", format="%d"),
                    "total_compra_monto": st.column_config.NumberColumn("Inversión ($)", format="$%.2f"),
                    "participacion": st.column_config.NumberColumn("% Part.", format="%.2f%%")
                }
            )
        else:
            st.info("Sin registros de tipos.")

    with col_t_res_seg:
        st.markdown("#### 🗂️ Resumen por Segmento")
        if not df_comp.empty and "segmento" in df_comp.columns:
            df_resumen_seg = df_comp.groupby("segmento").agg(
                total_proveedores=("id_proveedor", "nunique"),
                unidades_compradas=("unidades_compradas", "sum"),
                total_compra_monto=("total_compra_monto", "sum")
            ).reset_index()

            tot_gen_seg = df_resumen_seg["total_compra_monto"].sum()
            df_resumen_seg["participacion"] = (df_resumen_seg["total_compra_monto"] / tot_gen_seg * 100) if tot_gen_seg > 0 else 0
            df_resumen_seg = df_resumen_seg.sort_values("total_compra_monto", ascending=False)

            st.dataframe(
                df_resumen_seg,
                use_container_width=True,
                column_config={
                    "segmento": "Segmento",
                    "total_proveedores": st.column_config.NumberColumn("Cant. Provs", format="%d"),
                    "unidades_compradas": st.column_config.NumberColumn("Unidades", format="%d"),
                    "total_compra_monto": st.column_config.NumberColumn("Inversión ($)", format="$%.2f"),
                    "participacion": st.column_config.NumberColumn("% Part.", format="%.2f%%")
                }
            )
        else:
            st.info("Sin registros de segmentos.")

    with col_t_res_prv:
        st.markdown("#### 🚚 Resumen de Compras por Proveedor")
        if not df_comp.empty:
            cols_grp_prv = ["codigo_proveedor", "nombre_proveedor"]
            if "tipo_proveedor" in df_comp.columns:
                cols_grp_prv.append("tipo_proveedor")
            if "segmento" in df_comp.columns:
                cols_grp_prv.append("segmento")

            df_resumen_prv = df_comp.groupby(cols_grp_prv).agg(
                total_articulos=("id_producto", "nunique"),
                unidades_compradas=("unidades_compradas", "sum"),
                total_compra_monto=("total_compra_monto", "sum")
            ).reset_index()

            tot_gen_prv = df_resumen_prv["total_compra_monto"].sum()
            df_resumen_prv["participacion"] = (df_resumen_prv["total_compra_monto"] / tot_gen_prv * 100) if tot_gen_prv > 0 else 0
            df_resumen_prv = df_resumen_prv.sort_values("total_compra_monto", ascending=False)

            cfg_tbl_prv = {
                "codigo_proveedor": "Cód. Prov",
                "nombre_proveedor": "Proveedor / Droguería",
                "total_articulos": st.column_config.NumberColumn("Cant. Art.", format="%d"),
                "unidades_compradas": st.column_config.NumberColumn("Unidades", format="%d"),
                "total_compra_monto": st.column_config.NumberColumn("Inversión ($)", format="$%.2f"),
                "participacion": st.column_config.NumberColumn("% Part.", format="%.2f%%")
            }
            if "tipo_proveedor" in df_comp.columns:
                cfg_tbl_prv["tipo_proveedor"] = "Tipo"
            if "segmento" in df_comp.columns:
                cfg_tbl_prv["segmento"] = "Segmento"

            st.dataframe(
                df_resumen_prv,
                use_container_width=True,
                column_config=cfg_tbl_prv
            )
        else:
            st.info("Sin registros de proveedores.")

    with col_t_res_subl:
        st.markdown("#### 🌿 Por Sublínea")
        if not df_comp.empty and "descripcion_sublinea" in df_comp.columns:
            df_resumen_subl = df_comp.groupby("descripcion_sublinea").agg(
                total_articulos=("id_producto", "nunique"),
                unidades_compradas=("unidades_compradas", "sum"),
                total_compra_monto=("total_compra_monto", "sum")
            ).reset_index()

            tot_gen_subl = df_resumen_subl["total_compra_monto"].sum()
            df_resumen_subl["participacion"] = (df_resumen_subl["total_compra_monto"] / tot_gen_subl * 100) if tot_gen_subl > 0 else 0
            df_resumen_subl = df_resumen_subl.sort_values("total_compra_monto", ascending=False)

            st.dataframe(
                df_resumen_subl,
                use_container_width=True,
                column_config={
                    "descripcion_sublinea": "Sublínea",
                    "total_articulos": st.column_config.NumberColumn("Cant. Art.", format="%d"),
                    "unidades_compradas": st.column_config.NumberColumn("Unidades", format="%d"),
                    "total_compra_monto": st.column_config.NumberColumn("Inversión ($)", format="$%.2f"),
                    "participacion": st.column_config.NumberColumn("% Part.", format="%.2f%%")
                }
            )
        else:
            st.info("Sin registros de sublíneas.")

    st.divider()

    # --- COMPARATIVA DE COMPRAS ENTRE SUCURSALES ---
    st.markdown("#### 🏢 Comparativa de Compras y Abastecimiento entre Sucursales")
    if not df_comp.empty:
        df_comp_suc = df_comp.copy()
        if "codigo_sucursal" not in df_comp_suc.columns or "nombre_sucursal" not in df_comp_suc.columns:
            cols_merge_cs = [c for c in ["id_sucursal", "codigo_sucursal", "nombre"] if c in df_sucursales.columns]
            df_comp_suc = df_comp_suc.merge(
                df_sucursales[cols_merge_cs].rename(columns={"nombre": "nombre_sucursal"}),
                on="id_sucursal",
                how="left"
            )
        if "nombre_sucursal" not in df_comp_suc.columns and "nombre" in df_comp_suc.columns:
            df_comp_suc["nombre_sucursal"] = df_comp_suc["nombre"]

        cols_grp_csuc = [c for c in ["codigo_sucursal", "nombre_sucursal"] if c in df_comp_suc.columns]
        if not cols_grp_csuc:
            cols_grp_csuc = ["id_sucursal"]

        df_suc_c_agg = df_comp_suc.groupby(cols_grp_csuc).agg(
            total_comprado=("total_compra_monto", "sum"),
            unidades_compradas=("unidades_compradas", "sum"),
            droguerias_activas=("id_proveedor", "nunique")
        ).reset_index().sort_values("total_comprado", ascending=False)

        col_g_csuc, col_t_csuc = st.columns([3, 2])
        with col_g_csuc:
            y_col_c = "nombre_sucursal" if "nombre_sucursal" in df_suc_c_agg.columns else cols_grp_csuc[0]
            custom_c = [c for c in ["codigo_sucursal", "unidades_compradas", "droguerias_activas"] if c in df_suc_c_agg.columns]
            fig_csuc = px.bar(
                df_suc_c_agg,
                x="total_comprado",
                y=y_col_c,
                orientation="h",
                labels={"total_comprado": "Inversión en Compras ($)", y_col_c: "Sucursal"},
                title="Inversión en Compras por Farmacia ($)",
                color="total_comprado",
                color_continuous_scale="Oranges",
                custom_data=custom_c
            )
            fig_csuc.update_traces(
                hovertemplate="<b>%{y}</b><br><b>Inversión:</b> $%{x:,.2f}<extra></extra>"
            )
            fig_csuc.update_layout(yaxis={'categoryorder':'total ascending'}, height=340)
            st.plotly_chart(aplicar_estilo_farma(fig_csuc), use_container_width=True)

        with col_t_csuc:
            tot_gral_c = df_suc_c_agg["total_comprado"].sum()
            df_suc_c_agg["participacion"] = (df_suc_c_agg["total_comprado"] / tot_gral_c * 100) if tot_gral_c > 0 else 0
            st.markdown("##### 📌 Distribución de Compras")
            cols_tbl_c = [c for c in ["codigo_sucursal", "nombre_sucursal", "total_comprado", "unidades_compradas", "participacion"] if c in df_suc_c_agg.columns]
            st.dataframe(
                df_suc_c_agg[cols_tbl_c],
                use_container_width=True,
                hide_index=True,
                column_config={
                    "codigo_sucursal": "Cód.",
                    "nombre_sucursal": "Farmacia",
                    "total_comprado": st.column_config.NumberColumn("Inversión ($)", format="$%.2f"),
                    "unidades_compradas": st.column_config.NumberColumn("Unidades", format="%d"),
                    "participacion": st.column_config.NumberColumn("% Part.", format="%.1f%%")
                }
            )

    st.divider()

    st.markdown("#### 📋 Detalle de Artículos Comprados")
    if not df_comp.empty:
        cols_det_c = ["codigo_proveedor", "nombre_proveedor", "descripcion_linea"]
        if "descripcion_sublinea" in df_comp.columns:
            cols_det_c.append("descripcion_sublinea")
        cols_det_c.extend(["nombre_laboratorio", "codigo_articulo", "nombre_producto"])

        df_detalle_comp = df_comp.groupby(cols_det_c).agg(
            unidades=("unidades_compradas", "sum"),
            inversion_total=("total_compra_monto", "sum")
        ).reset_index().sort_values("inversion_total", ascending=False)

        cfg_det_c = {
            "codigo_proveedor": "Cód. Prov.",
            "nombre_proveedor": "Proveedor / Droguería",
            "descripcion_linea": "Línea",
            "nombre_laboratorio": "Laboratorio",
            "codigo_articulo": "Cód. Artículo",
            "nombre_producto": "Producto",
            "unidades": st.column_config.NumberColumn("Unidades Adquiridas", format="%d"),
            "inversion_total": st.column_config.NumberColumn("Inversión Total ($)", format="$%.2f")
        }
        if "descripcion_sublinea" in df_comp.columns:
            cfg_det_c["descripcion_sublinea"] = "Sublínea"

        st.dataframe(
            df_detalle_comp,
            use_container_width=True,
            column_config=cfg_det_c
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

    # --- NUEVA SECCIÓN: EVOLUCIÓN HISTÓRICA DEL VALOR DE INVENTARIO POR MES ---
    st.markdown("#### 📅 Evolución del Valor de Inventario Mes a Mes")
    if not df_inv_mes.empty:
        df_inv_mes_agg = df_inv_mes.groupby("periodo_mes").agg(
            valor_total_costo=("valor_total_costo", "sum"),
            valor_total_pvp=("valor_total_pvp", "sum"),
            total_unidades=("total_unidades", "sum")
        ).reset_index().sort_values("periodo_mes")

        df_inv_mes_agg["margen_potencial_pct"] = round(
            (df_inv_mes_agg["valor_total_pvp"] - df_inv_mes_agg["valor_total_costo"]) / df_inv_mes_agg["valor_total_pvp"] * 100, 2
        )

        col_g_imes, col_t_imes = st.columns([3, 2])

        with col_g_imes:
            fig_imes = go.Figure()

            # Barras Valor Costo
            fig_imes.add_trace(go.Bar(
                x=df_inv_mes_agg["periodo_mes"],
                y=df_inv_mes_agg["valor_total_costo"],
                name="💰 Valor Costo ($)",
                marker_color="#34495e",
                hovertemplate="<b>Mes:</b> %{x}<br><b>Valor Costo:</b> $%{y:,.2f}<extra></extra>"
            ))

            # Barras Valor PVP
            fig_imes.add_trace(go.Bar(
                x=df_inv_mes_agg["periodo_mes"],
                y=df_inv_mes_agg["valor_total_pvp"],
                name="🏷️ Valor PVP ($)",
                marker_color="#1abc9c",
                hovertemplate="<b>Mes:</b> %{x}<br><b>Valor PVP:</b> $%{y:,.2f}<extra></extra>"
            ))

            # Línea de Unidades en Stock
            fig_imes.add_trace(go.Scatter(
                x=df_inv_mes_agg["periodo_mes"],
                y=df_inv_mes_agg["total_unidades"],
                name="📦 Total Unidades",
                mode="lines+markers",
                line=dict(color="#e74c3c", width=2, dash="dot"),
                marker=dict(size=7),
                yaxis="y2",
                hovertemplate="<b>Unidades en Stock:</b> %{y:,}<extra></extra>"
            ))

            fig_imes.update_layout(
                title="Histórico Mensual del Capital Invertido y Potencial Comercial",
                barmode="group",
                hovermode="x unified",
                xaxis_title="Mes (Cierre Mensual)",
                yaxis=dict(title="Valor Total en Dólares ($)"),
                yaxis2=dict(title="Unidades en Stock", overlaying="y", side="right", showgrid=False),
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
            )
            st.plotly_chart(aplicar_estilo_farma(fig_imes), use_container_width=True)

        with col_t_imes:
            st.markdown("##### 📋 Cierres Mensuales de Inventario")
            st.dataframe(
                df_inv_mes_agg[["periodo_mes", "valor_total_costo", "valor_total_pvp", "margen_potencial_pct", "total_unidades"]],
                use_container_width=True,
                hide_index=True,
                column_config={
                    "periodo_mes": "Mes",
                    "valor_total_costo": st.column_config.NumberColumn("Valor Costo ($)", format="$%.2f"),
                    "valor_total_pvp": st.column_config.NumberColumn("Valor PVP ($)", format="$%.2f"),
                    "margen_potencial_pct": st.column_config.NumberColumn("Margen %", format="%.1f%%"),
                    "total_unidades": st.column_config.NumberColumn("Unidades", format="%d")
                }
            )
    else:
        st.info("Sin registros históricos de inventario mensual.")

    st.divider()

    # Valorización por Laboratorio, por Línea y por Sublínea
    col_v_lab, col_v_lin, col_v_sublin = st.columns(3)

    with col_v_lab:
        st.markdown("#### 🧪 Por Laboratorio")
        if not df_inv.empty:
            df_lab_val = df_inv.groupby("nombre_laboratorio").agg(
                stock_uds=("stock_actual", "sum"),
                monto_valorizado=("valor_total_inventario", "sum")
            ).reset_index().sort_values("monto_valorizado", ascending=False)

            fig_vlab = px.bar(
                df_lab_val.head(10),
                x="monto_valorizado",
                y="nombre_laboratorio",
                orientation="h",
                labels={"monto_valorizado": "Capital Invertido ($)", "nombre_laboratorio": "Laboratorio"},
                color="monto_valorizado",
                color_continuous_scale="Blues"
            )
            fig_vlab.update_layout(yaxis={'categoryorder':'total ascending'})
            st.plotly_chart(aplicar_estilo_farma(fig_vlab), use_container_width=True)
        else:
            st.info("Sin registros de inventario.")

    with col_v_lin:
        st.markdown("#### 🏷️ Por Línea de Producto")
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
                title="Capital por Línea"
            )
            st.plotly_chart(aplicar_estilo_farma(fig_vlin), use_container_width=True)
        else:
            st.info("Sin registros de líneas.")

    with col_v_sublin:
        st.markdown("#### 🌿 Por Sublínea de Producto")
        if not df_inv.empty and "descripcion_sublinea" in df_inv.columns:
            df_subl_val = df_inv.groupby("descripcion_sublinea").agg(
                stock_uds=("stock_actual", "sum"),
                monto_valorizado=("valor_total_inventario", "sum")
            ).reset_index().sort_values("monto_valorizado", ascending=False)

            fig_vsubl = px.pie(
                df_subl_val,
                names="descripcion_sublinea",
                values="monto_valorizado",
                hole=0.4,
                title="Capital por Sublínea",
                color_discrete_sequence=px.colors.qualitative.Prism
            )
            st.plotly_chart(aplicar_estilo_farma(fig_vsubl), use_container_width=True)
        else:
            st.info("Sin registros de sublíneas.")

    st.divider()

    # --- COMPARATIVA DE VALORIZACIÓN DE INVENTARIO ENTRE SUCURSALES ---
    st.markdown("#### 🏢 Comparativa de Stock y Valorización entre Farmacias")
    if not df_inv.empty:
        df_inv_suc_calc = df_inv.copy()
        if "codigo_sucursal" not in df_inv_suc_calc.columns or "nombre_sucursal" not in df_inv_suc_calc.columns:
            cols_merge_is = [c for c in ["id_sucursal", "codigo_sucursal", "nombre"] if c in df_sucursales.columns]
            df_inv_suc_calc = df_inv_suc_calc.merge(
                df_sucursales[cols_merge_is].rename(columns={"nombre": "nombre_sucursal"}),
                on="id_sucursal",
                how="left"
            )
        if "nombre_sucursal" not in df_inv_suc_calc.columns and "nombre" in df_inv_suc_calc.columns:
            df_inv_suc_calc["nombre_sucursal"] = df_inv_suc_calc["nombre"]

        cols_grp_isuc = [c for c in ["codigo_sucursal", "nombre_sucursal"] if c in df_inv_suc_calc.columns]
        if not cols_grp_isuc:
            cols_grp_isuc = ["id_sucursal"]

        df_suc_inv_agg = df_inv_suc_calc.groupby(cols_grp_isuc).agg(
            valor_costo=("valor_total_inventario", "sum"),
            valor_pvp=("valor_venta_inventario", "sum"),
            stock_unidades=("stock_actual", "sum"),
            articulos_distintos=("id_producto", "nunique")
        ).reset_index().sort_values("valor_costo", ascending=False)

        col_g_isuc, col_t_isuc = st.columns([3, 2])
        with col_g_isuc:
            y_col_i = "nombre_sucursal" if "nombre_sucursal" in df_suc_inv_agg.columns else cols_grp_isuc[0]
            custom_cod = df_suc_inv_agg["codigo_sucursal"] if "codigo_sucursal" in df_suc_inv_agg.columns else [""] * len(df_suc_inv_agg)
            custom_data_i = list(zip(custom_cod, df_suc_inv_agg["stock_unidades"], df_suc_inv_agg["articulos_distintos"]))

            fig_isuc = go.Figure()
            fig_isuc.add_trace(go.Bar(
                x=df_suc_inv_agg[y_col_i],
                y=df_suc_inv_agg["valor_costo"],
                name="💰 Valor Costo ($)",
                marker_color="#2c3e50",
                customdata=custom_data_i,
                hovertemplate="<b>%{x}</b><br><b>Valor Costo:</b> $%{y:,.2f}<br><b>Stock Físico:</b> %{customdata[1]:,} uds<br><b>Artículos:</b> %{customdata[2]}<extra></extra>"
            ))
            fig_isuc.add_trace(go.Bar(
                x=df_suc_inv_agg[y_col_i],
                y=df_suc_inv_agg["valor_pvp"],
                name="🏷️ Valor PVP ($)",
                marker_color="#16a085",
                hovertemplate="<b>Valor PVP:</b> $%{y:,.2f}<extra></extra>"
            ))
            fig_isuc.update_layout(
                title="Capital Inmovilizado en Stock por Farmacia (Costo vs PVP)",
                barmode="group",
                hovermode="x unified",
                xaxis_title="Farmacia / Sucursal",
                yaxis_title="Dólares ($)",
                height=340,
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
            )
            st.plotly_chart(aplicar_estilo_farma(fig_isuc), use_container_width=True)

        with col_t_isuc:
            tot_gral_inv = df_suc_inv_agg["valor_costo"].sum()
            df_suc_inv_agg["participacion"] = (df_suc_inv_agg["valor_costo"] / tot_gral_inv * 100) if tot_gral_inv > 0 else 0
            df_suc_inv_agg["margen_pct"] = round((df_suc_inv_agg["valor_pvp"] - df_suc_inv_agg["valor_costo"]) / df_suc_inv_agg["valor_pvp"] * 100, 1)

            st.markdown("##### 📌 Distribución de Capital")
            cols_tbl_i = [c for c in ["codigo_sucursal", "nombre_sucursal", "valor_costo", "stock_unidades", "margen_pct", "participacion"] if c in df_suc_inv_agg.columns]
            st.dataframe(
                df_suc_inv_agg[cols_tbl_i],
                use_container_width=True,
                hide_index=True,
                column_config={
                    "codigo_sucursal": "Cód.",
                    "nombre_sucursal": "Farmacia",
                    "valor_costo": st.column_config.NumberColumn("Valor Costo ($)", format="$%.2f"),
                    "stock_unidades": st.column_config.NumberColumn("Stock (Uds)", format="%d"),
                    "margen_pct": st.column_config.NumberColumn("Margen", format="%.1f%%"),
                    "participacion": st.column_config.NumberColumn("% Part.", format="%.1f%%")
                }
            )

    st.divider()

    # Tabla Detallada de Inventario Valorizado por Artículo
    st.markdown("#### 📋 Detalle de Inventario Valorizado por Artículo")
    if not df_inv.empty:
        cols_inv_art = ["codigo_articulo", "codigo_barras", "nombre_producto", "descripcion_linea"]
        if "descripcion_sublinea" in df_inv.columns:
            cols_inv_art.append("descripcion_sublinea")
        cols_inv_art.append("nombre_laboratorio")

        df_inv_articulo = df_inv.groupby(cols_inv_art).agg(
            stock_actual=("stock_actual", "sum"),
            costo_unitario=("costo_unitario", "mean"),
            precio_unitario=("precio_unitario", "mean"),
            monto_valorizado=("valor_total_inventario", "sum"),
            monto_pvp=("valor_venta_inventario", "sum")
        ).reset_index().sort_values("monto_valorizado", ascending=False)

        cfg_inv_art = {
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
        if "descripcion_sublinea" in df_inv.columns:
            cfg_inv_art["descripcion_sublinea"] = "Sublínea"

        st.dataframe(
            df_inv_articulo,
            use_container_width=True,
            column_config=cfg_inv_art
        )

    st.divider()

    # --- NUEVA SECCIÓN: BALANCE DE MOVIMIENTO POR PRODUCTO (COMPRAS VS VENTAS VS STOCK) ---
    st.markdown("#### 🔄 Balance de Movimiento por Producto: Compras vs Ventas")
    st.caption("Compara las unidades compradas e ingresadas frente a las unidades vendidas y el stock físico actual en el período.")

    # Calcular agregados de ventas por producto
    if not df_v_prod.empty:
        df_v_prod_agg = df_v_prod.groupby("codigo_articulo").agg(
            unidades_vendidas=("unidades_vendidas", "sum"),
            monto_vendido=("total_venta_monto", "sum")
        ).reset_index()
    else:
        df_v_prod_agg = pd.DataFrame(columns=["codigo_articulo", "unidades_vendidas", "monto_vendido"])

    # Calcular agregados de compras por producto
    if not df_comp.empty:
        df_comp_prod_agg = df_comp.groupby("codigo_articulo").agg(
            unidades_compradas=("unidades_compradas", "sum"),
            monto_comprado=("total_compra_monto", "sum")
        ).reset_index()
    else:
        df_comp_prod_agg = pd.DataFrame(columns=["codigo_articulo", "unidades_compradas", "monto_comprado"])

    # Base de inventario / catálogo de productos
    cols_base_bal = ["codigo_articulo", "codigo_barras", "nombre_producto", "descripcion_linea"]
    if "descripcion_sublinea" in df_inv.columns:
        cols_base_bal.append("descripcion_sublinea")
    cols_base_bal.append("nombre_laboratorio")

    if not df_inv.empty:
        df_inv_base = df_inv.groupby(cols_base_bal).agg(
            stock_actual=("stock_actual", "sum"),
            stock_minimo=("stock_minimo", "sum")
        ).reset_index()

        df_balance = df_inv_base.merge(df_comp_prod_agg, on="codigo_articulo", how="left")
        df_balance = df_balance.merge(df_v_prod_agg, on="codigo_articulo", how="left")
    else:
        df_balance = pd.merge(df_comp_prod_agg, df_v_prod_agg, on="codigo_articulo", how="outer")
        if not df_balance.empty and not df_catalogo_prod.empty:
            cols_cat_merge = ["codigo_articulo", "codigo_barras", "nombre_producto", "descripcion_linea"]
            if "descripcion_sublinea" in df_catalogo_prod.columns:
                cols_cat_merge.append("descripcion_sublinea")
            cols_cat_merge.append("nombre_laboratorio")
            df_balance = df_balance.merge(df_catalogo_prod[cols_cat_merge], on="codigo_articulo", how="left")
            df_balance["stock_actual"] = 0
            df_balance["stock_minimo"] = 0

    if not df_balance.empty:
        df_balance["unidades_compradas"] = df_balance["unidades_compradas"].fillna(0).astype(int)
        df_balance["unidades_vendidas"] = df_balance["unidades_vendidas"].fillna(0).astype(int)
        df_balance["monto_comprado"] = df_balance["monto_comprado"].fillna(0.0)
        df_balance["monto_vendido"] = df_balance["monto_vendido"].fillna(0.0)
        if "stock_actual" not in df_balance.columns:
            df_balance["stock_actual"] = 0
        df_balance["balance_unidades"] = df_balance["unidades_compradas"] - df_balance["unidades_vendidas"]

        # Buscador / filtro rápido de texto dentro de esta tabla
        col_bf_txt, col_bf_m1, col_bf_m2, col_bf_m3 = st.columns([2, 1, 1, 1])
        with col_bf_txt:
            filtro_txt_bal = st.text_input(
                "🔍 Filtrar producto en balance:",
                placeholder="Nombre, código o laboratorio...",
                key="filtro_txt_bal_inv"
            ).strip().lower()

        df_balance_mostrado = df_balance.copy()
        if filtro_txt_bal:
            mask_bal = (
                df_balance_mostrado["nombre_producto"].astype(str).str.lower().str.contains(filtro_txt_bal, na=False) |
                df_balance_mostrado["codigo_articulo"].astype(str).str.lower().str.contains(filtro_txt_bal, na=False) |
                df_balance_mostrado["nombre_laboratorio"].astype(str).str.lower().str.contains(filtro_txt_bal, na=False)
            )
            df_balance_mostrado = df_balance_mostrado[mask_bal]

        with col_bf_m1:
            st.metric("Total Uds Compradas", f"{df_balance_mostrado['unidades_compradas'].sum():,}")
        with col_bf_m2:
            st.metric("Total Uds Vendidas", f"{df_balance_mostrado['unidades_vendidas'].sum():,}")
        with col_bf_m3:
            st.metric("Stock Actual Total", f"{df_balance_mostrado['stock_actual'].sum():,}")

        # Ordenar por mayor volumen de movimiento (compras + ventas)
        df_balance_mostrado["movimiento_total"] = df_balance_mostrado["unidades_compradas"] + df_balance_mostrado["unidades_vendidas"]
        df_balance_mostrado = df_balance_mostrado.sort_values("movimiento_total", ascending=False)

        cols_mostrar_bal = [
            "codigo_articulo", "codigo_barras", "nombre_producto", "nombre_laboratorio", "descripcion_linea"
        ]
        if "descripcion_sublinea" in df_balance_mostrado.columns:
            cols_mostrar_bal.append("descripcion_sublinea")
        cols_mostrar_bal.extend([
            "unidades_compradas", "monto_comprado", "unidades_vendidas", "monto_vendido",
            "balance_unidades", "stock_actual"
        ])

        cfg_bal = {
            "codigo_articulo": "Cód. Artículo",
            "codigo_barras": "Código Barras",
            "nombre_producto": "Descripción del Producto",
            "nombre_laboratorio": "Laboratorio",
            "descripcion_linea": "Línea",
            "unidades_compradas": st.column_config.NumberColumn("📥 Uds Compradas", format="%d"),
            "monto_comprado": st.column_config.NumberColumn("Monto Compra ($)", format="$%.2f"),
            "unidades_vendidas": st.column_config.NumberColumn("📤 Uds Vendidas", format="%d"),
            "monto_vendido": st.column_config.NumberColumn("Monto Venta ($)", format="$%.2f"),
            "balance_unidades": st.column_config.NumberColumn("⚖️ Dif. (Ent - Sal)", format="%d"),
            "stock_actual": st.column_config.NumberColumn("📦 Stock Actual", format="%d")
        }
        if "descripcion_sublinea" in df_balance_mostrado.columns:
            cfg_bal["descripcion_sublinea"] = "Sublínea"

        st.dataframe(
            df_balance_mostrado[cols_mostrar_bal],
            use_container_width=True,
            column_config=cfg_bal
        )
    else:
        st.info("Sin registros para generar el balance de compras y ventas de productos.")

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
                    st.plotly_chart(aplicar_estilo_farma(fig_comp_p), use_container_width=True)

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
            st.plotly_chart(aplicar_estilo_farma(fig_v), use_container_width=True)

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
        st.plotly_chart(aplicar_estilo_farma(fig_p), use_container_width=True)
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

# =========================================================================
# TAB 6: DIAGNÓSTICO EN LÍNEA & SUGERENCIAS INTELIGENTES
# =========================================================================
with tab_sugerencias:
    st.subheader("🧠 Centro de Diagnóstico Operativo y Sugerencias en Línea")
    st.caption("Análisis algorítmico automatizado sobre el comportamiento de ventas, compras y niveles de inventario en el período filtrado.")

    dias_periodo = max((f_fin - f_ini).days, 1)

    # -------------------------------------------------------------
    # 1. MOTOR DE ANÁLISIS DE INVENTARIO
    # -------------------------------------------------------------
    # Calcular velocidad de ventas diarias por producto en el período
    df_analisis_inv = pd.DataFrame()
    if not df_inv.empty:
        # Stock actual por artículo
        cols_inv_prod = ["codigo_articulo", "codigo_barras", "nombre_producto", "descripcion_linea", "nombre_laboratorio"]
        if "descripcion_sublinea" in df_inv.columns:
            cols_inv_prod.append("descripcion_sublinea")

        df_inv_res = df_inv.groupby(cols_inv_prod).agg(
            stock_actual=("stock_actual", "sum"),
            stock_minimo=("stock_minimo", "sum"),
            costo_unitario=("costo_unitario", "mean"),
            precio_unitario=("precio_unitario", "mean"),
            valor_total_inventario=("valor_total_inventario", "sum")
        ).reset_index()

        # Unidades vendidas en el período
        if not df_v_prod.empty:
            df_v_uds = df_v_prod.groupby("codigo_articulo").agg(
                unidades_vendidas=("unidades_vendidas", "sum"),
                monto_vendido=("total_venta_monto", "sum")
            ).reset_index()
            df_analisis_inv = df_inv_res.merge(df_v_uds, on="codigo_articulo", how="left")
        else:
            df_analisis_inv = df_inv_res.copy()
            df_analisis_inv["unidades_vendidas"] = 0
            df_analisis_inv["monto_vendido"] = 0.0

        df_analisis_inv["unidades_vendidas"] = df_analisis_inv["unidades_vendidas"].fillna(0)
        df_analisis_inv["monto_vendido"] = df_analisis_inv["monto_vendido"].fillna(0.0)

        # Velocidad de venta diaria (Run Rate)
        df_analisis_inv["venta_diaria_promedio"] = df_analisis_inv["unidades_vendidas"] / dias_periodo

        # Días de cobertura de inventario proyectados
        # Si venta diaria es 0, días cobertura se establece en 999 (sin rotación)
        df_analisis_inv["dias_cobertura"] = df_analisis_inv.apply(
            lambda r: (r["stock_actual"] / r["venta_diaria_promedio"]) if r["venta_diaria_promedio"] > 0 else (999 if r["stock_actual"] > 0 else 0),
            axis=1
        )

        # Cantidad sugerida a reordenar para cubrir 30 días
        df_analisis_inv["sugerido_compra_30d"] = df_analisis_inv.apply(
            lambda r: max(int(np.ceil((r["venta_diaria_promedio"] * 30) + r["stock_minimo"] - r["stock_actual"])), 0),
            axis=1
        )
        df_analisis_inv["inversion_sugerida"] = df_analisis_inv["sugerido_compra_30d"] * df_analisis_inv["costo_unitario"]

    # Segmentación de Alertas de Inventario
    # A. Riesgo Crítico de Agotamiento / Quiebre (Cobertura < 7 días o Stock <= Stock Mínimo con demanda activa)
    df_quiebres_inminentes = pd.DataFrame()
    df_sobrestock = pd.DataFrame()
    df_hueso = pd.DataFrame()

    if not df_analisis_inv.empty:
        df_quiebres_inminentes = df_analisis_inv[
            ((df_analisis_inv["stock_actual"] <= df_analisis_inv["stock_minimo"]) | (df_analisis_inv["dias_cobertura"] <= 7)) &
            (df_analisis_inv["unidades_vendidas"] > 0)
        ].sort_values("dias_cobertura", ascending=True)

        # B. Sobrestock (Cobertura > 60 días con rotación)
        df_sobrestock = df_analisis_inv[
            (df_analisis_inv["dias_cobertura"] > 60) & 
            (df_analisis_inv["dias_cobertura"] < 999) & 
            (df_analisis_inv["stock_actual"] > df_analisis_inv["stock_minimo"] * 2)
        ].sort_values("valor_total_inventario", ascending=False)

        # C. Inventario Inmovilizado / Lento movimiento (Cero ventas en el período pero con stock físico)
        df_hueso = df_analisis_inv[
            (df_analisis_inv["unidades_vendidas"] == 0) & 
            (df_analisis_inv["stock_actual"] > 0)
        ].sort_values("valor_total_inventario", ascending=False)

    # -------------------------------------------------------------
    # 2. MOTOR DE ANÁLISIS DE COMPRAS & PROVEEDORES
    # -------------------------------------------------------------
    # Variación de costos entre proveedores para el mismo producto
    df_oportunidad_compras = pd.DataFrame()
    if not df_comp.empty and "id_proveedor" in df_comp.columns:
        df_costos_comp = df_comp.groupby(["codigo_articulo", "nombre_producto", "nombre_proveedor"]).agg(
            costo_promedio=("total_compra_monto", lambda x: (x.sum() / df_comp.loc[x.index, "unidades_compradas"].sum()) if df_comp.loc[x.index, "unidades_compradas"].sum() > 0 else 0),
            unidades_compradas=("unidades_compradas", "sum"),
            inversion_total=("total_compra_monto", "sum")
        ).reset_index()

        # Identificar artículos comprados a más de un proveedor con diferencia de costo
        prov_count = df_costos_comp.groupby("codigo_articulo")["nombre_proveedor"].nunique()
        articulos_multiproveedor = prov_count[prov_count > 1].index.tolist()

        if articulos_multiproveedor:
            df_multi = df_costos_comp[df_costos_comp["codigo_articulo"].isin(articulos_multiproveedor)]

            filas_oportunidad = []
            for cod_art, g_art in df_multi.groupby("codigo_articulo"):
                g_art_sorted = g_art.sort_values("costo_promedio")
                mejor_fila = g_art_sorted.iloc[0]
                peor_fila = g_art_sorted.iloc[-1]

                c_min = mejor_fila["costo_promedio"]
                c_max = peor_fila["costo_promedio"]
                dif = c_max - c_min

                if dif > 0.05:
                    uds_tot = g_art["unidades_compradas"].sum()
                    ahorro_pct = (dif / c_max * 100) if c_max > 0 else 0
                    ahorro_monto = dif * uds_tot

                    filas_oportunidad.append({
                        "codigo_articulo": cod_art,
                        "nombre_producto": mejor_fila["nombre_producto"],
                        "mejor_proveedor": mejor_fila["nombre_proveedor"],
                        "costo_min": c_min,
                        "proveedor_costoso": peor_fila["nombre_proveedor"],
                        "costo_max": c_max,
                        "diferencia_costo": dif,
                        "ahorro_potencial_pct": ahorro_pct,
                        "unidades_totales": uds_tot,
                        "ahorro_potencial_monto": ahorro_monto
                    })

            if filas_oportunidad:
                df_oportunidad_compras = pd.DataFrame(filas_oportunidad).sort_values("ahorro_potencial_monto", ascending=False)

    # -------------------------------------------------------------
    # 3. MOTOR DE ANÁLISIS DE VENTAS & TICKETS
    # -------------------------------------------------------------
    # Mix Contado vs Crédito y Ticket Promedio
    tot_ventas_periodo = df_v_dia["total_facturado"].sum() if not df_v_dia.empty else 0
    tot_contado_periodo = df_v_dia["ventas_contado"].sum() if "ventas_contado" in df_v_dia and not df_v_dia.empty else 0
    tot_credito_periodo = df_v_dia["ventas_credito"].sum() if "ventas_credito" in df_v_dia and not df_v_dia.empty else 0
    pct_credito_actual = (tot_credito_periodo / tot_ventas_periodo * 100) if tot_ventas_periodo > 0 else 0

    # KPIs Principales de Diagnóstico
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    kpi1.metric("🚨 Artículos en Riesgo de Quiebre", f"{len(df_quiebres_inminentes):,}", help="Artículos con demanda activa y menos de 7 días de cobertura o bajo stock mínimo.")
    kpi2.metric("📦 Capital en Sobrestock (>60d)", f"${df_sobrestock['valor_total_inventario'].sum():,.2f}" if not df_sobrestock.empty else "$0.00", f"{len(df_sobrestock)} productos")
    kpi3.metric("💤 Capital Inmovilizado (Sin Venta)", f"${df_hueso['valor_total_inventario'].sum():,.2f}" if not df_hueso.empty else "$0.00", f"{len(df_hueso)} productos")
    kpi4.metric("💡 Oportunidades de Compra Óptima", f"{len(df_oportunidad_compras):,}", help="Productos adquiridos con variación de costo relevante entre proveedores.")

    st.divider()

    # =============================================================
    # SECCIÓN 1: RECOMENDACIONES DE INVENTARIO & REORDEN
    # =============================================================
    st.markdown("### 📦 1. Acciones Inmediatas en Inventario & Abastecimiento")
    
    col_sug_inv1, col_sug_inv2 = st.columns(2)

    with col_sug_inv1:
        st.error(f"🚨 **Reposición Prioritaria (Quiebres y Cobertura Crítica: {len(df_quiebres_inminentes)} ítems)**")
        st.caption("Artículos de alta demanda cuya existencia actual cubre menos de 7 días o ya están en quiebre.")
        if not df_quiebres_inminentes.empty:
            st.dataframe(
                df_quiebres_inminentes[[
                    "codigo_articulo", "nombre_producto", "nombre_laboratorio", 
                    "stock_actual", "venta_diaria_promedio", "dias_cobertura", "sugerido_compra_30d", "inversion_sugerida"
                ]],
                use_container_width=True,
                column_config={
                    "codigo_articulo": "Código",
                    "nombre_producto": "Producto",
                    "nombre_laboratorio": "Laboratorio",
                    "stock_actual": st.column_config.NumberColumn("Stock Hoy", format="%d"),
                    "venta_diaria_promedio": st.column_config.NumberColumn("Venta/Día", format="%.1f"),
                    "dias_cobertura": st.column_config.NumberColumn("Días Rest.", format="%.1f d"),
                    "sugerido_compra_30d": st.column_config.NumberColumn("📦 Pedir (30d)", format="%d uds"),
                    "inversion_sugerida": st.column_config.NumberColumn("Inversión Est. ($)", format="$%.2f")
                }
            )
            inv_total_reorden = df_quiebres_inminentes["inversion_sugerida"].sum()
            st.info(f"💡 **Recomendación:** Se sugiere emitir órdenes de compra por un estimado de **${inv_total_reorden:,.2f}** para blindar la operación comercial de los próximos 30 días.")
        else:
            st.success("✅ No se detectan quiebres de inventario ni productos en nivel crítico para este período.")

    with col_sug_inv2:
        st.warning(f"💤 **Inventario Inmovilizado / Lenta Rotación ({len(df_hueso)} ítems)**")
        st.caption("Productos con existencias físicas y capital retenido que no registraron ventas en los últimos días.")
        if not df_hueso.empty:
            st.dataframe(
                df_hueso[[
                    "codigo_articulo", "nombre_producto", "nombre_laboratorio", 
                    "stock_actual", "costo_unitario", "valor_total_inventario"
                ]],
                use_container_width=True,
                column_config={
                    "codigo_articulo": "Código",
                    "nombre_producto": "Producto",
                    "nombre_laboratorio": "Laboratorio",
                    "stock_actual": st.column_config.NumberColumn("Stock Físico", format="%d"),
                    "costo_unitario": st.column_config.NumberColumn("Costo Prom.", format="$%.2f"),
                    "valor_total_inventario": st.column_config.NumberColumn("Capital Atrapado ($)", format="$%.2f")
                }
            )
            cap_hueso = df_hueso["valor_total_inventario"].sum()
            st.warning(f"💡 **Recomendación:** Existen **${cap_hueso:,.2f}** inmovilizados. Se aconseja implementar combos comerciales, promociones o evaluar devolución con proveedores.")
        else:
            st.success("✅ Todo el inventario disponible ha presentado rotación en el período.")

    st.divider()

    # =============================================================
    # SECCIÓN 2: OPTIMIZACIÓN DE COMPRAS Y COSTOS
    # =============================================================
    st.markdown("### 📥 2. Optimización de Compras y Negociación con Droguerías")

    col_cmp_opt1, col_cmp_opt2 = st.columns([3, 2])

    with col_cmp_opt1:
        st.markdown("#### ⚖️ Comparativa de Precios entre Proveedores")
        st.caption("Productos adquiridos a diferentes proveedores donde existe margen de ahorro por arbitraje de compra.")
        if not df_oportunidad_compras.empty:
            st.dataframe(
                df_oportunidad_compras[[
                    "codigo_articulo", "nombre_producto", 
                    "mejor_proveedor", "costo_min", 
                    "proveedor_costoso", "costo_max", 
                    "ahorro_potencial_pct", "ahorro_potencial_monto"
                ]],
                use_container_width=True,
                hide_index=True,
                column_config={
                    "codigo_articulo": "Cód.",
                    "nombre_producto": "Descripción del Producto",
                    "mejor_proveedor": "🏆 Mejor Proveedor",
                    "costo_min": st.column_config.NumberColumn("Mejor Costo ($)", format="$%.2f"),
                    "proveedor_costoso": "⚠️ Prov. Más Costoso",
                    "costo_max": st.column_config.NumberColumn("Costo Mayor ($)", format="$%.2f"),
                    "ahorro_potencial_pct": st.column_config.NumberColumn("Ahorro %", format="%.1f%%"),
                    "ahorro_potencial_monto": st.column_config.NumberColumn("Ahorro Estimado ($)", format="$%.2f")
                }
            )
            ahorro_total_estimado = df_oportunidad_compras["ahorro_potencial_monto"].sum()
            st.info(f"💡 **Recomendación:** Centralizar pedidos en el proveedor con mejor tarifa podría generar un ahorro acumulado de **${ahorro_total_estimado:,.2f}** en reposiciones futuras.")
        else:
            st.success("✅ Los costos de adquisición se encuentran estables o los artículos fueron cotizados con un único proveedor.")

    with col_cmp_opt2:
        st.markdown("#### 🏷️ Oportunidad en Líneas y Sublíneas")
        if not df_comp.empty and "descripcion_linea" in df_comp.columns:
            df_linea_comp = df_comp.groupby("descripcion_linea").agg(
                inversion=("total_compra_monto", "sum"),
                unidades=("unidades_compradas", "sum")
            ).reset_index().sort_values("inversion", ascending=False)

            fig_bar_cmp = px.bar(
                df_linea_comp,
                x="inversion",
                y="descripcion_linea",
                orientation="h",
                labels={"inversion": "Inversión ($)", "descripcion_linea": "Línea"},
                title="Concentración de Compras por Línea",
                color="inversion",
                color_continuous_scale="Teal"
            )
            fig_bar_cmp.update_layout(yaxis={'categoryorder':'total ascending'}, height=300)
            st.plotly_chart(aplicar_estilo_farma(fig_bar_cmp), use_container_width=True)

    st.divider()

    # =============================================================
    # SECCIÓN 3: ESTRATEGIA COMERCIAL & MEJORA DE VENTAS
    # =============================================================
    st.markdown("### 📊 3. Estrategia Comercial y Rendimiento en Ventas")

    col_v_sug1, col_v_sug2 = st.columns(2)

    with col_v_sug1:
        st.markdown("#### 💳 Mix de Facturación: Contado vs Crédito")
        st.write(f"- Facturación Total: **${tot_ventas_periodo:,.2f}**")
        st.write(f"- Ventas de Contado: **${tot_contado_periodo:,.2f}** ({100-pct_credito_actual:.1f}%)")
        st.write(f"- Ventas a Crédito: **${tot_credito_periodo:,.2f}** ({pct_credito_actual:.1f}%)")

        if pct_credito_actual > 40:
            st.warning(f"⚠️ **Atención:** El volumen de crédito representa el **{pct_credito_actual:.1f}%** de la venta total. Se sugiere revisar la política de plazos de cobranza para proteger el flujo de caja operativo.")
        elif pct_credito_actual < 10:
            st.info(f"💡 **Oportunidad:** El crédito solo representa el **{pct_credito_actual:.1f}%**. Existe margen para ofrecer facilidades crediticias a clientes corporativos recurrentes para incrementar el ticket promedio.")
        else:
            st.success("✅ La relación Contado / Crédito se mantiene en un rango equilibrado y saludable.")

    with col_v_sug2:
        st.markdown("#### 🎯 Productos Tracción (Estrategia 80/20 Pareto)")
        if not df_v_prod.empty:
            cols_pareto = ["codigo_articulo", "nombre_producto", "nombre_laboratorio", "descripcion_linea"]
            cols_disp = [c for c in cols_pareto if c in df_v_prod.columns]

            df_pareto = df_v_prod.groupby(cols_disp).agg(
                total_venta=("total_venta_monto", "sum"),
                unidades=("unidades_vendidas", "sum")
            ).reset_index().sort_values("total_venta", ascending=False)

            tot_ventas_p = df_pareto["total_venta"].sum()
            df_pareto["pct_individual"] = (df_pareto["total_venta"] / tot_ventas_p * 100) if tot_ventas_p > 0 else 0
            df_pareto["pct_acumulado"] = (df_pareto["total_venta"].cumsum() / tot_ventas_p * 100) if tot_ventas_p > 0 else 0
            df_pareto["precio_promedio"] = round(df_pareto["total_venta"] / df_pareto["unidades"], 2)

            top_80 = df_pareto[df_pareto["pct_acumulado"] <= 85].copy()
            # Si el corte fue muy estricto y quedó vacío, asegurar al menos los primeros
            if top_80.empty and not df_pareto.empty:
                top_80 = df_pareto.head(min(5, len(df_pareto))).copy()

            pct_catalogo_80 = (len(top_80) / len(df_pareto) * 100) if len(df_pareto) > 0 else 0

            st.write(f"- Artículos activos en venta: **{len(df_pareto)}**")
            st.write(f"- Artículos estrella (Clase A): **{len(top_80)} ({pct_catalogo_80:.1f}% del catálogo)**")
            st.info(f"💡 **Recomendación:** Blindar con stock de seguridad y acuerdos exclusivos estos **{len(top_80)} productos**, ya que concentran el 80% de la facturación.")

            # Tabla Interactiva de Artículos Tracción (Pareto 80/20)
            st.dataframe(
                top_80[[
                    "codigo_articulo", "nombre_producto", "nombre_laboratorio", 
                    "unidades", "total_venta", "pct_individual", "pct_acumulado"
                ]],
                use_container_width=True,
                hide_index=True,
                column_config={
                    "codigo_articulo": "Código",
                    "nombre_producto": "Producto Estrella (Tracción)",
                    "nombre_laboratorio": "Laboratorio",
                    "unidades": st.column_config.NumberColumn("Uds Vendidas", format="%d"),
                    "total_venta": st.column_config.NumberColumn("Facturación ($)", format="$%.2f"),
                    "pct_individual": st.column_config.NumberColumn("% Venta", format="%.2f%%"),
                    "pct_acumulado": st.column_config.NumberColumn("% Acumulado", format="%.1f%%")
                }
            )
        else:
            st.info("Sin registros de venta para calcular Pareto.")
