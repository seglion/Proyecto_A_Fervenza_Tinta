from src.app.pedidos.application.dtos import (
    PedidoDTO,
    LineaDePedidoDTO,
    CrearLineaDePedidoDTO,
    IntentoPagoPedidoDTO,
    ListaPedidosDTO,
    ListaPedidosAdminDTO,
    PedidoDetalleAdminDTO,
    TemporadaPedidoDTO,
    CrearTemporadaPedidoDTO,
    ActualizarPedidoManualDTO,
    PedidoCompletadoDTO
)

def test_pedido_dto_existe():
    assert PedidoDTO is not None

def test_linea_pedido_dto_existe():
    assert LineaDePedidoDTO is not None

def test_datos_linea_dto_existe():
    assert CrearLineaDePedidoDTO is not None

def test_intento_pago_dto_existe():
    assert IntentoPagoPedidoDTO is not None

def test_lista_pedidos_dto_existe():
    assert ListaPedidosDTO is not None

def test_lista_pedidos_admin_dto_existe():
    assert ListaPedidosAdminDTO is not None

def test_pedido_detalle_admin_dto_existe():
    assert PedidoDetalleAdminDTO is not None

def test_temporada_pedido_dto_existe():
    assert TemporadaPedidoDTO is not None

def test_datos_temporada_pedido_dto_existe():
    assert CrearTemporadaPedidoDTO is not None

def test_datos_pago_manual_dto_existe():
    assert ActualizarPedidoManualDTO is not None

def test_pedido_completado_dto_existe():
    assert PedidoCompletadoDTO is not None
