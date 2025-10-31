import pytest
from unittest.mock import AsyncMock
from uuid import uuid4
from datetime import date, datetime
from decimal import Decimal

from src.app.cuotas.application.use_cases.obtener_generar_mi_cuota_use_case import ObtenerGenerarMiCuotaUseCase
from src.app.cuotas.application.repositories.i_cuota_repository import ICuotaRepository
from src.app.cuotas.application.repositories.i_tipo_cuota_repository import ITipoCuotaRepository
from src.app.cuotas.application.repositories.i_temporada_cuota_repository import ITemporadaCuotaRepository
from src.app.cuotas.application.policies.cuota_policy import CuotaPolicy
from src.app.users.domain.entities import User
from src.app.users.domain.value_objects import Rol
from src.app.cuotas.domain.entities import Cuota, TemporadaCuota, TipoCuota
from src.app.cuotas.domain.value_objects import EstadoPago, MetodoPago, NombreTipoCuota
from src.app.cuotas.application.dtos import CuotaDTO
from src.app.cuotas.application.exceptions import TemporadaNoEncontrada, TipoCuotaNoEncontrado

@pytest.fixture
def mock_cuota_repository():
    return AsyncMock(spec=ICuotaRepository)

@pytest.fixture
def mock_tipo_cuota_repository():
    return AsyncMock(spec=ITipoCuotaRepository)

@pytest.fixture
def mock_temporada_cuota_repository():
    return AsyncMock(spec=ITemporadaCuotaRepository)

@pytest.fixture
def mock_cuota_policy():
    mock = AsyncMock(spec=CuotaPolicy)
    mock.es_administrador.return_value = False # Este UC es para usuarios normales
    return mock

@pytest.fixture
def user_registrado():
    return User(
        id=uuid4(),
        email="user@example.com",
        contrasena_hasheada="hashed_password",
        nombre="Test",
        apellidos="User",
        numero_telefono="123456789",
        rol=Rol.USUARIO,
        esta_activo=True,
        email_verificado=True,
        aprobado_por_admin=True
    )

@pytest.fixture
def temporada_activa():
    return TemporadaCuota(
        id=1,
        nombre_temporada="2025-2026",
        fecha_inicio=date(2025, 10, 1),
        fecha_fin=date(2026, 7, 25),
        fecha_creacion=datetime.now()
    )

@pytest.fixture
def cuota_existente(user_registrado, temporada_activa):
    return Cuota(
        id=uuid4(),
        usuario_id=user_registrado.id,
        tipo_de_cuota_id=1,
        importe_pagado=Decimal("50.00"),
        estado_pago=EstadoPago.PENDIENTE,
        fecha_pago=datetime.now(), # Asignar un valor concreto
        metodo_pago=MetodoPago.STRIPE, # Asignar un valor concreto
        id_transaccion_externa="existing_transaction_id", # Asignar un valor concreto
        notas_admin="existing_notes", # Asignar un valor concreto
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
        importe=Decimal("50.00"),
        fecha_creacion=datetime.now()
    )

@pytest.mark.asyncio
async def test_obtener_generar_mi_cuota_use_case_returns_cuota_dto_on_pass(
    mock_cuota_repository,
    mock_tipo_cuota_repository,
    mock_temporada_cuota_repository,
    mock_cuota_policy,
    user_registrado,
    temporada_activa,
    tipo_cuota_general
):
    # Arrange
    mock_temporada_cuota_repository.get_temporada_activa.return_value = temporada_activa
    mock_cuota_repository.buscar_cualquier_cuota_por_usuario_y_temporada.return_value = None
    mock_cuota_repository.ha_pagado_cuota_alta_antes.return_value = True
    mock_tipo_cuota_repository.get_tipo_cuota_general.return_value = tipo_cuota_general
    
    generated_cuota = Cuota(
        id=uuid4(),
        usuario_id=user_registrado.id,
        tipo_de_cuota_id=tipo_cuota_general.id,
        importe_pagado=tipo_cuota_general.importe,
        estado_pago=EstadoPago.PENDIENTE,
        fecha_creacion=datetime.now()
    )
    mock_cuota_repository.guardar.return_value = generated_cuota

    use_case = ObtenerGenerarMiCuotaUseCase(
        cuota_repository=mock_cuota_repository,
        tipo_cuota_repository=mock_tipo_cuota_repository,
        temporada_cuota_repository=mock_temporada_cuota_repository,
        cuota_policy=mock_cuota_policy,
    )

    # Act
    result = await use_case.execute(user_registrado)

    # Assert
    assert isinstance(result, CuotaDTO)
    assert result.estado_pago == EstadoPago.PENDIENTE
    assert result.tipo_de_cuota_id == tipo_cuota_general.id
    assert result.importe_pagado == tipo_cuota_general.importe
    mock_temporada_cuota_repository.get_temporada_activa.assert_called_once()
    mock_cuota_repository.buscar_cualquier_cuota_por_usuario_y_temporada.assert_called_once_with(
        user_registrado.id, temporada_activa.id
    )
    mock_cuota_repository.ha_pagado_cuota_alta_antes.assert_called_once_with(user_registrado.id)
    mock_tipo_cuota_repository.get_tipo_cuota_general.assert_called_once_with(temporada_activa.id)
    mock_cuota_repository.guardar.assert_called_once()

