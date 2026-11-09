# 💊 KPI Dashboard - Grupo San Anselmo
**Fecha de última sesión:** 09 de Noviembre de 2026

---

## 📌 Contexto General del Proyecto
Cuadro de Mando Integral y Dashboard analítico desarrollado en **Python / Streamlit** para el **Grupo San Anselmo**, conectado a **MySQL** (con modo de simulación offline integrado). Diseñado para una cadena de más de **35 farmacias** y un catálogo maestro de más de **40.000 artículos**.

- **Ubicación física del proyecto**: `C:\Users\Windows\.gemini\antigravity\scratch\dashboard-mysql`
- **Archivo principal del Dashboard**: `app.py`
- **Script de Creación de Base de Datos**: `creacion_tablas.sql`
- **Script de Datos de Prueba (Seed)**: `datos_prueba.sql`
- **Suite de Scripts VFP 9 (SPT con Tablas Temporales en Memoria)**:
  - `vfp_actualizar_sucursales.prg`: Sincronización de sucursales (4 caracteres, zona y fecha).
  - `vfp_sincronizar_articulos_upsert.prg`: Sincronización masiva de 40.000+ artículos con update/insert sin conflictos y resolución de claves.
  - `sync_lineas.prg`: Maestro de líneas (6 chars).
  - `sync_laboratorios.prg`: Maestro de laboratorios (6 chars).
  - `sync_proveedores.prg`: Maestro de proveedores/droguerías (10 chars).
  - `sync_clientes.prg`: Maestro de clientes (10 chars).
  - `sync_inventario_sucursal.prg`: Stock, costo unitario y precio unitario por farmacia.
  - `sync_ventas_diarias.prg`: Ventas globales diarias y tickets por farmacia.
  - `sync_ventas_producto.prg`: Detalle diario de artículos vendidos por farmacia.
  - `sync_compras_producto.prg`: Compras diarias por artículo y droguería.
  - `sync_tesoreria_cajas_bancos.prg`: Arqueo de cajas de efectivo (USD/VES) y cuentas bancarias.
  - `sync_cartera_cxc_cxp.prg`: Saldos de cartera CxC (clientes) y CxP (proveedores).
- **Lanzador de un clic para Windows**: `ejecutar.bat`
- **Credenciales MySQL**: `.streamlit/secrets.toml`

---

## 🏗️ Modelo de Datos MySQL (Definitivo y 100% Normalizado)

### 1. Tablas Maestras Base
- `sucursales`: `id_sucursal`, `codigo_sucursal VARCHAR(4) UNIQUE`, `nombre`, `ciudad`, `zona VARCHAR(50)`, `fecha_registro TIMESTAMP ON UPDATE CURRENT_TIMESTAMP`.
- `maestro_lineas`: `id_linea`, `codigo_linea VARCHAR(6) UNIQUE`, `descripcion_linea`, `fecha_registro`.
- `maestro_laboratorios`: `id_laboratorio`, `codigo_laboratorio VARCHAR(6) UNIQUE`, `nombre_laboratorio`, `fecha_registro`.
- `maestro_proveedores`: `id_proveedor`, `codigo_proveedor VARCHAR(10) UNIQUE`, `nombre_proveedor`, `rif_proveedor`, `fecha_registro`.
- `maestro_clientes`: `id_cliente`, `codigo_cliente VARCHAR(10) UNIQUE`, `nombre_cliente`, `tipo_cliente` (*Particular, Seguro / Empresa, Convenio*), `identificacion`, `fecha_registro`.
- `maestro_productos`: `id_producto`, `codigo_articulo VARCHAR(30) UNIQUE`, `codigo_barras VARCHAR(50)` (flexible, sin restricción de longitud mínima ni duplicidad forzada), `nombre_producto`, `id_linea`, `id_laboratorio`, `fecha_registro`.

