from pydantic import BaseModel

class Biorreactor(BaseModel):
    id: int | None = None
    codigo: int
    ubicacion: str | None = None
    estado: str