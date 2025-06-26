
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Usuario(BaseModel):
    id: int | None = None
    nombre: str
    email: str
    fecha_registro: datetime | None = None