### 2. Tablas Transaccionales de Rendimiento (KPIs)
- `kpi_ventas_diarias`: Facturación bruta, **ventas contado** (`ventas_contado`), **ventas crédito** (`ventas_credito`), **número de operaciones / tickets por farmacia** (`numero_operaciones`) y ticket promedio generado.
- `kpi_inventario_sucursal`: Stock actual, stock mínimo, costo unitario, **precio unitario de venta** (`precio_unitario`), valorización a costo (`valor_total_inventario`) y valorización a precio venta (`valor_venta_inventario`).
- `kpi_ventas_por_producto`: Salida diaria en unidades y monto por artículo (`id_producto`).
- `kpi_compras_por_producto`: Compras por artículo (`id_producto`) y droguería (`id_proveedor`) con unidades e inversión.
- `kpi_ventas_vendedor`: Desempeño y ventas por asesor comercial.
- `kpi_formas_pago`: Desglose de ingresos por canal (Efectivo, Débito, Crédito, Pago Móvil, etc.).
- `kpi_saldos_bancos`: Disponibilidad financiera en cuentas bancarias.
- `kpi_cajas_efectivo`: Arqueo físico de bóvedas y cajas chicas/operativas por sucursal en USD y VES.
- `kpi_cxc_diario`: Cuentas por cobrar enlazadas al maestro de clientes (`id_cliente`).
- `kpi_cxp_diario`: Cuentas por pagar enlazadas al maestro de proveedores (`id_proveedor`).
- `kpi_pagos_proveedores`: Egresos y pagos a proveedores (`id_proveedor`).

---

## 💻 Estado y Características del Dashboard (`app.py`)

1. **Filtros Dinámicos en Barra Lateral**:
   - Selector de **Zona Geográfica** (Gran Caracas, Centro, Occidente, etc.).
   - Selector en cascada de **Sucursal** (muestra código `[F001]`, nombre y ciudad).
   - Rango de fechas interactivo (`date_input`).
   - Filtro por **Línea de Producto** (`[LIN001]`).
   - Filtro por **Laboratorio / Fabricante** (`[LAB001]`).
   - Filtro por **Proveedor / Droguería** (`[PRV0000001]`).
   - Filtro por **Cliente** (`[CLI0000001]`).
   - Selector de modo: `Simulación (Datos de Prueba)` vs `Conexión MySQL en Vivo`.

2. **Pestañas Implementadas**:
   - 📊 **Ventas & Rendimiento**: Facturación total, tickets/operaciones, ticket promedio, unidades vendidas, evolución diaria, **Top 20 Productos Más Vendidos con selector de orden (Facturado $ vs Unidades)**, participación por laboratorios (con hover de unidades y montos) y tabla interactiva completa.
   - 📥 **Compras & Proveedores**: Inversión en compras, unidades adquiridas, **Top 5 Droguerías (orden por Inversión o Unidades)**, **Compras por Laboratorio (orden por Inversión o Unidades)** y tabla detallada.
   - 📦 **Inventario & Valorización**: 
     - Inventario valorizado a costo y a PVP con margen bruto potencial.
     - Valorización por laboratorio y por línea de producto.
     - Tabla valorizada por artículo con alertas de quiebre de stock.
     - **Módulo comparador de precios y stock entre sucursales con buscador predictivo**: permite buscar por nombre, código de artículo, código de barras o laboratorio sobre las 40.000 referencias mostrando precio mínimo, máximo, promedio, margen y stock disponible por tienda.
   - 👨‍💼 **Equipo de Ventas**: Ranking y productividad por asesor.
   - 💰 **Tesorería & Finanzas**: Arqueo de efectivo (bóvedas y cajas en USD/VES), cuentas bancarias, CxC por cliente y CxP por proveedor.

---

## 🚀 Cómo Retomar Mañana
1. **Ejecutar la app localmente**: Doble clic en `ejecutar.bat` o desde terminal:
   ```powershell
   cd C:\Users\Windows\.gemini\antigravity\scratch\dashboard-mysql
   python -m streamlit run app.py
   ```
2. **Para continuar en el chat**: Solo abre este chat o menciona *"Continuemos con el dashboard"* y retomaremos de inmediato.