@pytest.mark.asyncio
async def test_obtener_generar_mi_cuota_use_case_raises_exception_if_no_active_season(
    mock_cuota_repository,
    mock_tipo_cuota_repository,
    mock_temporada_cuota_repository,
    mock_cuota_policy,
    user_registrado
):
    # Arrange
    mock_temporada_cuota_repository.get_temporada_activa.return_value = None

    use_case = ObtenerGenerarMiCuotaUseCase(
        cuota_repository=mock_cuota_repository,
        tipo_cuota_repository=mock_tipo_cuota_repository,
        temporada_cuota_repository=mock_temporada_cuota_repository,
        cuota_policy=mock_cuota_policy,
    )

    # Act & Assert
    with pytest.raises(TemporadaNoEncontrada, match="No hay temporada activa en este momento."):
        await use_case.execute(user_registrado)

    mock_temporada_cuota_repository.get_temporada_activa.assert_called_once()
    mock_cuota_repository.buscar_cualquier_cuota_por_usuario_y_temporada.assert_not_called()
    mock_cuota_repository.guardar.assert_not_called()

@pytest.mark.asyncio
async def test_obtener_generar_mi_cuota_use_case_returns_existing_cuota_if_found(
    mock_cuota_repository,
    mock_tipo_cuota_repository,
    mock_temporada_cuota_repository,
    mock_cuota_policy,
    user_registrado,
    temporada_activa,
    cuota_existente
):
    # Arrange
    mock_temporada_cuota_repository.get_temporada_activa.return_value = temporada_activa
    mock_cuota_repository.buscar_cualquier_cuota_por_usuario_y_temporada.return_value = cuota_existente

    use_case = ObtenerGenerarMiCuotaUseCase(
        cuota_repository=mock_cuota_repository,
        tipo_cuota_repository=mock_tipo_cuota_repository,
        temporada_cuota_repository=mock_temporada_cuota_repository,
        cuota_policy=mock_cuota_policy,
    )

    # Act
    result = await use_case.execute(user_registrado)

    # Assert
    assert result.id == cuota_existente.id
    assert result.estado_pago == cuota_existente.estado_pago
    mock_temporada_cuota_repository.get_temporada_activa.assert_called_once()
    mock_cuota_repository.buscar_cualquier_cuota_por_usuario_y_temporada.assert_called_once_with(
        user_registrado.id, temporada_activa.id
    )
    mock_cuota_repository.guardar.assert_not_called()

