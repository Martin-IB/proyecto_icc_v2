from dao.db import get_db_connection
from models.biorreactor import Biorreactor
from typing import List, Optional

class BiorreactorRepository:
    def create(self, bior: Biorreactor) -> int:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                query = """
                    INSERT INTO Biorreactor (codigo, ubicacion, estado, Usuario_idUsuario)
                    VALUES (%s, %s, %s, %s)
                """
                cursor.execute(query, (
                    bior.codigo,
                    bior.ubicacion,
                    bior.estado,
                    bior.Usuario_idUsuario
                ))
                conn.commit()
                return cursor.lastrowid

    def get_by_id(self, idBiorreactor: int) -> Optional[Biorreactor]:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM Biorreactor WHERE idBiorreactor = %s", (idBiorreactor,))
                result = cursor.fetchone()
                return Biorreactor(**result) if result else None

    def get_all(self) -> List[Biorreactor]:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM Biorreactor")
                results = cursor.fetchall()
                return [Biorreactor(**row) for row in results]

    def update(self, idBiorreactor: int, bior: Biorreactor) -> bool:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                query = """
                    UPDATE Biorreactor
                    SET codigo = %s, ubicacion = %s, estado = %s, Usuario_idUsuario = %s
                    WHERE idBiorreactor = %s
                """
                cursor.execute(query, (
                    bior.codigo,
                    bior.ubicacion,
                    bior.estado,
                    bior.Usuario_idUsuario,
                    idBiorreactor
                ))
                conn.commit()
                return cursor.rowcount > 0

    def delete(self, idBiorreactor: int) -> bool:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("DELETE FROM Biorreactor WHERE idBiorreactor = %s", (idBiorreactor,))
                conn.commit()
                return cursor.rowcount > 0
