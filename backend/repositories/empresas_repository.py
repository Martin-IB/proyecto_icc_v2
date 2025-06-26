import pymysql
from models.empresas import Empresa
from dao.db import get_db_connection
from typing import List

class EmpresaRepository:
    def create(self, empresa: Empresa) -> int:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                query = """
                    INSERT INTO empresas (nombre, ruc, correo, direccion, pais, representante, telefono)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(query, (
                    empresa.nombre, empresa.ruc, empresa.correo, empresa.direccion,
                    empresa.pais, empresa.representante, empresa.telefono
                ))
                conn.commit()
                return cursor.lastrowid

    def get_by_id(self, empresa_id: int) -> Empresa | None:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                query = "SELECT * FROM empresas WHERE id = %s"
                cursor.execute(query, (empresa_id,))
                result = cursor.fetchone()
                return Empresa(**result) if result else None

    def get_all(self) -> List[Empresa]:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM empresas")
                results = cursor.fetchall()
                return [Empresa(**result) for result in results]

    def update(self, empresa_id: int, empresa: Empresa) -> bool:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                query = """
                    UPDATE empresas SET nombre=%s, ruc=%s, correo=%s, direccion=%s, 
                    pais=%s, representante=%s, telefono=%s WHERE id=%s
                """
                cursor.execute(query, (
                    empresa.nombre, empresa.ruc, empresa.correo, empresa.direccion,
                    empresa.pais, empresa.representante, empresa.telefono, empresa_id
                ))
                conn.commit()
                return cursor.rowcount > 0

    def delete(self, empresa_id: int) -> bool:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                query = "DELETE FROM empresas WHERE id = %s"
                cursor.execute(query, (empresa_id,))
                conn.commit()
                return cursor.rowcount > 0
