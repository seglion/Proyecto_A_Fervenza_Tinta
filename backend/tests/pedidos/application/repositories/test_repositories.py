from src.app.pedidos.application.repositories.i_pedido_repository import IPedidoRepository
from src.app.pedidos.application.repositories.i_temporada_pedido_repository import ITemporadaPedidoRepository

def test_i_pedido_repository_existe():
    assert IPedidoRepository is not None

def test_i_temporada_pedido_repository_existe():
    assert ITemporadaPedidoRepository is not None
