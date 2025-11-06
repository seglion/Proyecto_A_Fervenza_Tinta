import os
import pytest
from unittest.mock import AsyncMock, Mock
from uuid import UUID, uuid4
from datetime import datetime

from src.app.prendas.application.dtos import ActualizarPrendaDTO, PrendaActualizadaDTO, UsuarioPolicyDTO
from src.app.prendas.application.exceptions import NotAuthorizedError, PrendaNotFoundError
from src.app.prendas.application.use_cases.actualizar_prenda_use_case import ActualizarPrendaUseCase
from src.app.prendas.domain.entities import Prenda
from src.app.users.domain.value_objects import Rol

@pytest.fixture
def mock_prenda_repository():
    return AsyncMock()

@pytest.fixture
def mock_prenda_policy():
    return Mock()

@pytest.fixture
def admin_user_dto():
    return UsuarioPolicyDTO(rol=Rol.ADMIN, esta_activo=True)

@pytest.fixture
def non_admin_user_dto():
    return UsuarioPolicyDTO(rol=Rol.USUARIO, esta_activo=True)

@pytest.fixture
def existing_prenda():
    return Prenda(
        id=uuid4(),
        nombre="Camiseta Vieja",
        descripcion="Descripción vieja",
        precio=10.00,
        imagen_url="old_image.jpg",
        fecha_creacion=datetime.now()
    )

def test_actualizar_prenda_use_case_file_exists():
    file_path = "src/app/prendas/application/use_cases/actualizar_prenda_use_case.py"
    assert os.path.exists(file_path)
    assert os.path.isfile(file_path)

def test_actualizar_prenda_use_case_class_exists():
    from src.app.prendas.application.use_cases.actualizar_prenda_use_case import ActualizarPrendaUseCase
    assert isinstance(ActualizarPrendaUseCase, type)

def test_actualizar_prenda_use_case_execute_method_exists():
    from src.app.prendas.application.use_cases.actualizar_prenda_use_case import ActualizarPrendaUseCase
    assert hasattr(ActualizarPrendaUseCase, "execute")
    assert callable(getattr(ActualizarPrendaUseCase, "execute"))

@pytest.mark.asyncio
async def test_actualizar_prenda_use_case_execute_success(mock_prenda_repository, mock_prenda_policy, admin_user_dto, existing_prenda):
    # Arrange
    prenda_id = existing_prenda.id
    update_data = ActualizarPrendaDTO(nombre="Camiseta Nueva", precio=25.00)

    mock_prenda_policy.es_administrador.return_value = True
    mock_prenda_repository.get_by_id.return_value = existing_prenda
    mock_prenda_repository.save.return_value = existing_prenda # The updated prenda

    use_case = ActualizarPrendaUseCase(mock_prenda_repository, mock_prenda_policy)

    # Act
    result = await use_case.execute(prenda_id, update_data, admin_user_dto)

    # Assert
    mock_prenda_policy.es_administrador.assert_called_once_with(admin_user_dto)
    mock_prenda_repository.get_by_id.assert_called_once_with(prenda_id)
    mock_prenda_repository.save.assert_called_once_with(existing_prenda) # Should save the updated existing_prenda
    assert existing_prenda.nombre == update_data.nombre
    assert existing_prenda.precio == update_data.precio
    assert result == PrendaActualizadaDTO(id=prenda_id)

@pytest.mark.asyncio
async def test_actualizar_prenda_use_case_not_authorized(mock_prenda_repository, mock_prenda_policy, non_admin_user_dto):
    # Arrange
    prenda_id = uuid4()
    update_data = ActualizarPrendaDTO(nombre="Camiseta Nueva")

    mock_prenda_policy.es_administrador.return_value = False

    use_case = ActualizarPrendaUseCase(mock_prenda_repository, mock_prenda_policy)

    # Act & Assert
    with pytest.raises(NotAuthorizedError):
        await use_case.execute(prenda_id, update_data, non_admin_user_dto)

    mock_prenda_policy.es_administrador.assert_called_once_with(non_admin_user_dto)
    mock_prenda_repository.get_by_id.assert_not_called()
    mock_prenda_repository.save.assert_not_called()

@pytest.mark.asyncio
async def test_actualizar_prenda_use_case_prenda_not_found(mock_prenda_repository, mock_prenda_policy, admin_user_dto):
    # Arrange
    prenda_id = uuid4()
    update_data = ActualizarPrendaDTO(nombre="Camiseta Nueva")

    mock_prenda_policy.es_administrador.return_value = True
    mock_prenda_repository.get_by_id.return_value = None

    use_case = ActualizarPrendaUseCase(mock_prenda_repository, mock_prenda_policy)

    # Act & Assert
    with pytest.raises(PrendaNotFoundError):
        await use_case.execute(prenda_id, update_data, admin_user_dto)

    mock_prenda_policy.es_administrador.assert_called_once_with(admin_user_dto)
    mock_prenda_repository.get_by_id.assert_called_once_with(prenda_id)
    mock_prenda_repository.save.assert_not_called()