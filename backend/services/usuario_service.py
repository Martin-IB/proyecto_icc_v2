
from fastapi import HTTPException
from typing import List
from models.usuario import Usuario
from repositories.usuario_repository import UsuarioRepository

class UsuarioService:
    def __init__(self, repository: UsuarioRepository):
        self.repository = repository

    def create_usuario(self, usuario: Usuario) -> int:
        return self.repository.create(usuario)

    def get_usuario(self, idUsuario: int) -> Usuario:
        usuario = self.repository.get_by_id(idUsuario)
        if not usuario:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        return usuario

    def get_all_usuarios(self) -> List[Usuario]:
        usuarios = self.repository.get_all()
        if not usuarios:
            raise HTTPException(status_code=404, detail="No hay usuarios registrados")
        return usuarios

    def update_usuario(self, idUsuario: int, usuario: Usuario) -> Usuario:
        success = self.repository.update(idUsuario, usuario)
        if not success:
            raise HTTPException(status_code=404, detail="Usuario no encontrado para actualizar")
        return self.get_usuario(idUsuario)

    def delete_usuario(self, idUsuario: int) -> None:
        success = self.repository.delete(idUsuario)
        if not success:
            raise HTTPException(status_code=404, detail="Usuario no encontrado para eliminar")

    def login(self, email: str, password: str) -> Usuario:
        usuario = self.repository.login(email, password)
        if not usuario:
            raise HTTPException(status_code=401, detail="Credenciales inválidas")
        return usuario

def get_usuario_service() -> UsuarioService:
    return UsuarioService(UsuarioRepository())
