-- =========================================================================
-- SCRIPT DE DATOS DE PRUEBA / SEED
-- Compatible con el nuevo esquema de KPIs para Red de Farmacias
-- =========================================================================

-- 1. Sucursales
INSERT INTO sucursales (id_sucursal, codigo_sucursal, nombre, ciudad) VALUES
(1, 'F001', 'Farmacia Central', 'Caracas'),
(2, 'F002', 'Farmacia Las Mercedes', 'Caracas'),
(3, 'F003', 'Farmacia Bella Vista', 'Maracaibo'),
(4, 'F004', 'Farmacia Los Sauces', 'Valencia'),
(5, 'F005', 'Farmacia El Parral', 'Valencia')
ON DUPLICATE KEY UPDATE nombre=VALUES(nombre), codigo_sucursal=VALUES(codigo_sucursal);

-- 2. Maestro de Productos (Muestra representativa de catálogo)
INSERT INTO maestro_productos (id_producto, codigo_barras, nombre_producto, laboratorio, nombre_proveedor_habitual) VALUES
(1, '7591001', 'Atorvastatina 20mg x 30 Tab', 'Pfizer', 'Droguería Nena'),
(2, '7591002', 'Losartán Potásico 50mg x 30 Comp', 'Calox', 'Cobeca'),
(3, '7591003', 'Amoxicilina + Ác. Clavulánico 875mg', 'Genven', 'Drolanca'),
(4, '7591004', 'Ibuprofeno 400mg x 20 Cáps', 'Bayer', 'Cobeca'),
(5, '7591005', 'Paracetamol 500mg x 20 Tab', 'Calox', 'Droguería Nena'),
(6, '7591006', 'Omeprazol 20mg x 28 Cáps', 'Leti', 'Cobeca'),
(7, '7591007', 'Vitamina C 1000mg Efervescente', 'Bayer', 'Drolanca'),
(8, '7591008', 'Metformina 850mg x 30 Tab', 'Merck', 'Cobeca'),
(9, '7591009', 'Loratadina 10mg x 10 Tab', 'Leti', 'Droguería Nena'),
(10, '7591010', 'Cetirizina 10mg x 10 Tab', 'Genven', 'Cobeca')
ON DUPLICATE KEY UPDATE nombre_producto=VALUES(nombre_producto);

-- 3. Ventas Diarias
INSERT INTO kpi_ventas_diarias (id_sucursal, fecha, total_facturado, cantidad_tickets) VALUES
(1, CURDATE() - INTERVAL 2 DAY, 3450.80, 115),
(1, CURDATE() - INTERVAL 1 DAY, 4120.50, 130),
(1, CURDATE(), 2980.00, 95),
(2, CURDATE() - INTERVAL 1 DAY, 2890.00, 88),
(2, CURDATE(), 3150.25, 92),
(3, CURDATE() - INTERVAL 1 DAY, 1950.40, 65),
(3, CURDATE(), 2100.00, 70),
(4, CURDATE(), 1850.00, 60),
(5, CURDATE(), 2300.00, 75)
ON DUPLICATE KEY UPDATE total_facturado=VALUES(total_facturado);

-- 4. Inventario y Quiebres (con costo_unitario)
INSERT INTO kpi_inventario_sucursal (id_sucursal, id_producto, stock_actual, stock_minimo, costo_unitario) VALUES
(1, 1, 5, 25, 8.50),    -- Alerta: quiebre
(1, 2, 0, 30, 4.20),    -- Alerta: agotado
(1, 3, 40, 20, 12.00),  -- OK
(1, 4, 8, 20, 3.80),    -- Alerta: quiebre
(1, 5, 65, 30, 2.10),   -- OK
(2, 1, 0, 15, 8.50),    -- Alerta: agotado
(2, 2, 12, 20, 4.20),   -- Alerta: quiebre
(2, 6, 2, 25, 5.60)     -- Alerta: quiebre
ON DUPLICATE KEY UPDATE stock_actual=VALUES(stock_actual), costo_unitario=VALUES(costo_unitario);

-- 5. Ventas por Producto
INSERT INTO kpi_ventas_por_producto (id_sucursal, fecha, id_producto, unidades_vendidas, total_venta_monto) VALUES
(1, CURDATE(), 1, 22, 330.00),
(1, CURDATE(), 2, 35, 280.00),
(1, CURDATE(), 3, 18, 450.00),
(1, CURDATE(), 4, 40, 320.00),
(1, CURDATE(), 7, 25, 375.00),
(2, CURDATE(), 3, 15, 375.00),
(2, CURDATE(), 5, 30, 150.00)
ON DUPLICATE KEY UPDATE total_venta_monto=VALUES(total_venta_monto);

