"""
Modelos de la base de datos para el slice de Cuotas, definidos con SQLAlchemy.
"""
import uuid # Added uuid import
from app.core.database import Base
from sqlalchemy import Column, String, Integer, Date, DateTime, func, ForeignKey, Numeric, UUID, Enum, Text # Added UUID, Enum, Text
from datetime import date, datetime
from app.users.infrastructure.models import UsuarioModel # Added UsuarioModel import
from src.app.cuotas.domain.value_objects import MetodoPago # Import MetodoPago from domain

class TemporadaCuotaModel(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre_temporada = Column(String(100), unique=True, nullable=False)
    fecha_inicio = Column(Date, nullable=False)
    fecha_fin = Column(Date, nullable=False)
    fecha_creacion = Column(DateTime(timezone=True), nullable=False, default=func.now())

class TipoCuotaModel(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    temporada_id = Column(Integer, ForeignKey('temporadacuotas.id'), nullable=False)
    nombre = Column(String(100), nullable=False)
    importe = Column(Numeric(10, 2), nullable=False)
    fecha_creacion = Column(DateTime(timezone=True), nullable=False, default=func.now())

class CuotaModel(Base):
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    usuario_id = Column(UUID(as_uuid=True), ForeignKey('usuarios.id'), nullable=False)
    tipo_de_cuota_id = Column(Integer, ForeignKey('tipocuotas.id'), nullable=False)
    importe_pagado = Column(Numeric(10, 2), nullable=False)
    estado_pago = Column(String(50), nullable=False)
    fecha_pago = Column(DateTime(timezone=True), nullable=True)
    metodo_pago = Column(Enum(MetodoPago, name='tipo_metodo_pago'), nullable=True)
    id_transaccion_externa = Column(String(255), unique=True, nullable=True)
    notas_admin = Column(Text, nullable=True)
    fecha_creacion = Column(DateTime(timezone=True), nullable=False, default=func.now())

