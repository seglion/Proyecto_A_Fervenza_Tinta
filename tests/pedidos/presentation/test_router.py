from fastapi import APIRouter, FastAPI
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch, ANY # Import ANY
from uuid import UUID
from datetime import datetime, timezone, date # Add date
from decimal import Decimal
import json

from src.app.pedidos.presentation.router import router as pedidos_router
from src.app.pedidos.presentation.router import router_admin as pedidos_admin_router # Import admin router
from src.app.pedidos.presentation.router import get_listar_historial_pedidos_use_case # Import the dependency function
from src.app.pedidos.presentation.router import get_obtener_pedido_borrador_use_case # New import for the new use case
from src.app.pedidos.presentation.router import get_ver_detalle_mi_pedido_use_case # New import for the new use case
from src.app.pedidos.presentation.router import get_anadir_prenda_pedido_use_case # New import for the new use case
from src.app.pedidos.presentation.router import get_eliminar_prenda_pedido_use_case # New import for the new use case
from src.app.pedidos.presentation.router import get_confirmar_pago_pedido_use_case # Correct import for the dependency function
from src.app.pedidos.application.use_cases.confirmar_encargo_use_case import ConfirmarEncargoUseCase # Import the use case
from src.app.pedidos.application.use_cases.crear_temporada_pedido_use_case import CrearTemporadaPedidoUseCase # Import the use case
from src.app.pedidos.application.use_cases.listar_todos_pedidos_use_case import ListarTodosPedidosUseCase # Import the use case
from src.app.pedidos.application.use_cases.ver_detalle_pedido_admin_use_case import VerDetallePedidoAdminUseCase # Import the use case
from src.app.pedidos.application.use_cases.marcar_pago_manual_pedido_use_case import MarcarPagoManualPedidoUseCase # New import
from src.app.pedidos.presentation.router import get_confirmar_encargo_use_case # Import for ConfirmarEncargoUseCase
from src.app.pedidos.presentation.router import get_crear_temporada_pedido_use_case # Import for CrearTemporadaPedidoUseCase
from src.app.pedidos.presentation.router import get_listar_todos_pedidos_use_case # Import for ListarTodosPedidosUseCase
from src.app.pedidos.presentation.router import get_ver_detalle_pedido_admin_use_case # Import for VerDetallePedidoAdminUseCase
from src.app.pedidos.presentation.router import get_marcar_pago_manual_pedido_use_case # New import
from src.app.pedidos.application.use_cases.confirmar_pago_pedido_use_case import ConfirmarPagoPedidoUseCase # Correct Use Case
from src.app.core.dependencies import get_current_user # Import the actual dependency from core
from src.app.pedidos.application.dtos import ListaPedidosDTO, PedidoDTO, LineaDePedidoDTO, CrearLineaDePedidoDTO, IntentoPagoPedidoDTO, PedidoDetalleAdminDTO, DatosTemporadaPedidoDTO, TemporadaPedidoDTO, DatosPagoManualDTO # Also import PedidoDTO for use in the mock response if needed
from src.app.pedidos.application.use_cases.listar_historial_pedidos_use_case import ListarHistorialPedidosUseCase
from src.app.pedidos.application.use_cases.obtener_pedido_borrador_use_case import ObtenerPedidoBorradorUseCase # New Use Case
from src.app.pedidos.application.use_cases.ver_detalle_mi_pedido_use_case import VerDetalleMiPedidoUseCase # New Use Case
from src.app.pedidos.application.use_cases.anadir_prenda_pedido_use_case import AnadirPrendaPedidoUseCase # New Use Case
from src.app.pedidos.application.use_cases.eliminar_prenda_pedido_use_case import EliminarPrendaPedidoUseCase # New Use Case
from src.app.pedidos.application.use_cases.confirmar_pago_pedido_use_case import ConfirmarPagoPedidoUseCase # Correct Use Case
from src.app.pedidos.application.exceptions import AccesoDenegadoException, PedidoNoEncontradoException, TemporadaCerradaException, LineaDePedidoNoEncontradaException, PedidoVacioException, PedidoNoModificableException # Import specific exceptions
from src.app.pedidos.domain.entities import Pedido, LineaDePedido, TemporadaPedido # Import Pedido domain entity
from src.app.pedidos.domain.value_objects import EstadoPedido, MetodoPago as TipoMetodoPago # Import EstadoPedido
from src.app.users.domain.entities import User
from src.app.users.domain.value_objects import Rol # Import Rol for the override user

# Create a minimal FastAPI app and include the pedidos_router
app = FastAPI()
app.include_router(pedidos_router)
app.include_router(pedidos_admin_router) # Include admin router

