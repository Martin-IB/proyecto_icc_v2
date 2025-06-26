from pydantic import BaseModel
from typing import Optional

class Sensor(BaseModel):
    id: Optional[int] = None
    tipo: str
    modelo: str
    ubicacion: str
