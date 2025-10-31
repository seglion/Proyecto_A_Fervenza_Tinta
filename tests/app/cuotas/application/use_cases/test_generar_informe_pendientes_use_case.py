import pytest
from unittest.mock import AsyncMock, call
from uuid import uuid4
from datetime import date, datetime
from decimal import Decimal

from src.app.cuotas.application.use_cases.generar_informe_pendientes_use_case import GenerarInformePendientesUseCase
from src.app.cuotas.application.repositories.i_cuota_repository import ICuotaRepository
from src.app.cuotas.application.repositories.i_temporada_cuota_repository import ITemporadaCuotaRepository
from src.app.cuotas.application.repositories.i_tipo_cuota_repository import ITipoCuotaRepository
from src.app.users.application.repositories.i_user_repository import IUserRepository
from src.app.cuotas.application.policies.cuota_policy import CuotaPolicy
from src.app.users.domain.entities import User
from src.app.users.domain.value_objects import Rol
from src.app.cuotas.domain.entities import Cuota, TemporadaCuota, TipoCuota
from src.app.cuotas.domain.value_objects import EstadoPago, MetodoPago, NombreTipoCuota
from src.app.cuotas.application.dtos import InformePendientesDTO, UsuarioConCuotaPendienteDTO, CuotaDTO, UsuarioPolicyDTO
from src.app.users.application.dtos import UsuarioResponseDTO
from src.app.cuotas.application.exceptions import UnauthorizedException, TemporadaNoEncontrada, TipoCuotaNoEncontrado

# --- Fixtures --- #
@pytest.fixture
def mock_cuota_repository():
    return AsyncMock(spec=ICuotaRepository)

@pytest.fixture
def mock_temporada_cuota_repository():
    return AsyncMock(spec=ITemporadaCuotaRepository)

@pytest.fixture
def mock_tipo_cuota_repository():
    return AsyncMock(spec=ITipoCuotaRepository)

@pytest.fixture
def mock_user_repository():
    return AsyncMock(spec=IUserRepository)

@pytest.fixture
def mock_cuota_policy():
    return AsyncMock(spec=CuotaPolicy)

@pytest.fixture
def admin_user():
    return User(id=uuid4(), email="admin@test.com", contrasena_hasheada="hashed", nombre="Admin", apellidos="User", numero_telefono="123", rol=Rol.ADMIN, esta_activo=True, email_verificado=True, aprobado_por_admin=True)

@pytest.fixture
def non_admin_user():
    return User(id=uuid4(), email="user@test.com", contrasena_hasheada="hashed", nombre="Normal", apellidos="User", numero_telefono="123", rol=Rol.USUARIO, esta_activo=True, email_verificado=True, aprobado_por_admin=True)

@pytest.fixture
def temporada_activa():
    return TemporadaCuota(
        id=1,
        nombre_temporada="2025-2026",
        fecha_inicio=date(2025, 1, 1),
        fecha_fin=date(2026, 1, 1),
        fecha_creacion=datetime.now()
    )

@pytest.fixture
def tipo_cuota_general(temporada_activa):
    return TipoCuota(
        id=10,
        temporada_id=temporada_activa.id,
        nombre=NombreTipoCuota.SOCIO,
        importe=Decimal("100.00"),
        fecha_creacion=datetime.now()
    )

@pytest.fixture
def tipo_cuota_nuevo_socio(temporada_activa):
    return TipoCuota(
        id=11,
        temporada_id=temporada_activa.id,
        nombre=NombreTipoCuota.ALTA,
        importe=Decimal("150.00"),
        fecha_creacion=datetime.now()
    )

# --- Tests --- #

@pytest.mark.asyncio
async def test_generar_informe_pendientes_use_case_unauthorized_if_not_admin(
    mock_cuota_repository,
    mock_temporada_cuota_repository,
    mock_tipo_cuota_repository,
    mock_user_repository,
    mock_cuota_policy,
    non_admin_user
):
    # Arrange
    mock_cuota_policy.es_administrador.return_value = False

    use_case = GenerarInformePendientesUseCase(
        cuota_repository=mock_cuota_repository,
        temporada_cuota_repository=mock_temporada_cuota_repository,
        tipo_cuota_repository=mock_tipo_cuota_repository,
        usuario_repository=mock_user_repository,
        cuota_policy=mock_cuota_policy,
    )

    # Act & Assert
    with pytest.raises(UnauthorizedException, match="No tienes permiso para generar informes."):
        await use_case.execute(non_admin_user)

    mock_cuota_policy.es_administrador.assert_called_once_with(
        UsuarioPolicyDTO(rol=non_admin_user.rol.value, esta_activo=non_admin_user.esta_activo)
    )
    mock_temporada_cuota_repository.get_temporada_activa.assert_not_called()

