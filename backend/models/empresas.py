# MODELO CORREGIDO - models/empresa.py
from pydantic import BaseModel, EmailStr
from typing import Optional

class Empresa(BaseModel):
    idEmpresa: Optional[int] = None
    nombre: str
    ruc: str
    correo: EmailStr
    direccion: str
    pais: str
    representante: str
    telefono: str
    Usuario_idUsuario: int