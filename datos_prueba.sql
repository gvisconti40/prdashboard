-- =========================================================================
-- SCRIPT DE DATOS DE PRUEBA / SEED DEFINITIVO Y NORMALIZADO
-- GRUPO DE FARMACIAS (35+ SUCURSALES | MAESTROS CENTRALIZADOS)
-- =========================================================================

-- 1. Maestro Sucursales
INSERT INTO sucursales (id_sucursal, codigo_sucursal, nombre, ciudad, zona) VALUES
(1, 'F001', 'Farmacia Central', 'Caracas', 'Gran Caracas'),
(2, 'F002', 'Farmacia Las Mercedes', 'Caracas', 'Gran Caracas'),
(3, 'F003', 'Farmacia Bella Vista', 'Maracaibo', 'Occidente'),
(4, 'F004', 'Farmacia Los Sauces', 'Valencia', 'Centro'),
(5, 'F005', 'Farmacia El Parral', 'Valencia', 'Centro')
ON DUPLICATE KEY UPDATE nombre=VALUES(nombre), codigo_sucursal=VALUES(codigo_sucursal), zona=VALUES(zona);

-- 2. Maestro Líneas (Código 6 chars)
INSERT INTO maestro_lineas (id_linea, codigo_linea, descripcion_linea) VALUES
(1, 'LIN001', 'Cardiovascular'),
(2, 'LIN002', 'Antibióticos y Antivirales'),
(3, 'LIN003', 'Analgésicos y Antiinflamatorios'),
(4, 'LIN004', 'Gastrointestinales'),
(5, 'LIN005', 'Vitaminas y Suplementos'),
(6, 'LIN006', 'Antihistamínicos y Respiratorios'),
(7, 'LIN007', 'Endocrinología y Diabetes')
ON DUPLICATE KEY UPDATE descripcion_linea=VALUES(descripcion_linea);

-- 3. Maestro Laboratorios (Código 6 chars)
INSERT INTO maestro_laboratorios (id_laboratorio, codigo_laboratorio, nombre_laboratorio) VALUES
(1, 'LAB001', 'Pfizer'),
(2, 'LAB002', 'Bayer'),
(3, 'LAB003', 'Calox'),
(4, 'LAB004', 'Leti'),
(5, 'LAB005', 'Genven'),
(6, 'LAB006', 'Merck'),
(7, 'LAB007', 'Novartis'),
(8, 'LAB008', 'Sanofi')
ON DUPLICATE KEY UPDATE nombre_laboratorio=VALUES(nombre_laboratorio);

-- 4. Maestro Proveedores (Código 10 chars)
INSERT INTO maestro_proveedores (id_proveedor, codigo_proveedor, nombre_proveedor, rif_proveedor) VALUES
(1, 'PRV0000001', 'Droguería Cobeca', 'J-00012345-1'),
(2, 'PRV0000002', 'Droguería Nena', 'J-00045678-2'),
(3, 'PRV0000003', 'Drolanca', 'J-00089123-3'),
(4, 'PRV0000004', 'Grupo Farvenca', 'J-00078945-4'),
(5, 'PRV0000005', 'Droguería Vitalis', 'J-00032165-5')
ON DUPLICATE KEY UPDATE nombre_proveedor=VALUES(nombre_proveedor);

-- 5. Maestro Clientes (Código 10 chars)
INSERT INTO maestro_clientes (id_cliente, codigo_cliente, nombre_cliente, tipo_cliente, identificacion) VALUES
(1, 'CLI0000001', 'Roberto Méndez', 'Particular', 'V-14.238.901'),
(2, 'CLI0000002', 'Elena Salazar', 'Particular', 'V-18.765.432'),
(3, 'CLI0000003', 'Seguros Caracas', 'Seguro / Empresa', 'J-30491823-1'),
(4, 'CLI0000004', 'Mercantil Seguros', 'Seguro / Empresa', 'J-00012345-0'),
(5, 'CLI0000005', 'Empresas Polar (Convenio)', 'Convenio', 'J-00045678-9'),
(6, 'CLI0000006', 'Banesco Seguros', 'Seguro / Empresa', 'J-29837192-3')
ON DUPLICATE KEY UPDATE nombre_cliente=VALUES(nombre_cliente);

