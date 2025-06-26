import pymysql
from models.biorreactor import Biorreactor
from dao.db import get_db_connection
from typing import List

class BiorreactorRepository:
    def create(self, biorreactor: Biorreactor) -> int:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                query = """
                    INSERT INTO biorreactor (codigo, ubicacion, estado)
                    VALUES (%s, %s, %s)
                """
                cursor.execute(query, (biorreactor.codigo, biorreactor.ubicacion, biorreactor.estado))
                conn.commit()
                return cursor.lastrowid

    def get_by_id(self, biorreactor_id: int) -> Biorreactor | None:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                query = "SELECT * FROM biorreactor WHERE id = %s"
                cursor.execute(query, (biorreactor_id,))
                result = cursor.fetchone()
                return Biorreactor(**result) if result else None

    def get_all(self) -> List[Biorreactor]:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM biorreactor")
                results = cursor.fetchall()
                return [Biorreactor(**result) for result in results]

    def update(self, biorreactor_id: int, biorreactor: Biorreactor) -> bool:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                query = """
                    UPDATE biorreactor 
                    SET codigo = %s, ubicacion = %s, estado= %s
                    WHERE id = %s
                """
                cursor.execute(query, (biorreactor.codigo, biorreactor.ubicacion, biorreactor.estado, biorreactor_id))
                conn.commit()
                return cursor.rowcount > 0

    def delete(self, biorreactor_id: int) -> bool:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                query = "DELETE FROM biorreactor WHERE id = %s"
                cursor.execute(query, (biorreactor_id,))
                conn.commit()
                return cursor.rowcount > 0