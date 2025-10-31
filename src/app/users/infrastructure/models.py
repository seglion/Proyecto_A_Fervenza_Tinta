import uuid
from datetime import datetime
from sqlalchemy import (
    Column, String, Boolean, DateTime, Enum as SQLAlchemyEnum, ForeignKey
)
from sqlalchemy.dialects.postgresql import UUID
from app.core.database import Base
from app.users.domain.value_objects import Rol, TipoToken


class UsuarioModel(Base):
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, nullable=False, index=True)
    contrasena_hasheada = Column(String, nullable=False)
    nombre = Column(String(length=100), nullable=False)
    apellidos = Column(String(length=100), nullable=False)
    numero_telefono = Column(String(length=20), unique=True, nullable=False)
    rol = Column(SQLAlchemyEnum(Rol), nullable=False, default=Rol.USUARIO)
    apodo = Column(String(length=50), nullable=True)
    url_avatar = Column(String, nullable=True)
    esta_activo = Column(Boolean, default=True, nullable=False)
    email_verificado = Column(Boolean, default=False, nullable=False)
    aprobado_por_admin = Column(Boolean, default=False, nullable=False)
    fecha_creacion = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    fecha_actualizacion = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


class TokenModel(Base):
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
<<<<<<< HEAD
    usuario_id = Column(UUID(as_uuid=True), ForeignKey("usuarios.id"), nullable=False, index=True)
>>>>>>> feature/cuotas-presentation-layer
    hash_token = Column(String, unique=True, nullable=False, index=True)
    tipo_token = Column(SQLAlchemyEnum(TipoToken), nullable=False)
    fecha_expiracion = Column(DateTime(timezone=True), nullable=False)
    es_valido = Column(Boolean, default=True, nullable=False)
    fecha_creacion = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
