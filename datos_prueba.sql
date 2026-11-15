-- =========================================================================
-- SCRIPT DE DATOS DE PRUEBA / SEED DEFINITIVO Y NORMALIZADO
-- GRUPO DE FARMACIAS (HOMOLOGADO A NORMA MIVO ERP 7.1)
-- =========================================================================

-- 1. Maestro Sucursales
INSERT INTO sucursales (id_sucursal, codigo_sucursal, nombre, ciudad, zona) VALUES
(1, 'F001', 'Farmacia La Corina (Sede Principal)', 'Puerto Cabello', 'Carabobo'),
(2, 'F002', 'Farmacia La corina 2', 'Puerto Cabello', 'Carabobo'),
(3, 'F003', 'Farmacia Morillo', 'Valencia', 'Carabobo'),
(4, 'F004', 'Farmacia farmavital', 'Guacara', 'Carabobo'),
(5, 'F005', 'Farmacia Descuento a su salud', 'San Diego', 'Carabobo')
ON DUPLICATE KEY UPDATE nombre=VALUES(nombre), codigo_sucursal=VALUES(codigo_sucursal), ciudad=VALUES(ciudad), zona=VALUES(zona);

-- 2. Maestro Líneas (13 Líneas Maestras MIVO ERP 7.1)
INSERT INTO maestro_lineas (id_linea, codigo_linea, descripcion_linea) VALUES
(1, '01', 'Medicamentos'),
(2, '02', 'Cuidado Personal e Higiene'),
(3, '03', 'Belleza y Cosméticos'),
(4, '04', 'Bebés y Maternidad'),
(5, '05', 'Salud Sexual y Reproductiva'),
(6, '06', 'Nutrición y Suplementos'),
(7, '07', 'Alimentos y Bebidas'),
(8, '08', 'Cuidado del Hogar'),
(9, '09', 'Mascotas'),
(10, '10', 'Equipos Médicos y Diagnóstico'),
(11, '11', 'Ortopedia y Rehabilitación'),
(12, '12', 'Misceláneos y Papelería'),
(13, '13', 'Servicios Farmacéuticos')
ON DUPLICATE KEY UPDATE descripcion_linea=VALUES(descripcion_linea);

-- 3. Maestro Sublíneas (Muestra Homologada MIVO ERP 7.1)
INSERT INTO maestro_sublineas (id_sublinea, codigo_sublinea, descripcion_sublinea, id_linea) VALUES
(1, '0101', 'Analgésicos y Antiinflamatorios', 1),
(2, '0102', 'Antibióticos y Antivirales', 1),
(3, '0103', 'Cardiovascular e Hipertensión', 1),
(4, '0104', 'Gastrointestinal', 1),
(5, '0105', 'Respiratorio y Antihistamínicos', 1),
(6, '0106', 'Dermatología Médica', 1),
(7, '0107', 'Endocrinología y Diabetes', 1),
(8, '0201', 'Higiene Bucal', 2),
(9, '0202', 'Cuidado Capilar', 2),
(10, '0601', 'Vitaminas y Minerales', 6)
ON DUPLICATE KEY UPDATE descripcion_sublinea=VALUES(descripcion_sublinea), id_linea=VALUES(id_linea);

-- 4. Maestro Laboratorios / Fabricantes
INSERT INTO maestro_laboratorios (id_laboratorio, codigo_laboratorio, nombre_laboratorio) VALUES
(1, 'LAB001', 'Pfizer'),
(2, 'LAB002', 'Bayer'),
(3, 'LAB003', 'Calox'),
(4, 'LAB004', 'Laboratorios Leti'),
(5, 'LAB005', 'Genven'),
(6, 'LAB006', 'Merck'),
(7, 'LAB007', 'Novartis'),
(8, 'LAB008', 'Sanofi')
ON DUPLICATE KEY UPDATE nombre_laboratorio=VALUES(nombre_laboratorio);

