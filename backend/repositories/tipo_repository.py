import pymysql
from typing import List
from dao.db import get_db_connection
from models.tipo import Tipo

class TipoRepository:
    def create(self, tipo: Tipo) -> int:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                query = """
                    INSERT INTO tipo (nombre, email, password)
                    VALUES (%s, %s, %s)
                """
                cursor.execute(query, (tipo.nombre, tipo.email, tipo.password))
                conn.commit()
                return cursor.lastrowid
            
    def get_by_email(self, email: str) -> Tipo | None:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                query = "SELECT * FROM tipo WHERE email = %s"
                cursor.execute(query, (email,))
                result = cursor.fetchone()
                return Tipo(**result) if result else None
            
    def get_by_id(self, tipo_id: int) -> Tipo | None:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                query = "SELECT * FROM tipo WHERE id = %s"
                cursor.execute(query, (tipo_id,))
                result = cursor.fetchone()
                return Tipo(**result) if result else None

    def get_all(self) -> List[Tipo]:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM tipo")
                results = cursor.fetchall()
                return [Tipo(**row) for row in results]

    def update(self, tipo_id: int, tipo: Tipo) -> bool:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                query = "UPDATE tipo SET nombre = %s, email = %s WHERE id = %s"
                cursor.execute(query, (tipo.nombre, tipo.email, tipo_id))
                conn.commit()
                return cursor.rowcount > 0

    def delete(self, tipo_id: int) -> bool:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                query = "DELETE FROM tipo WHERE id = %s"
                cursor.execute(query, (tipo_id,))
                conn.commit()
                return cursor.rowcount > 0
