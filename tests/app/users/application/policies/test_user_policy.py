import pytest
from uuid import uuid4
from app.users.domain.entities import User
from app.users.application.policies.user_policy import UserPolicy

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
        apodo=None
    )
    policy = UserPolicy()
    assert policy.ver_perfil(current_user, user_id) is True

def test_user_policy_ver_perfil_ajeno():
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
        apodo=None
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
        apodo=None
    )
    policy = UserPolicy()
    assert policy.actualizar_perfil(current_user, user_id) is True

def test_user_policy_actualizar_perfil_ajeno():
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
        apodo=None
    )
    policy = UserPolicy()
    assert policy.actualizar_perfil(current_user, target_user_id) is False
