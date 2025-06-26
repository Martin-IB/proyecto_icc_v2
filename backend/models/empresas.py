from pydantic import BaseModel
from typing import Optional

class Empresa(BaseModel):
    id: Optional[int] = None
    nombre: str
    ruc: str
    correo: str
    direccion: str
    pais: str
    representante: str
    telefono: str
