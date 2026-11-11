# 💊 KPI Dashboard - Grupo San Anselmo
**Fecha de última sesión:** 10 de Noviembre de 2026

---

## 📌 Contexto General del Proyecto
Cuadro de Mando Integral y Dashboard analítico desarrollado en **Python / Streamlit** para el **Grupo San Anselmo**, conectado a **MySQL** (con modo de simulación offline integrado y fallback automático). Diseñado para una cadena de más de **35 farmacias** y un catálogo maestro de más de **40.000 artículos**.

- **Ubicación física del proyecto**: `C:\Users\Windows\.gemini\antigravity\scratch\dashboard-mysql`
- **Archivo principal del Dashboard**: `app.py`
- **Script de Creación de Base de Datos**: `creacion_tablas.sql` (19 tablas normalizadas con índices y FKs)
- **Script de Datos de Prueba (Seed)**: `datos_prueba.sql`
- **Suite de Scripts VFP 9 (SPT con Tablas Temporales en Memoria)**:
  - `vfp_actualizar_sucursales.prg`: Sincronización de sucursales (4 caracteres, zona y fecha).
  - `vfp_sincronizar_articulos_upsert.prg`: Sincronización masiva de 40.000+ artículos con update/insert sin conflictos y resolución de claves.
  - `sync_lineas.prg`: Maestro de líneas (6 chars).
  - `sync_laboratorios.prg`: Maestro de laboratorios (6 chars).
  - `sync_proveedores.prg`: Maestro de proveedores/droguerías (10 chars).
  - `sync_clientes.prg`: Maestro de clientes (10 chars).
  - `sync_inventario_sucursal.prg`: Stock, costo unitario y precio unitario por farmacia.
  - `sync_inventario_mensual.prg`: Cierres mensuales de inventario por farmacia (unidades, costo y PVP).
  - `sync_ventas_diarias.prg`: Ventas globales diarias, tickets, contado vs crédito y operaciones.
  - `sync_ventas_producto.prg`: Detalle diario de artículos vendidos por farmacia.
  - `sync_compras_diarias.prg`: Consolidado de compras diarias (contado vs crédito y número de facturas).
  - `sync_compras_producto.prg`: Compras diarias por artículo y droguería.
  - `sync_tesoreria_cajas_bancos.prg`: Arqueo de cajas de efectivo (USD/VES) y cuentas bancarias.
  - `sync_cartera_cxc_cxp.prg`: Saldos de cartera CxC (clientes) y CxP (proveedores).
- **Lanzador de un clic para Windows**: `ejecutar.bat`
- **Credenciales MySQL**: `.streamlit/secrets.toml`

---

## 🚀 Logros y Cambios Implementados en Esta Sesión (10/11/2026)

1. **Discriminación Completa de Contado vs Crédito en Ventas Diarias:**
   - Columnas `ventas_contado`, `ventas_credito`, `operaciones_contado` y `operaciones_credito` en `kpi_ventas_diarias`.
   - Gráfica interactiva de barras apiladas con Plotly Graph Objects (`go.Figure`) con tooltip unificado en hover:
     - Total Facturado del Día ($) y Nº de Operaciones.
     - Unidades Vendidas del Día.
     - Total Contado ($ y ops).
     - Total Crédito ($ y ops).
   - Acotada a los **últimos 30 días** para lectura ágil sin saturación de barras.

2. **Evolución Mes a Mes de Ventas, Ticket Promedio, Operaciones y Unidades:**
   - Gráfica combinada con doble eje Y:
     - Barras: Ventas Totales ($).
     - Línea con marcadores: Ticket Promedio ($) con etiquetas numéricas.
     - Línea punteada: Nº de Operaciones.
     - Tooltip con unidades vendidas.
   - Tabla lateral de **📌 Desglose Mensual** con: Mes, Ventas ($), Ticket Prom., Tickets (operaciones) y **Unidades vendidas**.

3. **Módulo de Compras Diarias y Mensuales:**
   - Tabla `kpi_compras_diarias` en MySQL con `total_comprado`, `unidades_compradas`, `numero_facturas_compra`, `compras_contado` y `compras_credito`.
   - Gráfica diaria de Compras (Contado vs Crédito) acotada a los **últimos 30 días**.
   - Gráficas mensuales de evolución de compras desglosadas por Laboratorio y por Droguería/Proveedor.
   - Script de sincronización VFP 9: `sync_compras_diarias.prg`.

4. **Histórico y Evolución del Valor de Inventario por Mes:**
   - Tabla `kpi_inventario_mensual` en MySQL para almacenar los cierres de mes por farmacia.
   - Gráfica comparativa mensual de **Valor Costo ($) vs Valor PVP ($)** con línea de **Unidades físicas en stock** (eje secundario).
   - Tabla de Cierres Mensuales con cálculo de Margen Bruto Potencial %.
   - Script de sincronización VFP 9: `sync_inventario_mensual.prg`.

5. **Correcciones de Conexión MySQL en Vivo:**
   - Agregado el bloque SQL `else:` completo para consultar directamente desde MySQL todas las tablas sin depender de mocks.
   - Corregido el alias `nombre` de sucursales en inventario que provocaba error en el comparador de PVP.
   - Rango de fechas por defecto establecido en 6 meses (180 días) para análisis intermensual.

---

## 📋 Estado del Repositorio y Próximos Pasos para Mañana
- Todos los archivos (`app.py`, `creacion_tablas.sql`, scripts `.prg`) han sido compilados y verificados sin errores.
- Listo para enviar a GitHub cuando el usuario lo desee:
  ```bash
  git add .
  git commit -m "feat: suite completa v2.0 - ventas y compras diarias, evolucion mensual e inventario valorizado"
  git push
  ```
