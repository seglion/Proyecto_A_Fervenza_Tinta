import pytest
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4
from datetime import datetime

from src.app.prendas.domain.entities import Prenda, VariantePrenda
from src.app.prendas.domain.value_objects import GeneroPrenda, TallaPrenda
from src.app.prendas.application.use_cases.listar_prendas_use_case import ListarPrendasUseCase
from src.app.prendas.application.dtos import ListaPrendasDTO, PrendaDTO, UsuarioPolicyDTO
from src.app.prendas.application.exceptions import UnauthorizedException
from src.app.users.domain.entities import User
from src.app.users.domain.value_objects import Rol


@pytest.fixture
def mock_prenda_repository():
    return AsyncMock()

@pytest.fixture
def mock_prenda_policy():
    return MagicMock()

@pytest.fixture
def active_user():
    return User(
        id=uuid4(),
        email="test@test.com",
        contrasena_hasheada="hashed_password",
        nombre="Test",
        apellidos="User",
        numero_telefono="123456789",
        rol=Rol.USUARIO,
        esta_activo=True,
        email_verificado=True,
        aprobado_por_admin=True,
        fecha_creacion=datetime.now(),
        fecha_actualizacion=datetime.now()
    )

@pytest.fixture
def inactive_user():
    return User(
        id=uuid4(),
        email="inactive@test.com",
        contrasena_hasheada="hashed_password",
        nombre="Inactive",
        apellidos="User",
        numero_telefono="987654321",
        rol=Rol.USUARIO,
        esta_activo=False,
        email_verificado=True,
        aprobado_por_admin=True,
        fecha_creacion=datetime.now(),
        fecha_actualizacion=datetime.now()
    )

@pytest.mark.asyncio
async def test_listar_prendas_use_case_execute_success(mock_prenda_repository, mock_prenda_policy, active_user):
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

    mock_prenda_repository.listar_todas.return_value = [prenda_1, prenda_2]
    mock_prenda_policy.es_usuario_activo.return_value = True

    use_case = ListarPrendasUseCase(mock_prenda_repository, mock_prenda_policy)

    # Act
    result = await use_case.execute(active_user)

    # Assert
    mock_prenda_repository.listar_todas.assert_called_once()
    mock_prenda_policy.es_usuario_activo.assert_called_once_with(
        UsuarioPolicyDTO(rol=active_user.rol.value, esta_activo=active_user.esta_activo)
    )
    assert isinstance(result, ListaPrendasDTO)
    assert len(result.prendas) == 2
    assert result.prendas[0].nombre == "Camiseta"
    assert result.prendas[1].nombre == "Pantalón"

@pytest.mark.asyncio
async def test_listar_prendas_use_case_execute_empty_list(mock_prenda_repository, mock_prenda_policy, active_user):
    # Arrange
    mock_prenda_repository.listar_todas.return_value = []
    mock_prenda_policy.es_usuario_activo.return_value = True

    use_case = ListarPrendasUseCase(mock_prenda_repository, mock_prenda_policy)

    # Act
    result = await use_case.execute(active_user)

    # Assert
    mock_prenda_repository.listar_todas.assert_called_once()
    mock_prenda_policy.es_usuario_activo.assert_called_once_with(
        UsuarioPolicyDTO(rol=active_user.rol.value, esta_activo=active_user.esta_activo)
    )
    assert isinstance(result, ListaPrendasDTO)
    assert len(result.prendas) == 0

@pytest.mark.asyncio
async def test_listar_prendas_use_case_unauthorized(mock_prenda_repository, mock_prenda_policy, inactive_user):
    # Arrange
    mock_prenda_policy.es_usuario_activo.return_value = False

    use_case = ListarPrendasUseCase(mock_prenda_repository, mock_prenda_policy)

    # Act & Assert
    with pytest.raises(UnauthorizedException, match="No está autorizado para listar prendas."):
        await use_case.execute(inactive_user)

    mock_prenda_policy.es_usuario_activo.assert_called_once_with(
        UsuarioPolicyDTO(rol=inactive_user.rol.value, esta_activo=inactive_user.esta_activo)
    )
    mock_prenda_repository.listar_todas.assert_not_called()