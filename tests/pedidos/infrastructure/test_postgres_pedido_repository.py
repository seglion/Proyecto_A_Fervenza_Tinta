import pytest
from src.app.pedidos.infrastructure.postgres_pedido_repository import PostgresPedidoRepository

def test_postgres_pedido_repository_existe():
    assert PostgresPedidoRepository is not None
