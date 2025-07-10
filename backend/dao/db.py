import pymysql
from contextlib import contextmanager

import time
import pymysql
from contextlib import contextmanager

DB_CONFIG = {
    'host':'host.docker.internal',
    #'host':'localhost',  
    'password': '',  # asegúrate que en docker-compose esté también vacío
    'database': 'db_proyect_final',
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor
}

@contextmanager
def get_db_connection():
    connection = None
    for attempt in range(5):
        try:
            connection = pymysql.connect(**DB_CONFIG)
            print("Conexión exitosa a la base de datos.")
            break
        except pymysql.err.OperationalError as e:
            print(f"Intento {attempt+1}/5 - Esperando conexión a la base de datos...")
            time.sleep(5)
    else:
        raise Exception("No se pudo conectar a la base de datos después de varios intentos.")

    try:
        yield connection
    finally:
        connection.close()



