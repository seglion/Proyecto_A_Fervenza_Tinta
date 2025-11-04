from pydantic import BaseModel, ConfigDict
from uuid import UUID
from decimal import Decimal
from typing import List, Optional
from datetime import datetime, date

from src.app.pedidos.domain.value_objects import EstadoPedido
# from src.app.users.application.dtos import UserDTO # Placeholder, will be imported later


class LineaPedidoDTO(BaseModel):
    id: UUID
    variante_prenda_id: UUID
    cantidad: int
    precio_unitario_conxelado: Decimal
    desc_variante_conxelada: str

    model_config = ConfigDict(from_attributes=True)


class PedidoDTO(BaseModel):
    id: UUID
    usuario_id: UUID
    temporada_id: int
    estado: EstadoPedido
    total_calculado: Decimal
    fecha_creacion: datetime
    metodo_pago: Optional[str] = None
    id_transaccion_externa: Optional[str] = None
    fecha_finalizacion: Optional[datetime] = None
    lineas: List[LineaPedidoDTO] = []

    model_config = ConfigDict(from_attributes=True)


class DatosLineaDTO(BaseModel):
    variante_id: UUID
    cantidad: int


class IntentoPagoDTO(BaseModel):
    url_pago: str

    model_config = ConfigDict(from_attributes=True)


class ListaPedidosDTO(BaseModel):
    pedidos: List[PedidoDTO]

    model_config = ConfigDict(from_attributes=True)


class PedidoDetalleAdminDTO(BaseModel):
    id: UUID
    usuario_id: UUID
    # usuario: UserDTO # Placeholder
    temporada_id: int
    estado: EstadoPedido
    total_calculado: Decimal
    fecha_creacion: datetime
    metodo_pago: Optional[str] = None
    id_transaccion_externa: Optional[str] = None
    fecha_finalizacion: Optional[datetime] = None
    lineas: List[LineaPedidoDTO] = []

    model_config = ConfigDict(from_attributes=True)


class ListaPedidosAdminDTO(BaseModel):
    pedidos: List[PedidoDetalleAdminDTO]

    model_config = ConfigDict(from_attributes=True)


class TemporadaPedidoDTO(BaseModel):
    id: int
    nombre_temporada: str
    fecha_inicio: date
    fecha_fin: date
    esta_activa: bool
    fecha_creacion: datetime

    model_config = ConfigDict(from_attributes=True)


class DatosTemporadaPedidoDTO(BaseModel):
    nombre_temporada: str
    fecha_inicio: date
    fecha_fin: date


class DatosPagoManualDTO(BaseModel):
    metodo_pago: str
    notas: Optional[str] = None


class PedidoCompletadoDTO(BaseModel):
    id: UUID
    estado: EstadoPedido
    fecha_finalizacion: datetime

    model_config = ConfigDict(from_attributes=True)