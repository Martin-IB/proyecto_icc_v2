from pydantic import BaseModel
from typing import Optional

class Sensor(BaseModel):
    idSensores: Optional[int] = None
    tipo: str
    modelo: str
    ubicacion: str
    Biorreactor_idBiorreactor: int