-- 6. Compras y Abastecimiento
INSERT INTO kpi_compras_por_producto (id_sucursal, fecha, id_producto, unidades_compradas, total_compra_monto) VALUES
(1, CURDATE() - INTERVAL 2 DAY, 1, 50, 600.00),
(1, CURDATE() - INTERVAL 2 DAY, 2, 100, 550.00),
(1, CURDATE() - INTERVAL 1 DAY, 3, 40, 760.00)
ON DUPLICATE KEY UPDATE total_compra_monto=VALUES(total_compra_monto);

-- 7. Ventas por Vendedor
INSERT INTO kpi_ventas_vendedor (id_sucursal, fecha, nombre_vendedor, total_vendido, cantidad_operaciones) VALUES
(1, CURDATE(), 'María Gómez', 1250.00, 38),
(1, CURDATE(), 'Carlos Pérez', 980.50, 32),
(1, CURDATE(), 'Ana Rodríguez', 749.50, 25),
(2, CURDATE(), 'José Morales', 1650.00, 50),
(2, CURDATE(), 'Laura Silva', 1500.25, 42)
ON DUPLICATE KEY UPDATE total_vendido=VALUES(total_vendido);

-- 8. Formas de Pago
INSERT INTO kpi_formas_pago (id_sucursal, fecha, forma_pago, total_ingresado) VALUES
(1, CURDATE(), 'Pago Móvil', 1250.00),
(1, CURDATE(), 'Tarjeta Débito', 950.00),
(1, CURDATE(), 'Efectivo', 480.00),
(1, CURDATE(), 'Transferencia', 300.00),
(2, CURDATE(), 'Pago Móvil', 1400.00),
(2, CURDATE(), 'Tarjeta Débito', 1100.00),
(2, CURDATE(), 'Efectivo', 650.25)
ON DUPLICATE KEY UPDATE total_ingresado=VALUES(total_ingresado);

-- 9. Saldos en Bancos
INSERT INTO kpi_saldos_bancos (id_sucursal, fecha, nombre_banco, numero_cuenta_oculto, saldo_disponible) VALUES
(1, CURDATE(), 'Banesco', '4521', 8450.00),
(1, CURDATE(), 'Banco Mercantil', '9012', 4320.50),
(1, CURDATE(), 'BBVA Provincial', '3341', 2980.00),
(2, CURDATE(), 'Banesco', '7810', 9200.00)
ON DUPLICATE KEY UPDATE saldo_disponible=VALUES(saldo_disponible);

-- 9.1 Cajas de Efectivo
INSERT INTO kpi_cajas_efectivo (id_sucursal, fecha, tipo_caja, moneda, saldo_efectivo) VALUES
(1, CURDATE(), 'Caja Principal / Bóveda', 'USD', 3450.00),
(1, CURDATE(), 'Caja Principal / Bóveda', 'VES', 125000.00),
(1, CURDATE(), 'Caja Chica', 'USD', 250.00),
(1, CURDATE(), 'Caja Punto de Venta', 'USD', 820.00),
(2, CURDATE(), 'Caja Principal / Bóveda', 'USD', 2900.00),
(2, CURDATE(), 'Caja Principal / Bóveda', 'VES', 98000.00)
ON DUPLICATE KEY UPDATE saldo_efectivo=VALUES(saldo_efectivo);

-- 10. Cuentas por Cobrar (CxC) por Cliente
INSERT INTO kpi_cxc_diario (id_sucursal, fecha, tipo_cliente, identificacion_cliente, nombre_cliente, saldo_pendiente, monto_otorgado_hoy, monto_recuperado_hoy) VALUES
(1, CURDATE(), 'Seguro / Empresa', 'J-30491823-1', 'Seguros Caracas', 4500.00, 600.00, 1200.00),
(1, CURDATE(), 'Seguro / Empresa', 'J-00012345-0', 'Mercantil Seguros', 3200.00, 450.00, 800.00),
(1, CURDATE(), 'Convenio', 'J-00045678-9', 'Empresas Polar (Convenio)', 1850.00, 200.00, 500.00),
(1, CURDATE(), 'Particular', 'V-14.238.901', 'Roberto Méndez', 420.00, 150.00, 0.00),
(2, CURDATE(), 'Particular', 'V-18.765.432', 'Elena Salazar', 310.50, 80.00, 50.00)
ON DUPLICATE KEY UPDATE saldo_pendiente=VALUES(saldo_pendiente);

-- 11. Cuentas por Pagar (CxP)
INSERT INTO kpi_cxp_diario (id_sucursal, fecha, nombre_proveedor, saldo_por_pagar) VALUES
(1, CURDATE(), 'Cobeca', 7850.00),
(1, CURDATE(), 'Droguería Nena', 5620.00),
(1, CURDATE(), 'Drolanca', 3940.00)
ON DUPLICATE KEY UPDATE saldo_por_pagar=VALUES(saldo_por_pagar);
