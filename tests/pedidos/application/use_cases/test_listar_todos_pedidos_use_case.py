from src.app.pedidos.application.use_cases.listar_todos_pedidos_use_case import ListarTodosPedidosUseCase

def test_listar_todos_pedidos_use_case_existe():
    assert ListarTodosPedidosUseCase is not None