-- 5. Maestro Tipos de Proveedor (MIVO ERP 7.1 - Norma Oficial)
INSERT INTO maestro_tipos_proveedor (codigo_tipo_proveedor, descripcion) VALUES
('01', 'Mercancía'),
('02', 'Servicios'),
('03', 'Activos y Equipos'),
('04', 'Tecnología'),
('05', 'Logística y Transporte'),
('06', 'Insumos y Mantenimiento'),
('07', 'Financiero'),
('08', 'Marketing y Publicidad'),
('09', 'Gubernamental'),
('10', 'Intercompañía'),
('99', 'Otros')
ON DUPLICATE KEY UPDATE descripcion=VALUES(descripcion);

-- 6. Maestro Segmentos de Proveedor (MIVO ERP 7.1 - Norma Oficial)
INSERT INTO maestro_segmentos_proveedor (codigo_segmento, descripcion) VALUES
('P0101', 'Droguerías Estratégicas'),
('P0102', 'Droguerías Habituales'),
('P0103', 'Droguerías Ocasionales'),
('P0104', 'Laboratorios Farmacéuticos Directos'),
('P0105', 'Farmacia Intercompañía'),
('P0106', 'Otros Distribuidores'),
('P0107', 'Distribuidores de Consumo Masivo'),
('P0108', 'Distribuidores de Alimentos'),
('P0109', 'Importadores Directos'),
('P0110', 'Fabricantes Locales'),
('P0111', 'Distribuidores de Misceláneos'),
('P0201', 'Servicios Públicos'),
('P0202', 'Servicios de Seguridad y Vigilancia'),
('P0203', 'Servicios de Mantenimiento'),
('P0401', 'Proveedores de Software'),
('P0402', 'Hardware e Infraestructura'),
('P0501', 'Transporte y Envíos'),
('P9999', 'Otros Proveedores')
ON DUPLICATE KEY UPDATE descripcion=VALUES(descripcion);

-- 7. Maestro Tipos y Segmentos de Cliente (MIVO ERP 7.1)
INSERT INTO maestro_tipos_cliente (codigo_tipo_cliente, descripcion) VALUES
('A01', 'Contado'),
('A02', 'Crédito')
ON DUPLICATE KEY UPDATE descripcion=VALUES(descripcion);

INSERT INTO maestro_segmentos_cliente (codigo_segmento_cliente, descripcion) VALUES
('C01', 'Ventas Mostrador'),
('C02', 'Empresa / Comercio'),
('C03', 'Farmacia Intercompañía'),
('C04', 'Instituciones / Seguros'),
('C05', 'Empleados'),
('C99', 'Otros Clientes')
ON DUPLICATE KEY UPDATE descripcion=VALUES(descripcion);

-- 8. Maestro Proveedores (Enlazados con códigos 01..10 y P0101..P9999)
INSERT INTO maestro_proveedores (id_proveedor, codigo_proveedor, nombre_proveedor, rif_proveedor, tipo_proveedor, segmento, telefono) VALUES
(1, 'PRV0000001', 'Droguería Cobeca', 'J-00012345-1', '01', 'P0101', '0261-7001000'),
(2, 'PRV0000002', 'Droguería Nena', 'J-00045678-2', '01', 'P0101', '0212-9052000'),
(3, 'PRV0000003', 'Drolanca', 'J-00089123-3', '01', 'P0102', '0274-2003000'),
(4, 'PRV0000004', 'Grupo Farvenca', 'J-00078945-4', '01', 'P0101', '0212-2004000'),
(5, 'PRV0000005', 'Laboratorios Leti Directo', 'J-00032165-5', '01', 'P0104', '0212-3605000'),
(6, 'PRV0000006', 'Mervis Technology CA', 'J-40192831-2', '04', 'P0401', '0212-7891234'),
(7, 'PRV0000007', 'Transfarma Logística', 'J-31298451-9', '05', 'P0501', '0241-8712390')
ON DUPLICATE KEY UPDATE nombre_proveedor=VALUES(nombre_proveedor), tipo_proveedor=VALUES(tipo_proveedor), segmento=VALUES(segmento);

