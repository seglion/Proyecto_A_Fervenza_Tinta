import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock
from uuid import uuid4
from decimal import Decimal
from datetime import datetime # Añadido

from src.app.users.domain.entities import User
from src.app.users.domain.value_objects import Rol
from src.app.core.dependencies import get_current_user
from src.app.core.database import get_db # Añadido
from src.app.prendas.presentation.router import (
    router as prendas_router,
    get_listar_prendas_use_case,
    get_ver_detalle_prenda_use_case,
    get_crear_prenda_use_case,
)
from src.app.prendas.application.dtos import ListaPrendasDTO, PrendaDetalleDTO, PrendaDTO, VariantePrendaDTO, TallaPrenda, GeneroPrenda, CrearPrendaDTO, PrendaCreadaDTO
from src.app.prendas.application.exceptions import PrendaNotFoundError, UnauthorizedException, NotAuthorizedError # Añadido NotAuthorizedError

# ------------------ Fixtures ------------------
@pytest.fixture(scope="function")
def app_client():
    app = FastAPI()
    app.include_router(prendas_router)
    with TestClient(app) as client:
        yield client

@pytest.fixture
def active_user():
    return User(id=uuid4(), rol=Rol.USUARIO, email="user@test.com", contrasena_hasheada="123", nombre="User", apellidos="Test", numero_telefono="987654321", esta_activo=True, email_verificado=True, aprobado_por_admin=True)

@pytest.fixture
def admin_user():
    return User(id=uuid4(), rol=Rol.ADMIN, email="admin@test.com", contrasena_hasheada="123", nombre="Admin", apellidos="Test", numero_telefono="123456789", esta_activo=True, email_verificado=True, aprobado_por_admin=True)

@pytest.fixture
def non_admin_user():
    return User(id=uuid4(), rol=Rol.USUARIO, email="nonadmin@test.com", contrasena_hasheada="123", nombre="NonAdmin", apellidos="User", numero_telefono="111222333", esta_activo=True, email_verificado=True, aprobado_por_admin=True)

@pytest.fixture
def mock_listar_prendas_use_case():
    mock = AsyncMock()
    mock.execute.return_value = ListaPrendasDTO(
        prendas=[
            PrendaDTO(
                id=uuid4(),
                nombre="Camiseta",
                descripcion="Camiseta de algodón",
                precio=Decimal("19.99"),
                imagen_url="http://example.com/camiseta.jpg", # Añadido
                fecha_creacion=datetime.now(), # Añadido
                variantes=[
                    VariantePrendaDTO(
                        id=uuid4(),
                        prenda_id=uuid4(),
                        talla=TallaPrenda.M,
                        color="Rojo",
                        stock=10,
                        genero=GeneroPrenda.HOMBRE,
                        fecha_creacion=datetime.now()
                    )
                ]
            )
        ]
    )
    return mock

@pytest.fixture
def mock_ver_detalle_prenda_use_case():
    mock = AsyncMock()
    mock.execute.return_value = PrendaDetalleDTO(
        id=uuid4(),
        nombre="Camiseta",
        descripcion="Camiseta de algodón",
        precio=Decimal("19.99"),
        imagen_url="http://example.com/camiseta.jpg", # Añadido
        fecha_creacion=datetime.now(), # Añadido
        variantes=[
            VariantePrendaDTO(
                id=uuid4(),
                prenda_id=uuid4(),
                talla=TallaPrenda.M,
                color="Rojo",
                stock=10,
                genero=GeneroPrenda.HOMBRE,
                fecha_creacion=datetime.now()
            )
        ]
    )
    return mock

@pytest.fixture
def mock_crear_prenda_use_case():
    mock = AsyncMock()
    mock.execute.return_value = PrendaCreadaDTO(id=uuid4())
    return mock

@pytest.fixture
def override_get_db(): # Ahora es síncrono y devuelve un generador
    def _override_get_db():
        yield AsyncMock() # Devuelve un mock de conexión
    return _override_get_db

# ------------------ Tests for listar_prendas ------------------

@pytest.mark.asyncio
async def test_listar_prendas_success(app_client, active_user, mock_listar_prendas_use_case):
    # Arrange
    app_client.app.dependency_overrides[get_current_user] = lambda: active_user
    app_client.app.dependency_overrides[get_listar_prendas_use_case] = lambda: mock_listar_prendas_use_case

    # Act
    response = app_client.get("/prendas/")

    # Assert
    assert response.status_code == 200
    assert "prendas" in response.json()
    assert len(response.json()["prendas"]) > 0
    mock_listar_prendas_use_case.execute.assert_called_once_with(active_user)

    # Cleanup
    app_client.app.dependency_overrides = {}

@pytest.mark.asyncio
async def test_listar_prendas_unauthorized(app_client, override_get_db):
    # Arrange
    app_client.app.dependency_overrides[get_current_user] = lambda: None
    app_client.app.dependency_overrides[get_db] = override_get_db # Ahora se asigna la función generadora

    # Act
    response = app_client.get("/prendas/")

    # Assert
    assert response.status_code == 403 # Cambiado de 401 a 403
    assert response.json() == {"detail": "No está autenticado para listar prendas."}

    # Cleanup
    app_client.app.dependency_overrides = {}

# ------------------ Tests for ver_detalle_prenda ------------------

