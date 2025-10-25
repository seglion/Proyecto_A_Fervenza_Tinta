import pytest
from unittest.mock import AsyncMock, Mock
from datetime import date, datetime

from src.app.cuotas.application.use_cases.actualizar_temporada_use_case import ActualizarTemporadaUseCase
from src.app.cuotas.application.policies.cuota_policy import CuotaPolicy
from src.app.users.domain.entities import User
from src.app.users.domain.value_objects import Rol
from src.app.cuotas.application.exceptions import UnauthorizedException, TemporadaNoEncontrada
from src.app.cuotas.application.dtos import ActualizarTemporadaDTO, TipoCuotaDTO, TemporadaDTO
from src.app.cuotas.domain.entities import TemporadaCuota

@pytest.mark.asyncio
async def test_actualizar_temporada_unauthorized():
    mock_policy = Mock(spec=CuotaPolicy)
    mock_policy.es_administrador.return_value = False

    use_case = ActualizarTemporadaUseCase(None, None, mock_policy)
    
    regular_user = User(rol=Rol.USUARIO, email="user@example.com", contrasena_hasheada="", nombre="", apellidos="", numero_telefono="", esta_activo=True)

    with pytest.raises(UnauthorizedException):
        await use_case.execute(regular_user, 1, None)

@pytest.mark.asyncio
async def test_actualizar_temporada_not_found():
    mock_policy = Mock(spec=CuotaPolicy)
    mock_policy.es_administrador.return_value = True

    mock_temporada_repo = AsyncMock()
    mock_temporada_repo.buscar_por_id.return_value = None

    use_case = ActualizarTemporadaUseCase(mock_temporada_repo, None, mock_policy)

    admin_user = User(rol=Rol.ADMIN, email="admin@example.com", contrasena_hasheada="", nombre="", apellidos="", numero_telefono="", esta_activo=True)

    with pytest.raises(TemporadaNoEncontrada):
        await use_case.execute(admin_user, 1, None)

@pytest.mark.asyncio
async def test_actualizar_temporada_success():
    mock_policy = Mock(spec=CuotaPolicy)
    mock_policy.es_administrador.return_value = True

    mock_temporada_repo = AsyncMock()
    mock_temporada_repo.buscar_por_id.return_value = TemporadaCuota(id=1, nombre_temporada="", fecha_inicio=date.today(), fecha_fin=date.today(), fecha_creacion=date.today())
    mock_temporada_repo.actualizar.return_value = TemporadaCuota(id=1, nombre_temporada="2025-2026", fecha_inicio=date(2025, 9, 1), fecha_fin=date(2026, 6, 30), fecha_creacion=date.today())

    mock_tipo_cuota_repo = AsyncMock()

    use_case = ActualizarTemporadaUseCase(mock_temporada_repo, mock_tipo_cuota_repo, mock_policy)

    admin_user = User(rol=Rol.ADMIN, email="admin@example.com", contrasena_hasheada="", nombre="", apellidos="", numero_telefono="", esta_activo=True)
    
    tipos_cuota_dto = [TipoCuotaDTO(id=1, nombre="General", importe=50, fecha_creacion=datetime.now())]
    actualizar_temporada_dto = ActualizarTemporadaDTO(nombre_temporada="2025-2026", fecha_inicio=date(2025, 9, 1), fecha_fin=date(2026, 6, 30), tipos_cuota=tipos_cuota_dto)

    result = await use_case.execute(admin_user, 1, actualizar_temporada_dto)

    mock_temporada_repo.actualizar.assert_called_once()
    mock_tipo_cuota_repo.actualizar_varios.assert_called_once()
    assert isinstance(result, TemporadaDTO)