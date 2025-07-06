import pymysql
from typing import List
from dao.db import get_db_connection
from models.tipo import Tipo

class TipoRepository:
    def create(self, tipo: Tipo) -> int:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                query = "INSERT INTO Tipo (nombre) VALUES (%s)"
                cursor.execute(query, (tipo.nombre,))
                conn.commit()
                return cursor.lastrowid 

    def get_by_id(self, idTipo: int) -> Tipo | None:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                query = "SELECT * FROM Tipo WHERE idTipo = %s"
                cursor.execute(query, (idTipo,))
                result = cursor.fetchone()
                return Tipo(**result) if result else None

    def get_all(self) -> List[Tipo]:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM Tipo")
                results = cursor.fetchall()
                return [Tipo(**row) for row in results]

    def update(self, idTipo: int, tipo: Tipo) -> bool:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                query = "UPDATE Tipo SET nombre = %s WHERE idTipo = %s"
                cursor.execute(query, (tipo.nombre, idTipo))
                conn.commit()
                return cursor.rowcount > 0

    def delete(self, idTipo: int) -> bool:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                query = "DELETE FROM Tipo WHERE idTipo = %s"
                cursor.execute(query, (idTipo,))
                conn.commit()
                return cursor.rowcount > 0
