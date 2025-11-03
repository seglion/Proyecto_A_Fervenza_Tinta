import os
from app.prendas.application.use_cases.eliminar_prenda_use_case import EliminarPrendaUseCase
from app.prendas.domain.entities import Prenda
from app.users.domain.value_objects import Rol
import pytest
from unittest.mock import AsyncMock, Mock
from uuid import UUID, uuid4
from datetime import datetime

from src.app.prendas.application.dtos import EliminarPrendaDTO, UsuarioPolicyDTO
from src.app.prendas.application.exceptions import NotAuthorizedError, PrendaNotFoundError
from src.app.prendas.application.policies.prenda_policy import PrendaPolicy
from src.app.prendas.application.repositories.i_prenda_repository import IPrendaRepository
from src.app.users.domain.entities import User # Importar User


@pytest.fixture
def mock_prenda_repository():
    return AsyncMock()

@pytest.fixture
def mock_prenda_policy():
    return Mock()

@pytest.fixture
def admin_user_dto():
    return UsuarioPolicyDTO(rol=Rol.ADMIN.value, esta_activo=True)

@pytest.fixture
def non_admin_user_dto():
    return UsuarioPolicyDTO(rol=Rol.USUARIO.value, esta_activo=True)

from src.app.prendas.domain.value_objects import TallaPrenda, GeneroPrenda
from src.app.prendas.domain.entities import VariantePrenda

@pytest.fixture
def existing_prenda():
    prenda_id = uuid4()
    variante_id = uuid4()
    return Prenda(
        id=prenda_id,
        nombre="Camiseta",
        descripcion="Descripción",
        precio=10.00,
        imagen_url="image.jpg",
        fecha_creacion=datetime.now(),
        variantes=[
            VariantePrenda(
                id=variante_id,
                prenda_id=prenda_id,
                talla=TallaPrenda.M,
                genero=GeneroPrenda.HOMBRE,
                fecha_creacion=datetime.now()
            )
        ]
    )

def test_eliminar_prenda_use_case_file_exists():
    file_path = "src/app/prendas/application/use_cases/eliminar_prenda_use_case.py"
    assert os.path.exists(file_path)
    assert os.path.isfile(file_path)

def test_eliminar_prenda_use_case_class_exists():
    from src.app.prendas.application.use_cases.eliminar_prenda_use_case import EliminarPrendaUseCase
    assert isinstance(EliminarPrendaUseCase, type)

def test_eliminar_prenda_use_case_execute_method_exists():
    from src.app.prendas.application.use_cases.eliminar_prenda_use_case import EliminarPrendaUseCase
    assert hasattr(EliminarPrendaUseCase, "execute")
    assert callable(getattr(EliminarPrendaUseCase, "execute"))

@pytest.mark.asyncio
async def test_eliminar_prenda_use_case_execute_success(mock_prenda_repository, mock_prenda_policy, admin_user_dto, existing_prenda):
    # Arrange
    prenda_id = existing_prenda.id

    mock_prenda_policy.es_administrador.return_value = True
    mock_prenda_repository.buscar_por_id_con_variantes.return_value = existing_prenda

    use_case = EliminarPrendaUseCase(mock_prenda_repository, mock_prenda_policy)

    # Act
    await use_case.execute(prenda_id, admin_user_dto)

    # Assert
    mock_prenda_policy.es_administrador.assert_called_once_with(admin_user_dto)
    mock_prenda_repository.buscar_por_id_con_variantes.assert_called_once_with(prenda_id)
    mock_prenda_repository.eliminar_por_id.assert_called_once_with(prenda_id)
    mock_prenda_repository.buscar_por_id_con_variantes.return_value = None
    assert await mock_prenda_repository.buscar_por_id_con_variantes(prenda_id) is None

@pytest.mark.asyncio
async def test_eliminar_prenda_use_case_not_authorized(mock_prenda_repository, mock_prenda_policy, non_admin_user_dto):
    # Arrange
    prenda_id = uuid4()

    mock_prenda_policy.es_administrador.return_value = False

    use_case = EliminarPrendaUseCase(mock_prenda_repository, mock_prenda_policy)

    # Act & Assert
    with pytest.raises(NotAuthorizedError):
        await use_case.execute(prenda_id, non_admin_user_dto)

    mock_prenda_policy.es_administrador.assert_called_once_with(non_admin_user_dto)
    mock_prenda_repository.buscar_por_id_con_variantes.assert_not_called()
    mock_prenda_repository.eliminar_por_id.assert_not_called()

@pytest.mark.asyncio
async def test_eliminar_prenda_use_case_prenda_not_found(mock_prenda_repository, mock_prenda_policy, admin_user_dto):
    # Arrange
    prenda_id = uuid4()

    mock_prenda_policy.es_administrador.return_value = True
    mock_prenda_repository.buscar_por_id_con_variantes.return_value = None

    use_case = EliminarPrendaUseCase(mock_prenda_repository, mock_prenda_policy)

    # Act & Assert
    with pytest.raises(PrendaNotFoundError):
        await use_case.execute(prenda_id, admin_user_dto)

    mock_prenda_policy.es_administrador.assert_called_once_with(admin_user_dto)
    mock_prenda_repository.buscar_por_id_con_variantes.assert_called_once_with(prenda_id)
    mock_prenda_repository.eliminar_por_id.assert_not_called()