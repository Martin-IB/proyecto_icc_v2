from typing import List
from fastapi import HTTPException
from models.tipo import Tipo
from repositories.tipo_repository import TipoRepository

class TipoService:
    def __init__(self, repository: TipoRepository):
        self.repository = repository

    def create_tipo(self, tipo: Tipo) -> int:
        return self.repository.create(tipo)

    def get_tipo(self, idTipo: int) -> Tipo:
        tipo = self.repository.get_by_id(idTipo)
        if not tipo:
            raise HTTPException(status_code=404, detail="Tipo no encontrado")
        return tipo

    def get_all_tipo(self) -> List[Tipo]:
        return self.repository.get_all()

    def update_tipo(self, idTipo: int, tipo: Tipo) -> Tipo:
        success = self.repository.update(idTipo, tipo)
        if not success:
            raise HTTPException(status_code=404, detail="Tipo no encontrado")
        return self.get_tipo(idTipo)

    def delete_tipo(self, idTipo: int) -> None:
        success = self.repository.delete(idTipo)
        if not success:
            raise HTTPException(status_code=404, detail="Tipo no encontrado")

def get_tipo_service() -> TipoService:
    return TipoService(TipoRepository())