@pytest.mark.asyncio
async def test_generar_informe_pendientes_use_case_raises_exception_if_no_active_season(
    mock_cuota_repository,
    mock_temporada_cuota_repository,
    mock_tipo_cuota_repository,
    mock_user_repository,
    mock_cuota_policy,
    admin_user
):
    # Arrange
    mock_cuota_policy.es_administrador.return_value = True
    mock_temporada_cuota_repository.get_temporada_activa.return_value = None

    use_case = GenerarInformePendientesUseCase(
        cuota_repository=mock_cuota_repository,
        temporada_cuota_repository=mock_temporada_cuota_repository,
        tipo_cuota_repository=mock_tipo_cuota_repository,
        usuario_repository=mock_user_repository,
        cuota_policy=mock_cuota_policy,
    )

    # Act & Assert
    with pytest.raises(TemporadaNoEncontrada, match="No hay temporada activa en este momento."):
        await use_case.execute(admin_user)

    mock_cuota_policy.es_administrador.assert_called_once()
    mock_temporada_cuota_repository.get_temporada_activa.assert_called_once()
    mock_tipo_cuota_repository.get_tipo_cuota_general.assert_not_called()

@pytest.mark.asyncio
async def test_generar_informe_pendientes_use_case_raises_exception_if_no_general_fee_type(
    mock_cuota_repository,
    mock_temporada_cuota_repository,
    mock_tipo_cuota_repository,
    mock_user_repository,
    mock_cuota_policy,
    admin_user,
    temporada_activa
):
    # Arrange
    mock_cuota_policy.es_administrador.return_value = True
    mock_temporada_cuota_repository.get_temporada_activa.return_value = temporada_activa
    mock_tipo_cuota_repository.get_tipo_cuota_general.return_value = None

    use_case = GenerarInformePendientesUseCase(
        cuota_repository=mock_cuota_repository,
        temporada_cuota_repository=mock_temporada_cuota_repository,
        tipo_cuota_repository=mock_tipo_cuota_repository,
        usuario_repository=mock_user_repository,
        cuota_policy=mock_cuota_policy,
    )

    # Act & Assert
    with pytest.raises(TipoCuotaNoEncontrado, match="No se encontró la cuota general para la temporada activa."):
        await use_case.execute(admin_user)

    mock_cuota_policy.es_administrador.assert_called_once()
    mock_temporada_cuota_repository.get_temporada_activa.assert_called_once()
    mock_tipo_cuota_repository.get_tipo_cuota_general.assert_called_once_with(temporada_activa.id)
    mock_tipo_cuota_repository.get_tipo_cuota_nuevo_socio.assert_not_called()

@pytest.mark.asyncio
async def test_generar_informe_pendientes_use_case_raises_exception_if_no_new_member_fee_type(
    mock_cuota_repository,
    mock_temporada_cuota_repository,
    mock_tipo_cuota_repository,
    mock_user_repository,
    mock_cuota_policy,
    admin_user,
    temporada_activa,
    tipo_cuota_general
):
    # Arrange
    mock_cuota_policy.es_administrador.return_value = True
    mock_temporada_cuota_repository.get_temporada_activa.return_value = temporada_activa
    mock_tipo_cuota_repository.get_tipo_cuota_general.return_value = tipo_cuota_general
    mock_tipo_cuota_repository.get_tipo_cuota_nuevo_socio.return_value = None

    use_case = GenerarInformePendientesUseCase(
        cuota_repository=mock_cuota_repository,
        temporada_cuota_repository=mock_temporada_cuota_repository,
        tipo_cuota_repository=mock_tipo_cuota_repository,
        usuario_repository=mock_user_repository,
        cuota_policy=mock_cuota_policy,
    )

    # Act & Assert
    with pytest.raises(TipoCuotaNoEncontrado, match="No se encontró la cuota de nuevo socio para la temporada activa."):
        await use_case.execute(admin_user)

    mock_cuota_policy.es_administrador.assert_called_once()
    mock_temporada_cuota_repository.get_temporada_activa.assert_called_once()
    mock_tipo_cuota_repository.get_tipo_cuota_general.assert_called_once_with(temporada_activa.id)
    mock_tipo_cuota_repository.get_tipo_cuota_nuevo_socio.assert_called_once_with(temporada_activa.id)

