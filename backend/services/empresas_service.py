# SERVICE CORREGIDO - services/empresa_service.py
from fastapi import HTTPException
from typing import List
from models.empresas import Empresa
from repositories.empresas_repository import EmpresaRepository

class EmpresaService:
    def __init__(self, repository: EmpresaRepository):
        self.repository = repository

    def create_empresa(self, empresa: Empresa) -> int:
        return self.repository.create(empresa)

    def get_empresa(self, idEmpresa: int) -> Empresa:
        empresa = self.repository.get_by_id(idEmpresa)
        if not empresa:
            raise HTTPException(status_code=404, detail="Empresa no encontrada")
        return empresa

    def get_all_empresas(self) -> List[Empresa]:
        return self.repository.get_all()

    def update_empresa(self, idEmpresa: int, empresa: Empresa) -> Empresa:
        success = self.repository.update(idEmpresa, empresa)
        if not success:
            raise HTTPException(status_code=404, detail="Empresa no encontrada")
        return self.get_empresa(idEmpresa)

    def delete_empresa(self, idEmpresa: int) -> None:
        success = self.repository.delete(idEmpresa)
        if not success:
            raise HTTPException(status_code=404, detail="Empresa no encontrada")

def get_empresa_service():
    return EmpresaService(EmpresaRepository())