from pydantic import BaseModel
from typing import Optional

class Tipo(BaseModel):
    id: int | None = None
    nombre: str
    email: str
    password:str