# --- OVERRIDE get_current_user GLOBALLY FOR THIS TEST MODULE --- #
# This ensures that get_current_user is properly mocked for all tests in this file.
# Store the mocked user instance
mocked_user_instance = User(
    id=UUID("d84f7cbd-3729-489a-bc8e-7a87a09a0079"), # Example UUID
    email="test@example.com",
    contrasena_hasheada="hashed_password",
    nombre="Test",
    apellidos="User",
    numero_telefono="123456789",
    esta_activo=True,
    email_verificado=True,
    rol=Rol.USUARIO,
    fecha_creacion=datetime(2025, 1, 1, 0, 0, 0, tzinfo=timezone.utc), # Fixed datetime
    fecha_actualizacion=datetime(2025, 1, 1, 0, 0, 0, tzinfo=timezone.utc) # Fixed datetime
)

# Define a mocked admin user instance
mocked_admin_user_instance = User(
    id=UUID("d84f7cbd-3729-489a-bc8e-7a87a09a0080"), # Different UUID for admin
    email="admin@example.com",
    contrasena_hasheada="hashed_admin_password",
    nombre="Admin",
    apellidos="User",
    numero_telefono="987654321",
    esta_activo=True,
    email_verificado=True,
    rol=Rol.ADMIN, # Set role to ADMIN
    fecha_creacion=datetime(2025, 1, 1, 0, 0, 0, tzinfo=timezone.utc),
    fecha_actualizacion=datetime(2025, 1, 1, 0, 0, 0, tzinfo=timezone.utc)
)

def override_get_current_user():
    return mocked_user_instance # Return the stored instance

app.dependency_overrides[get_current_user] = override_get_current_user
# ---------------------------------------------------------------- #

client = TestClient(app)

def test_router_exists_and_is_apirouter_instance():
    # This test still checks the original router object
    from src.app.pedidos.presentation.router import router
    assert isinstance(router, APIRouter)

def test_listar_pedidos_vacio_success():
    mock_use_case = AsyncMock(spec=ListarHistorialPedidosUseCase)
    mock_use_case.execute.return_value = [] # Simulate no orders

    # Temporarily override the use case dependency
    app.dependency_overrides[get_listar_historial_pedidos_use_case] = lambda: mock_use_case

    response = client.get(
        "/pedidos/",
        headers={"Authorization": "Bearer dummy_token"}
    )

    # Clean up the override
    del app.dependency_overrides[get_listar_historial_pedidos_use_case]

    assert response.status_code == 200
    assert response.json() == {"pedidos": []}
    mock_use_case.execute.assert_called_once_with(mocked_user_instance)

def test_listar_pedidos_acceso_denegado():
    mock_use_case = AsyncMock(spec=ListarHistorialPedidosUseCase)
    exception_detail = "Acceso denegado."
    mock_use_case.execute.side_effect = AccesoDenegadoException(exception_detail) # Simulate access denied

    # Temporarily override the use case dependency
    app.dependency_overrides[get_listar_historial_pedidos_use_case] = lambda: mock_use_case

    response = client.get(
        "/pedidos/",
        headers={"Authorization": "Bearer dummy_token"}
    )

    # Clean up the override
    del app.dependency_overrides[get_listar_historial_pedidos_use_case]

    assert response.status_code == 403
    assert response.json() == {"detail": exception_detail}
    mock_use_case.execute.assert_called_once_with(mocked_user_instance)

def test_obtener_pedido_borrador_success():
    # Create mock LineaDePedido domain entities
    mock_linea_1 = LineaDePedido(
        id=UUID("e1d1f0e0-c0c0-4c4c-8c8c-1e1e1e1e1e1e"),
        pedido_id=UUID("a1b1c1d1-e1f1-4a4a-8b8b-1c1c1c1c1c1c"),
        variante_prenda_id=UUID("f2a2b2c2-d2e2-4f4f-8a8a-2b2b2b2b2b2b"), # Corrected UUID
        cantidad=2,
        precio_unitario_conxelado=Decimal("15.00"),
        desc_variante_conxelada="Talla L, Color Rojo"
    )
    mock_linea_2 = LineaDePedido(
        id=UUID("e2d2f2e2-c2c2-4c4c-8c8c-1e1e1e1e1e1e"),
        pedido_id=UUID("a1b1c1d1-e1f1-4a4a-8b8b-1c1c1c1c1c1c"),
        variante_prenda_id=UUID("f3a3b3c3-d3e3-4f4f-8a8a-3b3b3b3b3b3b"), # Corrected UUID
        cantidad=1,
        precio_unitario_conxelado=Decimal("25.00"),
        desc_variante_conxelada="Talla M, Color Azul"
    )

    # Create a mock Pedido domain entity
    mock_pedido_borrador_domain = Pedido(
        id=UUID("a1b1c1d1-e1f1-4a4a-8b8b-1c1c1c1c1c1c"),
        usuario_id=mocked_user_instance.id,
        temporada_id=1,
        estado=EstadoPedido.BORRADOR,
        total_calculado=Decimal("55.00"),
        metodo_pago=None,
        id_transaccion_externa=None,
        fecha_creacion=datetime(2025, 1, 1, 10, 0, 0, tzinfo=timezone.utc),
        fecha_finalizacion=None,
        lineas=[mock_linea_1, mock_linea_2]
    )

    mock_use_case = AsyncMock(spec=ObtenerPedidoBorradorUseCase)
    mock_use_case.execute.return_value = mock_pedido_borrador_domain

    # Temporarily override the use case dependency
    app.dependency_overrides[get_obtener_pedido_borrador_use_case] = lambda: mock_use_case

    response = client.get(
        "/pedidos/borrador/",
        headers={"Authorization": "Bearer dummy_token"}
    )

    # Clean up the override
    del app.dependency_overrides[get_obtener_pedido_borrador_use_case]

    assert response.status_code == 200
    # Convert the domain entity to DTO for comparison
    expected_response_json = json.loads(PedidoDTO.model_validate(mock_pedido_borrador_domain).model_dump_json())
    assert response.json() == expected_response_json
    mock_use_case.execute.assert_called_once_with(mocked_user_instance)

