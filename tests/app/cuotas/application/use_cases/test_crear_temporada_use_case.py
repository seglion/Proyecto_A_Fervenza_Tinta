import pytest
from unittest.mock import Mock, AsyncMock
from datetime import date

from src.app.cuotas.application.use_cases.crear_temporada_use_case import CrearTemporadaUseCase
from src.app.cuotas.application.policies.cuota_policy import CuotaPolicy
from src.app.users.domain.entities import User
from src.app.users.domain.value_objects import Rol
from src.app.cuotas.application.exceptions import UnauthorizedException
from src.app.cuotas.application.dtos import CrearTemporadaDTO, TipoCuotaDTO, TemporadaCreadaDTO
from src.app.cuotas.domain.entities import TemporadaCuota

@pytest.fixture
def mock_temporada_cuota_repository():
    return Mock()

@pytest.fixture
def mock_tipo_cuota_repository():
    return Mock()

@pytest.fixture
def mock_cuota_policy():
    return Mock()

@pytest.mark.asyncio
async def test_crear_temporada_unauthorized():
    mock_policy = Mock(spec=CuotaPolicy)
    mock_policy.es_administrador.return_value = False

    use_case = CrearTemporadaUseCase(None, None, mock_policy)
    
    regular_user = User(rol=Rol.USUARIO, email="user@example.com", contrasena_hasheada="", nombre="", apellidos="", numero_telefono="", esta_activo=True)

    with pytest.raises(UnauthorizedException):
        await use_case.execute(regular_user, None)

@pytest.mark.asyncio
async def test_crear_temporada_success():
    mock_policy = Mock(spec=CuotaPolicy)
    mock_policy.es_administrador.return_value = True

    mock_temporada_repo = AsyncMock()
    mock_temporada_repo.guardar_temporada.return_value = TemporadaCuota(id=1, nombre_temporada="", fecha_inicio=date.today(), fecha_fin=date.today(), fecha_creacion=date.today())

    mock_tipo_cuota_repo = AsyncMock()

    use_case = CrearTemporadaUseCase(mock_temporada_repo, mock_tipo_cuota_repo, mock_policy)

    admin_user = User(rol=Rol.ADMIN, email="admin@example.com", contrasena_hasheada="", nombre="", apellidos="", numero_telefono="", esta_activo=True)
    
    tipos_cuota_dto = [TipoCuotaDTO(nombre="General", importe=50)]
    crear_temporada_dto = CrearTemporadaDTO(nombre_temporada="2025-2026", fecha_inicio=date(2025, 9, 1), fecha_fin=date(2026, 6, 30), tipos_cuota=tipos_cuota_dto)

    result = await use_case.execute(admin_user, crear_temporada_dto)

    mock_temporada_repo.guardar_temporada.assert_called_once()
    mock_tipo_cuota_repo.guardar_varios.assert_called_once()
    assert isinstance(result, TemporadaCreadaDTO)
    assert result.id == 1