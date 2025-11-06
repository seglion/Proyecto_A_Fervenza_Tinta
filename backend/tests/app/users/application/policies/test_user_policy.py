import pytest
from uuid import uuid4
from app.users.domain.entities import User
from app.users.application.policies.user_policy import UserPolicy
from app.users.domain.value_objects import Rol

def test_user_policy_ver_perfil_propio():
    """
    Tests that a user can view their own profile.
    """
    user_id = uuid4()
    current_user = User(
        id=user_id,
        email="test@example.com",
        contrasena_hasheada="hashed_password",
        nombre="Test",
        apellidos="User",
        numero_telefono="123456789",
        apodo=None,
        rol=Rol.USUARIO
    )
    policy = UserPolicy()
    assert policy.ver_perfil(current_user, user_id) is True

def test_user_policy_ver_perfil_ajeno_no_admin():
    """
    Tests that a user cannot view another user's profile (without admin role).
    """
    current_user_id = uuid4()
    target_user_id = uuid4()
    current_user = User(
        id=current_user_id,
        email="test@example.com",
        contrasena_hasheada="hashed_password",
        nombre="Test",
        apellidos="User",
        numero_telefono="123456789",
        apodo=None,
        rol=Rol.USUARIO
    )
    policy = UserPolicy()
    assert policy.ver_perfil(current_user, target_user_id) is False

def test_user_policy_actualizar_perfil_propio():
    """
    Tests that a user can update their own profile.
    """
    user_id = uuid4()
    current_user = User(
        id=user_id,
        email="test@example.com",
        contrasena_hasheada="hashed_password",
        nombre="Test",
        apellidos="User",
        numero_telefono="123456789",
        apodo=None,
        rol=Rol.USUARIO
    )
    policy = UserPolicy()
    assert policy.actualizar_perfil(current_user, user_id) is True

def test_user_policy_actualizar_perfil_ajeno_no_admin():
    """
    Tests that a user cannot update another user's profile (without admin role).
    """
    current_user_id = uuid4()
    target_user_id = uuid4()
    current_user = User(
        id=current_user_id,
        email="test@example.com",
        contrasena_hasheada="hashed_password",
        nombre="Test",
        apellidos="User",
        numero_telefono="123456789",
        apodo=None,
        rol=Rol.USUARIO
    )
    policy = UserPolicy()
    assert policy.actualizar_perfil(current_user, target_user_id) is False

def test_user_policy_es_administrador_true():
    """
    Tests that the es_administrador method returns True for an admin user.
    """
    admin_user = User(
        id=uuid4(),
        email="admin@example.com",
        contrasena_hasheada="hashed_password",
        nombre="Admin",
        apellidos="User",
        numero_telefono="123456789",
        apodo=None,
        rol=Rol.ADMIN
    )
    policy = UserPolicy()
    assert policy.es_administrador(admin_user) is True

def test_user_policy_es_administrador_false():
    """
    Tests that the es_administrador method returns False for a non-admin user.
    """
    user = User(
        id=uuid4(),
        email="user@example.com",
        contrasena_hasheada="hashed_password",
        nombre="User",
        apellidos="Test",
        numero_telefono="123456789",
        apodo=None,
        rol=Rol.USUARIO
    )
    policy = UserPolicy()
    assert policy.es_administrador(user) is False

def test_user_policy_admin_ver_perfil_ajeno():
    """
    Tests that an admin user can view another user's profile.
    """
    current_user_id = uuid4()
    target_user_id = uuid4()
    admin_user = User(
        id=current_user_id,
        email="admin@example.com",
        contrasena_hasheada="hashed_password",
        nombre="Admin",
        apellidos="User",
        numero_telefono="123456789",
        apodo=None,
        rol=Rol.ADMIN
    )
    policy = UserPolicy()
    assert policy.ver_perfil(admin_user, target_user_id) is True