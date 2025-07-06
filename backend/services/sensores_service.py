from typing import List
from fastapi import HTTPException
from models.sensores import Sensor
from repositories.sensores_repository import SensorRepository

class SensorService:
    def __init__(self, repository: SensorRepository):
        self.repository = repository

    def create_sensor(self, sensor: Sensor) -> int:
        return self.repository.create(sensor)

    def get_sensor(self, idSensores: int) -> Sensor:
        result = self.repository.get_by_id(idSensores)
        if not result:
            raise HTTPException(status_code=404, detail="Sensor no encontrado")
        return result

    def get_all_sensores(self) -> List[Sensor]:
        return self.repository.get_all()

    def update_sensor(self, idSensores: int, sensor: Sensor) -> Sensor:
        updated = self.repository.update(idSensores, sensor)
        if not updated:
            raise HTTPException(status_code=404, detail="Sensor no encontrado")
        return self.get_sensor(idSensores)

    def delete_sensor(self, idSensores: int) -> None:
        deleted = self.repository.delete(idSensores)
        if not deleted:
            raise HTTPException(status_code=404, detail="Sensor no encontrado")

def get_sensor_service():
    return SensorService(SensorRepository())
