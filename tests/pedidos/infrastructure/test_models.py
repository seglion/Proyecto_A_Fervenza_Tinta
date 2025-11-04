from src.app.pedidos.infrastructure.models import PedidoModel, LineaDePedidoModel, TemporadaPedidoModel

def test_pedido_model_existe():
    assert PedidoModel is not None

def test_linea_de_pedido_model_existe():
    assert LineaDePedidoModel is not None

def test_temporada_pedido_model_existe():
    assert TemporadaPedidoModel is not None
