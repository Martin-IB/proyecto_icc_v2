from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class LecturaSensores(BaseModel):
    idLectura_sensores: Optional[int] = None
    temperatura: float
    humedad: float
    estado_ambiente: Optional[str] = None
    fecha: Optional[datetime] = None
    Biorreactor_idBiorreactor: int
    Sensores_idSensores: int