@pytest.mark.asyncio
async def test_generar_informe_pendientes_use_case_generates_report_correctly(
    mock_cuota_repository,
    mock_temporada_cuota_repository,
    mock_tipo_cuota_repository,
    mock_user_repository,
    mock_cuota_policy,
    admin_user,
    temporada_activa,
    tipo_cuota_general,
    tipo_cuota_nuevo_socio
):
    # Arrange
    mock_cuota_policy.es_administrador.return_value = True
    mock_temporada_cuota_repository.get_temporada_activa.return_value = temporada_activa
    mock_tipo_cuota_repository.get_tipo_cuota_general.return_value = tipo_cuota_general
    mock_tipo_cuota_repository.get_tipo_cuota_nuevo_socio.return_value = tipo_cuota_nuevo_socio

    # Users for testing
    user1_id = uuid4()
    user2_id = uuid4()
    user3_id = uuid4()
    user4_id = uuid4()

    user1 = User(id=user1_id, email="user1@test.com", contrasena_hasheada="hashed", nombre="User1", apellidos="Test", numero_telefono="1", rol=Rol.USUARIO, esta_activo=True, email_verificado=True, aprobado_por_admin=True)
    user2 = User(id=user2_id, email="user2@test.com", contrasena_hasheada="hashed", nombre="User2", apellidos="Test", numero_telefono="2", rol=Rol.USUARIO, esta_activo=True, email_verificado=True, aprobado_por_admin=True)
    user3 = User(id=user3_id, email="user3@test.com", contrasena_hasheada="hashed", nombre="User3", apellidos="Test", numero_telefono="3", rol=Rol.USUARIO, esta_activo=True, email_verificado=True, aprobado_por_admin=True)
    user4 = User(id=user4_id, email="user4@test.com", contrasena_hasheada="hashed", nombre="User4", apellidos="Test", numero_telefono="4", rol=Rol.USUARIO, esta_activo=True, email_verificado=True, aprobado_por_admin=True)

    mock_user_repository.buscar_todos.return_value = [user1, user2, user3, user4]

    # User1: Existing pending fee
    cuota_user1 = Cuota(
        id=uuid4(), usuario_id=user1_id, tipo_de_cuota_id=tipo_cuota_general.id,
        importe_pagado=tipo_cuota_general.importe, estado_pago=EstadoPago.PENDIENTE,
        fecha_pago=None, metodo_pago=None, id_transaccion_externa=None, notas_admin=None, fecha_creacion=datetime.now()
    )
    # User4: Completed fee
    cuota_user4 = Cuota(
        id=uuid4(), usuario_id=user4_id, tipo_de_cuota_id=tipo_cuota_general.id,
        importe_pagado=tipo_cuota_general.importe, estado_pago=EstadoPago.COMPLETADO,
        fecha_pago=datetime.now(), metodo_pago=MetodoPago.EFECTIVO, id_transaccion_externa=None, notas_admin=None, fecha_creacion=datetime.now()
    )

    mock_cuota_repository.buscar_cualquier_cuota_por_usuario_y_temporada.side_effect = [
        cuota_user1, # For user1
        None,        # For user2
        None,        # For user3
        cuota_user4, # For user4
    ]

    mock_cuota_repository.ha_pagado_cuota_alta_antes.side_effect = [
        True,  # For user2
        False, # For user3
    ]

    # Side effect for guardar to return a valid Cuota object
    async def guardar_side_effect(cuota):
        return cuota

    mock_cuota_repository.guardar.side_effect = guardar_side_effect

    use_case = GenerarInformePendientesUseCase(
        cuota_repository=mock_cuota_repository,
        temporada_cuota_repository=mock_temporada_cuota_repository,
        tipo_cuota_repository=mock_tipo_cuota_repository,
        usuario_repository=mock_user_repository,
        cuota_policy=mock_cuota_policy,
    )

    # Act
    result = await use_case.execute(admin_user)

    # Assert
    assert isinstance(result, InformePendientesDTO)
    assert len(result.pendientes) == 3 # user1, user2, and user3 (user4 is completed)

    # Check user1 (existing pending)
    pending_user1 = next((p for p in result.pendientes if p.usuario.id == user1_id), None)
    assert pending_user1 is not None

    # Check user2 (newly generated general pending)
    pending_user2 = next((p for p in result.pendientes if p.usuario.id == user2_id), None)
    assert pending_user2 is not None

    # Check user3 (newly generated new member pending)
    pending_user3 = next((p for p in result.pendientes if p.usuario.id == user3_id), None)
    assert pending_user3 is not None

    # Check user4 (completed, should not be in report)
    pending_user4 = next((p for p in result.pendientes if p.usuario.id == user4_id), None)
    assert pending_user4 is None

    # Verify repository calls
    assert mock_cuota_repository.guardar.call_count == 2 # user2 and user3
