import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock
from uuid import uuid4
from datetime import date, datetime
from decimal import Decimal

from src.app.users.domain.entities import User
from src.app.users.domain.value_objects import Rol
from src.app.core.dependencies import get_current_user
from src.app.cuotas.presentation.router import get_admin_user, get_ver_detalle_cuota_use_case, get_registrar_cuota_manual_use_case, get_obtener_generar_mi_cuota_use_case, get_generar_informe_pendientes_use_case, get_consultar_historial_cuotas_use_case
from src.app.cuotas.application.dtos import DetalleCuotaDTO, CuotaDTO, TemporadaDTO, TipoCuotaDTO, CuotaCompletadaDTO, ActualizarCuotaManualDTO, InformePendientesDTO, HistorialCuotasDTO, CuotaDetalleResponseDTO
from src.app.users.application.dtos import UsuarioResponseDTO
from src.app.cuotas.domain.value_objects import MetodoPago, EstadoPago, NombreTipoCuota
from src.app.cuotas.application.exceptions import TemporadaNoEncontrada, TipoCuotaNoEncontrado

# ------------------ Fixtures ------------------
@pytest.fixture(scope="function")
def app_client():
    from src.app.cuotas.presentation.router import router as cuotas_router
    app = FastAPI()
    app.include_router(cuotas_router)
    with TestClient(app) as client:
        yield client

@pytest.fixture
def admin_user():
    return User(id=uuid4(), rol=Rol.ADMIN, email="admin@test.com", contrasena_hasheada="123", nombre="Admin", apellidos="Test", numero_telefono="123456789", esta_activo=True, email_verificado=True, aprobado_por_admin=True)

@pytest.fixture
def non_admin_user_active():
    return User(id=uuid4(), rol=Rol.USUARIO, email="user@test.com", contrasena_hasheada="123", nombre="User", apellidos="Test", numero_telefono="987654321", esta_activo=True, email_verificado=True, aprobado_por_admin=True)

@pytest.fixture
def mock_ver_detalle_cuota_use_case():
    mock = AsyncMock()
    cuota_id = uuid4()
    user_id = uuid4()
    # Create dummy data for UsuarioResponseDTO and TipoCuotaDTO
    dummy_user_dto = UsuarioResponseDTO(
        id=user_id,
        email="test@user.com",
        nombre="Test",
        apellidos="User",
        apodo="Tester",
        numero_telefono="123456789",
        url_avatar=None,
        esta_activo=True,
        rol="usuario"
    )
    dummy_tipo_cuota_dto = TipoCuotaDTO(
        id=1,
        nombre=NombreTipoCuota.SOCIO,
        importe=Decimal("50.00"),
        fecha_creacion=datetime.now()
    )

    mock.execute.return_value = DetalleCuotaDTO(
        cuota=CuotaDTO(
            id=cuota_id,
            usuario_id=user_id,
            tipo_de_cuota_id=1,
            importe_pagado=Decimal("50.00"),
            estado_pago=EstadoPago.COMPLETADO,
            fecha_pago=datetime.now(),
            metodo_pago=MetodoPago.STRIPE
        ),
        temporada=TemporadaDTO(
            id=1,
            nombre_temporada="2025-2026",
            fecha_inicio=date(2025, 10, 1),
            fecha_fin=date(2026, 7, 25),
            tipos_cuota=[
                TipoCuotaDTO(id=1, nombre=NombreTipoCuota.SOCIO, importe=Decimal("50.00"), fecha_creacion=datetime.now())
            ]
        ),
        tipo_cuota_detalle=dummy_tipo_cuota_dto, # New
        usuario_detalle=dummy_user_dto # New
    ).model_dump(by_alias=True, mode='json') # Convert to dict for direct comparison with response.json()
    return mock

@pytest.fixture
def mock_registrar_cuota_manual_use_case():
    mock = AsyncMock()
    mock.execute.return_value = CuotaCompletadaDTO(id=uuid4())
    return mock

