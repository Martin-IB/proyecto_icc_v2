from typing import List, Optional
from dao.db import get_db_connection
from models.sensores import Sensor

class SensorRepository:
    def create(self, sensor: Sensor) -> int:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                query = """
                    INSERT INTO Sensores (tipo, modelo, ubicacion, Biorreactor_idBiorreactor)
                    VALUES (%s, %s, %s, %s)
                """
                cursor.execute(query, (
                    sensor.tipo,
                    sensor.modelo,
                    sensor.ubicacion,
                    sensor.Biorreactor_idBiorreactor
                ))
                conn.commit()
                return cursor.lastrowid

    def get_by_id(self, idSensores: int) -> Optional[Sensor]:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM Sensores WHERE idSensores = %s", (idSensores,))
                result = cursor.fetchone()
                return Sensor(**result) if result else None

    def get_all(self) -> List[Sensor]:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM Sensores")
                results = cursor.fetchall()
                return [Sensor(**row) for row in results]

    def update(self, idSensores: int, sensor: Sensor) -> bool:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                query = """
                    UPDATE Sensores
                    SET tipo = %s, modelo = %s, ubicacion = %s, Biorreactor_idBiorreactor = %s
                    WHERE idSensores = %s
                """
                cursor.execute(query, (
                    sensor.tipo,
                    sensor.modelo,
                    sensor.ubicacion,
                    sensor.Biorreactor_idBiorreactor,
                    idSensores
                ))
                conn.commit()
                return cursor.rowcount > 0

    def delete(self, idSensores: int) -> bool:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("DELETE FROM Sensores WHERE idSensores = %s", (idSensores,))
                conn.commit()
                return cursor.rowcount > 0
