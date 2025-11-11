from uuid import UUID
from pydantic import BaseModel, EmailStr
from typing import List, Optional

class RegistrarUsuarioDTO(BaseModel):
    email: EmailStr
    contrasena: str
    nombre: str
    apellidos: str
    numero_telefono: str
    apodo: Optional[str] = None
    rol: str 

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
    numero_telefono: str
    url_avatar: Optional[str] = None
    esta_activo: bool
    rol: str
    email_verificado: bool
    aprobado_por_admin: bool

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