-- 9. Maestro Clientes (Enlazados a Tipos A01/A02 y Segmentos C01..C05, C99)
INSERT INTO maestro_clientes (id_cliente, codigo_cliente, nombre_cliente, tipo_cliente, segmento_cliente, identificacion) VALUES
(1, 'CLI0000001', 'Roberto Méndez', 'A01', 'C01', 'V-14.238.901'),
(2, 'CLI0000002', 'Elena Salazar', 'A01', 'C01', 'V-18.765.432'),
(3, 'CLI0000003', 'Seguros Caracas', 'A02', 'C04', 'J-30491823-1'),
(4, 'CLI0000004', 'Mercantil Seguros', 'A02', 'C04', 'J-00012345-0'),
(5, 'CLI0000005', 'Empresas Polar (Convenio)', 'A02', 'C02', 'J-00045678-9'),
(6, 'CLI0000006', 'Banesco Seguros', 'A02', 'C04', 'J-29837192-3'),
(7, 'CLI0000007', 'Carlos Mendoza (Personal Farma)', 'A01', 'C05', 'V-20.192.341')
ON DUPLICATE KEY UPDATE nombre_cliente=VALUES(nombre_cliente), tipo_cliente=VALUES(tipo_cliente), segmento_cliente=VALUES(segmento_cliente);

-- 10. Maestro Productos (Norma MIVO: SKU 6 dígitos, código de barras, enlazado a línea, sublínea y lab)
INSERT INTO maestro_productos (id_producto, codigo_articulo, codigo_barras, nombre_producto, id_linea, id_sublinea, id_laboratorio) VALUES
(1, '000101', '7591001000001', 'Atorvastatina 20mg x 30 Tab', 1, 3, 1),
(2, '000102', '7591002000002', 'Losartán Potásico 50mg x 30 Comp', 1, 3, 3),
(3, '000103', '7591003000003', 'Amoxicilina + Ác. Clavulánico 875mg', 1, 2, 5),
(4, '000104', '7591004000004', 'Ibuprofeno 400mg x 20 Cáps', 1, 1, 2),
(5, '000105', '7591005000005', 'Paracetamol 500mg x 20 Tab', 1, 1, 3),
(6, '000106', '7591006000006', 'Omeprazol 20mg x 28 Cáps', 1, 4, 4),
(7, '000107', '7591007000007', 'Vitamina C 1000mg Efervescente', 6, 10, 2),
(8, '000108', '7591008000008', 'Metformina 850mg x 30 Tab', 1, 7, 6),
(9, '000109', '7591009000009', 'Loratadina 10mg x 10 Tab', 1, 5, 4),
(10, '000110', '7591010000010', 'Cetirizina 10mg x 10 Tab', 1, 5, 5)
ON DUPLICATE KEY UPDATE nombre_producto=VALUES(nombre_producto), codigo_barras=VALUES(codigo_barras);

-- 11. Ventas Diarias
INSERT INTO kpi_ventas_diarias (id_sucursal, fecha, total_facturado, ventas_contado, ventas_credito, numero_operaciones, operaciones_contado, operaciones_credito) VALUES
(1, CURDATE() - INTERVAL 2 DAY, 3450.80, 2760.64, 690.16, 115, 92, 23),
(1, CURDATE() - INTERVAL 1 DAY, 4120.50, 3296.40, 824.10, 130, 104, 26),
(1, CURDATE(), 2980.00, 2384.00, 596.00, 95, 76, 19),
(2, CURDATE() - INTERVAL 1 DAY, 2890.00, 2312.00, 578.00, 88, 70, 18),
(2, CURDATE(), 3150.25, 2520.20, 630.05, 92, 74, 18),
(3, CURDATE() - INTERVAL 1 DAY, 1950.40, 1560.32, 390.08, 65, 52, 13),
(3, CURDATE(), 2100.00, 1680.00, 420.00, 70, 56, 14),
(4, CURDATE(), 1850.00, 1480.00, 370.00, 60, 48, 12),
(5, CURDATE(), 2300.00, 1840.00, 460.00, 75, 60, 15)
ON DUPLICATE KEY UPDATE total_facturado=VALUES(total_facturado), numero_operaciones=VALUES(numero_operaciones);