# --- New tests for Ver Detalle de Mi Pedido Use Case ---
def test_ver_detalle_mi_pedido_success():
    pedido_id = UUID("a1b1c1d1-e1f1-4a4a-8b8b-1c1c1c1c1c1c")
    # Create mock LineaDePedido domain entities
    mock_linea_1 = LineaDePedido(
        id=UUID("e1d1f0e0-c0c0-4c4c-8c8c-1e1e1e1e1e1e"),
        pedido_id=pedido_id,
        variante_prenda_id=UUID("f2a2b2c2-d2e2-4f4f-8a8a-2b2b2b2b2b2b"),
        cantidad=2,
        precio_unitario_conxelado=Decimal("15.00"),
        desc_variante_conxelada="Talla L, Color Rojo"
    )
    mock_linea_2 = LineaDePedido(
        id=UUID("e2d2f2e2-c2c2-4c4c-8c8c-1e1e1e1e1e1e"),
        pedido_id=pedido_id,
        variante_prenda_id=UUID("f3a3b3c3-d3e3-4f4f-8a8a-3b3b3b3b3b3b"),
        cantidad=1,
        precio_unitario_conxelado=Decimal("25.00"),
        desc_variante_conxelada="Talla M, Color Azul"
    )

    # Create a mock Pedido domain entity
    mock_pedido_detalle_domain = Pedido(
        id=pedido_id,
        usuario_id=mocked_user_instance.id,
        temporada_id=1,
        estado=EstadoPedido.COMPLETADO,
        total_calculado=Decimal("55.00"),
        metodo_pago=None,
        id_transaccion_externa=None,
        fecha_creacion=datetime(2025, 1, 1, 10, 0, 0, tzinfo=timezone.utc),
        fecha_finalizacion=datetime(2025, 1, 1, 11, 0, 0, tzinfo=timezone.utc),
        lineas=[mock_linea_1, mock_linea_2]
    )

    mock_use_case = AsyncMock(spec=VerDetalleMiPedidoUseCase)
    mock_use_case.execute.return_value = mock_pedido_detalle_domain

    app.dependency_overrides[get_ver_detalle_mi_pedido_use_case] = lambda: mock_use_case

    response = client.get(
        f"/pedidos/{pedido_id}",
        headers={"Authorization": "Bearer dummy_token"}
    )

    del app.dependency_overrides[get_ver_detalle_mi_pedido_use_case]

    assert response.status_code == 200
    expected_response_json = json.loads(PedidoDTO.model_validate(mock_pedido_detalle_domain).model_dump_json())
    assert response.json() == expected_response_json
    mock_use_case.execute.assert_called_once_with(pedido_id, mocked_user_instance.id)

def test_ver_detalle_mi_pedido_not_found():
    pedido_id = UUID("a1b1c1d1-e1f1-4a4a-8b8b-1c1c1c1c1c1c")
    mock_use_case = AsyncMock(spec=VerDetalleMiPedidoUseCase)
    exception_detail = "Pedido no encontrado."
    mock_use_case.execute.side_effect = PedidoNoEncontradoException(exception_detail)

    app.dependency_overrides[get_ver_detalle_mi_pedido_use_case] = lambda: mock_use_case

    response = client.get(
        f"/pedidos/{pedido_id}",
        headers={"Authorization": "Bearer dummy_token"}
    )

    del app.dependency_overrides[get_ver_detalle_mi_pedido_use_case]

    assert response.status_code == 404
    assert response.json() == {"detail": f"404: {exception_detail}"}
    mock_use_case.execute.assert_called_once_with(pedido_id, mocked_user_instance.id)

