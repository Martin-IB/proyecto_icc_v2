from typing import List, Optional
from dao.db import get_db_connection
from models.lectura_sensores import LecturaSensores

class LecturaRepository:
    def create(self, lectura: LecturaSensores) -> int:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                query = """
                    INSERT INTO Lectura_sensores 
                    (temperatura, humedad, estado_ambiente, Biorreactor_idBiorreactor, Sensores_idSensores)
                    VALUES (%s, %s, %s, %s, %s)
                """
                cursor.execute(query, (
                    lectura.temperatura,
                    lectura.humedad,
                    lectura.estado_ambiente,
                    lectura.Biorreactor_idBiorreactor,
                    lectura.Sensores_idSensores
                ))
                conn.commit()
                return cursor.lastrowid

    def get_by_id(self, idLectura_sensores: int) -> Optional[LecturaSensores]:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM Lectura_sensores WHERE idLectura_sensores = %s", (idLectura_sensores,))
                result = cursor.fetchone()
                return LecturaSensores(**result) if result else None

    def get_all(self) -> List[LecturaSensores]:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM Lectura_sensores")
                results = cursor.fetchall()
                return [LecturaSensores(**row) for row in results]