@pytest.mark.asyncio
async def test_obtener_generar_mi_cuota_use_case_generates_general_cuota_for_old_member_if_not_found(
    mock_cuota_repository,
    mock_tipo_cuota_repository,
    mock_temporada_cuota_repository,
    mock_cuota_policy,
    user_registrado,
    temporada_activa,
    tipo_cuota_general
):
    # Arrange
    mock_temporada_cuota_repository.get_temporada_activa.return_value = temporada_activa
    mock_cuota_repository.buscar_cualquier_cuota_por_usuario_y_temporada.return_value = None
    mock_cuota_repository.ha_pagado_cuota_alta_antes.return_value = True # Es socio antiguo
    mock_tipo_cuota_repository.get_tipo_cuota_general.return_value = tipo_cuota_general
    
    generated_cuota = Cuota(
        id=uuid4(),
        usuario_id=user_registrado.id,
        tipo_de_cuota_id=tipo_cuota_general.id,
        importe_pagado=tipo_cuota_general.importe,
        estado_pago=EstadoPago.PENDIENTE,
        fecha_creacion=datetime.now()
    )
    mock_cuota_repository.guardar.return_value = generated_cuota

    use_case = ObtenerGenerarMiCuotaUseCase(
        cuota_repository=mock_cuota_repository,
        tipo_cuota_repository=mock_tipo_cuota_repository,
        temporada_cuota_repository=mock_temporada_cuota_repository,
        cuota_policy=mock_cuota_policy,
    )

    # Act
    result = await use_case.execute(user_registrado)

    # Assert
    assert isinstance(result, CuotaDTO)
    assert result.estado_pago == EstadoPago.PENDIENTE
    assert result.tipo_de_cuota_id == tipo_cuota_general.id
    assert result.importe_pagado == tipo_cuota_general.importe
    mock_temporada_cuota_repository.get_temporada_activa.assert_called_once()
    mock_cuota_repository.buscar_cualquier_cuota_por_usuario_y_temporada.assert_called_once_with(
        user_registrado.id, temporada_activa.id
    )
    mock_cuota_repository.ha_pagado_cuota_alta_antes.assert_called_once_with(user_registrado.id)
    mock_tipo_cuota_repository.get_tipo_cuota_general.assert_called_once_with(temporada_activa.id)
    mock_cuota_repository.guardar.assert_called_once()

@pytest.mark.asyncio
async def test_obtener_generar_mi_cuota_use_case_generates_new_member_cuota_if_not_found(
    mock_cuota_repository,
    mock_tipo_cuota_repository,
    mock_temporada_cuota_repository,
    mock_cuota_policy,
    user_registrado,
    temporada_activa,
    tipo_cuota_nuevo_socio
):
    # Arrange
    mock_temporada_cuota_repository.get_temporada_activa.return_value = temporada_activa
    mock_cuota_repository.buscar_cualquier_cuota_por_usuario_y_temporada.return_value = None
    mock_cuota_repository.ha_pagado_cuota_alta_antes.return_value = False # Es socio nuevo
    mock_tipo_cuota_repository.get_tipo_cuota_nuevo_socio.return_value = tipo_cuota_nuevo_socio
    
    generated_cuota = Cuota(
        id=uuid4(),
        usuario_id=user_registrado.id,
        tipo_de_cuota_id=tipo_cuota_nuevo_socio.id,
        importe_pagado=tipo_cuota_nuevo_socio.importe,
        estado_pago=EstadoPago.PENDIENTE,
        fecha_creacion=datetime.now()
    )
    mock_cuota_repository.guardar.return_value = generated_cuota

    use_case = ObtenerGenerarMiCuotaUseCase(
        cuota_repository=mock_cuota_repository,
        tipo_cuota_repository=mock_tipo_cuota_repository,
        temporada_cuota_repository=mock_temporada_cuota_repository,
        cuota_policy=mock_cuota_policy,
    )

    # Act
    result = await use_case.execute(user_registrado)

    # Assert
    assert isinstance(result, CuotaDTO)
    assert result.estado_pago == EstadoPago.PENDIENTE
    assert result.tipo_de_cuota_id == tipo_cuota_nuevo_socio.id
    assert result.importe_pagado == tipo_cuota_nuevo_socio.importe
    mock_temporada_cuota_repository.get_temporada_activa.assert_called_once()
    mock_cuota_repository.buscar_cualquier_cuota_por_usuario_y_temporada.assert_called_once_with(
        user_registrado.id, temporada_activa.id
    )
    mock_cuota_repository.ha_pagado_cuota_alta_antes.assert_called_once_with(user_registrado.id)
    mock_tipo_cuota_repository.get_tipo_cuota_nuevo_socio.assert_called_once_with(temporada_activa.id)
    mock_cuota_repository.guardar.assert_called_once()