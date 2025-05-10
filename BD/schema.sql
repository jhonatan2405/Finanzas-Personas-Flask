-- Crear la base de datos
CREATE DATABASE IF NOT EXISTS finanzas_personales;
USE finanzas_personales;

-- Tabla de usuarios
CREATE TABLE IF NOT EXISTS usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    fecha_registro DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de categorías
CREATE TABLE IF NOT EXISTS categorias (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    tipo ENUM('ingreso', 'gasto') NOT NULL
);

-- Tabla de movimientos financieros
CREATE TABLE IF NOT EXISTS movimientos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    categoria_id INT NOT NULL,
    monto DECIMAL(10, 2) NOT NULL,
    descripcion VARCHAR(255),
    fecha DATE NOT NULL,
    tipo ENUM('ingreso', 'gasto') NOT NULL,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE,
    FOREIGN KEY (categoria_id) REFERENCES categorias(id)
);

-- Insertar categorías predeterminadas
INSERT INTO categorias (nombre, tipo) VALUES 
('Salario', 'ingreso'),
('Inversiones', 'ingreso'),
('Regalos', 'ingreso'),
('Otros ingresos', 'ingreso'),
('Alimentación', 'gasto'),
('Transporte', 'gasto'),
('Vivienda', 'gasto'),
('Entretenimiento', 'gasto'),
('Salud', 'gasto'),
('Educación', 'gasto'),
('Ropa', 'gasto'),
('Servicios', 'gasto'),
('Otros gastos', 'gasto');
