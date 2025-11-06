import pytest
from unittest.mock import AsyncMock, Mock
from uuid import uuid4
from datetime import date

from src.app.cuotas.application.repositories.i_cuota_repository import ICuotaRepository
from src.app.users.application.repositories.i_user_repository import IUserRepository


def test_use_case_file_exists():
    try:
        from src.app.cuotas.application.use_cases import desactivar_socios_inactivos_use_case
    except ImportError:
        pytest.fail("El fichero del caso de uso 'desactivar_socios_inactivos_use_case.py' no existe.")

def test_use_case_class_exists():
    try:
        from src.app.cuotas.application.use_cases.desactivar_socios_inactivos_use_case import DesactivarSociosInactivosUseCase
    except ImportError:
        pytest.fail("La clase del caso de uso 'DesactivarSociosInactivosUseCase' no existe.")

@pytest.mark.asyncio
async def test_use_case_initialization():
    mock_cuota_repo = AsyncMock(spec=ICuotaRepository)
    mock_user_repo = AsyncMock(spec=IUserRepository)
    try:
        from src.app.cuotas.application.use_cases.desactivar_socios_inactivos_use_case import DesactivarSociosInactivosUseCase
        DesactivarSociosInactivosUseCase(
            mock_cuota_repo,
            mock_user_repo
        )
    except (ImportError, TypeError) as e:
        pytest.fail(f"La inicialización de 'DesactivarSociosInactivosUseCase' falló: {e}")

@pytest.mark.asyncio
async def test_execute_method_exists():
    from src.app.cuotas.application.use_cases.desactivar_socios_inactivos_use_case import DesactivarSociosInactivosUseCase
    mock_cuota_repo = AsyncMock(spec=ICuotaRepository)
    mock_user_repo = AsyncMock(spec=IUserRepository)
    use_case = DesactivarSociosInactivosUseCase(
        mock_cuota_repo,
        mock_user_repo
    )
    assert hasattr(use_case, 'execute'), "El método 'execute' no existe en el caso de uso."

@pytest.mark.asyncio
async def test_desactivar_socios_inactivos_success():
    from src.app.cuotas.application.use_cases.desactivar_socios_inactivos_use_case import DesactivarSociosInactivosUseCase
    mock_cuota_repo = AsyncMock(spec=ICuotaRepository)
    mock_user_repo = AsyncMock(spec=IUserRepository)

    fecha_limite = date(2024, 1, 1)
    usuarios_a_desactivar_ids = [uuid4(), uuid4()]

    mock_cuota_repo.get_usuarios_inactivos_desde.return_value = usuarios_a_desactivar_ids

    use_case = DesactivarSociosInactivosUseCase(mock_cuota_repo, mock_user_repo)
    await use_case.execute(fecha_limite)

    mock_cuota_repo.get_usuarios_inactivos_desde.assert_called_once_with(fecha_limite)
    mock_user_repo.desactivar_usuarios.assert_called_once_with(usuarios_a_desactivar_ids)
