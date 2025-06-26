from typing import List
from fastapi import HTTPException
from models.tipo import Tipo
from repositories.tipo_repository import TipoRepository
from dao.db import get_db_connection  # asegúrate de importar esto correctamente

class TipoService:
    def __init__(self, repository: TipoRepository):
        self.repository = repository

    def create_tipo(self, tipo: Tipo) -> int:
        return self.repository.create(tipo)

    def login(self, email: str, password: str) -> Tipo:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                query = "SELECT id, nombre, email, password FROM tipo WHERE email = %s AND password = %s"
                cursor.execute(query, (email, password))
                result = cursor.fetchone()
                if result:
                    return Tipo(**result)
                else:
                    return None

    def get_tipo(self, tipo_id: int) -> Tipo:
        tipo = self.repository.get_by_id(tipo_id)
        if not tipo:
            raise HTTPException(status_code=404, detail="Tipo not found")
        return tipo

    def get_all_tipo(self) -> List[Tipo]:
        return self.repository.get_all()

    def update_tipo(self, tipo_id: int, tipo: Tipo) -> Tipo:
        success = self.repository.update(tipo_id, tipo)
        if not success:
            raise HTTPException(status_code=404, detail="Tipo not found")
        return self.get_tipo(tipo_id)

    def delete_tipo(self, tipo_id: int) -> None:
        success = self.repository.delete(tipo_id)
        if not success:
            raise HTTPException(status_code=404, detail="Tipo not found")

def get_tipo_service() -> TipoService:
    return TipoService(TipoRepository())
