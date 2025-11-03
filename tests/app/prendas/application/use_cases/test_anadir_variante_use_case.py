import os
import pytest
from unittest.mock import AsyncMock, Mock
from uuid import UUID, uuid4
from datetime import datetime

from src.app.prendas.application.dtos import AnadirVarianteDTO, UsuarioPolicyDTO, VarianteCreadaDTO
from src.app.prendas.application.exceptions import NotAuthorizedError, PrendaNotFoundError
from src.app.prendas.application.use_cases.anadir_variante_use_case import AnadirVarianteUseCase
from src.app.prendas.domain.entities import Prenda, VariantePrenda
from src.app.prendas.domain.value_objects import GeneroPrenda, TallaPrenda
from src.app.users.domain.value_objects import Rol

@pytest.fixture
def mock_prenda_repository():
    return AsyncMock()

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
def existing_prenda():
    return Prenda(
        id=uuid4(),
        nombre="Camiseta",
        descripcion="Descripción",
        precio=10.00,
        imagen_url="image.jpg",
        fecha_creacion=datetime.now()
    )

def test_anadir_variante_use_case_file_exists():
    file_path = "src/app/prendas/application/use_cases/anadir_variante_use_case.py"
    assert os.path.exists(file_path)
    assert os.path.isfile(file_path)

def test_anadir_variante_use_case_class_exists():
    from src.app.prendas.application.use_cases.anadir_variante_use_case import AnadirVarianteUseCase
    assert isinstance(AnadirVarianteUseCase, type)

def test_anadir_variante_use_case_execute_method_exists():
    from src.app.prendas.application.use_cases.anadir_variante_use_case import AnadirVarianteUseCase
    assert hasattr(AnadirVarianteUseCase, "execute")
    assert callable(getattr(AnadirVarianteUseCase, "execute"))

@pytest.mark.asyncio
async def test_anadir_variante_use_case_execute_success(mock_prenda_repository, mock_variante_prenda_repository, mock_prenda_policy, admin_user_dto, existing_prenda):
    # Arrange
    prenda_id = existing_prenda.id
    anadir_variante_dto = AnadirVarianteDTO(genero=GeneroPrenda.HOMBRE, talla=TallaPrenda.M)

    mock_prenda_policy.es_administrador.return_value = True
    mock_prenda_repository.buscar_por_id_con_variantes.return_value = existing_prenda
    mock_variante_prenda_repository.guardar.return_value = VariantePrenda(id=uuid4(), prenda_id=prenda_id, genero=anadir_variante_dto.genero, talla=anadir_variante_dto.talla, fecha_creacion=datetime.now())

    use_case = AnadirVarianteUseCase(mock_prenda_repository, mock_variante_prenda_repository, mock_prenda_policy)

    # Act
    result = await use_case.execute(prenda_id, anadir_variante_dto, admin_user_dto)

    # Assert
    mock_prenda_policy.es_administrador.assert_called_once_with(admin_user_dto)
    mock_prenda_repository.buscar_por_id_con_variantes.assert_called_once_with(prenda_id)
    mock_variante_prenda_repository.guardar.assert_called_once()
    saved_variante = mock_variante_prenda_repository.guardar.return_value
    assert isinstance(saved_variante, VariantePrenda)
    assert saved_variante.prenda_id == prenda_id
    assert saved_variante.genero == anadir_variante_dto.genero
    assert saved_variante.talla == anadir_variante_dto.talla
    assert isinstance(result, VarianteCreadaDTO)
    assert result.id == saved_variante.id

@pytest.mark.asyncio
async def test_anadir_variante_use_case_not_authorized(mock_prenda_repository, mock_variante_prenda_repository, mock_prenda_policy, non_admin_user_dto):
    # Arrange
    prenda_id = uuid4()
    anadir_variante_dto = AnadirVarianteDTO(genero=GeneroPrenda.HOMBRE, talla=TallaPrenda.M)

    mock_prenda_policy.es_administrador.return_value = False

    use_case = AnadirVarianteUseCase(mock_prenda_repository, mock_variante_prenda_repository, mock_prenda_policy)

    # Act & Assert
    with pytest.raises(NotAuthorizedError):
        await use_case.execute(prenda_id, anadir_variante_dto, non_admin_user_dto)

    mock_prenda_policy.es_administrador.assert_called_once_with(non_admin_user_dto)
    mock_prenda_repository.buscar_por_id_con_variantes.assert_not_called()
    mock_variante_prenda_repository.guardar.assert_not_called()

@pytest.mark.asyncio
async def test_anadir_variante_use_case_prenda_not_found(mock_prenda_repository, mock_variante_prenda_repository, mock_prenda_policy, admin_user_dto):
    # Arrange
    prenda_id = uuid4()
    anadir_variante_dto = AnadirVarianteDTO(genero=GeneroPrenda.HOMBRE, talla=TallaPrenda.M)

    mock_prenda_policy.es_administrador.return_value = True
    mock_prenda_repository.buscar_por_id_con_variantes.return_value = None
    mock_variante_prenda_repository.guardar.return_value = VariantePrenda(id=uuid4(), prenda_id=prenda_id, genero=anadir_variante_dto.genero, talla=anadir_variante_dto.talla, fecha_creacion=datetime.now())

    use_case = AnadirVarianteUseCase(mock_prenda_repository, mock_variante_prenda_repository, mock_prenda_policy)

    # Act & Assert
    with pytest.raises(PrendaNotFoundError):
        await use_case.execute(prenda_id, anadir_variante_dto, admin_user_dto)

    mock_prenda_policy.es_administrador.assert_called_once_with(admin_user_dto)
    mock_prenda_repository.buscar_por_id_con_variantes.assert_called_once_with(prenda_id)
    mock_variante_prenda_repository.guardar.assert_not_called()