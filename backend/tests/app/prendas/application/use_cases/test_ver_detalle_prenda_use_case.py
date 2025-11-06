import pytest
from unittest.mock import AsyncMock, MagicMock
from uuid import UUID, uuid4
from datetime import datetime

from src.app.prendas.domain.entities import Prenda, VariantePrenda
from src.app.prendas.domain.value_objects import GeneroPrenda, TallaPrenda
from src.app.prendas.application.use_cases.ver_detalle_prenda_use_case import VerDetallePrendaUseCase
from src.app.prendas.application.dtos import PrendaDetalleDTO, UsuarioPolicyDTO
from src.app.prendas.application.exceptions import PrendaNotFoundError, UnauthorizedException
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
        descripcion="Descripción detallada de la camiseta.",
        precio=25.00,
        imagen_url="camiseta_detalle.jpg",
        fecha_creacion=datetime.now(),
        variantes=[variante_1, variante_2]
    )

@pytest.mark.asyncio
async def test_ver_detalle_prenda_use_case_execute_success(mock_prenda_repository, mock_prenda_policy, active_user, existing_prenda_con_variantes):
    # Arrange
    prenda_id = existing_prenda_con_variantes.id

    mock_prenda_repository.buscar_por_id_con_variantes.return_value = existing_prenda_con_variantes
    mock_prenda_policy.es_usuario_activo.return_value = True

    use_case = VerDetallePrendaUseCase(mock_prenda_repository, mock_prenda_policy)

    # Act
    result = await use_case.execute(prenda_id, active_user)

    # Assert
    mock_prenda_repository.buscar_por_id_con_variantes.assert_called_once_with(prenda_id)
    mock_prenda_policy.es_usuario_activo.assert_called_once_with(
        UsuarioPolicyDTO(rol=active_user.rol.value, esta_activo=active_user.esta_activo)
    )
    assert isinstance(result, PrendaDetalleDTO)
    assert result.id == prenda_id
    assert result.nombre == "Camiseta Detalle"
    assert len(result.variantes) == 2

@pytest.mark.asyncio
async def test_ver_detalle_prenda_use_case_prenda_not_found(mock_prenda_repository, mock_prenda_policy, active_user):
    # Arrange
    prenda_id = uuid4()

    mock_prenda_repository.buscar_por_id_con_variantes.return_value = None
    mock_prenda_policy.es_usuario_activo.return_value = True

    use_case = VerDetallePrendaUseCase(mock_prenda_repository, mock_prenda_policy)

    # Act & Assert
    with pytest.raises(PrendaNotFoundError, match=f"No se encontró la prenda con el ID {prenda_id}"):
        await use_case.execute(prenda_id, active_user)

    mock_prenda_repository.buscar_por_id_con_variantes.assert_called_once_with(prenda_id)
    mock_prenda_policy.es_usuario_activo.assert_called_once_with(
        UsuarioPolicyDTO(rol=active_user.rol.value, esta_activo=active_user.esta_activo)
    )

@pytest.mark.asyncio
async def test_ver_detalle_prenda_use_case_unauthorized(mock_prenda_repository, mock_prenda_policy, inactive_user):
    # Arrange
    prenda_id = uuid4()

    mock_prenda_policy.es_usuario_activo.return_value = False

    use_case = VerDetallePrendaUseCase(mock_prenda_repository, mock_prenda_policy)

    # Act & Assert
    with pytest.raises(UnauthorizedException, match="No está autorizado para ver el detalle de la prenda."):
        await use_case.execute(prenda_id, inactive_user)

    mock_prenda_policy.es_usuario_activo.assert_called_once_with(
        UsuarioPolicyDTO(rol=inactive_user.rol.value, esta_activo=inactive_user.esta_activo)
    )
    mock_prenda_repository.buscar_por_id_con_variantes.assert_not_called()