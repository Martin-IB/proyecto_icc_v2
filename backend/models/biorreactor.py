from pydantic import BaseModel
from typing import Optional

class Biorreactor(BaseModel):
    idBiorreactor: Optional[int] = None
    codigo: Optional[int]
    ubicacion: str
    estado: str
    Usuario_idUsuario: int
