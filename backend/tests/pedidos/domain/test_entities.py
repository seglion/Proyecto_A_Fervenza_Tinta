from src.app.pedidos.domain.entities import LineaDePedido, Pedido, TemporadaPedido

def test_linea_de_pedido_entity_existe():
    assert LineaDePedido is not None

def test_pedido_entity_existe():
    assert Pedido is not None

def test_temporada_pedido_entity_existe():
    assert TemporadaPedido is not None
