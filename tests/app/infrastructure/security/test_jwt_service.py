import pytest
from app.core.services.i_jwt_service import IJWTService
from app.infrastructure.security.jwt_service import JWTService
from app.core.config import settings
from uuid import uuid4

SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"

def test_jwt_service_file_exists():
    """
    Tests if the jwt service file exists.
    """
    try:
        from app.infrastructure.security import jwt_service
    except ImportError:
        pytest.fail("File does not exist: src/app/infrastructure/security/jwt_service.py")

def test_jwt_service_class_exists():
    """
    Tests if the JWTService class exists in the file.
    """
    try:
        from app.infrastructure.security.jwt_service import JWTService
    except ImportError:
        pytest.fail("JWTService class does not exist in jwt_service.py")

def test_jwt_service_implements_interface():
    """
    Tests that JWTService implements the IJWTService interface.
    """
    assert issubclass(JWTService, IJWTService)

def test_jwt_service_generar_y_validar_tokens():
    """
    Tests that tokens are generated and can be validated successfully.
    """
    jwt_service = JWTService(
        secret_key=SECRET_KEY,
        algorithm=ALGORITHM,
        access_token_expire_minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES,
        refresh_token_expire_days=settings.REFRESH_TOKEN_EXPIRE_DAYS
    )
    user_id = uuid4()
    roles = ["user", "admin"]

    access_token, refresh_token = jwt_service.generar_tokens(user_id, roles)

    assert isinstance(access_token, str)
    assert isinstance(refresh_token, str)

    # Validate access token
    decoded_user_id = jwt_service.validar_access_token(access_token)
    assert decoded_user_id == user_id

    # Validate refresh token
    decoded_user_id_refresh = jwt_service.validar_refresh_token(refresh_token)
    assert decoded_user_id_refresh == user_id