def test_ver_detalle_mi_pedido_acceso_denegado():
    pedido_id = UUID("a1b1c1d1-e1f1-4a4a-8b8b-1c1c1c1c1c1c")
    mock_use_case = AsyncMock(spec=VerDetalleMiPedidoUseCase)
    exception_detail = "Acceso denegado."
    mock_use_case.execute.side_effect = AccesoDenegadoException(exception_detail)

    app.dependency_overrides[get_ver_detalle_mi_pedido_use_case] = lambda: mock_use_case

    response = client.get(
        f"/pedidos/{pedido_id}",
        headers={"Authorization": "Bearer dummy_token"}
    )

    del app.dependency_overrides[get_ver_detalle_mi_pedido_use_case]

    assert response.status_code == 403
    assert response.json() == {"detail": f"403: {exception_detail}"}
    mock_use_case.execute.assert_called_once_with(pedido_id, mocked_user_instance.id)

# --- New tests for Anadir Prenda a Pedido Use Case ---
def test_anadir_prenda_pedido_success():
    variante_id = UUID("f2a2b2c2-d2e2-4f4f-8a8a-2b2b2b2b2b2b")
    cantidad = 2
    crear_linea_dto = CrearLineaDePedidoDTO(variante_prenda_id=variante_id, cantidad=cantidad)

    # Mock de la respuesta del caso de uso
    mock_pedido_actualizado_domain = Pedido(
        id=UUID("a1b1c1d1-e1f1-4a4a-8b8b-1c1c1c1c1c1c"),
        usuario_id=mocked_user_instance.id,
        temporada_id=1,
        estado=EstadoPedido.BORRADOR,
        total_calculado=Decimal("30.00"),
        metodo_pago=None,
        id_transaccion_externa=None,
        fecha_creacion=datetime(2025, 1, 1, 10, 0, 0, tzinfo=timezone.utc),
        fecha_finalizacion=None,
        lineas=[
            LineaDePedido(
                id=UUID("e1d1f0e0-c0c0-4c4c-8c8c-1e1e1e1e1e1e"),
                pedido_id=UUID("a1b1c1d1-e1f1-4a4a-8b8b-1c1c1c1c1c1c"),
                variante_prenda_id=variante_id,
                cantidad=cantidad,
                precio_unitario_conxelado=Decimal("15.00"),
                desc_variante_conxelada="Talla L, Color Rojo"
            )
        ]
    )

    mock_use_case = AsyncMock(spec=AnadirPrendaPedidoUseCase)
    mock_use_case.execute.return_value = mock_pedido_actualizado_domain

    app.dependency_overrides[get_anadir_prenda_pedido_use_case] = lambda: mock_use_case

    response = client.post(
        "/pedidos/borrador/lineas",
        headers={"Authorization": "Bearer dummy_token"},
        json=json.loads(crear_linea_dto.model_dump_json())
    )

    del app.dependency_overrides[get_anadir_prenda_pedido_use_case]

    assert response.status_code == 200
    expected_response_json = json.loads(PedidoDTO.model_validate(mock_pedido_actualizado_domain).model_dump_json())
    assert response.json() == expected_response_json
    mock_use_case.execute.assert_called_once_with(mocked_user_instance, crear_linea_dto)

def test_anadir_prenda_pedido_temporada_cerrada():
    variante_id = UUID("f2a2b2c2-d2e2-4f4f-8a8a-2b2b2b2b2b2b")
    cantidad = 2
    crear_linea_dto = CrearLineaDePedidoDTO(variante_prenda_id=variante_id, cantidad=cantidad)

    mock_use_case = AsyncMock(spec=AnadirPrendaPedidoUseCase)
    exception_detail = "Temporada cerrada."
    mock_use_case.execute.side_effect = TemporadaCerradaException(exception_detail)

    app.dependency_overrides[get_anadir_prenda_pedido_use_case] = lambda: mock_use_case

    response = client.post(
        "/pedidos/borrador/lineas",
        headers={"Authorization": "Bearer dummy_token"},
        json=json.loads(crear_linea_dto.model_dump_json())
    )

    del app.dependency_overrides[get_anadir_prenda_pedido_use_case]

    assert response.status_code == 409
    assert response.json() == {"detail": f"409: {exception_detail}"}
    mock_use_case.execute.assert_called_once_with(mocked_user_instance, crear_linea_dto)

