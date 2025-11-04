from src.app.pedidos.application.dtos import (
    PedidoDTO,
    LineaPedidoDTO,
    DatosLineaDTO,
    IntentoPagoDTO,
    ListaPedidosDTO,
    ListaPedidosAdminDTO,
    PedidoDetalleAdminDTO,
    TemporadaPedidoDTO,
    DatosTemporadaPedidoDTO,
    DatosPagoManualDTO,
    PedidoCompletadoDTO
)

def test_pedido_dto_existe():
    assert PedidoDTO is not None

def test_linea_pedido_dto_existe():
    assert LineaPedidoDTO is not None

def test_datos_linea_dto_existe():
    assert DatosLineaDTO is not None

def test_intento_pago_dto_existe():
    assert IntentoPagoDTO is not None

def test_lista_pedidos_dto_existe():
    assert ListaPedidosDTO is not None

def test_lista_pedidos_admin_dto_existe():
    assert ListaPedidosAdminDTO is not None

def test_pedido_detalle_admin_dto_existe():
    assert PedidoDetalleAdminDTO is not None

def test_temporada_pedido_dto_existe():
    assert TemporadaPedidoDTO is not None

def test_datos_temporada_pedido_dto_existe():
    assert DatosTemporadaPedidoDTO is not None

def test_datos_pago_manual_dto_existe():
    assert DatosPagoManualDTO is not None

def test_pedido_completado_dto_existe():
    assert PedidoCompletadoDTO is not None
