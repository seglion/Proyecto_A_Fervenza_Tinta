import os
import pytest
from unittest.mock import AsyncMock, Mock
from uuid import UUID, uuid4
from datetime import datetime

from src.app.prendas.application.dtos import ListaPrendasDTO, PrendaDTO, VariantePrendaDTO
from src.app.prendas.application.use_cases.listar_prendas_use_case import ListarPrendasUseCase
from src.app.prendas.domain.entities import Prenda, VariantePrenda
from src.app.prendas.domain.value_objects import GeneroPrenda, TallaPrenda

@pytest.fixture
def mock_prenda_repository():
    return AsyncMock()

def test_listar_prendas_use_case_file_exists():
    file_path = "src/app/prendas/application/use_cases/listar_prendas_use_case.py"
    assert os.path.exists(file_path)
    assert os.path.isfile(file_path)

def test_listar_prendas_use_case_class_exists():
    from src.app.prendas.application.use_cases.listar_prendas_use_case import ListarPrendasUseCase
    assert isinstance(ListarPrendasUseCase, type)

def test_listar_prendas_use_case_execute_method_exists():
    from src.app.prendas.application.use_cases.listar_prendas_use_case import ListarPrendasUseCase
    assert hasattr(ListarPrendasUseCase, "execute")
    assert callable(getattr(ListarPrendasUseCase, "execute"))

@pytest.mark.asyncio
async def test_listar_prendas_use_case_execute_success(mock_prenda_repository):
    # Arrange
    prenda_id_1 = uuid4()
    prenda_id_2 = uuid4()
    variante_id_1 = uuid4()
    variante_id_2 = uuid4()

    variante_1 = VariantePrenda(
        id=variante_id_1,
        prenda_id=prenda_id_1,
        genero=GeneroPrenda.HOMBRE,
        talla=TallaPrenda.M,
        fecha_creacion=datetime.now()
    )
    variante_2 = VariantePrenda(
        id=variante_id_2,
        prenda_id=prenda_id_2,
        genero=GeneroPrenda.MUJER,
        talla=TallaPrenda.S,
        fecha_creacion=datetime.now()
    )

    prenda_1 = Prenda(
        id=prenda_id_1,
        nombre="Camiseta",
        descripcion="Descripción Camiseta",
        precio=19.99,
        imagen_url="camiseta.jpg",
        fecha_creacion=datetime.now(),
        variantes=[variante_1]
    )
    prenda_2 = Prenda(
        id=prenda_id_2,
        nombre="Pantalón",
        descripcion="Descripción Pantalón",
        precio=39.99,
        imagen_url="pantalon.jpg",
        fecha_creacion=datetime.now(),
        variantes=[variante_2]
    )

    mock_prenda_repository.get_all.return_value = [prenda_1, prenda_2]

    use_case = ListarPrendasUseCase(mock_prenda_repository)

    # Act
    result = await use_case.execute()

    # Assert
    mock_prenda_repository.get_all.assert_called_once()
    assert isinstance(result, ListaPrendasDTO)
    assert len(result.prendas) == 2
    assert result.prendas[0].id == prenda_1.id
    assert result.prendas[0].nombre == prenda_1.nombre
    assert result.prendas[0].variantes[0].id == variante_1.id
    assert result.prendas[1].id == prenda_2.id
    assert result.prendas[1].nombre == prenda_2.nombre
    assert result.prendas[1].variantes[0].id == variante_2.id

@pytest.mark.asyncio
async def test_listar_prendas_use_case_execute_empty_list(mock_prenda_repository):
    # Arrange
    mock_prenda_repository.get_all.return_value = []

    use_case = ListarPrendasUseCase(mock_prenda_repository)

    # Act
    result = await use_case.execute()

    # Assert
    mock_prenda_repository.get_all.assert_called_once()
    assert isinstance(result, ListaPrendasDTO)
    assert len(result.prendas) == 0