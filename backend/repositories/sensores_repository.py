import pymysql
from models.sensores import Sensor
from dao.db import get_db_connection
from typing import List

class SensorRepository:
    def create(self, sensor: Sensor) -> int:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                query = """
                    INSERT INTO sensores (tipo, modelo, ubicacion)
                    VALUES (%s, %s, %s)
                """
                cursor.execute(query, (sensor.tipo, sensor.modelo, sensor.ubicacion))
                conn.commit()
                return cursor.lastrowid

    def get_by_id(self, sensor_id: int) -> Sensor | None:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                query = "SELECT * FROM sensores WHERE id = %s"
                cursor.execute(query, (sensor_id,))
                result = cursor.fetchone()
                return Sensor(**result) if result else None

    def get_all(self) -> List[Sensor]:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM sensores")
                results = cursor.fetchall()
                return [Sensor(**result) for result in results]

    def update(self, sensor_id: int, sensor: Sensor) -> bool:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                query = """
                    UPDATE sensores
                    SET tipo = %s, modelo = %s, ubicacion = %s
                    WHERE id = %s
                """
                cursor.execute(query, (sensor.tipo, sensor.modelo, sensor.ubicacion, sensor_id))
                conn.commit()
                return cursor.rowcount > 0

    def delete(self, sensor_id: int) -> bool:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                query = "DELETE FROM sensores WHERE id = %s"
                cursor.execute(query, (sensor_id,))
                conn.commit()
                return cursor.rowcount > 0
