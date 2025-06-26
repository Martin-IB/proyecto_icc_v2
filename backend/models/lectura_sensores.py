from pydantic import BaseModel
from datetime import datetime

class LecturaSensor(BaseModel):
    id: int | None = None
    temperatura: float
    humedad: float
    fecha: datetime | None = None
