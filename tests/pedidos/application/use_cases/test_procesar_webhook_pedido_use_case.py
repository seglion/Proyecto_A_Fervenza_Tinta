from src.app.pedidos.application.use_cases.procesar_webhook_pedido_use_case import ProcesarWebhookPedidoUseCase

def test_procesar_webhook_pedido_use_case_existe():
    assert ProcesarWebhookPedidoUseCase is not None