@pytest.fixture
def mock_obtener_generar_mi_cuota_use_case():
    mock = AsyncMock()
    return mock

@pytest.fixture
def mock_generar_informe_pendientes_use_case():
    mock = AsyncMock()
    mock.execute.return_value = InformePendientesDTO(pendientes=[])
    return mock

@pytest.fixture
def mock_consultar_historial_cuotas_use_case():
    mock = AsyncMock()
    detailed_cuota_dto = CuotaDetalleResponseDTO(
        id=uuid4(),
        usuario_id=uuid4(),
        tipo_de_cuota_id=1,
        importe_pagado=Decimal("50.00"),
        estado_pago=EstadoPago.COMPLETADO,
        fecha_pago=datetime.now(),
        metodo_pago=MetodoPago.STRIPE,
        id_transaccion_externa="pi_123",
        notas_admin=None,
        usuario_nombre="Test",
        usuario_apellidos="User",
        tipo_cuota_nombre=NombreTipoCuota.SOCIO,
        temporada_nombre="2024-2025"
    )
    mock.execute.return_value = HistorialCuotasDTO(historial=[detailed_cuota_dto])
    return mock

@pytest.fixture
def expected_cuota_dto(non_admin_user_active):
    return CuotaDTO(
        id=uuid4(),
        usuario_id=non_admin_user_active.id,
        tipo_de_cuota_id=1,
        importe_pagado=Decimal("60.00"),
        estado_pago=EstadoPago.PENDIENTE,
        fecha_pago=None,
        metodo_pago=None,
        id_transaccion_externa=None,
        notas_admin=None,
        fecha_creacion=datetime.now()
    )

# ------------------ Tests for VerDetalleCuota ------------------

@pytest.mark.asyncio
async def test_ver_detalle_cuota_success(app_client, admin_user, mock_ver_detalle_cuota_use_case):
    # Arrange
    cuota_id = uuid4()
    app_client.app.dependency_overrides[get_current_user] = lambda: admin_user
    app_client.app.dependency_overrides[get_admin_user] = lambda: admin_user
    app_client.app.dependency_overrides[get_ver_detalle_cuota_use_case] = lambda: mock_ver_detalle_cuota_use_case

    # Act
    response = app_client.get(f"/cuotas/{cuota_id}")

    # Assert
    assert response.status_code == 200
    # The mock returns a dict, so compare directly
    assert response.json()["cuota"]["id"] == str(mock_ver_detalle_cuota_use_case.execute.return_value["cuota"]["id"])
    assert response.json()["cuota"]["estado_pago"] == mock_ver_detalle_cuota_use_case.execute.return_value["cuota"]["estado_pago"]
    mock_ver_detalle_cuota_use_case.execute.assert_called_once_with(admin_user, cuota_id)


    # Cleanup
    app_client.app.dependency_overrides = {}

@pytest.mark.asyncio
async def test_ver_detalle_cuota_unauthorized_if_not_admin(app_client, non_admin_user_active):
    # Arrange
    cuota_id = uuid4()
    app_client.app.dependency_overrides[get_current_user] = lambda: non_admin_user_active
    
    # Act
    response = app_client.get(f"/cuotas/{cuota_id}")
    
    # Assert
    assert response.status_code == 403
    assert response.json() == {"detail": "The user doesn't have enough privileges"}
    
    # Cleanup
    app_client.app.dependency_overrides = {}

    # ------------------ Tests for RegistrarCuotaManual (Refactored) ------------------

