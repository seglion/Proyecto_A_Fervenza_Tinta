import uuid
from datetime import datetime
from sqlalchemy import Column, String, Text, Numeric, DateTime, ForeignKey, func, Enum as SQLAlchemyEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.core.database import Base
from src.app.prendas.domain.value_objects import GeneroPrenda, TallaPrenda

class PrendaModel(Base):
    __tablename__ = "prendas"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nombre = Column(String(100), unique=True, nullable=False)
    descripcion = Column(Text, nullable=True)
    precio = Column(Numeric(10, 2), nullable=False)
    imagen_url = Column(String(255), nullable=True)
    fecha_creacion = Column(DateTime(timezone=True), default=func.now(), nullable=False)

    variantes = relationship("VariantePrendaModel", back_populates="prenda", cascade="all, delete-orphan")

class VariantePrendaModel(Base):
    __tablename__ = "variantes_prenda"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    prenda_id = Column(UUID(as_uuid=True), ForeignKey("prendas.id"), nullable=False)
    genero = Column(SQLAlchemyEnum(GeneroPrenda, name="genero_prenda_enum"), nullable=False)
    talla = Column(SQLAlchemyEnum(TallaPrenda, name="talla_prenda_enum"), nullable=False)
    fecha_creacion = Column(DateTime(timezone=True), default=func.now(), nullable=False)

    prenda = relationship("PrendaModel", back_populates="variantes")