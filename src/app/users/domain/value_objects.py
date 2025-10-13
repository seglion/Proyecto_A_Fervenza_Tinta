"""
Value Objects for the Users slice.
"""
from enum import Enum

class TipoToken(Enum):
    VERIFICACION_EMAIL = "verificacion_email"
    RESETEO_CONTRASENA = "reseteo_contrasena"

class Rol(Enum):
    ADMIN = "admin"
    USUARIO = "usuario"
