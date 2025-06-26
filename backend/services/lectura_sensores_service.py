from fastapi import HTTPException
from models.lectura_sensores import LecturaSensor
from repositories.lectura_sensores_repository import LecturaSensorRepository
from typing import List

class LecturaSensorService:
    def __init__(self, repository: LecturaSensorRepository):
        self.repository = repository

    def create_lectura(self, lectura: LecturaSensor) -> int:
        return self.repository.create(lectura)

    def get_lectura(self, lectura_id: int) -> LecturaSensor:
        lectura = self.repository.get_by_id(lectura_id)
        if not lectura:
            raise HTTPException(status_code=404, detail="Lectura not found")
        return lectura

    def get_all_lecturas(self) -> List[LecturaSensor]:
        return self.repository.get_all()
    
    def update_lectura(self, lectura_id: int, lectura: LecturaSensor) -> LecturaSensor:
        success = self.repository.update(lectura_id, lectura)
        if not success:
            raise HTTPException(status_code=404, detail="Lectura no encontrada")
        return self.get_lectura(lectura_id)

    def delete_lectura(self, lectura_id: int) -> None:
        success = self.repository.delete(lectura_id)
        if not success:
            raise HTTPException(status_code=404, detail="Lectura no encontrada")


from dao.db import get_db_connection

def get_lectura_sensor_service() -> LecturaSensorService:
    return LecturaSensorService(LecturaSensorRepository(get_db_connection))
