CREATE DATABASE IF NOT EXISTS restaurante_db;
USE restaurante_db;

-- 1. Tabla Usuario
CREATE TABLE IF NOT EXISTS Usuario (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    documento VARCHAR(20) NOT NULL UNIQUE,
    telefono VARCHAR(20) NOT NULL,
    otro_contacto VARCHAR(100)
);

-- 2. Tabla Mesa
CREATE TABLE IF NOT EXISTS Mesa (
    id INT AUTO_INCREMENT PRIMARY KEY,
    num_mesa INT NOT NULL,
    capacidad INT NOT NULL,
    ubicacion VARCHAR(50) NOT NULL
);

-- Insertar mesa inicial de prueba
INSERT INTO Mesa (id, num_mesa, capacidad, ubicacion) 
VALUES (1, 1, 4, 'Interior') 
ON DUPLICATE KEY UPDATE id=id;

-- 3. Tabla Reserva
CREATE TABLE IF NOT EXISTS Reserva (
    id INT AUTO_INCREMENT PRIMARY KEY,
    fecha_hora DATETIME NOT NULL,
    comensales INT NOT NULL,
    observaciones TEXT,
    usuario_id INT NOT NULL,
    mesa_id INT NOT NULL,
    FOREIGN KEY (usuario_id) REFERENCES Usuario(id),
    FOREIGN KEY (mesa_id) REFERENCES Mesa(id)
);