# --- New tests for Eliminar Prenda de Pedido Use Case ---
def test_eliminar_prenda_pedido_success():
    linea_id = UUID("e1d1f0e0-c0c0-4c4c-8c8c-1e1e1e1e1e1e")

    # Mock de la respuesta del caso de uso (pedido sin la línea)
    mock_pedido_actualizado_domain = Pedido(
        id=UUID("a1b1c1d1-e1f1-4a4a-8b8b-1c1c1c1c1c1c"),
        usuario_id=mocked_user_instance.id,
        temporada_id=1,
        estado=EstadoPedido.BORRADOR,
        total_calculado=Decimal("0.00"),
        metodo_pago=None,
        id_transaccion_externa=None,
        fecha_creacion=datetime(2025, 1, 1, 10, 0, 0, tzinfo=timezone.utc),
        fecha_finalizacion=None,
        lineas=[]
    )

    mock_use_case = AsyncMock(spec=EliminarPrendaPedidoUseCase)
    mock_use_case.execute.return_value = mock_pedido_actualizado_domain

    app.dependency_overrides[get_eliminar_prenda_pedido_use_case] = lambda: mock_use_case

    response = client.delete(
        f"/pedidos/borrador/lineas/{linea_id}",
        headers={"Authorization": "Bearer dummy_token"}
    )

    del app.dependency_overrides[get_eliminar_prenda_pedido_use_case]

    assert response.status_code == 200
    expected_response_json = json.loads(PedidoDTO.model_validate(mock_pedido_actualizado_domain).model_dump_json())
    assert response.json() == expected_response_json
    mock_use_case.execute.assert_called_once_with(mocked_user_instance, linea_id)

def test_eliminar_prenda_pedido_linea_not_found():
    linea_id = UUID("e1d1f0e0-c0c0-4c4c-8c8c-1e1e1e1e1e1e")

    mock_use_case = AsyncMock(spec=EliminarPrendaPedidoUseCase)
    exception_detail = "Línea de pedido no encontrada."
    mock_use_case.execute.side_effect = LineaDePedidoNoEncontradaException(exception_detail)

    app.dependency_overrides[get_eliminar_prenda_pedido_use_case] = lambda: mock_use_case

    response = client.delete(
        f"/pedidos/borrador/lineas/{linea_id}",
        headers={"Authorization": "Bearer dummy_token"}
    )

    del app.dependency_overrides[get_eliminar_prenda_pedido_use_case]

    assert response.status_code == 404
    assert response.json() == {"detail": f"404: {exception_detail}"}
    mock_use_case.execute.assert_called_once_with(mocked_user_instance, linea_id)

# --- New tests for Confirmar Pedido y Iniciar Pago Use Case ---
def test_confirmar_pedido_e_iniciar_pago_success():
    # Mock de la respuesta del caso de uso
    mock_intento_pago_dto = IntentoPagoPedidoDTO(url_pago="https://checkout.stripe.com/pay/cs_test_12345")

    mock_use_case = AsyncMock(spec=ConfirmarPagoPedidoUseCase)
    mock_use_case.execute.return_value = mock_intento_pago_dto

    app.dependency_overrides[get_confirmar_pago_pedido_use_case] = lambda: mock_use_case

    response = client.post(
        "/pedidos/borrador/confirmar-pago",
        headers={"Authorization": "Bearer dummy_token"}
    )

    del app.dependency_overrides[get_confirmar_pago_pedido_use_case]

    assert response.status_code == 200
    assert response.json() == {"url_pago": "https://checkout.stripe.com/pay/cs_test_12345"}
    mock_use_case.execute.assert_called_once_with(mocked_user_instance)

def test_confirmar_pedido_e_iniciar_pago_pedido_vacio():
    mock_use_case = AsyncMock(spec=ConfirmarPagoPedidoUseCase)
    exception_detail = "El pedido está vacío."
    mock_use_case.execute.side_effect = PedidoVacioException(exception_detail)

    app.dependency_overrides[get_confirmar_pago_pedido_use_case] = lambda: mock_use_case

    response = client.post(
        "/pedidos/borrador/confirmar-pago",
        headers={"Authorization": "Bearer dummy_token"}
    )

    del app.dependency_overrides[get_confirmar_pago_pedido_use_case]

    assert response.status_code == 409

