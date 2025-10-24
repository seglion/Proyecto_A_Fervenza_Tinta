import pytest
from unittest.mock import AsyncMock, Mock

from src.app.cuotas.application.use_cases.listar_temporadas_use_case import ListarTemporadasUseCase
from src.app.cuotas.application.dtos import ListaTemporadasDTO
from src.app.cuotas.application.policies.cuota_policy import CuotaPolicy
from src.app.users.domain.entities import User
from src.app.users.domain.value_objects import Rol
from src.app.cuotas.application.exceptions import UnauthorizedException

@pytest.mark.asyncio
async def test_listar_temporadas_unauthorized():
    mock_policy = Mock(spec=CuotaPolicy)
    mock_policy.es_administrador.return_value = False

    use_case = ListarTemporadasUseCase(None, mock_policy)
    
    regular_user = User(rol=Rol.USUARIO, email="user@example.com", contrasena_hasheada="", nombre="", apellidos="", numero_telefono="", esta_activo=True)

    with pytest.raises(UnauthorizedException):
        await use_case.execute(regular_user)

@pytest.mark.asyncio
async def test_listar_temporadas_success():
    mock_temporada_repo = AsyncMock()
    mock_temporada_repo.listar_todas.return_value = []

    mock_policy = Mock(spec=CuotaPolicy)
    mock_policy.es_administrador.return_value = True

    use_case = ListarTemporadasUseCase(mock_temporada_repo, mock_policy)

    admin_user = User(rol=Rol.ADMIN, email="admin@example.com", contrasena_hasheada="", nombre="", apellidos="", numero_telefono="", esta_activo=True)

    result = await use_case.execute(admin_user)

    mock_temporada_repo.listar_todas.assert_called_once()
    assert isinstance(result, ListaTemporadasDTO)