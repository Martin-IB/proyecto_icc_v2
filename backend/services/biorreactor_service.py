from models.biorreactor import Biorreactor,BiorreactorUpdate
from repositories.biorreactor_repository import BiorreactorRepository
from typing import List
from fastapi import HTTPException

class BiorreactorService:
    def __init__(self, repository: BiorreactorRepository):
        self.repository = repository

    def create_biorreactor(self, bior: BiorreactorUpdate) -> Biorreactor:
        id_creado = self.repository.create(bior)
        return self.repository.get_by_id(id_creado)

    def get_biorreactor(self, idBiorreactor: int) -> Biorreactor:
        result = self.repository.get_by_id(idBiorreactor)
        if not result:
            raise HTTPException(status_code=404, detail="Biorreactor no encontrado")
        return result

    def get_all_biorreactores(self) -> List[Biorreactor]:
        return self.repository.get_all()

    def update_biorreactor(self, idBiorreactor: int, bior: Biorreactor) -> Biorreactor:
        updated = self.repository.update(idBiorreactor, bior)
        if not updated:
            raise HTTPException(status_code=404, detail="Biorreactor no encontrado")
        return self.get_biorreactor(idBiorreactor)

    def delete_biorreactor(self, idBiorreactor: int) -> None:
        deleted = self.repository.delete(idBiorreactor)
        if not deleted:
            raise HTTPException(status_code=404, detail="Biorreactor no encontrado")

def get_biorreactor_service():
    return BiorreactorService(BiorreactorRepository())
