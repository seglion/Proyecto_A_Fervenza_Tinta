import os
import pytest
from unittest.mock import Mock, AsyncMock
from uuid import uuid4
from datetime import datetime

from src.app.prendas.application.dtos import CrearPrendaDTO, UsuarioPolicyDTO
from src.app.prendas.application.use_cases.crear_prenda_use_case import CrearPrendaUseCase
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

def test_crear_prenda_use_case_file_exists():
    file_path = "src/app/prendas/application/use_cases/crear_prenda_use_case.py"
    assert os.path.exists(file_path)
    assert os.path.isfile(file_path)

def test_crear_prenda_use_case_class_exists():
    from src.app.prendas.application.use_cases.crear_prenda_use_case import CrearPrendaUseCase
    assert isinstance(CrearPrendaUseCase, type)

def test_crear_prenda_use_case_execute_method_exists():
    from src.app.prendas.application.use_cases.crear_prenda_use_case import CrearPrendaUseCase
    assert hasattr(CrearPrendaUseCase, "execute")
    assert callable(getattr(CrearPrendaUseCase, "execute"))

@pytest.mark.asyncio
async def test_crear_prenda_use_case_execute(mock_prenda_repository, mock_prenda_policy, admin_user_dto):
    # Arrange
    mock_prenda_policy.es_administrador.return_value = True
    
    # Mock the save method to return a Prenda instance with a UUID id
    crear_prenda_dto = CrearPrendaDTO(nombre="Camiseta", descripcion="Camiseta de algodón", precio=19.99, imagen_url="http://example.com/img.png")
    mock_prenda_repository.guardar.side_effect = lambda prenda: prenda
    use_case = CrearPrendaUseCase(mock_prenda_repository, mock_prenda_policy)

    # Act
    await use_case.execute(crear_prenda_dto, admin_user_dto)

    # Assert
    mock_prenda_policy.es_administrador.assert_called_once_with(admin_user_dto)
    mock_prenda_repository.guardar.assert_called_once()
    saved_prenda = mock_prenda_repository.guardar.call_args[0][0]
    assert isinstance(saved_prenda, Prenda)
    assert saved_prenda.nombre == crear_prenda_dto.nombre