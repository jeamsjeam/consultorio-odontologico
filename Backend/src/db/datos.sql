INSERT INTO rol (nombre) VALUES ('Administrador'), ('Cliente');
INSERT INTO usuario (usuario, clave, estado, rolId) VALUES ('admin', '1234', true, 1);
INSERT INTO tipo_persona (nombre) VALUES ('Empleado'), ('Cliente');
INSERT INTO estado_cita (nombre) VALUES ('Creada'), ('Asistio'), ('No asistio'), ('Borrada');
INSERT INTO pais (nombre) VALUES ('Venezuela');
INSERT INTO estado (nombre, paisId) VALUES ('Táchira', 1);
INSERT INTO municipio (nombre, estadoId) VALUES ('Junin', 1), ('San Cristóbal', 1);
INSERT INTO servicio (nombre, costo, descripcion, estado, imagen) VALUES
('Limpieza dental profesional', 120000.00, 'Eliminación de placa y sarro en dientes', 1, "imagen1"),
('Blanqueamiento dental', 450000.00, 'Tratamiento para aclarar el tono de los dientes', 1, "imagen1"),
('Extracción de muela', 180000.00, 'Extracción de muela de forma simple', 1, "imagen1"),
('Ortodoncia', 150000.00, 'Pago mensual para tratamiento de ortodoncia', 1, "imagen1"),
('Implante dental', 3000000.00, 'Implante dental individual con corona', 1, "imagen1"),
('Carilla de porcelana', 1000000.00, 'Carilla estética para dientes frontales', 1, "imagen1"),
('Tratamiento de conducto', 350000.00, 'Endodoncia para salvar dientes con infección', 1, "imagen1"),
('Resina dental', 100000.00, 'Empaste estético para cavidades', 1, "imagen1"),
('Diseño de sonrisa', 2500000.00, 'Tratamiento estético completo para sonrisa', 1, "imagen1"),
('Prótesis dental', 2000000.00, 'Prótesis parcial o completa según necesidad', 1, "imagen1");
