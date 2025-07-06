from fastapi import HTTPException
from typing import List
from models.lectura_sensores import LecturaSensores
from repositories.lectura_sensores_repository import LecturaRepository

class LecturaService:
    def __init__(self, repository: LecturaRepository):
        self.repository = repository

    def create_lectura(self, lectura: LecturaSensores) -> int:
        return self.repository.create(lectura)

    def get_lectura(self, idLectura_sensores: int) -> LecturaSensores:
        lectura = self.repository.get_by_id(idLectura_sensores)
        if not lectura:
            raise HTTPException(status_code=404, detail="Lectura no encontrada")
        return lectura

    def get_all_lecturas(self) -> List[LecturaSensores]:
        return self.repository.get_all()

def get_lectura_service():
    return LecturaService(LecturaRepository())
