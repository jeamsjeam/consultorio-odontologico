INSERT INTO rol (nombre) VALUES ('Administrador'), ('Cliente');
INSERT INTO usuario (usuario, clave, estado, rolId) VALUES ('admin', '1234', true, 1);
INSERT INTO tipo_persona (nombre) VALUES ('Empleado'), ('Cliente');
INSERT INTO estado_cita (nombre) VALUES ('Creada'), ('Asistio'), ('No asistio'), ('Borrada');
INSERT INTO pais (nombre) VALUES ('Venezuela');
INSERT INTO estado (nombre, paisId) VALUES ('Táchira', 1);
INSERT INTO municipio (nombre, estadoId) VALUES ('Junin', 1), ('San Cristóbal', 1);
INSERT INTO servicio (nombre, costo, descripcion, estado, imagen) VALUES
('Restauracion de resina', 120000.00, 'Reconstrucción con resina compuesta. UD 11.', 1, "imagen1"),
('Extracciones Dentales ', 450000.00, 'procedimiento quirúrgico destruido por una caries profunda', 1, "imagen2"),
('Blanqueamiento Dental ', 180000.00, 'tratamiento estético que aclara el color de los dientes ', 1, "imagen3"),
('Limpieza Dental ', 150000.00, 'Eliminación de placa bacteriana y sarro en dientes', 1, "imagen4"),
('Tratamiento Conducto ', 3000000.00, 'procedimiento dental que se realiza para salvar un diente', 1, "imagen5"),
('Protesis removibles ', 1000000.00, 'aparato bucal para reemplazar piezas dentales faltantes ', 1, "imagen6"),
('Ortodoncia ', 350000.00, ' cementación de los brackets', 1, "imagen7"),
('Radriografias periapicales', 100000.00, 'examen de rayos X de un diente o varios ', 1, "imagen8");

