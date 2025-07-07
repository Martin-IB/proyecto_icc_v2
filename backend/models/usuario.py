
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

class Usuario(BaseModel):
    idUsuario: Optional[int] = Field(default=None)
    nombre: str
    email: EmailStr
    password: str
    fecha_registro: Optional[datetime] = None
    Tipo_idTipo: int

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class UsuarioUpdate(BaseModel):
    nombre: str
    email: str
    password: str
    Tipo_idTipo: int
