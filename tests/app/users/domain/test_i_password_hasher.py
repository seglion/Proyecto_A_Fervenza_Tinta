import pytest
from abc import ABC
from app.core.security.i_password_hasher import IPasswordHasher

def test_password_hasher_interface_file_exists():
    """
    Tests if the password hasher interface file exists.
    """
    try:
        from app.core.security import i_password_hasher
    except ImportError:
        pytest.fail("Password hasher interface file does not exist: src/app/core/security/i_password_hasher.py")

def test_password_hasher_interface_class_exists():
    """
    Tests if the IPasswordHasher class exists in the interface file.
    """
    try:
        from app.core.security.i_password_hasher import IPasswordHasher
        assert issubclass(IPasswordHasher, ABC)
    except ImportError:
        pytest.fail("IPasswordHasher class does not exist in i_password_hasher.py")

def test_ipasswordhasher_has_hash_method():
    """
    Tests if the IPasswordHasher interface has a 'hash' abstract method.
    """
    assert hasattr(IPasswordHasher, 'hash')
    assert 'password' in IPasswordHasher.hash.__annotations__
    assert IPasswordHasher.hash.__annotations__['password'] == str
    assert IPasswordHasher.hash.__annotations__['return'] == str

def test_ipasswordhasher_has_verify_method():
    """
    Tests if the IPasswordHasher interface has a 'verify' abstract method.
    """
    assert hasattr(IPasswordHasher, 'verify')
    assert 'password' in IPasswordHasher.verify.__annotations__
    assert 'hashed_password' in IPasswordHasher.verify.__annotations__
    assert IPasswordHasher.verify.__annotations__['hashed_password'] == str
    assert IPasswordHasher.verify.__annotations__['return'] == bool
