import uuid
from sqlalchemy import Column, String, Integer, Date, DateTime, func, ForeignKey, Numeric, UUID, Enum, Text, Boolean
from sqlalchemy.orm import relationship

from app.core.database import Base
from src.app.pedidos.domain.value_objects import EstadoPedido, MetodoPago


class TemporadaPedidoModel(Base):
    

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre_temporada = Column(String(100), unique=True, nullable=False)
    fecha_inicio = Column(Date, nullable=False)
    fecha_fin = Column(Date, nullable=False)
    esta_activa = Column(Boolean, default=False, nullable=False)
    fecha_creacion = Column(DateTime(timezone=True), nullable=False, default=func.now())


class PedidoModel(Base):
    

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    usuario_id = Column(UUID(as_uuid=True), ForeignKey('usuarios.id'), nullable=False)
    temporada_id = Column(Integer, ForeignKey('temporadapedidos.id'), nullable=False)
    estado = Column(Enum(EstadoPedido, name='estado_pedido_enum'), nullable=False)
    total_calculado = Column(Numeric(10, 2), nullable=False)
    metodo_pago = Column(Enum(MetodoPago, name='metodo_pago_pedido_enum'), nullable=True)
    id_transaccion_externa = Column(String(255), unique=True, nullable=True)
    fecha_creacion = Column(DateTime(timezone=True), nullable=False, default=func.now())
    fecha_finalizacion = Column(DateTime(timezone=True), nullable=True)

    lineas = relationship("LineaDePedidoModel", back_populates="pedido")


class LineaDePedidoModel(Base):
    

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    pedido_id = Column(UUID(as_uuid=True), ForeignKey('pedidos.id'), nullable=False)
    variante_prenda_id = Column(UUID(as_uuid=True), ForeignKey('varianteprendas.id'), nullable=False)
    cantidad = Column(Integer, nullable=False)
    precio_unitario_conxelado = Column(Numeric(10, 2), nullable=False)
    desc_variante_conxelada = Column(String(255), nullable=False)

    pedido = relationship("PedidoModel", back_populates="lineas")
