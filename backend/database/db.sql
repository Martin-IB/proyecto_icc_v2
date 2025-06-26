
DROP DATABASE IF EXISTS db_proyectICC;
CREATE DATABASE db_proyectICC;
USE db_proyectICC;

-- Tabla de datos para administrador
CREATE TABLE tipo (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(45),
    email VARCHAR(45),
);

-- Tabla de datos para ususario
CREATE TABLE ususario (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre FLOAT,
    email FLOAT,
    fecha_registro DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de datos para los biorrrecatores
CREATE TABLE biorreactor (
    id INT AUTO_INCREMENT PRIMARY KEY,
    codigo INT,
    ubicacion VARCHAR(45),
    estado VARCHAR(45)
);

-- Tabla de datos para sensores
CREATE TABLE sensores(
    id INT AUTO_INCREMENT PRIMARY KEY,
    tipo VARCHAR(45),
    modelo VARCHAR(45)
);

-- Tabla de datos de lectura e los sensores
CREATE TABLE lectura_sensores (
    id INT AUTO_INCREMENT PRIMARY KEY,
    temperatura FLOAT,
    humedad FLOAT,
    fecha DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de datos de las empresas
CREATE TABLE empresas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(45),
    ruc VARCHAR(45),
    correo VARCHAR(45),
    direccion VARCHAR(45),
    pais VARCHAR(45),
    representante VARCHAR(45),
    telefono VARCHAR(45)
);