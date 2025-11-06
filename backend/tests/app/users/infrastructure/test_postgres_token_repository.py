import pytest
import pytest_asyncio
from uuid import uuid4
from datetime import datetime, timedelta, timezone

from app.core.config import settings
from app.users.application.repositories.i_token_repository import ITokenRepository
from app.users.domain.entities import Token, User
from app.users.domain.value_objects import TipoToken, Rol
from app.users.infrastructure.postgres_token_repository import PostgresTokenRepository
# from src.app.users.infrastructure.models import UsuarioModel # No es necesario importar UsuarioModel aquí si se crean las tablas manualmente
import asyncpg

# Marcar todos los tests de este fichero como tests asíncronos
pytestmark = pytest.mark.asyncio


@pytest_asyncio.fixture
async def db_connection():
    """Crea un pool, una conexión y una transacción para un único test, y luego lo limpia todo."""
    pool = await asyncpg.create_pool(settings.DATABASE_URL)
    async with pool.acquire() as connection:
        async with connection.transaction():
            # Eliminar y crear la tabla usuarios para asegurar un estado limpio
            await connection.execute("DROP TABLE IF EXISTS tokens;")
            await connection.execute("DROP TABLE IF EXISTS usuarios CASCADE;") # CASCADE para eliminar dependencias
            await connection.execute("""
            CREATE TABLE usuarios (
                id UUID PRIMARY KEY,
                email VARCHAR(255) UNIQUE NOT NULL,
                contrasena_hasheada VARCHAR(255) NOT NULL,
                nombre VARCHAR(100) NOT NULL,
                apellidos VARCHAR(100) NOT NULL,
                numero_telefono VARCHAR(20) UNIQUE NOT NULL,
                rol VARCHAR(50) NOT NULL,
                apodo VARCHAR(50),
                url_avatar VARCHAR(255),
                esta_activo BOOLEAN DEFAULT TRUE NOT NULL,
                email_verificado BOOLEAN DEFAULT FALSE NOT NULL,
                aprobado_por_admin BOOLEAN DEFAULT FALSE NOT NULL,
                fecha_creacion TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP NOT NULL,
                fecha_actualizacion TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP NOT NULL
            );
            """)
            # Eliminar y crear la tabla tokens para asegurar un estado limpio
            await connection.execute("""
            CREATE TABLE tokens (
                id UUID PRIMARY KEY,
                usuario_id UUID NOT NULL REFERENCES usuarios(id),
                hash_token VARCHAR(255) UNIQUE NOT NULL,
                tipo_token VARCHAR(50) NOT NULL,
                fecha_expiracion TIMESTAMPTZ NOT NULL,
                es_valido BOOLEAN DEFAULT TRUE,
                fecha_creacion TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
            );
            """)
            yield connection
    await pool.close()

@pytest_asyncio.fixture
async def sample_user(db_connection) -> User:
    """Inserta un usuario de ejemplo en la base de datos y lo devuelve."""
    user_id = uuid4()
    await db_connection.execute("""
        INSERT INTO usuarios (id, email, contrasena_hasheada, nombre, apellidos, numero_telefono, rol)
        VALUES ($1, $2, $3, $4, $5, $6, $7)
    """, str(user_id), "test@example.com", "hashed_password", "Test", "User", "123456789", Rol.USUARIO.value)
    return User(
        id=user_id,
        email="test@example.com",
        contrasena_hasheada="hashed_password",
        nombre="Test",
        apellidos="User",
        numero_telefono="123456789",
        rol=Rol.USUARIO,
        esta_activo=True,
        email_verificado=False,
        aprobado_por_admin=False,
        fecha_creacion=datetime.now(timezone.utc),
        fecha_actualizacion=datetime.now(timezone.utc)
    )

@pytest.fixture
def sample_token(sample_user: User) -> Token:
    """Devuelve un objeto Token de ejemplo asociado a un usuario existente."""
    return Token(
        id=uuid4(),
        usuario_id=sample_user.id,
        hash_token=f"hash_de_prueba_{uuid4()}", # Hash único
        tipo_token=TipoToken.VERIFICACION_EMAIL,
        fecha_expiracion=datetime.now(timezone.utc) + timedelta(days=1)
    )


# --- Tests de Estructura de la Clase ---

def test_postgres_token_repository_class_exists():
    assert PostgresTokenRepository is not None


def test_postgres_token_repository_implements_interface():
    assert issubclass(PostgresTokenRepository, ITokenRepository)


async def test_repository_is_instantiable_with_db_connection(db_connection):
    _ = PostgresTokenRepository(db_connection)


# --- Tests de Comportamiento de Métodos ---

async def test_crear_token_inserts_correctly(db_connection, sample_token):
    # Arrange
    repo = PostgresTokenRepository(db_connection)

    # Act
    await repo.crear(sample_token)

    # Assert
    saved_token_row = await db_connection.fetchrow(
        "SELECT * FROM tokens WHERE id = $1", sample_token.id
    )

    assert saved_token_row is not None
    assert str(saved_token_row['id']) == str(sample_token.id)
    assert saved_token_row['hash_token'] == sample_token.hash_token


async def test_buscar_por_hash_encuentra_token_existente(db_connection, sample_token):
    # Arrange
    repo = PostgresTokenRepository(db_connection)
    await repo.crear(sample_token)

    # Act
    found_token = await repo.buscar_por_hash(sample_token.hash_token)

    # Assert
    assert found_token is not None
    assert found_token.id == sample_token.id


async def test_buscar_por_hash_devuelve_none_si_no_existe(db_connection):
    # Arrange
    repo = PostgresTokenRepository(db_connection)

    # Act
    found_token = await repo.buscar_por_hash("hash_inexistente")

    # Assert
    assert found_token is None


async def test_actualizar_modifica_token_existente(db_connection, sample_token):
    # Arrange
    repo = PostgresTokenRepository(db_connection)
    await repo.crear(sample_token)

    # Modificar el token en memoria
    sample_token.es_valido = False

    # Act
    updated_token = await repo.actualizar(sample_token)

    # Assert
    assert updated_token.es_valido is False
    db_row = await db_connection.fetchrow("SELECT es_valido FROM tokens WHERE id = $1", sample_token.id)
    assert db_row['es_valido'] is False
