from fastapi import HTTPException
from typing import List
from models.registro import Registro,ComandoEntrada
from repositories.registro_repository import RegistroRepository

class RegistroService:
    def __init__(self, repository: RegistroRepository):
        self.repository = repository

    def create_registro(self, registro: Registro) -> int:
        return self.repository.create(registro)

    def get_registro(self, idRegistro: int) -> Registro:
        registro = self.repository.get_by_id(idRegistro)
        if not registro:
            raise HTTPException(status_code=404, detail="Registro no encontrado")
        return registro

    def get_all_registros(self) -> List[Registro]:
        return self.repository.get_all()
    
    def registrar_comando(self, comando: ComandoEntrada) -> int:
        registro = Registro(**comando.dict())
        return self.create_registro(registro)
    
    def update_registro(self, idRegistro: int, registro: Registro) -> Registro:
        success = self.repository.update(idRegistro, registro)
        if not success:
            raise HTTPException(status_code=404, detail="Registro no encontrado")
        return self.get_registro(idRegistro)

    def delete_registro(self, idRegistro: int) -> None:
        success = self.repository.delete(idRegistro)
        if not success:
            raise HTTPException(status_code=404, detail="Registro no encontrado")

def get_registro_service():
    return RegistroService(RegistroRepository())
