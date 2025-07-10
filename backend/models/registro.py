from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Registro(BaseModel):
    idRegistro: Optional[int] = None
    tipo_evento: str
    description: str
    fecha: Optional[datetime] = None
    Usuario_idUsuario: int
    Biorreactor_idBiorreactor: int
    Sensores_idSensores: int
class ComandoEntrada(BaseModel):
    tipo_evento: str
    description: str
    Usuario_idUsuario: int
    Biorreactor_idBiorreactor: int
    Sensores_idSensores: int