# --- New tests for Marcar Pedido como Pagado Manualmente (Admin) Use Case ---
def test_marcar_pedido_pagado_manual_success():
    pedido_id = UUID("a1b1c1d1-e1f1-4a4a-8b8b-1c1c1c1c1c1c")
    marcar_pago_manual_dto = DatosPagoManualDTO(metodo_pago=TipoMetodoPago.MANUAL)

    mock_pedido_actualizado_domain = Pedido(
        id=pedido_id,
        usuario_id=mocked_user_instance.id,
        temporada_id=1,
        estado=EstadoPedido.COMPLETADO,
        total_calculado=Decimal("55.00"),
        metodo_pago=TipoMetodoPago.MANUAL,
        id_transaccion_externa=None,
        fecha_creacion=datetime(2025, 1, 1, 10, 0, 0, tzinfo=timezone.utc),
        fecha_finalizacion=datetime(2025, 1, 1, 11, 0, 0, tzinfo=timezone.utc),
        lineas=[]
    )

    mock_use_case = AsyncMock(spec=MarcarPagoManualPedidoUseCase)
    mock_use_case.execute.return_value = mock_pedido_actualizado_domain

    app.dependency_overrides[get_current_user] = lambda: mocked_admin_user_instance
    app.dependency_overrides[get_marcar_pago_manual_pedido_use_case] = lambda: mock_use_case

    response = client.post(
        f"/admin/pedidos/{pedido_id}/marcar-pagado",
        headers={"Authorization": "Bearer admin_token"},
        json=json.loads(marcar_pago_manual_dto.model_dump_json())
    )

    del app.dependency_overrides[get_marcar_pago_manual_pedido_use_case]
    app.dependency_overrides[get_current_user] = override_get_current_user

    assert response.status_code == 200
    expected_response_json = json.loads(PedidoDTO.model_validate(mock_pedido_actualizado_domain).model_dump_json())
    assert response.json() == expected_response_json
    mock_use_case.execute.assert_called_once_with(pedido_id, marcar_pago_manual_dto, mocked_admin_user_instance)

def test_marcar_pedido_pagado_manual_acceso_denegado():
    pedido_id = UUID("a1b1c1d1-e1f1-4a4a-8b8b-1c1c1c1c1c1c")
    marcar_pago_manual_dto = DatosPagoManualDTO(metodo_pago=TipoMetodoPago.MANUAL)

    mock_use_case = AsyncMock(spec=MarcarPagoManualPedidoUseCase)

    app.dependency_overrides[get_current_user] = lambda: mocked_user_instance
    app.dependency_overrides[get_marcar_pago_manual_pedido_use_case] = lambda: mock_use_case

    response = client.post(
        f"/admin/pedidos/{pedido_id}/marcar-pagado",
        headers={"Authorization": "Bearer user_token"},
        json=json.loads(marcar_pago_manual_dto.model_dump_json())
    )

    del app.dependency_overrides[get_marcar_pago_manual_pedido_use_case]
    app.dependency_overrides[get_current_user] = override_get_current_user

    assert response.status_code == 403
    assert response.json() == {"detail": "The user doesn't have enough privileges"}
    mock_use_case.execute.assert_not_called()

def test_marcar_pedido_pagado_manual_pedido_no_encontrado():
    pedido_id = UUID("a1b1c1d1-e1f1-4a4a-8b8b-1c1c1c1c1c1c")
    marcar_pago_manual_dto = DatosPagoManualDTO(metodo_pago=TipoMetodoPago.MANUAL)

    mock_use_case = AsyncMock(spec=MarcarPagoManualPedidoUseCase)
    exception_detail = "Pedido no encontrado."
    mock_use_case.execute.side_effect = PedidoNoEncontradoException(exception_detail)

    app.dependency_overrides[get_current_user] = lambda: mocked_admin_user_instance
    app.dependency_overrides[get_marcar_pago_manual_pedido_use_case] = lambda: mock_use_case

    response = client.post(
        f"/admin/pedidos/{pedido_id}/marcar-pagado",
        headers={"Authorization": "Bearer admin_token"},
        json=json.loads(marcar_pago_manual_dto.model_dump_json())
    )

    del app.dependency_overrides[get_marcar_pago_manual_pedido_use_case]
    app.dependency_overrides[get_current_user] = override_get_current_user

    assert response.status_code == 404
    assert response.json() == {"detail": f"404: {exception_detail}"}
    mock_use_case.execute.assert_called_once_with(pedido_id, marcar_pago_manual_dto, mocked_admin_user_instance)

def test_marcar_pedido_pagado_manual_pedido_ya_pagado():
    pedido_id = UUID("a1b1c1d1-e1f1-4a4a-8b8b-1c1c1c1c1c1c")
    marcar_pago_manual_dto = DatosPagoManualDTO(metodo_pago=TipoMetodoPago.MANUAL)

    mock_use_case = AsyncMock(spec=MarcarPagoManualPedidoUseCase)
    exception_detail = "El pedido no se puede modificar en su estado actual."
    mock_use_case.execute.side_effect = PedidoNoModificableException(exception_detail)

    app.dependency_overrides[get_current_user] = lambda: mocked_admin_user_instance
    app.dependency_overrides[get_marcar_pago_manual_pedido_use_case] = lambda: mock_use_case

    response = client.post(
        f"/admin/pedidos/{pedido_id}/marcar-pagado",
        headers={"Authorization": "Bearer admin_token"},
        json=json.loads(marcar_pago_manual_dto.model_dump_json())
    )

    del app.dependency_overrides[get_marcar_pago_manual_pedido_use_case]
    app.dependency_overrides[get_current_user] = override_get_current_user

    assert response.status_code == 409
    assert response.json() == {"detail": f"409: {exception_detail}"}
    mock_use_case.execute.assert_called_once_with(pedido_id, marcar_pago_manual_dto, mocked_admin_user_instance)

