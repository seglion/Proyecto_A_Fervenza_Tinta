from pydantic import BaseModel, ConfigDict
from datetime import date, datetime
from decimal import Decimal
from typing import List, Optional
from uuid import UUID

from src.app.pedidos.domain.value_objects import EstadoPedido, MetodoPago
from src.app.users.application.dtos import UsuarioResponseDTO 

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
    esta_activa: bool = False

class ActualizarTemporadaPedidoDTO(BaseModel):
    nombre_temporada: Optional[str] = None
    fecha_inicio: Optional[date] = None
    fecha_fin: Optional[date] = None
    esta_activa: Optional[bool] = None

class ListaTemporadasPedidoDTO(BaseModel):
    temporadas: List[TemporadaPedidoDTO]


# --- LineaDePedido DTOs ---
class LineaDePedidoDTO(BaseModel):
    id: UUID
    pedido_id: UUID
    variante_prenda_id: UUID
    cantidad: int
    precio_unitario_conxelado: Decimal
    desc_variante_conxelada: str

    model_config = ConfigDict(from_attributes=True)

class CrearLineaDePedidoDTO(BaseModel):
    variante_prenda_id: UUID
    cantidad: int


# --- Pedido DTOs ---
class PedidoDTO(BaseModel):
    id: UUID
    usuario_id: UUID
    temporada_id: int
    estado: EstadoPedido
    total_calculado: Decimal
    metodo_pago: Optional[MetodoPago] = None
    id_transaccion_externa: Optional[str] = None
    fecha_creacion: datetime
    fecha_finalizacion: Optional[datetime] = None
    lineas: List[LineaDePedidoDTO] = [] 

    model_config = ConfigDict(from_attributes=True)

class ListaPedidosDTO(BaseModel):
    pedidos: List[PedidoDTO]

class PedidoDetalleDTO(PedidoDTO):

    pass

class IntentoPagoPedidoDTO(BaseModel):
    url_pago: str

class PedidoCompletadoDTO(BaseModel):
    id: UUID
    estado: EstadoPedido
    total_calculado: Decimal
    metodo_pago: Optional[MetodoPago] = None
    id_transaccion_externa: Optional[str] = None
    fecha_finalizacion: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)

class PedidoAdminDTO(BaseModel):
    id: UUID
    usuario_id: UUID
    temporada_id: int
    estado: EstadoPedido
    total_calculado: Decimal
    metodo_pago: Optional[MetodoPago] = None
    id_transaccion_externa: Optional[str] = None
    fecha_creacion: datetime
    fecha_finalizacion: Optional[datetime] = None
    usuario_detalle: Optional[UsuarioResponseDTO] = None 
    model_config = ConfigDict(from_attributes=True)

class ListaPedidosAdminDTO(BaseModel):
    pedidos: List[PedidoAdminDTO]

class PedidoDetalleAdminDTO(PedidoAdminDTO):
    lineas: List[LineaDePedidoDTO] = []

class ActualizarEstadoPedidoDTO(BaseModel):
    estado: EstadoPedido
    metodo_pago: Optional[MetodoPago] = None
    id_transaccion_externa: Optional[str] = None
    fecha_finalizacion: Optional[datetime] = None

class DatosPagoManualDTO(BaseModel):
    metodo_pago: MetodoPago
    id_transaccion_externa: Optional[str] = None


class ResumenVarianteDTO(BaseModel):
    temporada_id: int
    variante_prenda_id: UUID
    desc_variante_conxelada: str
    total_cantidad: Decimal
    temporada_nombre: str 
    class Config: 
        from_attributes = True

class ResumenProduccionDTO(BaseModel):
    resumen: List[ResumenVarianteDTO]