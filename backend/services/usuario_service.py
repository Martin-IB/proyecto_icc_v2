from fastapi import HTTPException
from models.usuario import Usuario
from repositories.usuario_repository import UsuarioRepository
from typing import List
from dao.db import get_db_connection

class UsuarioService:
    def __init__(self, repository: UsuarioRepository):
        self.repository = repository

    def create_usuario(self, usuario: Usuario) -> int:
        if usuario.nombre == "":
            raise HTTPException(status_code=400, detail="nombre cannot be empty")
        return self.repository.create(usuario)

    def get_usuario(self, usuario_id: int) -> Usuario:
        usuario = self.repository.get_by_id(usuario_id)
        if not usuario:
            raise HTTPException(status_code=404, detail="Usuario not found")
        return usuario

    def get_all_usuario(self) -> List[Usuario]:
        return self.repository.get_all()

    def update_usuario(self, usuario_id: int, usuario: Usuario) -> Usuario:
        if usuario.nombre == "":
            raise HTTPException(status_code=400, detail="Nombre cannot be empty")
        success = self.repository.update(usuario_id, usuario)
        if not success:
            raise HTTPException(status_code=404, detail="Usuario not found")
        return self.get_usuario(usuario_id)

    def delete_usuario(self, usuario_id: int) -> None:
        success = self.repository.delete(usuario_id)
        if not success:
            raise HTTPException(status_code=404, detail="Usuario not found")

def get_usuario_service() -> UsuarioService:
    return UsuarioService(UsuarioRepository(get_db_connection))
