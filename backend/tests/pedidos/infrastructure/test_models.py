import pytest
from pathlib import Path
from sqlalchemy import Column, String, Integer, Date, DateTime, func, ForeignKey, Numeric, UUID, Enum, Text, Boolean
from sqlalchemy.orm import relationship, RelationshipProperty
from app.core.database import Base
from src.app.pedidos.domain.value_objects import EstadoPedido, MetodoPago
from src.app.pedidos.infrastructure.models import TemporadaPedidoModel, PedidoModel, LineaDePedidoModel

# Test para verificar la existencia del archivo models.py
def test_models_file_exists():
    path = Path("src/app/pedidos/infrastructure/models.py")
    assert path.exists(), f"El archivo {path} no existe."

# Test para verificar la existencia de la clase TemporadaPedidoModel
def test_temporada_pedido_model_exists():
    assert issubclass(TemporadaPedidoModel, Base)

# Test para verificar las columnas de TemporadaPedidoModel
def test_temporada_pedido_model_columns():
    columns = TemporadaPedidoModel.__table__.columns
    assert "id" in columns
    assert "nombre_temporada" in columns
    assert "fecha_inicio" in columns
    assert "fecha_fin" in columns
    assert "esta_activa" in columns
    assert "fecha_creacion" in columns

    assert isinstance(columns["id"].type, Integer)
    assert columns["id"].primary_key
    assert columns["id"].autoincrement

    assert isinstance(columns["nombre_temporada"].type, String)
    assert columns["nombre_temporada"].unique
    assert not columns["nombre_temporada"].nullable

    assert isinstance(columns["fecha_inicio"].type, Date)
    assert not columns["fecha_inicio"].nullable

    assert isinstance(columns["fecha_fin"].type, Date)
    assert not columns["fecha_fin"].nullable

    assert isinstance(columns["esta_activa"].type, Boolean)
    assert not columns["esta_activa"].nullable
    assert columns["esta_activa"].default.arg == False

    assert isinstance(columns["fecha_creacion"].type, DateTime)
    assert not columns["fecha_creacion"].nullable

# Test para verificar la existencia de la clase PedidoModel
def test_pedido_model_exists():
    assert issubclass(PedidoModel, Base)

# Test para verificar las columnas de PedidoModel
def test_pedido_model_columns():
    columns = PedidoModel.__table__.columns
    assert "id" in columns
    assert "usuario_id" in columns
    assert "temporada_id" in columns
    assert "estado" in columns
    assert "total_calculado" in columns
    assert "metodo_pago" in columns
    assert "id_transaccion_externa" in columns
    assert "fecha_creacion" in columns
    assert "fecha_finalizacion" in columns

    assert isinstance(columns["id"].type, UUID)
    assert columns["id"].primary_key

    assert isinstance(columns["usuario_id"].type, UUID)
    assert not columns["usuario_id"].nullable
    assert columns["usuario_id"].foreign_keys

    assert isinstance(columns["temporada_id"].type, Integer)
    assert not columns["temporada_id"].nullable
    assert columns["temporada_id"].foreign_keys

    assert isinstance(columns["estado"].type, Enum)
    assert not columns["estado"].nullable

    assert isinstance(columns["total_calculado"].type, Numeric)
    assert not columns["total_calculado"].nullable

    assert isinstance(columns["metodo_pago"].type, Enum)
    assert columns["metodo_pago"].nullable

    assert isinstance(columns["id_transaccion_externa"].type, String)
    assert columns["id_transaccion_externa"].unique
    assert columns["id_transaccion_externa"].nullable

    assert isinstance(columns["fecha_creacion"].type, DateTime)
    assert not columns["fecha_creacion"].nullable

    assert isinstance(columns["fecha_finalizacion"].type, DateTime)
    assert columns["fecha_finalizacion"].nullable

    assert "lineas" in PedidoModel.__dict__
    assert isinstance(PedidoModel.lineas.property, RelationshipProperty)

# Test para verificar la existencia de la clase LineaDePedidoModel
def test_linea_de_pedido_model_exists():
    assert issubclass(LineaDePedidoModel, Base)

# Test para verificar las columnas de LineaDePedidoModel
def test_linea_de_pedido_model_columns():
    columns = LineaDePedidoModel.__table__.columns
    assert "id" in columns
    assert "pedido_id" in columns
    assert "variante_prenda_id" in columns
    assert "cantidad" in columns
    assert "precio_unitario_conxelado" in columns
    assert "desc_variante_conxelada" in columns

    assert isinstance(columns["id"].type, UUID)
    assert columns["id"].primary_key

    assert isinstance(columns["pedido_id"].type, UUID)
    assert not columns["pedido_id"].nullable
    assert columns["pedido_id"].foreign_keys

    assert isinstance(columns["variante_prenda_id"].type, UUID)
    assert not columns["variante_prenda_id"].nullable
    assert columns["variante_prenda_id"].foreign_keys

    assert isinstance(columns["cantidad"].type, Integer)
    assert not columns["cantidad"].nullable

    assert isinstance(columns["precio_unitario_conxelado"].type, Numeric)
    assert not columns["precio_unitario_conxelado"].nullable

    assert isinstance(columns["desc_variante_conxelada"].type, String)
    assert not columns["desc_variante_conxelada"].nullable

    assert "pedido" in LineaDePedidoModel.__dict__
    assert isinstance(LineaDePedidoModel.pedido.property, RelationshipProperty)