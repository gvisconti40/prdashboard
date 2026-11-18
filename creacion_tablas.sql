-- =========================================================================
-- SCRIPT DEFINITIVO Y OPTIMIZADO: BASE DE DATOS CENTRALIZADA PARA KPIs
-- PROYECTO: GRUPO DE FARMACIAS (DISEÑO NORMALIZADO PARA ALTO VOLUMEN)
-- Métrica: 35+ Sucursales | 40,000+ Productos por Catálogo
-- =========================================================================

-- 1. Catálogo Base de Sucursales / Farmacias
CREATE TABLE IF NOT EXISTS sucursales (
    id_sucursal INT AUTO_INCREMENT PRIMARY KEY,
    codigo_sucursal VARCHAR(4) NOT NULL UNIQUE,  -- Código alfanumérico único (Ej: S001, MCY1)
    nombre VARCHAR(100) NOT NULL,
    ciudad VARCHAR(50),
    zona VARCHAR(50) NOT NULL DEFAULT 'Centro',  -- Clasificación territorial (Ej: Gran Caracas, Centro, Occidente)
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_sucursal_zona (zona)
);

-- 2. TABLA MAESTRA: LÍNEAS DE PRODUCTOS / CATEGORÍAS
CREATE TABLE IF NOT EXISTS maestro_lineas (
    id_linea INT AUTO_INCREMENT PRIMARY KEY,
    codigo_linea VARCHAR(6) NOT NULL UNIQUE,     -- Código de línea de 6 caracteres (Ej: LIN001, MED002)
    descripcion_linea VARCHAR(100) NOT NULL,     -- Ej: Medicamentos, Cuidado Personal, Material Médico, Misceláneos
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- 3. TABLA MAESTRA: SUBLÍNEAS DE PRODUCTOS
CREATE TABLE IF NOT EXISTS maestro_sublineas (
    id_sublinea INT AUTO_INCREMENT PRIMARY KEY,
    codigo_sublinea VARCHAR(6) NOT NULL UNIQUE,          -- Código de sublínea de 6 caracteres (Ej: SL001)
    descripcion_sublinea VARCHAR(100) NOT NULL,          -- Descripción de la sublínea
    id_linea INT NULL,                                   -- Opcional enlace a la línea padre
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (id_linea) REFERENCES maestro_lineas(id_linea) ON UPDATE CASCADE ON DELETE SET NULL
);

-- 4. TABLA MAESTRA: LABORATORIOS / FABRICANTES
CREATE TABLE IF NOT EXISTS maestro_laboratorios (
    id_laboratorio INT AUTO_INCREMENT PRIMARY KEY,
    codigo_laboratorio VARCHAR(6) NOT NULL UNIQUE, -- Código de laboratorio de 6 caracteres (Ej: LAB001, PFIZER)
    nombre_laboratorio VARCHAR(120) NOT NULL,       -- Ej: Pfizer, Bayer, Calox, Leti, Genven, Merck
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- 4. TABLA MAESTRA: TIPOS DE PROVEEDOR (Norma MIVO ERP 7.1)
CREATE TABLE IF NOT EXISTS maestro_tipos_proveedor (
    id_tipo_proveedor INT AUTO_INCREMENT PRIMARY KEY,
    codigo_tipo_proveedor VARCHAR(10) NOT NULL UNIQUE,  -- Códigos oficiales MIVO: 01, 02, 03... 10, 99
    descripcion VARCHAR(120) NOT NULL,                  -- Descripción oficial según informe gerencial
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- 5. TABLA MAESTRA: SEGMENTOS DE PROVEEDOR (Norma MIVO ERP 7.1)
CREATE TABLE IF NOT EXISTS maestro_segmentos_proveedor (
    id_segmento INT AUTO_INCREMENT PRIMARY KEY,
    codigo_segmento VARCHAR(10) NOT NULL UNIQUE,        -- Códigos oficiales MIVO: P0101 a P0111, P0201 a P0801, P9999
    descripcion VARCHAR(120) NOT NULL,                  -- Droguerías Estratégicas, Habituales, Laboratorios, etc.
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- 6. TABLA MAESTRA: PROVEEDORES / DROGUERÍAS / DISTRIBUIDORES (Homologado MIVO ERP 7.1)
CREATE TABLE IF NOT EXISTS maestro_proveedores (
    id_proveedor INT AUTO_INCREMENT PRIMARY KEY,
    codigo_proveedor VARCHAR(20) NOT NULL UNIQUE,       -- Código de proveedor (Ej: PRV0000001, COBECA0001)
    nombre_proveedor VARCHAR(150) NOT NULL,             -- Ej: Droguería Cobeca, Droguería Nena, Drolanca
    rif_proveedor VARCHAR(20),                          -- Ej: J-00012345-1
    tipo_proveedor VARCHAR(10) DEFAULT '01',            -- Clave foránea al tipo de proveedor oficial (01 Mercancía)
    segmento VARCHAR(10) DEFAULT 'P0101',               -- Clave foránea al segmento de proveedor (P0101 Droguerías Estratégicas)
    telefono VARCHAR(30),
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (tipo_proveedor) REFERENCES maestro_tipos_proveedor(codigo_tipo_proveedor)
        ON UPDATE CASCADE ON DELETE RESTRICT,
    FOREIGN KEY (segmento) REFERENCES maestro_segmentos_proveedor(codigo_segmento)
        ON UPDATE CASCADE ON DELETE RESTRICT
);

-- 7. TABLA MAESTRA: TIPOS Y SEGMENTOS DE CLIENTE (Norma MIVO ERP 7.1)
CREATE TABLE IF NOT EXISTS maestro_tipos_cliente (
    id_tipo_cliente INT AUTO_INCREMENT PRIMARY KEY,
    codigo_tipo_cliente VARCHAR(10) NOT NULL UNIQUE,    -- Códigos oficiales MIVO: A01 (Contado), A02 (Crédito)
    descripcion VARCHAR(100) NOT NULL,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS maestro_segmentos_cliente (
    id_segmento_cliente INT AUTO_INCREMENT PRIMARY KEY,
    codigo_segmento_cliente VARCHAR(10) NOT NULL UNIQUE,-- Códigos oficiales MIVO: C01 a C05, C99
    descripcion VARCHAR(100) NOT NULL,                  -- Mostrador, Empresa, Intercompañía, Instituciones, Empleados
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- 7.1 TABLA MAESTRA: CLIENTES (Normalizado con Tipos y Segmentos MIVO ERP 7.1)
CREATE TABLE IF NOT EXISTS maestro_clientes (
    id_cliente INT AUTO_INCREMENT PRIMARY KEY,
    codigo_cliente VARCHAR(20) NOT NULL UNIQUE,         -- Código de cliente de hasta 20 caracteres
    nombre_cliente VARCHAR(150) NOT NULL,               -- Nombre o Razón Social
    tipo_cliente VARCHAR(10) NOT NULL DEFAULT 'A01',    -- Enlace a maestro_tipos_cliente (A01 / A02)
    segmento_cliente VARCHAR(10) NOT NULL DEFAULT 'C01',-- Enlace a maestro_segmentos_cliente (C01..C05, C99)
    identificacion VARCHAR(30),                         -- Cédula o RIF
    telefono VARCHAR(30),
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_cte_tipo (tipo_cliente),
    INDEX idx_cte_seg (segmento_cliente),
    FOREIGN KEY (tipo_cliente) REFERENCES maestro_tipos_cliente(codigo_tipo_cliente)
        ON UPDATE CASCADE ON DELETE RESTRICT,
    FOREIGN KEY (segmento_cliente) REFERENCES maestro_segmentos_cliente(codigo_segmento_cliente)
        ON UPDATE CASCADE ON DELETE RESTRICT
);

-- 8. TABLA MAESTRA: PRODUCTOS (Normalizada con enlace a Líneas, Sublíneas y Laboratorios)
CREATE TABLE IF NOT EXISTS maestro_productos (
    id_producto INT AUTO_INCREMENT PRIMARY KEY,
    codigo_articulo VARCHAR(30) NOT NULL UNIQUE,  -- Código interno de artículo de hasta 30 caracteres
    codigo_barras VARCHAR(50),                    -- Código de barras comercial (flexible, sin longitud mínima)
    nombre_producto VARCHAR(150) NOT NULL,        -- Descripción del producto
    id_linea INT NOT NULL,                        -- Enlace al maestro de líneas
    id_sublinea INT NULL DEFAULT 1,               -- Enlace al maestro de sublíneas
    id_laboratorio INT NOT NULL,                  -- Enlace al maestro de laboratorios
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (id_linea) REFERENCES maestro_lineas(id_linea),
    FOREIGN KEY (id_sublinea) REFERENCES maestro_sublineas(id_sublinea),
    FOREIGN KEY (id_laboratorio) REFERENCES maestro_laboratorios(id_laboratorio),
    INDEX idx_prod_linea (id_linea),
    INDEX idx_prod_sublinea (id_sublinea),
    INDEX idx_prod_lab (id_laboratorio),
    INDEX idx_prod_barras (codigo_barras)
);

-- 7. KPI: Ventas Diarias Globales por Farmacia (Discriminando Contado, Crédito y Cashea con Operaciones)
CREATE TABLE IF NOT EXISTS kpi_ventas_diarias (
    id_registro BIGINT AUTO_INCREMENT PRIMARY KEY,
    id_sucursal INT NOT NULL,
    fecha DATE NOT NULL,
    total_facturado DECIMAL(12, 2) NOT NULL,       -- Ventas brutas totales del día (contado + credito + cashea)
    ventas_contado DECIMAL(12, 2) NOT NULL DEFAULT 0.00,  -- Ventas cobradas de inmediato (efectivo, tarjeta, pago móvil)
    ventas_credito DECIMAL(12, 2) NOT NULL DEFAULT 0.00,  -- Ventas a crédito tradicionales (seguros, convenios empresariales, particulares)
    ventas_cashea DECIMAL(12, 2) NOT NULL DEFAULT 0.00,   -- Ventas bajo modalidad Cashea (tipo_fp = 'CASH')
    numero_operaciones INT NOT NULL,               -- Cantidad total de tickets / operaciones / ventas
    operaciones_contado INT NOT NULL DEFAULT 0,    -- Tickets / transacciones de contado
    operaciones_credito INT NOT NULL DEFAULT 0,    -- Facturas / operaciones a crédito tradicional
    operaciones_cashea INT NOT NULL DEFAULT 0,    -- Facturas / operaciones modalidad Cashea
    ticket_promedio DECIMAL(10, 2) GENERATED ALWAYS AS (total_facturado / numero_operaciones) STORED,
    ultima_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (id_sucursal) REFERENCES sucursales(id_sucursal),
    UNIQUE KEY uq_sucursal_fecha (id_sucursal, fecha)
);

-- 8. KPI: Inventario de Productos por Sucursal (Con Costo Unitario y Precio de Venta)
CREATE TABLE IF NOT EXISTS kpi_inventario_sucursal (
    id_inventario BIGINT AUTO_INCREMENT PRIMARY KEY,
    id_sucursal INT NOT NULL,
    id_producto INT NOT NULL,                     -- Enlace numérico al maestro de productos
    stock_actual INT NOT NULL DEFAULT 0,
    stock_minimo INT NOT NULL DEFAULT 0,          -- Umbral por farmacia
    costo_unitario DECIMAL(10, 2) NOT NULL DEFAULT 0.00,  -- Costo de adquisición/reposición
    precio_unitario DECIMAL(10, 2) NOT NULL DEFAULT 0.00, -- Precio de venta al público (PVP)
    valor_total_inventario DECIMAL(12, 2) GENERATED ALWAYS AS (stock_actual * costo_unitario) STORED,
    valor_venta_inventario DECIMAL(12, 2) GENERATED ALWAYS AS (stock_actual * precio_unitario) STORED,
    ultima_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (id_sucursal) REFERENCES sucursales(id_sucursal),
    FOREIGN KEY (id_producto) REFERENCES maestro_productos(id_producto),
    UNIQUE KEY uq_sucursal_producto (id_sucursal, id_producto)
);

-- 8.1. KPI: Histórico Mensual de Valorización de Inventario por Farmacia
CREATE TABLE IF NOT EXISTS kpi_inventario_mensual (
    id_registro BIGINT AUTO_INCREMENT PRIMARY KEY,
    id_sucursal INT NOT NULL,
    periodo_mes VARCHAR(7) NOT NULL,              -- Formato YYYY-MM (ej: '2026-10')
    fecha_cierre DATE NOT NULL,                   -- Fecha del último día o corte del mes
    total_unidades INT NOT NULL DEFAULT 0,        -- Total de unidades en existencia al cierre
    valor_total_costo DECIMAL(14, 2) NOT NULL,    -- Valorización a costo de reposición en USD
    valor_total_pvp DECIMAL(14, 2) NOT NULL,      -- Valorización a precio de venta al público (PVP) en USD
    margen_potencial_pct DECIMAL(5, 2) GENERATED ALWAYS AS (
        CASE WHEN valor_total_pvp > 0 THEN ((valor_total_pvp - valor_total_costo) / valor_total_pvp * 100) ELSE 0 END
    ) STORED,
    ultima_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (id_sucursal) REFERENCES sucursales(id_sucursal),
    UNIQUE KEY uq_sucursal_mes_inv (id_sucursal, periodo_mes)
);

-- 9. KPI: Ventas Diarias Consolidadas por Producto
CREATE TABLE IF NOT EXISTS kpi_ventas_por_producto (
    id_registro BIGINT AUTO_INCREMENT PRIMARY KEY,
    id_sucursal INT NOT NULL,
    fecha DATE NOT NULL,
    id_producto INT NOT NULL,                     -- Enlace al maestro de productos
    unidades_vendidas INT NOT NULL,               -- Salidas diarias
    total_venta_monto DECIMAL(12, 2) NOT NULL,    -- Total facturado por el producto
    ultima_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (id_sucursal) REFERENCES sucursales(id_sucursal),
    FOREIGN KEY (id_producto) REFERENCES maestro_productos(id_producto),
    UNIQUE KEY uq_suc_fecha_prod (id_sucursal, fecha, id_producto)
);

-- 10. KPI: Compras y Abastecimiento Diario Global por Farmacia (Consolidado de Compras)
CREATE TABLE IF NOT EXISTS kpi_compras_diarias (
    id_registro BIGINT AUTO_INCREMENT PRIMARY KEY,
    id_sucursal INT NOT NULL,
    fecha DATE NOT NULL,
    total_comprado DECIMAL(12, 2) NOT NULL,        -- Inversión total en compras del día en USD
    unidades_compradas INT NOT NULL DEFAULT 0,     -- Total de unidades/cajas ingresadas
    numero_facturas_compra INT NOT NULL DEFAULT 0, -- Cantidad de facturas / recepciones de compras
    compras_contado DECIMAL(12, 2) NOT NULL DEFAULT 0.00,  -- Monto de compras pagadas de contado
    compras_credito DECIMAL(12, 2) NOT NULL DEFAULT 0.00,  -- Monto de compras a crédito de proveedores
    ultima_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (id_sucursal) REFERENCES sucursales(id_sucursal),
    UNIQUE KEY uq_sucursal_fecha_compra (id_sucursal, fecha)
);

-- 10.1. KPI: Compras y Abastecimiento Diario por Producto y Proveedor
CREATE TABLE IF NOT EXISTS kpi_compras_por_producto (
    id_registro BIGINT AUTO_INCREMENT PRIMARY KEY,
    id_sucursal INT NOT NULL,
    fecha DATE NOT NULL,
    id_producto INT NOT NULL,                     -- Enlace al maestro de productos
    id_proveedor INT NOT NULL,                    -- Enlace al maestro de proveedores
    unidades_compradas INT NOT NULL,              -- Volumen adquirido
    total_compra_monto DECIMAL(12, 2) NOT NULL,   -- Inversión/Costo total
    ultima_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (id_sucursal) REFERENCES sucursales(id_sucursal),
    FOREIGN KEY (id_producto) REFERENCES maestro_productos(id_producto),
    FOREIGN KEY (id_proveedor) REFERENCES maestro_proveedores(id_proveedor),
    INDEX idx_comp_prov (id_proveedor),
    UNIQUE KEY uq_suc_fecha_compra_prod_prov (id_sucursal, fecha, id_producto, id_proveedor)
);

-- 11. KPI: Ventas por Vendedor y Sucursal (Evaluación del Personal)
CREATE TABLE IF NOT EXISTS kpi_ventas_vendedor (
    id_registro BIGINT AUTO_INCREMENT PRIMARY KEY,
    id_sucursal INT NOT NULL,
    fecha DATE NOT NULL,
    nombre_vendedor VARCHAR(100) NOT NULL,
    total_vendido DECIMAL(12, 2) NOT NULL,
    cantidad_operaciones INT NOT NULL,
    ultima_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (id_sucursal) REFERENCES sucursales(id_sucursal),
    UNIQUE KEY uq_sucursal_vendedor_fecha (id_sucursal, nombre_vendedor, fecha)
);

-- 12. KPI: Métodos de Pago Utilizados (Flujo Financiero por Sucursal - Dinámico)
CREATE TABLE IF NOT EXISTS kpi_formas_pago (
    id_registro BIGINT AUTO_INCREMENT PRIMARY KEY,
    id_sucursal INT NOT NULL,
    fecha DATE NOT NULL,
    forma_pago VARCHAR(50) NOT NULL,              -- Texto dinámico desde Profit/reng_tip (US$, BS, Tarjetas por banco, etc.)
    total_ingresado DECIMAL(12, 2) NOT NULL,
    ultima_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (id_sucursal) REFERENCES sucursales(id_sucursal),
    UNIQUE KEY uq_sucursal_pago_fecha (id_sucursal, forma_pago, fecha)
);

-- 13. KPI: Saldos de Cuentas Bancarias (Tesorería / Disponibilidad Bancaria)
CREATE TABLE IF NOT EXISTS kpi_saldos_bancos (
    id_registro BIGINT AUTO_INCREMENT PRIMARY KEY,
    id_sucursal INT NOT NULL,
    fecha DATE NOT NULL,
    nombre_banco VARCHAR(80) NOT NULL,
    numero_cuenta_oculto VARCHAR(10) NOT NULL,
    saldo_disponible DECIMAL(14, 2) NOT NULL,
    ultima_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (id_sucursal) REFERENCES sucursales(id_sucursal),
    UNIQUE KEY uq_sucursal_banco_fecha (id_sucursal, nombre_banco, numero_cuenta_oculto, fecha)
);

-- 14. KPI: Cajas de Efectivo por Sucursal (Bóveda / Cajas Operativas - Dinámico)
CREATE TABLE IF NOT EXISTS kpi_cajas_efectivo (
    id_registro BIGINT AUTO_INCREMENT PRIMARY KEY,
    id_sucursal INT NOT NULL,
    fecha DATE NOT NULL,
    tipo_caja VARCHAR(60) NOT NULL DEFAULT 'Caja Principal / Bóveda',
    moneda VARCHAR(20) NOT NULL DEFAULT 'USD',
    saldo_efectivo DECIMAL(12, 2) NOT NULL,
    ultima_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (id_sucursal) REFERENCES sucursales(id_sucursal),
    UNIQUE KEY uq_sucursal_caja_fecha (id_sucursal, tipo_caja, moneda, fecha)
);

-- 15. KPI: Cuentas por Cobrar (CxC) por Cliente Enlazado al Maestro
CREATE TABLE IF NOT EXISTS kpi_cxc_diario (
    id_registro BIGINT AUTO_INCREMENT PRIMARY KEY,
    id_sucursal INT NOT NULL,
    fecha DATE NOT NULL,
    id_cliente INT NOT NULL,                      -- Enlace al maestro de clientes
    saldo_pendiente DECIMAL(12, 2) NOT NULL,      -- Lo que nos debe acumulado a la fecha
    monto_otorgado_hoy DECIMAL(12, 2) NOT NULL DEFAULT 0.00,  -- Crédito nuevo asignado hoy
    monto_recuperado_hoy DECIMAL(12, 2) NOT NULL DEFAULT 0.00,-- Cobranza/Abonos recibidos hoy
    ultima_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (id_sucursal) REFERENCES sucursales(id_sucursal),
    FOREIGN KEY (id_cliente) REFERENCES maestro_clientes(id_cliente),
    UNIQUE KEY uq_suc_cxc_fecha (id_sucursal, id_cliente, fecha)
);

-- 16. KPI: Cuentas por Pagar (CxP) Enlazadas al Maestro de Proveedores
CREATE TABLE IF NOT EXISTS kpi_cxp_diario (
    id_registro BIGINT AUTO_INCREMENT PRIMARY KEY,
    id_sucursal INT NOT NULL,
    fecha DATE NOT NULL,
    id_proveedor INT NOT NULL,                    -- Enlace al maestro de proveedores
    saldo_por_pagar DECIMAL(12, 2) NOT NULL,      -- Deuda total acumulada a la fecha
    ultima_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (id_sucursal) REFERENCES sucursales(id_sucursal),
    FOREIGN KEY (id_proveedor) REFERENCES maestro_proveedores(id_proveedor),
    UNIQUE KEY uq_suc_cxp_fecha (id_sucursal, id_proveedor, fecha)
);

-- 17. KPI: Egresos por Pagos Realizados a Proveedores
CREATE TABLE IF NOT EXISTS kpi_pagos_proveedores (
    id_registro BIGINT AUTO_INCREMENT PRIMARY KEY,
    id_sucursal INT NOT NULL,
    fecha DATE NOT NULL,
    id_proveedor INT NOT NULL,                    -- Enlace al maestro de proveedores
    monto_pagado DECIMAL(12, 2) NOT NULL,         -- Dinero liquidado hoy
    medio_pago ENUM('Transferencia', 'Cheque', 'Divisas', 'Otro') NOT NULL,
    ultima_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (id_sucursal) REFERENCES sucursales(id_sucursal),
    FOREIGN KEY (id_proveedor) REFERENCES maestro_proveedores(id_proveedor),
    UNIQUE KEY uq_suc_pago_prov_fecha (id_sucursal, id_proveedor, fecha, medio_pago)
);
