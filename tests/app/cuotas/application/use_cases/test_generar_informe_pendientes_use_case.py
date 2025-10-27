import pytest
from unittest.mock import AsyncMock, Mock
from uuid import uuid4

from src.app.cuotas.application.repositories.i_cuota_repository import ICuotaRepository
from src.app.cuotas.application.policies.cuota_policy import CuotaPolicy
from src.app.users.domain.entities import User
from src.app.users.domain.value_objects import Rol
from src.app.cuotas.application.dtos import InformePendientesDTO, UsuarioResponseDTO


def test_use_case_file_exists():
    try:
        from src.app.cuotas.application.use_cases import generar_informe_pendientes_use_case
    except ImportError:
        pytest.fail("El fichero del caso de uso 'generar_informe_pendientes_use_case.py' no existe.")

def test_use_case_class_exists():
    try:
        from src.app.cuotas.application.use_cases.generar_informe_pendientes_use_case import GenerarInformePendientesUseCase
    except ImportError:
        pytest.fail("La clase del caso de uso 'GenerarInformePendientesUseCase' no existe.")

@pytest.mark.asyncio
async def test_use_case_initialization():
    mock_cuota_repo = AsyncMock(spec=ICuotaRepository)
    mock_policy = Mock(spec=CuotaPolicy)
    try:
        from src.app.cuotas.application.use_cases.generar_informe_pendientes_use_case import GenerarInformePendientesUseCase
        GenerarInformePendientesUseCase(
            mock_cuota_repo,
            mock_policy
        )
    except (ImportError, TypeError) as e:
        pytest.fail(f"La inicialización de 'GenerarInformePendientesUseCase' falló: {e}")

@pytest.mark.asyncio
async def test_execute_method_exists():
    from src.app.cuotas.application.use_cases.generar_informe_pendientes_use_case import GenerarInformePendientesUseCase
    mock_cuota_repo = AsyncMock(spec=ICuotaRepository)
    mock_policy = Mock(spec=CuotaPolicy)
    use_case = GenerarInformePendientesUseCase(
        mock_cuota_repo,
        mock_policy
    )
    assert hasattr(use_case, 'execute'), "El método 'execute' no existe en el caso de uso."

@pytest.mark.asyncio
async def test_generar_informe_pendientes_success():
    from src.app.cuotas.application.use_cases.generar_informe_pendientes_use_case import GenerarInformePendientesUseCase
    mock_cuota_repo = AsyncMock(spec=ICuotaRepository)
    mock_policy = Mock(spec=CuotaPolicy)

    admin_user = User(id=uuid4(), rol=Rol.ADMIN, email="admin@example.com", contrasena_hasheada="", nombre="", apellidos="", numero_telefono="", esta_activo=True)
    temporada_id = 1
    usuarios_pendientes = [
        User(id=uuid4(), rol=Rol.USUARIO, email="user1@example.com", contrasena_hasheada="", nombre="", apellidos="", numero_telefono="", esta_activo=True),
        User(id=uuid4(), rol=Rol.USUARIO, email="user2@example.com", contrasena_hasheada="", nombre="", apellidos="", numero_telefono="", esta_activo=True)
    ]

    mock_policy.es_administrador.return_value = True
    mock_cuota_repo.get_usuarios_pendientes_por_temporada.return_value = usuarios_pendientes

    use_case = GenerarInformePendientesUseCase(mock_cuota_repo, mock_policy)
    result = await use_case.execute(admin_user, temporada_id)

    assert isinstance(result, InformePendientesDTO)
    assert len(result.pendientes) == 2
    assert isinstance(result.pendientes[0], UsuarioResponseDTO)