-- 6. Maestro Productos (Código de artículo 30 chars, código de barras >= 15 chars, enlazado a línea y lab)
INSERT INTO maestro_productos (id_producto, codigo_articulo, codigo_barras, nombre_producto, id_linea, id_laboratorio) VALUES
(1, 'ART-CARDIO-00001', '759100100000015', 'Atorvastatina 20mg x 30 Tab', 1, 1),
(2, 'ART-CARDIO-00002', '759100200000025', 'Losartán Potásico 50mg x 30 Comp', 1, 3),
(3, 'ART-ANTI-000001',  '759100300000035', 'Amoxicilina + Ác. Clavulánico 875mg', 2, 5),
(4, 'ART-ANALG-00001',  '759100400000045', 'Ibuprofeno 400mg x 20 Cáps', 3, 2),
(5, 'ART-ANALG-00002',  '759100500000055', 'Paracetamol 500mg x 20 Tab', 3, 3),
(6, 'ART-GASTRO-0001',  '759100600000065', 'Omeprazol 20mg x 28 Cáps', 4, 4),
(7, 'ART-VITAM-00001',  '759100700000075', 'Vitamina C 1000mg Efervescente', 5, 2),
(8, 'ART-ENDOC-00001',  '759100800000085', 'Metformina 850mg x 30 Tab', 7, 6),
(9, 'ART-RESP-000001',  '759100900000095', 'Loratadina 10mg x 10 Tab', 6, 4),
(10, 'ART-RESP-000002', '759101000000105', 'Cetirizina 10mg x 10 Tab', 6, 5)
ON DUPLICATE KEY UPDATE nombre_producto=VALUES(nombre_producto), codigo_barras=VALUES(codigo_barras);

-- 7. Ventas Diarias
INSERT INTO kpi_ventas_diarias (id_sucursal, fecha, total_facturado, numero_operaciones) VALUES
(1, CURDATE() - INTERVAL 2 DAY, 3450.80, 115),
(1, CURDATE() - INTERVAL 1 DAY, 4120.50, 130),
(1, CURDATE(), 2980.00, 95),
(2, CURDATE() - INTERVAL 1 DAY, 2890.00, 88),
(2, CURDATE(), 3150.25, 92),
(3, CURDATE() - INTERVAL 1 DAY, 1950.40, 65),
(3, CURDATE(), 2100.00, 70),
(4, CURDATE(), 1850.00, 60),
(5, CURDATE(), 2300.00, 75)
ON DUPLICATE KEY UPDATE total_facturado=VALUES(total_facturado), numero_operaciones=VALUES(numero_operaciones);

-- 8. Inventario por Sucursal
INSERT INTO kpi_inventario_sucursal (id_sucursal, id_producto, stock_actual, stock_minimo, costo_unitario) VALUES
(1, 1, 5, 25, 8.50),
(1, 2, 0, 30, 4.20),
(1, 3, 40, 20, 12.00),
(1, 4, 8, 20, 3.80),
(1, 5, 65, 30, 2.10),
(2, 1, 0, 15, 8.50),
(2, 2, 12, 20, 4.20),
(2, 6, 2, 25, 5.60)
ON DUPLICATE KEY UPDATE stock_actual=VALUES(stock_actual), costo_unitario=VALUES(costo_unitario);

-- 9. Ventas por Producto
INSERT INTO kpi_ventas_por_producto (id_sucursal, fecha, id_producto, unidades_vendidas, total_venta_monto) VALUES
(1, CURDATE(), 1, 22, 330.00),
(1, CURDATE(), 2, 35, 280.00),
(1, CURDATE(), 3, 18, 450.00),
(1, CURDATE(), 4, 40, 320.00),
(1, CURDATE(), 7, 25, 375.00),
(2, CURDATE(), 3, 15, 375.00),
(2, CURDATE(), 5, 30, 150.00)
ON DUPLICATE KEY UPDATE total_venta_monto=VALUES(total_venta_monto);

