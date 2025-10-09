"""
Domain entities for the Users slice.
"""
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional
from uuid import UUID

from app.users.domain.value_objects import TipoToken


@dataclass
class Role:
    nombre: str
    id: Optional[int] = None
    descripcion: Optional[str] = None


@dataclass
class Token:
    usuario_id: UUID
    tipo_token: TipoToken
    hash_token: str
    fecha_expiracion: datetime
    id: Optional[UUID] = None
    es_valido: bool = True
    fecha_creacion: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


@dataclass
class User:
    email: str
    contrasena_hasheada: str
    apodo: str
    numero_telefono: str
    id: Optional[UUID] = None
    nombre: Optional[str] = None
    apellidos: Optional[str] = None
    url_avatar: Optional[str] = None
    esta_activo: bool = True
    email_verificado: bool = False
    aprobado_por_admin: bool = False
    fecha_creacion: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    fecha_actualizacion: datetime = field(default_factory=lambda: datetime.now(timezone.utc))