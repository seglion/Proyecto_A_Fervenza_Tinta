"""
Value Objects for the Users slice.
"""
import re
from dataclasses import dataclass
from enum import Enum
from typing import Self

class TipoToken(Enum):
    VERIFICACION_EMAIL = "VERIFICACION_EMAIL"
    RESETEO_CONTRASENA = "RESETEO_CONTRASENA"
    REFRESH_TOKEN = "REFRESH_TOKEN"

class Rol(Enum):
    ADMIN = "ADMIN"
    USUARIO = "USUARIO"

@dataclass(frozen=True)
class Password:
    value: str

    def __post_init__(self):
        self._validate(self.value)

    @staticmethod
    def _validate(password: str):
        if len(password) < 8:
            raise ValueError("Password must be at least 8 characters long.")
        if not re.search(r"[A-Z]", password):
            raise ValueError("Password must contain at least one uppercase letter.")
        if not re.search(r"[a-z]", password):
            raise ValueError("Password must contain at least one lowercase letter.")
        if not re.search(r"\d", password):
            raise ValueError("Password must contain at least one number.")
        if not re.search(r"[!@#$%^&*()_+\-=\[\]{}|;:\'\",.<>/?]", password):
            raise ValueError("Password must contain at least one special character.")

    @classmethod
    def create(cls, password: str) -> Self:
        return cls(password)
