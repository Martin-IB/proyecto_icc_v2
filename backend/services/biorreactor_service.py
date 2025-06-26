from fastapi import HTTPException
from models.biorreactor import Biorreactor
from repositories.biorreactor_repository import BiorreactorRepository
from typing import List

class BiorreactorService:
    def __init__(self, repository: BiorreactorRepository):
        self.repository = repository


    def create_biorreactor(self, biorreactor: Biorreactor) -> int:
        if biorreactor.codigo < 0:
            raise HTTPException(status_code=400, detail="codigo cannot be negative")
        return self.repository.create(biorreactor)

    def get_biorreactor(self, biorreactor_id: int) -> Biorreactor:
        biorreactor = self.repository.get_by_id(biorreactor_id)
        if not biorreactor:
            raise HTTPException(status_code=404, detail="Biorreactor not found")
        return biorreactor

    def get_all_biorreactor(self) -> List[Biorreactor]:
        return self.repository.get_all()

    def update_biorreactor(self, biorreactor_id: int, biorreactor: Biorreactor) -> Biorreactor:
        if biorreactor.codigo < 0:
            raise HTTPException(status_code=400, detail="Codigo cannot be negative")
        success = self.repository.update(biorreactor_id, biorreactor)
        if not success:
            raise HTTPException(status_code=404, detail="Biorreactor not found")
        return self.get_biorreactor(biorreactor_id)

    def delete_biorreactor(self, biorreactor_id: int) -> None:
        success = self.repository.delete(biorreactor_id)
        if not success:
            raise HTTPException(status_code=404, detail="Biorreactor not found")

def get_biorreactor_service() -> BiorreactorService:
    return BiorreactorService(BiorreactorRepository())