-- 12. Inventario por Sucursal (Con PVP y Costo)
INSERT INTO kpi_inventario_sucursal (id_sucursal, id_producto, stock_actual, stock_minimo, costo_unitario, precio_unitario) VALUES
(1, 1, 5, 25, 8.50, 12.75),
(1, 2, 0, 30, 4.20, 6.30),
(1, 3, 40, 20, 12.00, 18.00),
(1, 4, 8, 20, 3.80, 5.70),
(1, 5, 65, 30, 2.10, 3.15),
(1, 6, 14, 15, 5.60, 8.40),
(1, 7, 22, 10, 4.50, 6.75),
(2, 1, 0, 15, 8.50, 12.75),
(2, 2, 12, 20, 4.20, 6.30),
(2, 6, 2, 25, 5.60, 8.40)
ON DUPLICATE KEY UPDATE stock_actual=VALUES(stock_actual), costo_unitario=VALUES(costo_unitario), precio_unitario=VALUES(precio_unitario);

-- 13. Ventas por Producto
INSERT INTO kpi_ventas_por_producto (id_sucursal, fecha, id_producto, unidades_vendidas, total_venta_monto) VALUES
(1, CURDATE(), 1, 22, 280.50),
(1, CURDATE(), 2, 35, 220.50),
(1, CURDATE(), 3, 18, 324.00),
(1, CURDATE(), 4, 40, 228.00),
(1, CURDATE(), 7, 25, 168.75),
(2, CURDATE(), 3, 15, 270.00),
(2, CURDATE(), 5, 30, 94.50)
ON DUPLICATE KEY UPDATE total_venta_monto=VALUES(total_venta_monto);

-- 14. Compras Diarias Globales
INSERT INTO kpi_compras_diarias (id_sucursal, fecha, total_comprado, unidades_compradas, numero_facturas_compra, compras_contado, compras_credito) VALUES
(1, CURDATE() - INTERVAL 2 DAY, 1150.00, 150, 2, 345.00, 805.00),
(1, CURDATE() - INTERVAL 1 DAY, 760.00, 40, 1, 228.00, 532.00),
(2, CURDATE() - INTERVAL 1 DAY, 980.00, 75, 2, 294.00, 686.00)
ON DUPLICATE KEY UPDATE total_comprado=VALUES(total_comprado);

-- 15. Compras por Producto y Proveedor (Permite Arbitraje de Precios)
INSERT INTO kpi_compras_por_producto (id_sucursal, fecha, id_producto, id_proveedor, unidades_compradas, total_compra_monto) VALUES
(1, CURDATE() - INTERVAL 2 DAY, 1, 2, 50, 425.00),
(1, CURDATE() - INTERVAL 1 DAY, 1, 1, 40, 320.00),
(1, CURDATE() - INTERVAL 2 DAY, 2, 1, 100, 420.00),
(1, CURDATE() - INTERVAL 1 DAY, 2, 3, 50, 225.00),
(1, CURDATE() - INTERVAL 1 DAY, 3, 3, 40, 480.00),
(1, CURDATE() - INTERVAL 2 DAY, 3, 4, 30, 390.00)
ON DUPLICATE KEY UPDATE total_compra_monto=VALUES(total_compra_monto);

-- 16. Ventas por Vendedor
INSERT INTO kpi_ventas_vendedor (id_sucursal, fecha, nombre_vendedor, total_vendido, cantidad_operaciones) VALUES
(1, CURDATE(), 'María Gómez', 1250.00, 38),
(1, CURDATE(), 'Carlos Pérez', 980.50, 32),
(1, CURDATE(), 'Ana Rodríguez', 749.50, 25),
(2, CURDATE(), 'José Morales', 1650.00, 50),
(2, CURDATE(), 'Laura Silva', 1500.25, 42)
ON DUPLICATE KEY UPDATE total_vendido=VALUES(total_vendido);

-- 17. Formas de Pago
INSERT INTO kpi_formas_pago (id_sucursal, fecha, forma_pago, total_ingresado) VALUES
(1, CURDATE(), 'Pago Móvil', 1250.00),
(1, CURDATE(), 'Tarjeta Débito', 950.00),
(1, CURDATE(), 'Efectivo', 480.00),
(1, CURDATE(), 'Transferencia', 300.00),
(2, CURDATE(), 'Pago Móvil', 1400.00),
(2, CURDATE(), 'Tarjeta Débito', 1100.00),
(2, CURDATE(), 'Efectivo', 650.25)
ON DUPLICATE KEY UPDATE total_ingresado=VALUES(total_ingresado);

-- 18. Bancos y Cajas
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

-- 19. CxC (enlazado a id_cliente) y CxP (enlazado a id_proveedor)
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
