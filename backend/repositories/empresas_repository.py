from typing import List, Optional
from dao.db import get_db_connection
from models.empresas import Empresa

class EmpresaRepository:
    def create(self, empresa: Empresa) -> int:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                query = """
                    INSERT INTO Empresa 
                    (nombre, ruc, correo, direccion, pais, representante, telefono, Usuario_idUsuario)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(query, (
                    empresa.nombre,
                    empresa.ruc,
                    empresa.correo,
                    empresa.direccion,
                    empresa.pais,
                    empresa.representante,
                    empresa.telefono,
                    empresa.Usuario_idUsuario
                ))
                conn.commit()
                return cursor.lastrowid

    def get_by_id(self, idEmpresa: int) -> Optional[Empresa]:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM Empresa WHERE idEmpresa = %s", (idEmpresa,))
                result = cursor.fetchone()
                return Empresa(**result) if result else None

    def get_all(self) -> List[Empresa]:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM Empresa")
                results = cursor.fetchall()
                return [Empresa(**row) for row in results]

    def update(self, idEmpresa: int, empresa: Empresa) -> bool:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                query = """
                    UPDATE Empresa 
                    SET nombre=%s, ruc=%s, correo=%s, direccion=%s, pais=%s, 
                        representante=%s, telefono=%s, Usuario_idUsuario=%s
                    WHERE idEmpresa = %s
                """
                cursor.execute(query, (
                    empresa.nombre,
                    empresa.ruc,
                    empresa.correo,
                    empresa.direccion,
                    empresa.pais,
                    empresa.representante,
                    empresa.telefono,
                    empresa.Usuario_idUsuario,
                    idEmpresa
                ))
                conn.commit()
                return cursor.rowcount > 0

    def delete(self, idEmpresa: int) -> bool:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("DELETE FROM Empresa WHERE idEmpresa = %s", (idEmpresa,))
                conn.commit()
                return cursor.rowcount > 0