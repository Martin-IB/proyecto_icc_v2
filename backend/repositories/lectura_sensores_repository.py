from models.lectura_sensores import LecturaSensor
from dao.db import get_db_connection
from typing import List

class LecturaSensorRepository:
    def __init__(self, db_connection):
        self.db_connection = db_connection

    def create(self, lectura: LecturaSensor) -> int:
        with self.db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO lectura_sensores (temperatura, humedad) VALUES (%s, %s)",
                    (lectura.temperatura, lectura.humedad)
                )
                conn.commit()
                return cursor.lastrowid

    def get_by_id(self, lectura_id: int) -> LecturaSensor | None:
        with self.db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM lectura_sensores WHERE id = %s", (lectura_id,))
                result = cursor.fetchone()
                return LecturaSensor(**result) if result else None

    def get_all(self) -> List[LecturaSensor]:
        with self.db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM lectura_sensores")
                results = cursor.fetchall()
                return [LecturaSensor(**row) for row in results]
            
    def update(self, lectura_id: int, lectura: LecturaSensor) -> bool:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                query = """
                    UPDATE lectura_sensores
                    SET temperatura = %s, humedad = %s
                    WHERE id = %s
                """
                cursor.execute(query, (lectura.temperatura, lectura.humedad, lectura_id))
                conn.commit()
                return cursor.rowcount > 0

    def delete(self, lectura_id: int) -> bool:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                query = "DELETE FROM lectura_sensores WHERE id = %s"
                cursor.execute(query, (lectura_id,))
                conn.commit()
                return cursor.rowcount > 0

