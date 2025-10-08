"""
Domain entities for the Users slice.
"""
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional
from uuid import UUID


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
    esta_activo: bool = False
    email_verificado: bool = False
    aprobado_por_admin: bool = False
    fecha_creacion: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    fecha_actualizacion: datetime = field(default_factory=lambda: datetime.now(timezone.utc))