from dataclasses import dataclass, field
from uuid import UUID, uuid4
from datetime import datetime, timezone
from typing import List, Optional
from app.users.domain.value_objects import Rol, TipoToken

@dataclass
class User:
    email: str
    contrasena_hasheada: str
    nombre: str
    apellidos: str
    numero_telefono: str
    rol: Rol
    id: UUID = field(default_factory=uuid4)
    apodo: Optional[str] = None
    url_avatar: Optional[str] = None
    esta_activo: bool = True
    email_verificado: bool = False
    aprobado_por_admin: bool = False
    fecha_creacion: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    fecha_actualizacion: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

@dataclass
class Token:
    id: UUID
    usuario_id: UUID
    hash_token: str
    tipo_token: TipoToken
    fecha_expiracion: datetime
    es_valido: bool = True
    fecha_creacion: datetime = field(default_factory=lambda: datetime.now(timezone.utc))