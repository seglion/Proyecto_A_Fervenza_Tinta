from dataclasses import dataclass, field
from datetime import datetime, date
from decimal import Decimal
from typing import Optional, List
from uuid import UUID

from src.app.pedidos.domain.value_objects import EstadoPedido, MetodoPago


@dataclass
class LineaDePedido:
    id: UUID
    pedido_id: UUID
    variante_prenda_id: UUID
    cantidad: int
    precio_unitario_conxelado: Decimal
    desc_variante_conxelada: str


@dataclass
class Pedido:
    id: UUID
    usuario_id: UUID
    temporada_id: int
    estado: EstadoPedido
    total_calculado: Decimal
    fecha_creacion: datetime
    lineas: List[LineaDePedido] = field(default_factory=list)
    metodo_pago: Optional[MetodoPago] = None
    id_transaccion_externa: Optional[str] = None
    fecha_finalizacion: Optional[datetime] = None


@dataclass
class TemporadaPedido:
    id: Optional[int]
    nombre_temporada: str
    fecha_inicio: date
    fecha_fin: date
    esta_activa: bool
    fecha_creacion: datetime
