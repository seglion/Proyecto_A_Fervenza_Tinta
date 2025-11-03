import os
import pytest
from unittest.mock import AsyncMock, Mock
from uuid import UUID, uuid4
from datetime import datetime

from src.app.prendas.application.dtos import PrendaDetalleDTO, UsuarioPolicyDTO, VariantePrendaDTO
from src.app.prendas.application.exceptions import PrendaNotFoundError
from src.app.prendas.application.use_cases.ver_detalle_prenda_use_case import VerDetallePrendaUseCase
from src.app.prendas.domain.entities import Prenda, VariantePrenda
from src.app.prendas.domain.value_objects import GeneroPrenda, TallaPrenda
from src.app.users.domain.value_objects import Rol

@pytest.fixture
def mock_prenda_repository():
    return AsyncMock()

@pytest.fixture
def existing_prenda_con_variantes():
    prenda_id = uuid4()
    variante_id_1 = uuid4()
    variante_id_2 = uuid4()

    variante_1 = VariantePrenda(
        id=variante_id_1,
        prenda_id=prenda_id,
        genero=GeneroPrenda.HOMBRE,
        talla=TallaPrenda.M,
        fecha_creacion=datetime.now()
    )
    variante_2 = VariantePrenda(
        id=variante_id_2,
        prenda_id=prenda_id,
        genero=GeneroPrenda.MUJER,
        talla=TallaPrenda.S,
        fecha_creacion=datetime.now()
    )

    return Prenda(
        id=prenda_id,
        nombre="Camiseta Detalle",
        descripcion="Descripción detallada de la camiseta",
        precio=29.99,
        imagen_url="camiseta_detalle.jpg",
        fecha_creacion=datetime.now(),
        variantes=[variante_1, variante_2]
    )

def test_ver_detalle_prenda_use_case_file_exists():
    file_path = "src/app/prendas/application/use_cases/ver_detalle_prenda_use_case.py"
    assert os.path.exists(file_path)
    assert os.path.isfile(file_path)

def test_ver_detalle_prenda_use_case_class_exists():
    from src.app.prendas.application.use_cases.ver_detalle_prenda_use_case import VerDetallePrendaUseCase
    assert isinstance(VerDetallePrendaUseCase, type)

def test_ver_detalle_prenda_use_case_execute_method_exists():
    from src.app.prendas.application.use_cases.ver_detalle_prenda_use_case import VerDetallePrendaUseCase
    assert hasattr(VerDetallePrendaUseCase, "execute")
    assert callable(getattr(VerDetallePrendaUseCase, "execute"))

@pytest.mark.asyncio
async def test_ver_detalle_prenda_use_case_execute_success(mock_prenda_repository, existing_prenda_con_variantes):
    # Arrange
    prenda_id = existing_prenda_con_variantes.id

    mock_prenda_repository.get_by_id_con_variantes.return_value = existing_prenda_con_variantes

    use_case = VerDetallePrendaUseCase(mock_prenda_repository)

    # Act
    result = await use_case.execute(prenda_id)

    # Assert
    mock_prenda_repository.get_by_id_con_variantes.assert_called_once_with(prenda_id)
    assert isinstance(result, PrendaDetalleDTO)
    assert result.id == existing_prenda_con_variantes.id
    assert result.nombre == existing_prenda_con_variantes.nombre
    assert len(result.variantes) == 2
    assert result.variantes[0].id == existing_prenda_con_variantes.variantes[0].id

@pytest.mark.asyncio
async def test_ver_detalle_prenda_use_case_prenda_not_found(mock_prenda_repository):
    # Arrange
    prenda_id = uuid4()

    mock_prenda_repository.get_by_id_con_variantes.return_value = None

    use_case = VerDetallePrendaUseCase(mock_prenda_repository)

    # Act & Assert
    with pytest.raises(PrendaNotFoundError):
        await use_case.execute(prenda_id)

    mock_prenda_repository.get_by_id_con_variantes.assert_called_once_with(prenda_id)