-- 10. Compras por Producto y Proveedor
INSERT INTO kpi_compras_por_producto (id_sucursal, fecha, id_producto, id_proveedor, unidades_compradas, total_compra_monto) VALUES
(1, CURDATE() - INTERVAL 2 DAY, 1, 2, 50, 600.00),
(1, CURDATE() - INTERVAL 2 DAY, 2, 1, 100, 550.00),
(1, CURDATE() - INTERVAL 1 DAY, 3, 3, 40, 760.00)
ON DUPLICATE KEY UPDATE total_compra_monto=VALUES(total_compra_monto);

-- 11. Ventas por Vendedor
INSERT INTO kpi_ventas_vendedor (id_sucursal, fecha, nombre_vendedor, total_vendido, cantidad_operaciones) VALUES
(1, CURDATE(), 'María Gómez', 1250.00, 38),
(1, CURDATE(), 'Carlos Pérez', 980.50, 32),
(1, CURDATE(), 'Ana Rodríguez', 749.50, 25),
(2, CURDATE(), 'José Morales', 1650.00, 50),
(2, CURDATE(), 'Laura Silva', 1500.25, 42)
ON DUPLICATE KEY UPDATE total_vendido=VALUES(total_vendido);

-- 12. Formas de Pago
INSERT INTO kpi_formas_pago (id_sucursal, fecha, forma_pago, total_ingresado) VALUES
(1, CURDATE(), 'Pago Móvil', 1250.00),
(1, CURDATE(), 'Tarjeta Débito', 950.00),
(1, CURDATE(), 'Efectivo', 480.00),
(1, CURDATE(), 'Transferencia', 300.00),
(2, CURDATE(), 'Pago Móvil', 1400.00),
(2, CURDATE(), 'Tarjeta Débito', 1100.00),
(2, CURDATE(), 'Efectivo', 650.25)
ON DUPLICATE KEY UPDATE total_ingresado=VALUES(total_ingresado);

-- 13. Bancos y Cajas
INSERT INTO kpi_saldos_bancos (id_sucursal, fecha, nombre_banco, numero_cuenta_oculto, saldo_disponible) VALUES
(1, CURDATE(), 'Banesco', '4521', 8450.00),
(1, CURDATE(), 'Banco Mercantil', '9012', 4320.50),
(1, CURDATE(), 'BBVA Provincial', '3341', 2980.00),
(2, CURDATE(), 'Banesco', '7810', 9200.00)
ON DUPLICATE KEY UPDATE saldo_disponible=VALUES(saldo_disponible);

INSERT INTO kpi_cajas_efectivo (id_sucursal, fecha, tipo_caja, moneda, saldo_efectivo) VALUES
(1, CURDATE(), 'Caja Principal / Bóveda', 'USD', 3450.00),
(1, CURDATE(), 'Caja Principal / Bóveda', 'VES', 125000.00),
(1, CURDATE(), 'Caja Chica', 'USD', 250.00),
(1, CURDATE(), 'Caja Punto de Venta', 'USD', 820.00),
(2, CURDATE(), 'Caja Principal / Bóveda', 'USD', 2900.00),
(2, CURDATE(), 'Caja Principal / Bóveda', 'VES', 98000.00)
ON DUPLICATE KEY UPDATE saldo_efectivo=VALUES(saldo_efectivo);

-- 14. CxC (enlazado a id_cliente) y CxP (enlazado a id_proveedor)
INSERT INTO kpi_cxc_diario (id_sucursal, fecha, id_cliente, saldo_pendiente, monto_otorgado_hoy, monto_recuperado_hoy) VALUES
(1, CURDATE(), 3, 4500.00, 600.00, 1200.00),
(1, CURDATE(), 4, 3200.00, 450.00, 800.00),
(1, CURDATE(), 5, 1850.00, 200.00, 500.00),
(1, CURDATE(), 1, 420.00, 150.00, 0.00),
(2, CURDATE(), 2, 310.50, 80.00, 50.00)
ON DUPLICATE KEY UPDATE saldo_pendiente=VALUES(saldo_pendiente);

INSERT INTO kpi_cxp_diario (id_sucursal, fecha, id_proveedor, saldo_por_pagar) VALUES
(1, CURDATE(), 1, 7850.00),
(1, CURDATE(), 2, 5620.00),
(1, CURDATE(), 3, 3940.00)
ON DUPLICATE KEY UPDATE saldo_por_pagar=VALUES(saldo_por_pagar);
