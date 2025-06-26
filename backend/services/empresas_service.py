from fastapi import HTTPException
from models.empresas import Empresa
from repositories.empresas_repository import EmpresaRepository
from typing import List

class EmpresaService:
    def __init__(self, repository: EmpresaRepository):
        self.repository = repository

    def create_empresa(self, empresa: Empresa) -> int:
        return self.repository.create(empresa)

    def get_empresa(self, empresa_id: int) -> Empresa:
        empresa = self.repository.get_by_id(empresa_id)
        if not empresa:
            raise HTTPException(status_code=404, detail="Empresa no encontrada")
        return empresa

    def get_all_empresas(self) -> List[Empresa]:
        return self.repository.get_all()

    def update_empresa(self, empresa_id: int, empresa: Empresa) -> Empresa:
        success = self.repository.update(empresa_id, empresa)
        if not success:
            raise HTTPException(status_code=404, detail="Empresa no encontrada")
        return self.get_empresa(empresa_id)

    def delete_empresa(self, empresa_id: int) -> None:
        success = self.repository.delete(empresa_id)
        if not success:
            raise HTTPException(status_code=404, detail="Empresa no encontrada")

def get_empresa_service() -> EmpresaService:
    return EmpresaService(EmpresaRepository())
