from typing import List, Optional
from dao.db import get_db_connection
from models.registro import Registro

class RegistroRepository:
    def create(self, registro: Registro) -> int:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                query = """
                    INSERT INTO Registro 
                    (tipo_evento, description, Usuario_idUsuario, Biorreactor_idBiorreactor, Sensores_idSensores)
                    VALUES (%s, %s, %s, %s, %s)
                """
                cursor.execute(query, (
                    registro.tipo_evento,
                    registro.description,
                    registro.Usuario_idUsuario,
                    registro.Biorreactor_idBiorreactor,
                    registro.Sensores_idSensores
                ))
                conn.commit()
                return cursor.lastrowid

    def get_by_id(self, idRegistro: int) -> Optional[Registro]:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM Registro WHERE idRegistro = %s", (idRegistro,))
                result = cursor.fetchone()
                return Registro(**result) if result else None

    def get_all(self) -> List[Registro]:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM Registro")
                results = cursor.fetchall()
                return [Registro(**row) for row in results]
            
    def get_comandos_voz(self) -> List[Registro]:
        with get_db_connection() as conn:
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute("SELECT * FROM Registro WHERE tipo_evento = 'Voz' ORDER BY fecha DESC")
                results = cursor.fetchall()
                return [Registro(**row) for row in results]



    def update(self, idRegistro: int, registro: Registro) -> bool:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                query = """
                    UPDATE Registro 
                    SET tipo_evento = %s, description = %s, Usuario_idUsuario = %s, 
                        Biorreactor_idBiorreactor = %s, Sensores_idSensores = %s
                    WHERE idRegistro = %s
                """
                cursor.execute(query, (
                    registro.tipo_evento,
                    registro.description,
                    registro.Usuario_idUsuario,
                    registro.Biorreactor_idBiorreactor,
                    registro.Sensores_idSensores,
                    idRegistro
                ))
                conn.commit()
                return cursor.rowcount > 0

    def delete(self, idRegistro: int) -> bool:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("DELETE FROM Registro WHERE idRegistro = %s", (idRegistro,))
                conn.commit()
                return cursor.rowcount > 0
