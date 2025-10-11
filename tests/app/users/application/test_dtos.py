import pytest
from pydantic import BaseModel, EmailStr
from uuid import UUID
from typing import Optional, List

def test_dtos_file_exists():
    """
    Tests if the dtos file exists.
    """
    try:
        from app.users.application import dtos
    except ImportError:
        pytest.fail("DTOs file does not exist: src/app/users/application/dtos.py")

def test_registrar_usuario_dto_exists():
    """
    Tests if the RegistrarUsuarioDTO class exists and has the correct fields.
    """
    try:
        from app.users.application.dtos import RegistrarUsuarioDTO
        assert issubclass(RegistrarUsuarioDTO, BaseModel)
        # Check for required fields
        assert RegistrarUsuarioDTO.model_fields['email'].annotation == EmailStr
        assert RegistrarUsuarioDTO.model_fields['contrasena'].is_required()
        assert RegistrarUsuarioDTO.model_fields['numero_telefono'].is_required()
        assert RegistrarUsuarioDTO.model_fields['nombre'].is_required()
        assert RegistrarUsuarioDTO.model_fields['apellidos'].is_required()
        # Check for optional field
        assert not RegistrarUsuarioDTO.model_fields['apodo'].is_required()
    except (ImportError, KeyError):
        pytest.fail("RegistrarUsuarioDTO class does not exist or is misconfigured in dtos.py")

def test_usuario_creado_dto_exists():
    """
    Tests if the UsuarioCreadoDTO class exists and has the correct fields.
    """
    try:
        from app.users.application.dtos import UsuarioCreadoDTO
        assert issubclass(UsuarioCreadoDTO, BaseModel)
        assert UsuarioCreadoDTO.model_fields['id'].annotation == UUID
        assert UsuarioCreadoDTO.model_fields['email'].annotation == EmailStr
    except (ImportError, KeyError):
        pytest.fail("UsuarioCreadoDTO class does not exist or is misconfigured in dtos.py")

def test_tokens_dto_exists():
    """
    Tests if the TokensDTO class exists and has the correct fields.
    """
    try:
        from app.users.application.dtos import TokensDTO
        assert issubclass(TokensDTO, BaseModel)
        assert TokensDTO.model_fields['access_token'].annotation == str
        assert TokensDTO.model_fields['refresh_token'].annotation == str
        assert TokensDTO.model_fields['token_type'].annotation == str
    except (ImportError, KeyError):
        pytest.fail("TokensDTO class does not exist or is misconfigured in dtos.py")

def test_usuario_response_dto_exists():
    """
    Tests if the UsuarioResponseDTO class exists and has the correct fields.
    """
    try:
        from app.users.application.dtos import UsuarioResponseDTO
        assert issubclass(UsuarioResponseDTO, BaseModel)
        assert UsuarioResponseDTO.model_fields['id'].annotation == UUID
        assert UsuarioResponseDTO.model_fields['email'].annotation == EmailStr
        assert UsuarioResponseDTO.model_fields['nombre'].annotation == str
        assert UsuarioResponseDTO.model_fields['apellidos'].annotation == str
        assert not UsuarioResponseDTO.model_fields['apodo'].is_required()
        assert UsuarioResponseDTO.model_fields['numero_telefono'].annotation == str
        assert not UsuarioResponseDTO.model_fields['url_avatar'].is_required()
        assert UsuarioResponseDTO.model_fields['esta_activo'].annotation == bool
        assert UsuarioResponseDTO.model_fields['roles'].annotation == List[str]
    except (ImportError, KeyError):
        pytest.fail("UsuarioResponseDTO class does not exist or is misconfigured in dtos.py")

def test_actualizar_mi_perfil_dto_exists():
    """
    Tests if the ActualizarMiPerfilDTO class exists and has the correct optional fields.
    """
    try:
        from app.users.application.dtos import ActualizarMiPerfilDTO
        assert issubclass(ActualizarMiPerfilDTO, BaseModel)
        assert not ActualizarMiPerfilDTO.model_fields['nombre'].is_required()
        assert not ActualizarMiPerfilDTO.model_fields['apellidos'].is_required()
        assert not ActualizarMiPerfilDTO.model_fields['apodo'].is_required()
        assert not ActualizarMiPerfilDTO.model_fields['numero_telefono'].is_required()
        assert not ActualizarMiPerfilDTO.model_fields['url_avatar'].is_required()
    except (ImportError, KeyError):
        pytest.fail("ActualizarMiPerfilDTO class does not exist or is misconfigured in dtos.py")

def test_cambiar_contrasena_dto_exists():
    """
    Tests if the CambiarContrasenaDTO class exists and has the correct fields.
    """
    try:
        from app.users.application.dtos import CambiarContrasenaDTO
        assert issubclass(CambiarContrasenaDTO, BaseModel)
        assert CambiarContrasenaDTO.model_fields['contrasena_antigua'].is_required()
        assert CambiarContrasenaDTO.model_fields['contrasena_nueva'].is_required()
    except (ImportError, KeyError):
        pytest.fail("CambiarContrasenaDTO class does not exist or is misconfigured in dtos.py")
