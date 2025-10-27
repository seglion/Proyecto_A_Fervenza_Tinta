from dataclasses import dataclass, field
from datetime import date, datetime
from decimal import Decimal
from typing import List
from uuid import UUID, uuid4

from src.app.cuotas.domain.value_objects import EstadoPago, MetodoPago

@dataclass
class TipoCuota:
    id: int
    temporada_id: int
    nombre: str
    importe: Decimal
    fecha_creacion: datetime

@dataclass
class TemporadaCuota:
    id: int
    nombre_temporada: str
    fecha_inicio: date
    fecha_fin: date
    fecha_creacion: datetime
    tipos_cuota: List[TipoCuota] = field(default_factory=list)

@dataclass
class Cuota:
    usuario_id: UUID
    tipo_de_cuota_id: int
    importe_pagado: Decimal
    estado_pago: EstadoPago
    id: UUID = field(default_factory=uuid4)
    fecha_pago: datetime | None = None
    metodo_pago: MetodoPago | None = None
    id_transaccion_externa: str | None = None
    notas_admin: str | None = None
    fecha_creacion: datetime = field(default_factory=datetime.now)
