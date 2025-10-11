import pytest
from app.core.security.i_password_hasher import IPasswordHasher
from app.infrastructure.security.argon2_password_hasher import Argon2PasswordHasher

def test_argon2_password_hasher_file_exists():
    """
    Tests if the argon2 password hasher file exists.
    """
    try:
        from app.infrastructure.security import argon2_password_hasher
    except ImportError:
        pytest.fail("File does not exist: src/app/infrastructure/security/argon2_password_hasher.py")

def test_argon2_password_hasher_class_exists():
    """
    Tests if the Argon2PasswordHasher class exists in the file.
    """
    try:
        from app.infrastructure.security.argon2_password_hasher import Argon2PasswordHasher
    except ImportError:
        pytest.fail("Argon2PasswordHasher class does not exist in argon2_password_hasher.py")

def test_argon2_password_hasher_implements_interface():
    """
    Tests that Argon2PasswordHasher implements the IPasswordHasher interface.
    """
    assert issubclass(Argon2PasswordHasher, IPasswordHasher)

def test_argon2_password_hasher_hash_and_verify():
    """
    Tests that the hash and verify methods work correctly.
    """
    password_hasher = Argon2PasswordHasher()
    password = "password123"
    hashed_password = password_hasher.hash(password)

    assert isinstance(hashed_password, str)
    assert password_hasher.verify(password, hashed_password) is True
    assert password_hasher.verify("wrong_password", hashed_password) is False
