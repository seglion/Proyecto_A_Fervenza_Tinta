from pydantic import BaseModel
from datetime import date, datetime
from decimal import Decimal
from typing import List, Optional
from uuid import UUID

from src.app.cuotas.domain.value_objects import EstadoPago, MetodoPago
from src.app.users.application.dtos import UsuarioResponseDTO
from src.app.users.domain.value_objects import Rol

class TipoCuotaDTO(BaseModel):
    nombre: str
    importe: Decimal

class CrearTemporadaDTO(BaseModel):
    nombre_temporada: str
    fecha_inicio: date
    fecha_fin: date
    tipos_cuota: List[TipoCuotaDTO]

class TemporadaCreadaDTO(BaseModel):
    id: int

class TemporadaDTO(BaseModel):
    id: int
    nombre_temporada: str
    fecha_inicio: date
    fecha_fin: date
    tipos_cuota: List[TipoCuotaDTO]

class ListaTemporadasDTO(BaseModel):
    temporadas: List[TemporadaDTO]

class ActualizarTemporadaDTO(BaseModel):
    nombre_temporada: Optional[str] = None
    fecha_inicio: Optional[date] = None
    fecha_fin: Optional[date] = None
    tipos_cuota: Optional[List[TipoCuotaDTO]] = None

class CuotaDTO(BaseModel):
    id: UUID
    usuario_id: UUID
    tipo_de_cuota_id: int
    importe_pagado: Decimal
    estado_pago: EstadoPago
    fecha_pago: Optional[datetime] = None
    metodo_pago: Optional[MetodoPago] = None
    id_transaccion_externa: Optional[str] = None
    notas_admin: Optional[str] = None

class ListaCuotasDTO(BaseModel):
    cuotas: List[CuotaDTO]

class EstadoPagoDTO(BaseModel):
    estado: EstadoPago
    cuota: Optional[CuotaDTO] = None

class IntentoPagoDTO(BaseModel):
    url_pago: str

class HistorialCuotasDTO(BaseModel):
    historial: List[CuotaDTO]

class DetalleCuotaDTO(BaseModel):
    cuota: CuotaDTO
    temporada: TemporadaDTO

class RegistrarCuotaManualDTO(BaseModel):
    usuario_id: UUID
    tipo_cuota_id: int
    importe: Decimal
    metodo: MetodoPago
    notas: Optional[str] = None

class InformePendientesDTO(BaseModel):
    pendientes: List[UsuarioResponseDTO]

class UsuarioPolicyDTO(BaseModel):
    rol: Rol
    esta_activo: bool