@pytest.mark.asyncio
async def test_registrar_cuota_manual_endpoint_success(app_client, mock_registrar_cuota_manual_use_case, admin_user):
    # Arrange
    cuota_id = uuid4()
    app_client.app.dependency_overrides[get_admin_user] = lambda: admin_user
    app_client.app.dependency_overrides[get_current_user] = lambda: admin_user # Needed for get_admin_user
    app_client.app.dependency_overrides[get_registrar_cuota_manual_use_case] = lambda: mock_registrar_cuota_manual_use_case

    update_data = ActualizarCuotaManualDTO(
        importe=Decimal("75.00"),
        metodo=MetodoPago.EFECTIVO,
        notas="Pago en efectivo por el socio"
    )

    # Act
    response = app_client.put(f"/cuotas/{cuota_id}/registrar-manual", json=update_data.model_dump(mode='json'))

    # Assert
    assert response.status_code == 200
    assert response.json() == {"id": str(mock_registrar_cuota_manual_use_case.execute.return_value.id)}
    mock_registrar_cuota_manual_use_case.execute.assert_called_once_with(admin_user, cuota_id, update_data)

    # Cleanup
    app_client.app.dependency_overrides = {}

# ------------------ Tests for ObtenerGenerarMiCuota ------------------

@pytest.mark.asyncio
async def test_obtener_generar_mi_cuota_activa_endpoint_returns_existing_cuota(app_client, non_admin_user_active, mock_obtener_generar_mi_cuota_use_case, expected_cuota_dto):
    # Arrange
    app_client.app.dependency_overrides[get_current_user] = lambda: non_admin_user_active
    app_client.app.dependency_overrides[get_obtener_generar_mi_cuota_use_case] = lambda: mock_obtener_generar_mi_cuota_use_case
    mock_obtener_generar_mi_cuota_use_case.execute.return_value = expected_cuota_dto

    # Act
    response = app_client.get("/cuotas/mi-cuota-activa")

    # Assert
    assert response.status_code == 200
    assert response.json() == expected_cuota_dto.model_dump(by_alias=True, mode='json') # Ensure correct serialization
    mock_obtener_generar_mi_cuota_use_case.execute.assert_called_once_with(non_admin_user_active)

# ------------------ Tests for GenerarInformePendientes ------------------

@pytest.mark.asyncio
async def test_generar_informe_pendientes_success(app_client, admin_user, mock_generar_informe_pendientes_use_case):
    # Arrange
    app_client.app.dependency_overrides[get_current_user] = lambda: admin_user
    app_client.app.dependency_overrides[get_admin_user] = lambda: admin_user
    app_client.app.dependency_overrides[get_generar_informe_pendientes_use_case] = lambda: mock_generar_informe_pendientes_use_case

    # Act
    response = app_client.get("/cuotas/informe-pendientes")

    # Assert
    assert response.status_code == 200
    assert "pendientes" in response.json()
    mock_generar_informe_pendientes_use_case.execute.assert_called_once_with(admin_user)

    # Cleanup
    app_client.app.dependency_overrides = {}

# ------------------ Tests for ConsultarHistorialCuotas ------------------

@pytest.mark.asyncio
async def test_consultar_historial_cuotas_success(app_client, non_admin_user_active, mock_consultar_historial_cuotas_use_case):
    # Arrange
    app_client.app.dependency_overrides[get_current_user] = lambda: non_admin_user_active
    app_client.app.dependency_overrides[get_consultar_historial_cuotas_use_case] = lambda: mock_consultar_historial_cuotas_use_case
    
    mock_return = mock_consultar_historial_cuotas_use_case.execute.return_value
    expected_first_item = mock_return.historial[0]

    # Act
    response = app_client.get("/cuotas/historial")
    response_json = response.json()

    # Assert
    assert response.status_code == 200
    assert "historial" in response_json
    assert isinstance(response_json["historial"], list)
    assert len(response_json["historial"]) > 0
    
    first_item = response_json["historial"][0]
    assert first_item["id"] == str(expected_first_item.id)
    assert first_item["temporada_nombre"] == expected_first_item.temporada_nombre
    assert first_item["importe_pagado"] == str(expected_first_item.importe_pagado)
    assert first_item["estado_pago"] == expected_first_item.estado_pago.value
    
    mock_consultar_historial_cuotas_use_case.execute.assert_called_once_with(non_admin_user_active)

    # Cleanup
    app_client.app.dependency_overrides = {}