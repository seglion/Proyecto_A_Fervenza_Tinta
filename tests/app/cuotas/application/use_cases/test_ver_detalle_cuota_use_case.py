import pytest
from unittest.mock import AsyncMock, Mock
from uuid import uuid4
from datetime import datetime, date

from src.app.cuotas.application.use_cases.ver_detalle_cuota_use_case import VerDetalleCuotaUseCase
from src.app.cuotas.application.repositories.i_cuota_repository import ICuotaRepository
from src.app.cuotas.application.repositories.i_tipo_cuota_repository import ITipoCuotaRepository
from src.app.cuotas.application.repositories.i_temporada_cuota_repository import ITemporadaCuotaRepository
from src.app.users.application.repositories.i_user_repository import IUserRepository
from src.app.cuotas.application.policies.cuota_policy import CuotaPolicy
from src.app.users.domain.entities import User
from src.app.users.domain.value_objects import Rol
from src.app.cuotas.domain.entities import Cuota, TipoCuota, TemporadaCuota
from src.app.cuotas.application.dtos import DetalleCuotaDTO

@pytest.mark.asyncio
async def test_use_case_initialization():
    mock_cuota_repo = AsyncMock(spec=ICuotaRepository)
    mock_tipo_cuota_repo = AsyncMock(spec=ITipoCuotaRepository)
    mock_temporada_cuota_repo = AsyncMock(spec=ITemporadaCuotaRepository)
    mock_usuario_repo = AsyncMock(spec=IUserRepository)
    mock_policy = Mock(spec=CuotaPolicy)
    try:
        VerDetalleCuotaUseCase(
            cuota_repository=mock_cuota_repo,
            tipo_cuota_repository=mock_tipo_cuota_repo,
            temporada_cuota_repository=mock_temporada_cuota_repo,
            usuario_repository=mock_usuario_repo,
            cuota_policy=mock_policy
        )
    except (ImportError, TypeError) as e:
        pytest.fail(f"La inicialización de 'VerDetalleCuotaUseCase' falló: {e}")

@pytest.mark.asyncio
async def test_execute_method_exists():
    mock_cuota_repo = AsyncMock(spec=ICuotaRepository)
    mock_tipo_cuota_repo = AsyncMock(spec=ITipoCuotaRepository)
    mock_temporada_cuota_repo = AsyncMock(spec=ITemporadaCuotaRepository)
    mock_usuario_repo = AsyncMock(spec=IUserRepository)
    mock_policy = Mock(spec=CuotaPolicy)
    use_case = VerDetalleCuotaUseCase(
        cuota_repository=mock_cuota_repo,
        tipo_cuota_repository=mock_tipo_cuota_repo,
        temporada_cuota_repository=mock_temporada_cuota_repo,
        usuario_repository=mock_usuario_repo,
        cuota_policy=mock_policy
    )
    assert hasattr(use_case, 'execute'), "El método 'execute' no existe en el caso de uso."

@pytest.mark.asyncio
async def test_ver_detalle_cuota_success():
    mock_cuota_repo = AsyncMock(spec=ICuotaRepository)
    mock_tipo_cuota_repo = AsyncMock(spec=ITipoCuotaRepository)
    mock_temporada_cuota_repo = AsyncMock(spec=ITemporadaCuotaRepository)
    mock_usuario_repo = AsyncMock(spec=IUserRepository)
    mock_policy = Mock(spec=CuotaPolicy)

    admin_user = User(id=uuid4(), rol=Rol.ADMIN, email="admin@example.com", contrasena_hasheada="", nombre="", apellidos="", numero_telefono="", esta_activo=True)
    cuota_id = uuid4()
    usuario_id = uuid4()
    tipo_cuota_id = 1
    temporada_id = 1

    cuota_existente = Cuota(id=cuota_id, usuario_id=usuario_id, tipo_de_cuota_id=tipo_cuota_id, importe_pagado=50, estado_pago="completado", fecha_creacion=datetime.now())
    usuario_existente = User(id=usuario_id, rol=Rol.USUARIO, email="user@example.com", contrasena_hasheada="", nombre="Test", apellidos="User", numero_telefono="", esta_activo=True)
    tipo_cuota_existente = TipoCuota(id=tipo_cuota_id, temporada_id=temporada_id, nombre="General", importe=50, fecha_creacion=datetime.now())
    temporada_existente = TemporadaCuota(id=temporada_id, nombre_temporada="2025-2026", fecha_inicio=date.today(), fecha_fin=date.today(), fecha_creacion=datetime.now())

    mock_policy.es_administrador.return_value = True
    mock_cuota_repo.buscar_por_id.return_value = cuota_existente
    mock_usuario_repo.buscar_por_id.return_value = usuario_existente
    mock_tipo_cuota_repo.buscar_por_id.return_value = tipo_cuota_existente
    mock_temporada_cuota_repo.buscar_por_id.return_value = temporada_existente

    use_case = VerDetalleCuotaUseCase(
        cuota_repository=mock_cuota_repo,
        tipo_cuota_repository=mock_tipo_cuota_repo,
        temporada_cuota_repository=mock_temporada_cuota_repo,
        usuario_repository=mock_usuario_repo,
        cuota_policy=mock_policy
    )

    result = await use_case.execute(admin_user, cuota_id)

    assert isinstance(result, DetalleCuotaDTO)
    assert result.cuota.id == cuota_id
    assert result.usuario_detalle.id == usuario_id
    assert result.tipo_cuota_detalle.id == tipo_cuota_id
    assert result.temporada.id == temporada_id
