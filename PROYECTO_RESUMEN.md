# 💊 KPI Dashboard - Red de Farmacias

Documento de seguimiento técnico y contextual del proyecto para retomar sesiones en cualquier momento.

---

## 📌 Contexto del Proyecto
Dashboard analítico y gerencial desarrollado en **Streamlit** y conectado a **MySQL**, optimizado para una red de más de 35 sucursales farmacéuticas y más de 40.000 referencias en catálogo.

- **Directorio del Proyecto**: `C:\Users\Windows\.gemini\antigravity\scratch\dashboard-mysql`
- **Archivo Principal**: `app.py`
- **Script de Datos de Prueba**: `datos_prueba.sql`
- **Configuración de Conexión**: `.streamlit/secrets.toml`

---

## 🏗️ Esquema de Base de Datos Implementado
El diseño está normalizado para soportar alto volumen y transacciones distribuidas:
1. `sucursales`: Catálogo de farmacias, ciudades, **zona geográfica** y código alfanumérico único (`id_sucursal`, `codigo_sucursal VARCHAR(4)`, `nombre`, `ciudad`, `zona VARCHAR(50)`).
   *(Permite análisis y segmentación territorial como: Gran Caracas, Centro, Occidente, Oriente, Los Andes, etc.).*
2. `maestro_productos`: Catálogo unificado de más de 40.000 artículos (`id_producto`, `codigo_barras`, `nombre_producto`, `laboratorio`).
   *(Nota: Se desvincula el proveedor del producto, ya que un artículo puede adquirirse a múltiples droguerías/proveedores).*
3. `kpi_ventas_diarias`: Facturación bruta, **número de operaciones / tickets** (`numero_operaciones`) y ticket promedio generado por farmacia.
4. `kpi_inventario_sucursal`: Stock actual, stock mínimo y costo unitario por farmacia (`id_inventario`, `id_sucursal`, `id_producto`, `stock_actual`, `stock_minimo`, `costo_unitario`, `valor_total_inventario` como columna generada/calculada para valorización).
5. `kpi_ventas_por_producto`: Salida diaria en unidades y monto por artículo.
6. `kpi_compras_por_producto`: Entrada de mercancía, volumen, costos de adquisición y **proveedor al que se le compró** (`nombre_proveedor`).
7. `kpi_ventas_vendedor`: Desempeño, operaciones y ventas por asesor.
8. `kpi_formas_pago`: Canales de cobro (Efectivo, Débito, Crédito, Pago Móvil, etc.).
9. `kpi_saldos_bancos`: Disponibilidad financiera en cuentas bancarias.
9.1 `kpi_cajas_efectivo`: Cajas de efectivo por sucursal (`id_registro`, `id_sucursal`, `fecha`, `tipo_caja`, `moneda`, `saldo_efectivo`).
10. `kpi_cxc_diario`: Cuentas por cobrar desagregadas por cliente (`id_registro`, `id_sucursal`, `fecha`, `tipo_cliente`, `identificacion_cliente`, `nombre_cliente`, `saldo_pendiente`, `monto_otorgado_hoy`, `monto_recuperado_hoy`).
11. `kpi_cxp_diario`: Cuentas por pagar y compromisos con laboratorios/proveedores.
12. `kpi_pagos_proveedores`: Egresos y liquidación de facturas comerciales.

---

## 💻 Características del Dashboard (`app.py`)
- **Modo Dual**: Selector en la barra lateral para alternar entre:
  - `Simulación (Datos de Prueba)`: Genera datos sintéticos realistas al vuelo para pruebas sin necesidad de base de datos activa.
  - `Conexión MySQL en Vivo`: Conexión directa a través de credenciales en `secrets.toml`.
- **Filtros Dinámicos**:
  - Filtro por sucursal específica o consolidado general de la red.
  - Selector de rango de fechas (`date_input`).
  - **Filtro por Laboratorio (Marca)**: Permite segmentar ventas, compras, inventario y evolución por fabricante (ej: Bayer, Pfizer, Calox).
  - **Filtro por Proveedor Habitual (Distribuidor)**: Permite evaluar compras, quiebres de inventario y cuentas por pagar por droguería/distribuidor (ej: Cobeca, Droguería Nena).
  - Botón para limpiar caché y forzar recarga.
- **Pestañas**:
  - 📊 **Ventas & Rendimiento**: Facturación total, tickets, ticket promedio, unidades vendidas, evolución diaria, **Top 20 Productos Más Vendidos**, participación por laboratorios y **tabla interactiva con el detalle completo de artículos vendidos** (código, unidades, precio promedio y monto total).
  - 📥 **Compras & Proveedores**: Inversión en abastecimiento, **Top 5 Compras por Droguería / Proveedor**, **Compras por Laboratorio** (gráfico de barras y distribución con detalle emergente de unidades y montos), evolución por fechas y detalle cruzado por artículo.
  - 👨‍💼 **Equipo de Ventas**: Ranking de vendedores por facturación, volumen de operaciones y ticket medio.
  - 💰 **Tesorería & Finanzas**: Métodos de cobro, saldos bancarios y balance entre CxC (clientes) vs CxP (proveedores).

---

## 🚀 Comandos Rápidos

### Ejecutar la Aplicación:
```powershell
cd C:\Users\Windows\.gemini\antigravity\scratch\dashboard-mysql
streamlit run app.py
```
