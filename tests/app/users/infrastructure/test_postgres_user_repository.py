import pytest
import pytest_asyncio
from uuid import uuid4
from datetime import datetime, timezone

from app.core.config import settings
from app.users.application.repositories.i_user_repository import IUserRepository
from app.users.domain.entities import User
from app.users.domain.value_objects import Rol
from app.users.infrastructure.postgres_user_repository import PostgresUserRepository
import asyncpg

# Marcar todos los tests de este fichero como tests asíncronos
pytestmark = pytest.mark.asyncio


@pytest.fixture
def sample_user() -> User:
    """Devuelve un objeto User de ejemplo con un email único."""
    unique_id = uuid4()
    return User(
        id=unique_id,
        email=f"test.{unique_id}@example.com",
        contrasena_hasheada="hashed_password_test",
        nombre="Test",
        apellidos="User",
        rol=Rol.USUARIO,
        numero_telefono=str(uuid4())[:20]
    )


@pytest_asyncio.fixture
async def db_connection():
    """Crea un pool, una conexión y una transacción para un único test, y luego lo limpia todo."""
    pool = await asyncpg.create_pool(settings.DATABASE_URL)
    async with pool.acquire() as connection:
        async with connection.transaction():
            # Solución temporal: Crear la tabla para este test
            await connection.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id UUID PRIMARY KEY,
                email VARCHAR(255) UNIQUE NOT NULL,
                contrasena_hasheada VARCHAR(255) NOT NULL,
                nombre VARCHAR(255) NOT NULL,
                apellidos VARCHAR(255) NOT NULL,
                numero_telefono VARCHAR(20),
                rol VARCHAR(50) NOT NULL,
                apodo VARCHAR(255),
                url_avatar VARCHAR(255),
                esta_activo BOOLEAN DEFAULT TRUE,
                email_verificado BOOLEAN DEFAULT FALSE,
                aprobado_por_admin BOOLEAN DEFAULT FALSE,
                fecha_creacion TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
                fecha_actualizacion TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
            );
            """)
            yield connection
    await pool.close()


# --- Tests de Estructura de la Clase ---

def test_postgres_user_repository_class_exists():
    assert PostgresUserRepository is not None


def test_postgres_user_repository_implements_interface():
    assert issubclass(PostgresUserRepository, IUserRepository)


async def test_repository_is_instantiable_with_db_connection(db_connection):
    _ = PostgresUserRepository(db_connection)


# --- Tests de Comportamiento de Métodos ---

async def test_crear_user_inserts_correctly(db_connection, sample_user):
    # Arrange
    repo = PostgresUserRepository(db_connection)

    # Act
    await repo.crear(sample_user)

    # Assert
    saved_user_row = await db_connection.fetchrow(
        "SELECT * FROM usuarios WHERE id = $1", sample_user.id
    )

    assert saved_user_row is not None
    assert str(saved_user_row['id']) == str(sample_user.id)


async def test_buscar_por_email_encuentra_usuario_existente(db_connection, sample_user):
    # Arrange
    repo = PostgresUserRepository(db_connection)
    await repo.crear(sample_user)

    # Act
    found_user = await repo.buscar_por_email(sample_user.email)

    # Assert
    assert found_user is not None
    assert found_user.id == sample_user.id


async def test_buscar_por_email_devuelve_none_si_no_existe(db_connection):
    # Arrange
    repo = PostgresUserRepository(db_connection)

    # Act
    found_user = await repo.buscar_por_email("no.existe@example.com")

    # Assert
    assert found_user is None


async def test_buscar_por_id_encuentra_usuario_existente(db_connection, sample_user):
    # Arrange
    repo = PostgresUserRepository(db_connection)
    await repo.crear(sample_user)

    # Act
    found_user = await repo.buscar_por_id(sample_user.id)

    # Assert
    assert found_user is not None
    assert found_user.id == sample_user.id


async def test_buscar_por_id_devuelve_none_si_no_existe(db_connection):
    # Arrange
    repo = PostgresUserRepository(db_connection)

    # Act
    found_user = await repo.buscar_por_id(uuid4())

    # Assert
    assert found_user is None


async def test_actualizar_modifica_usuario_existente(db_connection, sample_user):
    # Arrange: Insertar el usuario inicial
    repo = PostgresUserRepository(db_connection)
    await repo.crear(sample_user)

    # Modificar el usuario en memoria
    sample_user.nombre = "Nombre Actualizado"
    sample_user.apodo = "Apodo Actualizado"
    sample_user.fecha_actualizacion = datetime.now(timezone.utc)

    # Act
    updated_user = await repo.actualizar(sample_user)

    # Assert
    assert updated_user.nombre == "Nombre Actualizado"

    # Verificar que los cambios se persistieron en la BD
    db_row = await db_connection.fetchrow("SELECT * FROM usuarios WHERE id = $1", sample_user.id)
    assert db_row is not None
    assert db_row['nombre'] == "Nombre Actualizado"
    assert db_row['apodo'] == "Apodo Actualizado"
    assert db_row['fecha_actualizacion'] > sample_user.fecha_creacion


async def test_actualizar_contrasena_modifica_la_contrasena(db_connection, sample_user):
    # Arrange: Insertar el usuario inicial
    repo = PostgresUserRepository(db_connection)
    await repo.crear(sample_user)

    new_hashed_password = "nueva_contrasena_hasheada"

    # Act
    await repo.actualizar_contrasena(sample_user.id, new_hashed_password)

    # Assert
    db_row = await db_connection.fetchrow("SELECT contrasena_hasheada FROM usuarios WHERE id = $1", sample_user.id)
    assert db_row is not None
    assert db_row['contrasena_hasheada'] == new_hashed_password


async def test_desactivar_cuenta_cambia_el_estado_a_false(db_connection, sample_user):
    # Arrange: Insertar el usuario inicial (está activo por defecto)
    repo = PostgresUserRepository(db_connection)
    await repo.crear(sample_user)

    # Act
    await repo.desactivar_cuenta(sample_user.id)

    # Assert
    db_row = await db_connection.fetchrow("SELECT esta_activo FROM usuarios WHERE id = $1", sample_user.id)
    assert db_row is not None
    assert db_row['esta_activo'] is False


async def test_buscar_todos_devuelve_lista_de_usuarios(db_connection, sample_user):
    # Arrange
    repo = PostgresUserRepository(db_connection)
    await repo.crear(sample_user) # Crear un primer usuario

    # Crear un segundo usuario
    user2_id = uuid4()
    user2 = User(id=user2_id, email=f"test.{user2_id}@example.com", contrasena_hasheada="p2", nombre="U2", apellidos="S2", rol=Rol.USUARIO, numero_telefono=str(uuid4())[:20])
    await repo.crear(user2)

    # Act
    list_of_users = await repo.buscar_todos()

    # Assert
    assert isinstance(list_of_users, list)
    assert len(list_of_users) >= 2
    assert any(u.id == sample_user.id for u in list_of_users)
    assert any(u.id == user2.id for u in list_of_users)
