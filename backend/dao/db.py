import pymysql
from contextlib import contextmanager

import time
import pymysql
from contextlib import contextmanager

DB_CONFIG = {
    'host': 'host.docker.internal',  # nombre del servicio en docker-compose
    'user': 'root',
    'password': '',  # asegúrate que en docker-compose esté también vacío
    'database': 'db_proyectICC',
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor
}

@contextmanager
def get_db_connection():
    connection = None
    for attempt in range(20):  # hasta 10 intentos
        try:
            connection = pymysql.connect(**DB_CONFIG)
            print("Conexión exitosa a la base de datos.")
            break
        except pymysql.err.OperationalError as e:
            print(f"Intento {attempt+1}/20 - Esperando conexión a la base de datos...")
            time.sleep(5)  # espera 3 segundos
    else:
        raise Exception(" No se pudo conectar a la base de datos después de varios intentos.")

    try:
        yield connection
    finally:
        connection.close()

# Initialize database
def init_db():
    with get_db_connection() as conn:
        with conn.cursor() as cursor:

            # Create usuario table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS usuario (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    nombre VARCHAR(255),
                    email VARCHAR(255),
                    fecha_registro DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # Create biorreactor table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS biorreactor (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    codigo INT,
                    ubicacion VARCHAR(45),
                    estado VARCHAR(24)
                )
            """)

            # Create lectura_sensores table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS lectura_sensores (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    temperatura FLOAT,
                    humedad FLOAT,
                    fecha DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)

            #  Create tipo table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS tipo (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    nombre VARCHAR(45),
                    email VARCHAR(45),
                    password varchar(45) 
                )
            """)

            #  Create sensores table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS sensores (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    tipo VARCHAR(45),
                    modelo VARCHAR(45),
                    ubicacion VARCHAR(45)
                )
            """)

            #  Create empresas table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS empresas (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    nombre VARCHAR(45),
                    ruc VARCHAR(45),
                    correo VARCHAR(45),
                    direccion VARCHAR(45),
                    pais VARCHAR(45),
                    representante VARCHAR(45),
                    telefono VARCHAR(45)
                )
            """)

            conn.commit()
