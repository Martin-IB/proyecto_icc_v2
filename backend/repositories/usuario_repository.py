

from typing import List, Optional
from dao.db import get_db_connection
from models.usuario import Usuario,UsuarioUpdate

class UsuarioRepository:
    def create(self, usuario: UsuarioUpdate) -> int:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                query = """
                    INSERT INTO Usuario (nombre, email, password, Tipo_idTipo)
                    VALUES (%s, %s, %s, %s)
                """
                cursor.execute(query, (
                    usuario.nombre,
                    usuario.email,
                    usuario.password,
                    usuario.Tipo_idTipo
                ))
                conn.commit()
                return cursor.lastrowid


    def get_by_id(self, idUsuario: int) -> Optional[Usuario]:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    SELECT 
                        idUsuario, 
                        nombre, 
                        email, 
                        password, 
                        fecha_registro, 
                        Tipo_idTipo 
                    FROM Usuario 
                    WHERE idUsuario = %s
                """, (idUsuario,))
                result = cursor.fetchone()
                return Usuario(**result) if result else None

    def get_all(self) -> List[Usuario]:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    SELECT 
                        idUsuario, 
                        nombre, 
                        email, 
                        password, 
                        fecha_registro, 
                        Tipo_idTipo 
                    FROM Usuario
                """)
                results = cursor.fetchall()
                return [Usuario(**row) for row in results]

    def update(self, idUsuario: int, usuario: Usuario) -> bool:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                query = """
                    UPDATE Usuario 
                    SET nombre = %s, email = %s, password = %s, Tipo_idTipo = %s 
                    WHERE idUsuario = %s
                """
                cursor.execute(query, (
                    usuario.nombre,
                    usuario.email,
                    usuario.password,
                    usuario.Tipo_idTipo,
                    idUsuario
                ))
                conn.commit()
                return cursor.rowcount > 0

    def delete(self, idUsuario: int) -> bool:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("DELETE FROM Usuario WHERE idUsuario = %s", (idUsuario,))
                conn.commit()
                return cursor.rowcount > 0

    def login(self, email: str, password: str) -> Optional[Usuario]:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                query = "SELECT * FROM Usuario WHERE email = %s AND password = %s"
                cursor.execute(query, (email, password))
                result = cursor.fetchone()
                print("Resultado de login SQL:", result)
                return Usuario(**result) if result else None