@pytest.mark.asyncio
async def test_ver_detalle_prenda_success(app_client, active_user, mock_ver_detalle_prenda_use_case):
    # Arrange
    prenda_id = uuid4()
    app_client.app.dependency_overrides[get_current_user] = lambda: active_user
    app_client.app.dependency_overrides[get_ver_detalle_prenda_use_case] = lambda: mock_ver_detalle_prenda_use_case

    # Act
    response = app_client.get(f"/prendas/{prenda_id}")

    # Assert
    assert response.status_code == 200
    assert response.json()["id"] == str(mock_ver_detalle_prenda_use_case.execute.return_value.id)
    mock_ver_detalle_prenda_use_case.execute.assert_called_once_with(prenda_id, active_user)

    # Cleanup
    app_client.app.dependency_overrides = {}

@pytest.mark.asyncio
async def test_ver_detalle_prenda_not_found(app_client, active_user, mock_ver_detalle_prenda_use_case):
    # Arrange
    prenda_id = uuid4()
    app_client.app.dependency_overrides[get_current_user] = lambda: active_user
    app_client.app.dependency_overrides[get_ver_detalle_prenda_use_case] = lambda: mock_ver_detalle_prenda_use_case
    mock_ver_detalle_prenda_use_case.execute.side_effect = PrendaNotFoundError(f"No se encontró la prenda con el ID {prenda_id}")

    # Act
    response = app_client.get(f"/prendas/{prenda_id}")

    # Assert
    assert response.status_code == 404
    assert response.json() == {"detail": f"No se encontró la prenda con el ID {prenda_id}"}
    mock_ver_detalle_prenda_use_case.execute.assert_called_once_with(prenda_id, active_user)

    # Cleanup
    app_client.app.dependency_overrides = {}

@pytest.mark.asyncio
async def test_ver_detalle_prenda_unauthorized(app_client, override_get_db):
    # Arrange
    prenda_id = uuid4()
    app_client.app.dependency_overrides[get_current_user] = lambda: None
    app_client.app.dependency_overrides[get_db] = override_get_db # Ahora se asigna la función generadora

    # Act
    response = app_client.get(f"/prendas/{prenda_id}")

    # Assert
    assert response.status_code == 403 # Cambiado de 401 a 403
    assert response.json() == {"detail": "No está autenticado para ver el detalle de la prenda."}

    # Cleanup
    app_client.app.dependency_overrides = {}

# ------------------ Tests for crear_prenda ------------------

@pytest.mark.asyncio
async def test_crear_prenda_success(app_client, admin_user, mock_crear_prenda_use_case):
    # Arrange
    app_client.app.dependency_overrides[get_current_user] = lambda: admin_user
    app_client.app.dependency_overrides[get_crear_prenda_use_case] = lambda: mock_crear_prenda_use_case

    create_data = CrearPrendaDTO(
        nombre="Sudadera",
        descripcion="Sudadera de algodón con capucha",
        precio=Decimal("45.00"),
        imagen_url="http://example.com/sudadera.jpg"
    )

    # Act
    response = app_client.post("/prendas/", json=create_data.model_dump(mode='json'))

    # Assert
    assert response.status_code == 201
    assert "id" in response.json()
    mock_crear_prenda_use_case.execute.assert_called_once_with(create_data, admin_user)

    # Cleanup
    app_client.app.dependency_overrides = {}

@pytest.mark.asyncio
async def test_crear_prenda_forbidden(app_client, non_admin_user, mock_crear_prenda_use_case):
    # Arrange
    app_client.app.dependency_overrides[get_current_user] = lambda: non_admin_user
    app_client.app.dependency_overrides[get_crear_prenda_use_case] = lambda: mock_crear_prenda_use_case
    mock_crear_prenda_use_case.execute.side_effect = NotAuthorizedError("No tienes permiso para crear una prenda.")

    create_data = CrearPrendaDTO(
        nombre="Sudadera",
        descripcion="Sudadera de algodón con capucha",
        precio=Decimal("45.00"),
        imagen_url="http://example.com/sudadera.jpg"
    )

    # Act
    response = app_client.post("/prendas/", json=create_data.model_dump(mode='json'))

    # Assert
    assert response.status_code == 403
    assert response.json() == {"detail": "The user doesn't have enough privileges"}
    mock_crear_prenda_use_case.execute.assert_not_called()

    # Cleanup
    app_client.app.dependency_overrides = {}

@pytest.mark.asyncio
async def test_crear_prenda_unauthorized(app_client, override_get_db):
    # Arrange
    app_client.app.dependency_overrides[get_current_user] = lambda: None
    # No necesitamos mockear get_admin_user_dependency porque get_current_user ya devuelve None
    app_client.app.dependency_overrides[get_db] = override_get_db

    create_data = CrearPrendaDTO(
        nombre="Sudadera",
        descripcion="Sudadera de algodón con capucha",
        precio=Decimal("45.00"),
        imagen_url="http://example.com/sudadera.jpg"
    )

    # Act
    response = app_client.post("/prendas/", json=create_data.model_dump(mode='json'))

    # Assert
    assert response.status_code == 401 # El use case lanza NotAuthorizedError con 403 si el user es None
    assert response.json() == {"detail": "Not authenticated"}

    # Cleanup
    app_client.app.dependency_overrides = {}
