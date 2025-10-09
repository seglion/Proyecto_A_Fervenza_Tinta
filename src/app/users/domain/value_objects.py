"""
Value Objects for the Users slice.
"""
from enum import Enum


class TipoToken(str, Enum):
    VERIFICACION_EMAIL = "verificacion_email"
    RESETEO_CONTRASENA = "reseteo_contrasena"
