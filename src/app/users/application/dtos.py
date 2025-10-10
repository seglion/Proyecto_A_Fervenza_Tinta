from pydantic import BaseModel, EmailStr
from typing import Optional, List
from uuid import UUID

class RegistrarUsuarioDTO(BaseModel):
    email: EmailStr
    contrasena: str
    nombre: str
    apellidos: str
    numero_telefono: str
    apodo: Optional[str] = None

class UsuarioCreadoDTO(BaseModel):
    id: UUID
    email: EmailStr

class TokensDTO(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str

class UsuarioResponseDTO(BaseModel):
    id: UUID
    email: EmailStr
    nombre: str
    apellidos: str
    apodo: Optional[str] = None
    numero_telefono: str
    url_avatar: Optional[str] = None
    esta_activo: bool
    roles: List[str]
