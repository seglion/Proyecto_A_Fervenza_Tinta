import pytest
from typing import Optional
from uuid import UUID
from datetime import datetime
from app.users.domain.entities import User

def test_user_entity_file_exists():
    """
    Tests if the user entity file exists.
    """
    try:
        from app.users.domain import entities
    except ImportError:
        pytest.fail("User entity file does not exist: src/app/users/domain/entities.py")

def test_user_class_exists():
    """
    Tests if the User class exists in the entities file.
    """
    try:
        from app.users.domain.entities import User
    except ImportError:
        pytest.fail("User class does not exist in entities.py")

def test_user_has_id_attribute():
    """
    Tests if the User class has an 'id' attribute with the correct type.
    """
    assert 'id' in User.__annotations__
    assert User.__annotations__['id'] == Optional[UUID]

def test_user_has_email_attribute():
    """
    Tests if the User class has an 'email' attribute with the correct type.
    """
    assert 'email' in User.__annotations__
    assert User.__annotations__['email'] == str

def test_user_has_contrasena_hasheada_attribute():
    """
    Tests if the User class has a 'contrasena_hasheada' attribute with the correct type.
    """
    assert 'contrasena_hasheada' in User.__annotations__
    assert User.__annotations__['contrasena_hasheada'] == str

def test_user_has_nombre_attribute():
    """
    Tests if the User class has a 'nombre' attribute with the correct type.
    """
    assert 'nombre' in User.__annotations__
    assert User.__annotations__['nombre'] == Optional[str]

def test_user_has_apellidos_attribute():
    """
    Tests if the User class has an 'apellidos' attribute with the correct type.
    """
    assert 'apellidos' in User.__annotations__
    assert User.__annotations__['apellidos'] == Optional[str]

def test_user_has_apodo_attribute():
    """
    Tests if the User class has an 'apodo' attribute with the correct type.
    """
    assert 'apodo' in User.__annotations__
    assert User.__annotations__['apodo'] == str

def test_user_has_numero_telefono_attribute():
    """
    Tests if the User class has a 'numero_telefono' attribute with the correct type.
    """
    assert 'numero_telefono' in User.__annotations__
    assert User.__annotations__['numero_telefono'] == str

def test_user_has_url_avatar_attribute():
    """
    Tests if the User class has a 'url_avatar' attribute with the correct type.
    """
    assert 'url_avatar' in User.__annotations__
    assert User.__annotations__['url_avatar'] == Optional[str]

def test_user_has_esta_activo_attribute():
    """
    Tests if the User class has an 'esta_activo' attribute with the correct type.
    """
    assert 'esta_activo' in User.__annotations__
    assert User.__annotations__['esta_activo'] == bool

def test_user_esta_activo_defaults_to_true():
    """Tests that a new user defaults to esta_activo=True."""
    user = User(email="test@test.com", contrasena_hasheada="hash", apodo="test", numero_telefono="123")
    assert user.esta_activo is True

def test_user_has_email_verificado_attribute():
    """
    Tests if the User class has an 'email_verificado' attribute with the correct type.
    """
    assert 'email_verificado' in User.__annotations__
    assert User.__annotations__['email_verificado'] == bool

def test_user_email_verificado_defaults_to_false():
    """Tests that a new user defaults to email_verificado=False."""
    user = User(email="test@test.com", contrasena_hasheada="hash", apodo="test", numero_telefono="123")
    assert user.email_verificado is False

def test_user_has_aprobado_por_admin_attribute():
    """
    Tests if the User class has an 'aprobado_por_admin' attribute with the correct type.
    """
    assert 'aprobado_por_admin' in User.__annotations__
    assert User.__annotations__['aprobado_por_admin'] == bool

def test_user_aprobado_por_admin_defaults_to_false():
    """Tests that a new user defaults to aprobado_por_admin=False."""
    user = User(email="test@test.com", contrasena_hasheada="hash", apodo="test", numero_telefono="123")
    assert user.aprobado_por_admin is False

def test_user_has_fecha_creacion_attribute():
    """
    Tests if the User class has a 'fecha_creacion' attribute with the correct type.
    """
    assert 'fecha_creacion' in User.__annotations__
    assert User.__annotations__['fecha_creacion'] == datetime

def test_user_fecha_creacion_defaults_to_utcnow():
    """Tests that a new user defaults to fecha_creacion being a datetime object."""
    user = User(email="test@test.com", contrasena_hasheada="hash", apodo="test", numero_telefono="123")
    assert isinstance(user.fecha_creacion, datetime)

def test_user_has_fecha_actualizacion_attribute():
    """
    Tests if the User class has a 'fecha_actualizacion' attribute with the correct type.
    """
    assert 'fecha_actualizacion' in User.__annotations__
    assert User.__annotations__['fecha_actualizacion'] == datetime

def test_user_fecha_actualizacion_defaults_to_utcnow():

    """Tests that a new user defaults to fecha_actualizacion being a datetime object."""

    user = User(email="test@test.com", contrasena_hasheada="hash", apodo="test", numero_telefono="123")

    assert isinstance(user.fecha_actualizacion, datetime)