# --- New tests for Crear Temporada Pedido Use Case (Admin) ---
def test_crear_temporada_pedido_success():
    # Mock de los datos de entrada
    datos_temporada = DatosTemporadaPedidoDTO(
        nombre_temporada="Temporada Test 2025-2026",
        fecha_inicio=date(2025, 9, 1),
        fecha_fin=date(2026, 5, 31),
        esta_activa=False
    )

    # Mock de la respuesta del caso de uso
    mock_temporada_creada_domain = TemporadaPedido(
        id=1,
        nombre_temporada="Temporada Test 2025-2026",
        fecha_inicio=date(2025, 9, 1),
        fecha_fin=date(2026, 5, 31),
        esta_activa=False,
        fecha_creacion=datetime(2025, 8, 1, 10, 0, 0, tzinfo=timezone.utc)
    )

    mock_use_case = AsyncMock(spec=CrearTemporadaPedidoUseCase)
    mock_use_case.execute.return_value = TemporadaPedidoDTO.model_validate(mock_temporada_creada_domain)

    # Override get_current_user to return an admin user for this test
    app.dependency_overrides[get_current_user] = lambda: mocked_admin_user_instance
    app.dependency_overrides[get_crear_temporada_pedido_use_case] = lambda: mock_use_case

    response = client.post(
        "/admin/pedidos/temporadas",
        headers={"Authorization": "Bearer admin_token"},
        json=json.loads(datos_temporada.model_dump_json())
    )

    # Clean up overrides
    del app.dependency_overrides[get_crear_temporada_pedido_use_case]
    app.dependency_overrides[get_current_user] = override_get_current_user # Restore original user override

    assert response.status_code == 201
    expected_response_json = json.loads(TemporadaPedidoDTO.model_validate(mock_temporada_creada_domain).model_dump_json())
    assert response.json() == expected_response_json
    mock_use_case.execute.assert_called_once_with(datos_temporada, mocked_admin_user_instance)

def test_crear_temporada_pedido_acceso_denegado():
    # Mock de los datos de entrada
    datos_temporada = DatosTemporadaPedidoDTO(
        nombre_temporada="Temporada Test 2025-2026",
        fecha_inicio=date(2025, 9, 1),
        fecha_fin=date(2026, 5, 31),
        esta_activa=False
    )

    mock_use_case = AsyncMock(spec=CrearTemporadaPedidoUseCase)

    # Ensure a non-admin user is used
    app.dependency_overrides[get_current_user] = override_get_current_user # This is already the default, but explicit for clarity
    app.dependency_overrides[get_crear_temporada_pedido_use_case] = lambda: mock_use_case

    response = client.post(
        "/admin/pedidos/temporadas",
        headers={"Authorization": "Bearer user_token"},
        json=json.loads(datos_temporada.model_dump_json())
    )

    # Clean up overrides
    del app.dependency_overrides[get_crear_temporada_pedido_use_case]
    # get_current_user override remains as default non-admin

    assert response.status_code == 403
    assert response.json() == {"detail": "The user doesn't have enough privileges"}
    mock_use_case.execute.assert_not_called()


