import pytest
from uuid import UUID, uuid4
from datetime import datetime, timezone, timedelta
from typing import Optional

from app.users.domain.entities import User
from app.users.domain.value_objects import Rol

def test_user_creation():
    """
    Tests that a User object can be created with all required fields.
    """
    user = User(
        email="test@example.com",
        contrasena_hasheada="hashed_password",
        nombre="Test",
        apellidos="User",
        apodo="testuser",
        numero_telefono="123456789",
        rol=Rol.USUARIO
    )
    assert isinstance(user, User)
    assert user.email == "test@example.com"
    assert user.contrasena_hasheada == "hashed_password"
    assert user.nombre == "Test"
    assert user.apellidos == "User"
    assert user.apodo == "testuser"
    assert user.numero_telefono == "123456789"
    assert user.rol == Rol.USUARIO
    assert isinstance(user.id, UUID)
    assert user.esta_activo is True
    assert user.email_verificado is False
    assert user.aprobado_por_admin is False
    assert isinstance(user.fecha_creacion, datetime)
    assert isinstance(user.fecha_actualizacion, datetime)

def test_user_creation_with_optional_fields():
    """
    Tests that a User object can be created with optional fields.
    """
    user = User(
        email="test2@example.com",
        contrasena_hasheada="hashed_password2",
        nombre="Test2",
        apellidos="User2",
        apodo="testuser2",
        numero_telefono="987654321",
        rol=Rol.ADMIN,
        url_avatar="http://example.com/avatar.jpg",
        esta_activo=False,
        email_verificado=True,
        aprobado_por_admin=True
    )
    assert user.email == "test2@example.com"
    assert user.rol == Rol.ADMIN
    assert user.url_avatar == "http://example.com/avatar.jpg"
    assert user.esta_activo is False
    assert user.email_verificado is True
    assert user.aprobado_por_admin is True

def test_user_id_is_uuid():
    """
    Tests that the user ID is a UUID.
    """
    user = User(
        email="test@example.com",
        contrasena_hasheada="hashed_password",
        nombre="Test",
        apellidos="User",
        apodo="testuser",
        numero_telefono="123456789",
        rol=Rol.USUARIO
    )
    assert isinstance(user.id, UUID)

def test_user_fecha_creacion_defaults_to_utcnow():
    """
    Tests that a new user defaults to fecha_creacion being a datetime object.
    """
    user = User(
        email="test@test.com",
        contrasena_hasheada="hash",
        nombre="Test",
        apellidos="User",
        apodo="testuser",
        numero_telefono="123",
        rol=Rol.USUARIO
    )
    assert isinstance(user.fecha_creacion, datetime)
    assert user.fecha_creacion.tzinfo is not None

def test_user_fecha_actualizacion_defaults_to_utcnow():
    """
    Tests that a new user defaults to fecha_actualizacion being a datetime object.
    """
    user = User(
        email="test@test.com",
        contrasena_hasheada="hash",
        nombre="Test",
        apellidos="User",
        apodo="testuser",
        numero_telefono="123",
        rol=Rol.USUARIO
    )
    assert isinstance(user.fecha_actualizacion, datetime)
    assert user.fecha_actualizacion.tzinfo is not None

def test_user_esta_activo_defaults_to_true():
    """
    Tests that a new user defaults to esta_activo=True.
    """
    user = User(
        email="test@test.com",
        contrasena_hasheada="hash",
        nombre="Test",
        apellidos="User",
        apodo="testuser",
        numero_telefono="123",
        rol=Rol.USUARIO
    )
    assert user.esta_activo is True

def test_user_email_verificado_defaults_to_false():
    """
    Tests that a new user defaults to email_verificado=False.
    """
    user = User(
        email="test@test.com",
        contrasena_hasheada="hash",
        nombre="Test",
        apellidos="User",
        apodo="testuser",
        numero_telefono="123",
        rol=Rol.USUARIO
    )
    assert user.email_verificado is False

def test_user_aprobado_por_admin_defaults_to_false():
    """
    Tests that a new user defaults to aprobado_por_admin=False.
    """
    user = User(
        email="test@test.com",
        contrasena_hasheada="hash",
        nombre="Test",
        apellidos="User",
        apodo="testuser",
        numero_telefono="123",
        rol=Rol.USUARIO
    )
    assert user.aprobado_por_admin is False