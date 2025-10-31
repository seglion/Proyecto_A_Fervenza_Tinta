import pytest
from unittest.mock import AsyncMock, Mock
from uuid import uuid4
from datetime import datetime, date

from src.app.cuotas.application.repositories.i_cuota_repository import ICuotaRepository
from src.app.cuotas.application.repositories.i_tipo_cuota_repository import ITipoCuotaRepository
from src.app.cuotas.application.repositories.i_temporada_cuota_repository import ITemporadaCuotaRepository
from src.app.cuotas.application.policies.cuota_policy import CuotaPolicy
from src.app.users.domain.entities import User
from src.app.users.domain.value_objects import Rol
from src.app.cuotas.domain.entities import Cuota, TipoCuota, TemporadaCuota
from src.app.cuotas.domain.value_objects import EstadoPago, NombreTipoCuota # Importar NombreTipoCuota
from src.app.cuotas.application.dtos import HistorialCuotasDTO, CuotaDTO, CuotaDetalleResponseDTO
from src.app.cuotas.application.exceptions import UnauthorizedException
from src.app.cuotas.application.dtos import UsuarioPolicyDTO
from src.app.cuotas.application.use_cases.consultar_historial_cuotas_use_case import ConsultarHistorialCuotasUseCase

def test_use_case_file_exists():
    try:
        from src.app.cuotas.application.use_cases import consultar_historial_cuotas_use_case
    except ImportError:
        pytest.fail("El fichero del caso de uso 'consultar_historial_cuotas_use_case.py' no existe.")

def test_use_case_class_exists():
    try:
        from src.app.cuotas.application.use_cases.consultar_historial_cuotas_use_case import ConsultarHistorialCuotasUseCase
    except ImportError:
        pytest.fail("La clase del caso de uso 'ConsultarHistorialCuotasUseCase' no existe.")

@pytest.mark.asyncio
async def test_use_case_initialization():
    mock_cuota_repo = AsyncMock(spec=ICuotaRepository)
    mock_tipo_cuota_repo = AsyncMock(spec=ITipoCuotaRepository)
    mock_temporada_repo = AsyncMock(spec=ITemporadaCuotaRepository)
    mock_policy = Mock(spec=CuotaPolicy)
    try:
        ConsultarHistorialCuotasUseCase(
            cuota_repository=mock_cuota_repo,
            tipo_cuota_repository=mock_tipo_cuota_repo,
            temporada_cuota_repository=mock_temporada_repo,
            cuota_policy=mock_policy
        )
    except (ImportError, TypeError) as e:
        pytest.fail(f"La inicialización de 'ConsultarHistorialCuotasUseCase' falló: {e}")

@pytest.mark.asyncio
async def test_execute_method_exists():
    mock_cuota_repo = AsyncMock(spec=ICuotaRepository)
    mock_tipo_cuota_repo = AsyncMock(spec=ITipoCuotaRepository)
    mock_temporada_repo = AsyncMock(spec=ITemporadaCuotaRepository)
    mock_policy = Mock(spec=CuotaPolicy)
    use_case = ConsultarHistorialCuotasUseCase(
        cuota_repository=mock_cuota_repo,
        tipo_cuota_repository=mock_tipo_cuota_repo,
        temporada_cuota_repository=mock_temporada_repo,
        cuota_policy=mock_policy
    )
    assert hasattr(use_case, 'execute'), "El método 'execute' no existe en el caso de uso."

@pytest.mark.asyncio
async def test_consultar_historial_cuotas_success():
    # 1. Arrange
    mock_cuota_repo = AsyncMock(spec=ICuotaRepository)
    mock_tipo_cuota_repo = AsyncMock(spec=ITipoCuotaRepository)
    mock_temporada_repo = AsyncMock(spec=ITemporadaCuotaRepository)
    mock_policy = Mock(spec=CuotaPolicy)

    user_id = uuid4()
    user = User(id=user_id, rol=Rol.USUARIO, email="user@example.com", contrasena_hasheada="", nombre="Test", apellidos="User", numero_telefono="", esta_activo=True)
    
    tipo_cuota_id = 1
    temporada_id = 2024

    # Mock data from repos
    cuota_db = Cuota(id=uuid4(), usuario_id=user_id, tipo_de_cuota_id=tipo_cuota_id, importe_pagado=50, estado_pago=EstadoPago.COMPLETADO, fecha_creacion=datetime.now())
    tipo_cuota_db = TipoCuota(id=tipo_cuota_id, nombre=NombreTipoCuota.SOCIO, importe=50, temporada_id=temporada_id, fecha_creacion=datetime.now())
    temporada_db = TemporadaCuota(id=temporada_id, nombre_temporada="Temporada 2024", fecha_inicio=date(2024,1,1), fecha_fin=date(2024,12,31), fecha_creacion=datetime.now())

    mock_policy.puede_consultar_historial.return_value = True
    mock_cuota_repo.buscar_por_usuario_id.return_value = [cuota_db]
    mock_tipo_cuota_repo.buscar_por_id.return_value = tipo_cuota_db
    mock_temporada_repo.buscar_por_id.return_value = temporada_db

    use_case = ConsultarHistorialCuotasUseCase(
        cuota_repository=mock_cuota_repo,
        tipo_cuota_repository=mock_tipo_cuota_repo,
        temporada_cuota_repository=mock_temporada_repo,
        cuota_policy=mock_policy
    )
    
    # 2. Act
    result = await use_case.execute(user)

    # 3. Assert
    assert isinstance(result, HistorialCuotasDTO)
    assert len(result.historial) == 1
    
    detalle_dto = result.historial[0]
    assert isinstance(detalle_dto, CuotaDetalleResponseDTO)
    assert detalle_dto.id == cuota_db.id
    assert detalle_dto.tipo_cuota_nombre == tipo_cuota_db.nombre.value # Usar .value
    assert detalle_dto.temporada_nombre == temporada_db.nombre_temporada
    assert detalle_dto.usuario_nombre == user.nombre
    assert detalle_dto.usuario_apellidos == user.apellidos

    mock_cuota_repo.buscar_por_usuario_id.assert_called_once_with(user_id)
    mock_tipo_cuota_repo.buscar_por_id.assert_called_once_with(tipo_cuota_id)
    mock_temporada_repo.buscar_por_id.assert_called_once_with(temporada_id)

@pytest.mark.asyncio
async def test_consultar_historial_cuotas_unauthorized():
    mock_cuota_repo = AsyncMock(spec=ICuotaRepository)
    mock_tipo_cuota_repo = AsyncMock(spec=ITipoCuotaRepository)
    mock_temporada_repo = AsyncMock(spec=ITemporadaCuotaRepository)
    mock_policy = Mock(spec=CuotaPolicy)

    user = User(id=uuid4(), rol=Rol.USUARIO, email="user@example.com", contrasena_hasheada="", nombre="", apellidos="", numero_telefono="", esta_activo=False) # Inactive user

    mock_policy.puede_consultar_historial.return_value = False

    use_case = ConsultarHistorialCuotasUseCase(
        cuota_repository=mock_cuota_repo,
        tipo_cuota_repository=mock_tipo_cuota_repo,
        temporada_cuota_repository=mock_temporada_repo,
        cuota_policy=mock_policy
    )

    with pytest.raises(UnauthorizedException, match="No tienes permiso para consultar el historial de cuotas."):
        await use_case.execute(user)

    mock_policy.puede_consultar_historial.assert_called_once_with(UsuarioPolicyDTO(rol=user.rol.value, esta_activo=user.esta_activo))
    mock_cuota_repo.buscar_por_usuario_id.assert_not_called()
