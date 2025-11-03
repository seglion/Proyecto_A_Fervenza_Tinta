import os
import pytest
from unittest.mock import AsyncMock, Mock
from uuid import UUID, uuid4
from datetime import datetime

from src.app.prendas.application.dtos import EliminarVarianteDTO, UsuarioPolicyDTO
from src.app.prendas.application.exceptions import NotAuthorizedError, PrendaNotFoundError
from src.app.prendas.application.use_cases.eliminar_variante_use_case import EliminarVarianteUseCase
from src.app.prendas.domain.entities import VariantePrenda
from src.app.prendas.domain.value_objects import GeneroPrenda, TallaPrenda
from src.app.users.domain.value_objects import Rol

@pytest.fixture
def mock_variante_prenda_repository():
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
def existing_variante_prenda():
    return VariantePrenda(
        id=uuid4(),
        prenda_id=uuid4(),
        genero=GeneroPrenda.HOMBRE,
        talla=TallaPrenda.M,
        fecha_creacion=datetime.now()
    )

def test_eliminar_variante_use_case_file_exists():
    file_path = "src/app/prendas/application/use_cases/eliminar_variante_use_case.py"
    assert os.path.exists(file_path)
    assert os.path.isfile(file_path)

def test_eliminar_variante_use_case_class_exists():
    from src.app.prendas.application.use_cases.eliminar_variante_use_case import EliminarVarianteUseCase
    assert isinstance(EliminarVarianteUseCase, type)

def test_eliminar_variante_use_case_execute_method_exists():
    from src.app.prendas.application.use_cases.eliminar_variante_use_case import EliminarVarianteUseCase
    assert hasattr(EliminarVarianteUseCase, "execute")
    assert callable(getattr(EliminarVarianteUseCase, "execute"))

@pytest.mark.asyncio
async def test_eliminar_variante_use_case_execute_success(mock_variante_prenda_repository, mock_prenda_policy, admin_user_dto, existing_variante_prenda):
    # Arrange
    variante_id = existing_variante_prenda.id
    eliminar_variante_dto = EliminarVarianteDTO(id=variante_id)

    mock_prenda_policy.es_administrador.return_value = True
    mock_variante_prenda_repository.get_by_id.return_value = existing_variante_prenda

    use_case = EliminarVarianteUseCase(mock_variante_prenda_repository, mock_prenda_policy)

    # Act
    await use_case.execute(variante_id, admin_user_dto)

    # Assert
    mock_prenda_policy.es_administrador.assert_called_once_with(admin_user_dto)
    mock_variante_prenda_repository.get_by_id.assert_called_once_with(variante_id)
    mock_variante_prenda_repository.delete.assert_called_once_with(existing_variante_prenda)

@pytest.mark.asyncio
async def test_eliminar_variante_use_case_not_authorized(mock_variante_prenda_repository, mock_prenda_policy, non_admin_user_dto):
    # Arrange
    variante_id = uuid4()

    mock_prenda_policy.es_administrador.return_value = False

    use_case = EliminarVarianteUseCase(mock_variante_prenda_repository, mock_prenda_policy)

    # Act & Assert
    with pytest.raises(NotAuthorizedError):
        await use_case.execute(variante_id, non_admin_user_dto)

    mock_prenda_policy.es_administrador.assert_called_once_with(non_admin_user_dto)
    mock_variante_prenda_repository.get_by_id.assert_not_called()
    mock_variante_prenda_repository.delete.assert_not_called()

@pytest.mark.asyncio
async def test_eliminar_variante_use_case_variante_not_found(mock_variante_prenda_repository, mock_prenda_policy, admin_user_dto):
    # Arrange
    variante_id = uuid4()

    mock_prenda_policy.es_administrador.return_value = True
    mock_variante_prenda_repository.get_by_id.return_value = None

    use_case = EliminarVarianteUseCase(mock_variante_prenda_repository, mock_prenda_policy)

    # Act & Assert
    with pytest.raises(PrendaNotFoundError):
        await use_case.execute(variante_id, admin_user_dto)

    mock_prenda_policy.es_administrador.assert_called_once_with(admin_user_dto)
    mock_variante_prenda_repository.get_by_id.assert_called_once_with(variante_id)
    mock_variante_prenda_repository.delete.assert_not_called()