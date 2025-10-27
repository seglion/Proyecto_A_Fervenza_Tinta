from uuid import UUID
from pydantic import BaseModel, EmailStr, ConfigDict
from typing import List, Optional

class RegistrarUsuarioDTO(BaseModel):
    email: EmailStr
    contrasena: str
    nombre: str
    apellidos: str
    numero_telefono: str
    apodo: Optional[str] = None
    rol: str # Default to 'usuario' in use case

class UsuarioCreadoDTO(BaseModel):
    id: UUID
    email: EmailStr

class IniciarSesionDTO(BaseModel):
    email: EmailStr
    contrasena: str

class UsuarioResponseDTO(BaseModel):
    id: UUID
    email: EmailStr
    nombre: str
    apellidos: str
    apodo: Optional[str] = None
    numero_telefono: Optional[str] = None
    url_avatar: Optional[str] = None
    esta_activo: bool
    rol: str

    model_config = ConfigDict(from_attributes=True)

class ActualizarMiPerfilDTO(BaseModel):
    nombre: Optional[str] = None
    apellidos: Optional[str] = None
    apodo: Optional[str] = None
    numero_telefono: Optional[str] = None
    url_avatar: Optional[str] = None

class CambiarContrasenaDTO(BaseModel):
    contrasena_antigua: str
    contrasena_nueva: str

class ConfirmarNuevaContrasenaDTO(BaseModel):
    token: str
    nueva_contrasena: str

class ListaUsuariosResponseDTO(BaseModel):
    usuarios: List[UsuarioResponseDTO]