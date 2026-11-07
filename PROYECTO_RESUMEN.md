# 💊 KPI Dashboard - Red de Farmacias

Documento de seguimiento técnico y contextual del proyecto para retomar sesiones en cualquier momento.

---

## 📌 Contexto del Proyecto
Dashboard analítico y gerencial desarrollado en **Streamlit** y conectado a **MySQL**, optimizado para una red de más de 35 sucursales farmacéuticas y más de 40.000 referencias en catálogo normalizado.

- **Directorio del Proyecto**: `C:\Users\Windows\.gemini\antigravity\scratch\dashboard-mysql`
- **Archivo Principal**: `app.py`
- **Script Creación Tablas MySQL**: `creacion_tablas.sql`
- **Script Datos de Prueba**: `datos_prueba.sql`
- **Script Sincronización VFP**: `vfp_actualizar_sucursales.prg`
- **Configuración de Conexión**: `.streamlit/secrets.toml`

---

## 🏗️ Esquema de Base de Datos Centralizada (Totalmente Normalizada)

### Tablas Maestras Base
1. `sucursales`: Catálogo de farmacias, ciudades, **zona geográfica** y código alfanumérico único (`id_sucursal`, `codigo_sucursal VARCHAR(4)`, `nombre`, `ciudad`, `zona VARCHAR(50)`, `fecha_registro`).
2. `maestro_lineas`: Categorías y líneas comerciales (`id_linea`, `codigo_linea VARCHAR(6)`, `descripcion_linea`, `fecha_registro`).
3. `maestro_laboratorios`: Fabricantes y marcas (`id_laboratorio`, `codigo_laboratorio VARCHAR(6)`, `nombre_laboratorio`, `fecha_registro`).
4. `maestro_proveedores`: Droguerías y distribuidores (`id_proveedor`, `codigo_proveedor VARCHAR(10)`, `nombre_proveedor`, `rif_proveedor`, `fecha_registro`).
5. `maestro_clientes`: Clientes particulares, aseguradoras y convenios (`id_cliente`, `codigo_cliente VARCHAR(10)`, `nombre_cliente`, `tipo_cliente`, `identificacion`, `fecha_registro`).
6. `maestro_productos`: Catálogo unificado de más de 40.000 referencias (`id_producto`, `codigo_articulo VARCHAR(30)`, `codigo_barras VARCHAR(50)`, `nombre_producto`, `id_linea`, `id_laboratorio`).

### Tablas Transaccionales de KPIs
7. `kpi_ventas_diarias`: Facturación bruta, **número de operaciones / tickets** (`numero_operaciones`) y ticket promedio por farmacia.
8. `kpi_inventario_sucursal`: Stock actual, stock mínimo, costo unitario y capital inmovilizado calculado (`valor_total_inventario`).
9. `kpi_ventas_por_producto`: Salida diaria en unidades y monto por producto (`id_producto`).
10. `kpi_compras_por_producto`: Entrada de mercancía, unidades y costo por producto (`id_producto`) y droguería (`id_proveedor`).
11. `kpi_ventas_vendedor`: Desempeño y ventas por asesor.
12. `kpi_formas_pago`: Canales de cobro (Efectivo, Débito, Crédito, Pago Móvil, etc.).
13. `kpi_saldos_bancos`: Disponibilidad financiera en cuentas bancarias.
14. `kpi_cajas_efectivo`: Efectivo disponible en bóvedas y cajas operativas por moneda.
15. `kpi_cxc_diario`: Cuentas por cobrar enlazadas al maestro de clientes (`id_cliente`).
16. `kpi_cxp_diario`: Cuentas por pagar enlazadas al maestro de proveedores (`id_proveedor`).
17. `kpi_pagos_proveedores`: Egresos y pagos a proveedores (`id_proveedor`).

---

## 💻 Características del Dashboard (`app.py`)
- **Filtros Maestros Dinámicos**:
  - Filtro por **Zona Geográfica** (Gran Caracas, Centro, Occidente, etc.).
  - Filtro por **Sucursal** (con código de 4 caracteres y ciudad).
  - Filtro por **Rango de Fechas** (`date_input`).
  - Filtro por **Línea de Producto** (con código de 6 caracteres).
  - Filtro por **Laboratorio / Fabricante** (con código de 6 caracteres).
  - Filtro por **Proveedor / Droguería** (con código de 10 caracteres).
  - Filtro por **Cliente** (para cartera de CxC con código de 10 caracteres).
- **Pestañas**:
  - 📊 **Ventas & Rendimiento**: Facturación total, tickets/operaciones, ticket promedio, unidades vendidas, evolución diaria, **Top 20 Productos Más Vendidos** (con código de 30 chars), participación por laboratorios y tabla detallada completa.
  - 📥 **Compras & Proveedores**: Inversión en abastecimiento, **Top 5 Compras por Droguería**, compras por laboratorio (con unidades y montos) y detalle de artículos comprados.
  - 📦 **Inventario & Valorización**: Inventario valorizado total, unidades en stock, valorización por laboratorio, valorización por línea y tabla valorizada por artículo con alertas de quiebre.
  - 👨‍💼 **Equipo de Ventas**: Ranking y productividad por asesor.
  - 💰 **Tesorería & Finanzas**: Arqueo de cajas de efectivo (USD/VES), saldos en cuentas bancarias, CxC por cliente y CxP por proveedor.

---

## 🚀 Comandos Rápidos
```powershell
cd C:\Users\Windows\.gemini\antigravity\scratch\dashboard-mysql
python -m streamlit run app.py
```
