-- =========================================================================
-- SCRIPT DEFINITIVO Y OPTIMIZADO: BASE DE DATOS CENTRALIZADA PARA KPIs
-- PROYECTO: GRUPO DE FARMACIAS (DISEÑO NORMALIZADO PARA ALTO VOLUMEN)
-- Métrica: 35+ Sucursales | 40,000+ Productos por Catálogo
-- =========================================================================

-- 1. Catálogo Base de Sucursales / Farmacias
CREATE TABLE IF NOT EXISTS sucursales (
    id_sucursal INT AUTO_INCREMENT PRIMARY KEY,
    codigo_sucursal VARCHAR(4) NOT NULL UNIQUE, -- Código alfanumérico único de 4 caracteres (Ej: S001, MCY1, CCS2)
    nombre VARCHAR(100) NOT NULL,
    ciudad VARCHAR(50),
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. TABLA MAESTRA DE PRODUCTOS (Normalizada y sin proveedor fijo)
-- El proveedor no es fijo del producto; se registra en las compras.
CREATE TABLE IF NOT EXISTS maestro_productos (
    id_producto INT AUTO_INCREMENT PRIMARY KEY,
    codigo_barras VARCHAR(50) NOT NULL UNIQUE, 
    nombre_producto VARCHAR(150) NOT NULL,
    laboratorio VARCHAR(120) NOT NULL,         -- Marca/Fabricante (Ej: Bayer, Pfizer, Calox)
    INDEX idx_maestro_lab (laboratorio)
);

-- 3. KPI: Ventas Diarias Globales (Facturación General y Ticket Promedio)
CREATE TABLE IF NOT EXISTS kpi_ventas_diarias (
    id_registro BIGINT AUTO_INCREMENT PRIMARY KEY,
    id_sucursal INT NOT NULL,
    fecha DATE NOT NULL,
    total_facturado DECIMAL(12, 2) NOT NULL,    -- Ventas brutas del día
    cantidad_tickets INT NOT NULL,              -- Transacciones/clientes atendidos
    ticket_promedio DECIMAL(10, 2) GENERATED ALWAYS AS (total_facturado / cantidad_tickets) STORED,
    ultima_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (id_sucursal) REFERENCES sucursales(id_sucursal),
    UNIQUE KEY uq_sucursal_fecha (id_sucursal, fecha)
);

-- 4. KPI: Inventario de Productos por Sucursal (Con Costo Unitario para Valorización)
-- Alerta de quiebre de stock cruzado con el catálogo maestro y cálculo de capital inmovilizado.
CREATE TABLE IF NOT EXISTS kpi_inventario_sucursal (
    id_inventario BIGINT AUTO_INCREMENT PRIMARY KEY,
    id_sucursal INT NOT NULL,
    id_producto INT NOT NULL,                  -- Enlace al maestro de productos
    stock_actual INT NOT NULL DEFAULT 0,
    stock_minimo INT NOT NULL DEFAULT 0,       -- Umbral personalizado por farmacia
    costo_unitario DECIMAL(10, 2) NOT NULL DEFAULT 0.00, -- Costo promedio/reposición para valorización
    valor_total_inventario DECIMAL(12, 2) GENERATED ALWAYS AS (stock_actual * costo_unitario) STORED,
    ultima_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (id_sucursal) REFERENCES sucursales(id_sucursal),
    FOREIGN KEY (id_producto) REFERENCES maestro_productos(id_producto),
    UNIQUE KEY uq_sucursal_producto (id_sucursal, id_producto)
);

-- 5. KPI: Ventas Consolidadas Diarias por Producto
CREATE TABLE IF NOT EXISTS kpi_ventas_por_producto (
    id_registro BIGINT AUTO_INCREMENT PRIMARY KEY,
    id_sucursal INT NOT NULL,
    fecha DATE NOT NULL,
    id_producto INT NOT NULL,                  -- Enlace al maestro de productos
    unidades_vendidas INT NOT NULL,            -- Volumen de salida diario
    total_venta_monto DECIMAL(12, 2) NOT NULL, -- Ingreso acumulado por el producto
    ultima_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (id_sucursal) REFERENCES sucursales(id_sucursal),
    FOREIGN KEY (id_producto) REFERENCES maestro_productos(id_producto),
    UNIQUE KEY uq_suc_fecha_prod (id_sucursal, fecha, id_producto)
);

-- 6. KPI: Compras y Abastecimiento Diario por Producto y Proveedor
-- Aquí se asocia el proveedor/distribuidor al que se le compró
CREATE TABLE IF NOT EXISTS kpi_compras_por_producto (
    id_registro BIGINT AUTO_INCREMENT PRIMARY KEY,
    id_sucursal INT NOT NULL,
    fecha DATE NOT NULL,
    id_producto INT NOT NULL,                  -- Enlace al maestro de productos
    nombre_proveedor VARCHAR(120) NOT NULL,    -- Droguería / Distribuidor (Ej: Cobeca, Nena, Drolanca)
    unidades_compradas INT NOT NULL,           -- Volumen ingresado
    total_compra_monto DECIMAL(12, 2) NOT NULL,-- Inversión/Costo de adquisición
    ultima_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (id_sucursal) REFERENCES sucursales(id_sucursal),
    FOREIGN KEY (id_producto) REFERENCES maestro_productos(id_producto),
    INDEX idx_comp_prov (nombre_proveedor),
    UNIQUE KEY uq_suc_fecha_compra_prod_prov (id_sucursal, fecha, id_producto, nombre_proveedor)
);

-- 7. KPI: Ventas por Vendedor y Sucursal (Evaluación del Personal)
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

-- 8. KPI: Métodos de Pago Utilizados (Flujo Financiero por Sucursal)
CREATE TABLE IF NOT EXISTS kpi_formas_pago (
    id_registro BIGINT AUTO_INCREMENT PRIMARY KEY,
    id_sucursal INT NOT NULL,
    fecha DATE NOT NULL,
    forma_pago ENUM('Efectivo', 'Tarjeta Crédito', 'Tarjeta Débito', 'Transferencia', 'Pago Móvil', 'Otro') NOT NULL,
    total_ingresado DECIMAL(12, 2) NOT NULL,
    ultima_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (id_sucursal) REFERENCES sucursales(id_sucursal),
    UNIQUE KEY uq_sucursal_pago_fecha (id_sucursal, forma_pago, fecha)
);

-- 9. KPI: Saldos de Cuentas Bancarias (Tesorería / Disponibilidad Bancaria)
CREATE TABLE IF NOT EXISTS kpi_saldos_bancos (
    id_registro BIGINT AUTO_INCREMENT PRIMARY KEY,
    id_sucursal INT NOT NULL,
    fecha DATE NOT NULL,                        -- Saldo al cierre de la jornada
    nombre_banco VARCHAR(80) NOT NULL,          -- Entidad bancaria
    numero_cuenta_oculto VARCHAR(10) NOT NULL,  -- Últimos 4 dígitos de control
    saldo_disponible DECIMAL(14, 2) NOT NULL,   -- Capital disponible
    ultima_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (id_sucursal) REFERENCES sucursales(id_sucursal),
    UNIQUE KEY uq_sucursal_banco_fecha (id_sucursal, nombre_banco, numero_cuenta_oculto, fecha)
);

-- 9.1 KPI: Cajas de Efectivo por Sucursal (Caja Principal / Bóveda / Cajas Operativas)
CREATE TABLE IF NOT EXISTS kpi_cajas_efectivo (
    id_registro BIGINT AUTO_INCREMENT PRIMARY KEY,
    id_sucursal INT NOT NULL,
    fecha DATE NOT NULL,
    tipo_caja ENUM('Caja Principal / Bóveda', 'Caja Chica', 'Caja Punto de Venta') NOT NULL DEFAULT 'Caja Principal / Bóveda',
    moneda ENUM('USD', 'VES', 'EUR', 'Otra') NOT NULL DEFAULT 'USD',
    saldo_efectivo DECIMAL(12, 2) NOT NULL,     -- Saldo físico verificado al cierre
    ultima_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (id_sucursal) REFERENCES sucursales(id_sucursal),
    UNIQUE KEY uq_sucursal_caja_fecha (id_sucursal, tipo_caja, moneda, fecha)
);

-- 10. KPI: Cuentas por Cobrar (CxC) por Cliente (Particulares, Seguros y Convenios Empresariales)
CREATE TABLE IF NOT EXISTS kpi_cxc_diario (
    id_registro BIGINT AUTO_INCREMENT PRIMARY KEY,
    id_sucursal INT NOT NULL,
    fecha DATE NOT NULL,
    tipo_cliente ENUM('Particular', 'Seguro / Empresa', 'Convenio') NOT NULL DEFAULT 'Particular',
    identificacion_cliente VARCHAR(30),         -- Cédula, RIF o Nro. Afiliado
    nombre_cliente VARCHAR(150) NOT NULL,       -- Nombre del cliente o razón social
    saldo_pendiente DECIMAL(12, 2) NOT NULL,    -- Lo que nos debe acumulado a la fecha
    monto_otorgado_hoy DECIMAL(12, 2) NOT NULL DEFAULT 0.00,  -- Crédito nuevo asignado hoy
    monto_recuperado_hoy DECIMAL(12, 2) NOT NULL DEFAULT 0.00,-- Cobranza/Abonos recibidos hoy
    ultima_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (id_sucursal) REFERENCES sucursales(id_sucursal),
    INDEX idx_cxc_tipo (tipo_cliente),
    UNIQUE KEY uq_suc_cxc_fecha (id_sucursal, nombre_cliente, fecha)
);

-- 11. KPI: Cuentas por Pagar (CxP) - Deudas vigentes con Proveedores/Laboratorios
CREATE TABLE IF NOT EXISTS kpi_cxp_diario (
    id_registro BIGINT AUTO_INCREMENT PRIMARY KEY,
    id_sucursal INT NOT NULL,
    fecha DATE NOT NULL,
    nombre_proveedor VARCHAR(120) NOT NULL,    -- Distribuidor al que le debemos
    saldo_por_pagar DECIMAL(12, 2) NOT NULL,   -- Deuda total acumulada a la fecha
    ultima_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (id_sucursal) REFERENCES sucursales(id_sucursal),
    UNIQUE KEY uq_suc_cxp_fecha (id_sucursal, nombre_proveedor, fecha)
);

-- 12. KPI: Egresos por Pagos Realizados a Proveedores
CREATE TABLE IF NOT EXISTS kpi_pagos_proveedores (
    id_registro BIGINT AUTO_INCREMENT PRIMARY KEY,
    id_sucursal INT NOT NULL,
    fecha DATE NOT NULL,
    nombre_proveedor VARCHAR(120) NOT NULL,
    monto_pagado DECIMAL(12, 2) NOT NULL,      -- Dinero abonado o liquidado hoy
    medio_pago ENUM('Transferencia', 'Cheque', 'Divisas', 'Otro') NOT NULL,
    ultima_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (id_sucursal) REFERENCES sucursales(id_sucursal),
    UNIQUE KEY uq_suc_pago_prov_fecha (id_sucursal, nombre_proveedor, fecha, medio_pago)
);
