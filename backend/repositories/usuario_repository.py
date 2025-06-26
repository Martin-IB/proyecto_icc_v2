from models.usuario import Usuario
from dao.db import get_db_connection
from typing import List

class UsuarioRepository:
    def __init__(self, db_connection):
        self.db_connection = db_connection

    def create(self, usuario: Usuario) -> int:
        with self.db_connection() as conn:
            with conn.cursor() as cursor:
                query = "INSERT INTO usuario (nombre, email) VALUES (%s, %s)"
                cursor.execute(query, (usuario.nombre, usuario.email))
                conn.commit()
                return cursor.lastrowid

    def get_by_id(self, usuario_id: int) -> Usuario | None:
        with self.db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM usuario WHERE id = %s", (usuario_id,))
                result = cursor.fetchone()
                return Usuario(**result) if result else None

    def get_all(self) -> List[Usuario]:
        with self.db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM usuario")
                results = cursor.fetchall()
                return [Usuario(**row) for row in results]

    def update(self, usuario_id: int, usuario: Usuario) -> bool:
        with self.db_connection() as conn:
            with conn.cursor() as cursor:
                query = "UPDATE usuario SET nombre = %s, email = %s WHERE id = %s"
                cursor.execute(query, (usuario.nombre, usuario.email, usuario_id))
                conn.commit()
                return cursor.rowcount > 0

    def delete(self, usuario_id: int) -> bool:
        with self.db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("DELETE FROM usuario WHERE id = %s", (usuario_id,))
                conn.commit()
                return cursor.rowcount > 0
