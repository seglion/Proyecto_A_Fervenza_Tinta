from src.app.pedidos.application.policies.pedido_policy import PedidoPolicy

def test_pedido_policy_existe():
    assert PedidoPolicy is not None

def test_pedido_policy_tiene_metodos():
    assert hasattr(PedidoPolicy, 'es_administrador')
    assert hasattr(PedidoPolicy, 'ver_pedido')
    assert hasattr(PedidoPolicy, 'gestionar_temporadas')
    assert hasattr(PedidoPolicy, 'listar_todos_pedidos')
    assert hasattr(PedidoPolicy, 'marcar_pagado')
    assert hasattr(PedidoPolicy, 'cancelar_pedido')