# --- New tests for Ver Detalle de un Pedido (Admin) Use Case ---
def test_ver_detalle_pedido_admin_success():
    pedido_id = UUID("a1b1c1d1-e1f1-4a4a-8b8b-1c1c1c1c1c1c")
    user_id = UUID("d84f7cbd-3729-489a-bc8e-7a87a09a0079") # Example user ID

    # Mock LineaDePedido domain entities
    mock_linea_1 = LineaDePedido(
        id=UUID("e1d1f0e0-c0c0-4c4c-8c8c-1e1e1e1e1e1e"),
        pedido_id=pedido_id,
        variante_prenda_id=UUID("f2a2b2c2-d2e2-4f4f-8a8a-2b2b2b2b2b2b"),
        cantidad=2,
        precio_unitario_conxelado=Decimal("15.00"),
        desc_variante_conxelada="Talla L, Color Rojo"
    )
    mock_linea_2 = LineaDePedido(
        id=UUID("e2d2f2e2-c2c2-4c4c-8c8c-1e1e1e1e1e1e"),
        pedido_id=pedido_id,
        variante_prenda_id=UUID("f3a3b3c3-d3e3-4f4f-8a8a-3b3b3b3b3b3b"),
        cantidad=1,
        precio_unitario_conxelado=Decimal("25.00"),
        desc_variante_conxelada="Talla M, Color Azul"
    )

    # Mock User domain entity
    mock_user_pedido = User(
        id=user_id,
        email="user_pedido@example.com",
        contrasena_hasheada="hashed_password",
        nombre="User",
        apellidos="Pedido",
        numero_telefono="111222333",
        esta_activo=True,
        email_verificado=True,
        rol=Rol.USUARIO,
        fecha_creacion=datetime(2025, 1, 1, 0, 0, 0, tzinfo=timezone.utc),
        fecha_actualizacion=datetime(2025, 1, 1, 0, 0, 0, tzinfo=timezone.utc)
    )

    # Mock Pedido domain entity with user and lines
    mock_pedido_detalle_admin_domain = Pedido(
        id=pedido_id,
        usuario_id=user_id,
        temporada_id=1,
        estado=EstadoPedido.COMPLETADO,
        total_calculado=Decimal("55.00"),
        metodo_pago=None,
        id_transaccion_externa=None,
        fecha_creacion=datetime(2025, 1, 1, 10, 0, 0, tzinfo=timezone.utc),
        fecha_finalizacion=datetime(2025, 1, 1, 11, 0, 0, tzinfo=timezone.utc),
        lineas=[mock_linea_1, mock_linea_2]
    )

    mock_use_case = AsyncMock(spec=VerDetallePedidoAdminUseCase)
    mock_use_case.execute.return_value = PedidoDetalleAdminDTO.model_validate(mock_pedido_detalle_admin_domain)

    # Override get_current_user to return an admin user for this test
    app.dependency_overrides[get_current_user] = lambda: mocked_admin_user_instance
    app.dependency_overrides[get_ver_detalle_pedido_admin_use_case] = lambda: mock_use_case

    response = client.get(
        f"/admin/pedidos/{pedido_id}",
        headers={"Authorization": "Bearer admin_token"}
    )

    # Clean up overrides
    del app.dependency_overrides[get_ver_detalle_pedido_admin_use_case]
    app.dependency_overrides[get_current_user] = override_get_current_user # Restore original user override

    assert response.status_code == 200
    expected_response_json = json.loads(PedidoDetalleAdminDTO.model_validate(mock_pedido_detalle_admin_domain).model_dump_json())
    assert response.json() == expected_response_json
    mock_use_case.execute.assert_called_once_with(pedido_id, mocked_admin_user_instance)

# --- New tests for Confirmar Pedido como Encargo Use Case ---
def test_confirmar_pedido_como_encargo_success():
    # Mock de la respuesta del caso de uso
    mock_pedido_finalizado_domain = Pedido(
        id=UUID("a1b1c1d1-e1f1-4a4a-8b8b-1c1c1c1c1c1c"),
        usuario_id=mocked_user_instance.id,
        temporada_id=1,
        estado=EstadoPedido.ENCARGADO,
        total_calculado=Decimal("55.00"),
        metodo_pago=None,
        id_transaccion_externa=None,
        fecha_creacion=datetime(2025, 1, 1, 10, 0, 0, tzinfo=timezone.utc),
        fecha_finalizacion=datetime(2025, 1, 1, 11, 0, 0, tzinfo=timezone.utc),
        lineas=[]
    )

    mock_use_case = AsyncMock(spec=ConfirmarEncargoUseCase)
    mock_use_case.execute.return_value = mock_pedido_finalizado_domain

    app.dependency_overrides[get_confirmar_encargo_use_case] = lambda: mock_use_case

    response = client.post(
        "/pedidos/borrador/confirmar-encargo",
        headers={"Authorization": "Bearer dummy_token"}
    )

    del app.dependency_overrides[get_confirmar_encargo_use_case]

    assert response.status_code == 201
    expected_response_json = json.loads(PedidoDTO.model_validate(mock_pedido_finalizado_domain).model_dump_json())
    assert response.json() == expected_response_json
    mock_use_case.execute.assert_called_once_with(mocked_user_instance)

def test_confirmar_pedido_como_encargo_temporada_cerrada():
    mock_use_case = AsyncMock(spec=ConfirmarEncargoUseCase)
    exception_detail = "Temporada cerrada."
    mock_use_case.execute.side_effect = TemporadaCerradaException(exception_detail)

    app.dependency_overrides[get_confirmar_encargo_use_case] = lambda: mock_use_case

    response = client.post(
        "/pedidos/borrador/confirmar-encargo",
        headers={"Authorization": "Bearer dummy_token"}
    )

    del app.dependency_overrides[get_confirmar_encargo_use_case]

    assert response.status_code == 409