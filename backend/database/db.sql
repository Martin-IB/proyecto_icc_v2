-- Base de datos
CREATE DATABASE IF NOT EXISTS db_proyect_final;
USE db_proyect_final;

-- Tabla Tipo
DROP TABLE IF EXISTS Tipo;
CREATE TABLE Tipo (
  idTipo INT NOT NULL,
  nombre VARCHAR(45),
  PRIMARY KEY (idTipo)
) ENGINE=InnoDB;

-- Tabla Usuario
DROP TABLE IF EXISTS Usuario;
CREATE TABLE Usuario (
  idUsuario INT NOT NULL,
  nombre VARCHAR(45),
  email VARCHAR(45),
  password VARCHAR(45),
  fecha_registro DATETIME DEFAULT CURRENT_TIMESTAMP,
  Tipo_idTipo INT NOT NULL,
  PRIMARY KEY (idUsuario),
  INDEX fk_Usuario_Tipo_idx (Tipo_idTipo),
  CONSTRAINT fk_Usuario_Tipo
    FOREIGN KEY (Tipo_idTipo) REFERENCES Tipo(idTipo)
    ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB;

-- Tabla Biorreactor
DROP TABLE IF EXISTS Biorreactor;
CREATE TABLE Biorreactor (
  idBiorreactor INT NOT NULL AUTO_INCREMENT,
  codigo INT,
  ubicacion VARCHAR(45),
  estado VARCHAR(45),
  Usuario_idUsuario INT NOT NULL,
  PRIMARY KEY (idBiorreactor),
  INDEX fk_Biorreactor_Usuario_idx (Usuario_idUsuario),
  CONSTRAINT fk_Biorreactor_Usuario
    FOREIGN KEY (Usuario_idUsuario) REFERENCES Usuario(idUsuario)
    ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB;

-- Tabla Sensores
CREATE TABLE Sensores (
  idSensores INT NOT NULL AUTO_INCREMENT,
  tipo VARCHAR(45),
  modelo VARCHAR(45),
  ubicacion VARCHAR(45),
  Biorreactor_idBiorreactor INT NOT NULL,
  PRIMARY KEY (idSensores),
  INDEX fk_Sensores_Biorreactor1_idx (Biorreactor_idBiorreactor ASC),
  CONSTRAINT fk_Sensores_Biorreactor1
    FOREIGN KEY (Biorreactor_idBiorreactor)
    REFERENCES Biorreactor (idBiorreactor)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
) ENGINE=InnoDB;


-- Tabla Empresa
DROP TABLE IF EXISTS Empresa;
CREATE TABLE Empresa (
  idEmpresa INT NOT NULL AUTO_INCREMENT,
  nombre VARCHAR(45),
  ruc VARCHAR(45),
  correo VARCHAR(45),
  direccion VARCHAR(45),
  pais VARCHAR(45),
  representante VARCHAR(45),
  telefono VARCHAR(45),
  Usuario_idUsuario INT NOT NULL,
  PRIMARY KEY (idEmpresa),
  INDEX fk_Empresa_Usuario_idx (Usuario_idUsuario),
  CONSTRAINT fk_Empresa_Usuario
    FOREIGN KEY (Usuario_idUsuario) REFERENCES Usuario(idUsuario)
    ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB;

-- Tabla Registro
DROP TABLE IF EXISTS Registro;
CREATE TABLE Registro (
  idRegistro INT NOT NULL AUTO_INCREMENT,
  tipo_evento VARCHAR(45),
  description TEXT,
  fecha DATETIME DEFAULT CURRENT_TIMESTAMP,
  Usuario_idUsuario INT NOT NULL,
  Biorreactor_idBiorreactor INT NOT NULL,
  Sensores_idSensores INT NOT NULL,
  PRIMARY KEY (idRegistro),
  INDEX fk_Registro_Usuario_idx (Usuario_idUsuario),
  INDEX fk_Registro_Biorreactor_idx (Biorreactor_idBiorreactor),
  INDEX fk_Registro_Sensores_idx (Sensores_idSensores),
  CONSTRAINT fk_Registro_Usuario
    FOREIGN KEY (Usuario_idUsuario) REFERENCES Usuario(idUsuario)
    ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT fk_Registro_Biorreactor
    FOREIGN KEY (Biorreactor_idBiorreactor) REFERENCES Biorreactor(idBiorreactor)
    ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT fk_Registro_Sensores
    FOREIGN KEY (Sensores_idSensores) REFERENCES Sensores(idSensores)
    ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB;

-- Tabla Lectura_sensores
DROP TABLE IF EXISTS Lectura_sensores;
CREATE TABLE Lectura_sensores (
  idLectura_sensores INT NOT NULL AUTO_INCREMENT,
  temperatura DECIMAL(5,2),
  humedad DECIMAL(5,2),
  fecha DATETIME DEFAULT CURRENT_TIMESTAMP,
  Biorreactor_idBiorreactor INT NOT NULL,
  Sensores_idSensores INT NOT NULL,
  PRIMARY KEY (idLectura_sensores),
  INDEX fk_Lectura_Biorreactor_idx (Biorreactor_idBiorreactor),
  INDEX fk_Lectura_Sensores_idx (Sensores_idSensores),
  CONSTRAINT fk_Lectura_Biorreactor
    FOREIGN KEY (Biorreactor_idBiorreactor) REFERENCES Biorreactor(idBiorreactor)
    ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT fk_Lectura_Sensores
    FOREIGN KEY (Sensores_idSensores) REFERENCES Sensores(idSensores)
    ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB;
