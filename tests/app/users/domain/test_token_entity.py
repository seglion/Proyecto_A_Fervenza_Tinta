import pytest
from uuid import UUID, uuid4
from datetime import datetime, timezone, timedelta
from typing import Optional

from app.users.domain.entities import Token
from app.users.domain.value_objects import TipoToken

def test_token_creation():
    """
    Tests that a Token object can be created with all required fields.
    """
    token = Token(
        id=uuid4(),
        usuario_id=uuid4(),
        hash_token="some_hash",
        tipo_token=TipoToken.VERIFICACION_EMAIL,
        fecha_expiracion=datetime.now(timezone.utc) + timedelta(hours=1)
    )
    assert isinstance(token, Token)
    assert isinstance(token.id, UUID)
    assert isinstance(token.usuario_id, UUID)
    assert token.hash_token == "some_hash"
    assert token.tipo_token == TipoToken.VERIFICACION_EMAIL
    assert isinstance(token.fecha_expiracion, datetime)
    assert token.es_valido is True
    assert isinstance(token.fecha_creacion, datetime)

def test_token_has_id_attribute():
    """
    Tests if the Token class has an 'id' attribute with the correct type.
    """
    assert 'id' in Token.__annotations__
    assert Token.__annotations__['id'] == UUID

def test_token_has_usuario_id_attribute():
    """
    Tests if the Token class has a 'usuario_id' attribute with the correct type.
    """
    assert 'usuario_id' in Token.__annotations__
    assert Token.__annotations__['usuario_id'] == UUID

def test_token_has_hash_token_attribute():
    """
    Tests if the Token class has a 'hash_token' attribute with the correct type.
    """
    assert 'hash_token' in Token.__annotations__
    assert Token.__annotations__['hash_token'] == str

def test_token_has_tipo_token_attribute():
    """
    Tests if the Token class has a 'tipo_token' attribute with the correct type.
    """
    assert 'tipo_token' in Token.__annotations__
    assert Token.__annotations__['tipo_token'] == TipoToken

def test_token_has_fecha_expiracion_attribute():
    """
    Tests if the Token class has a 'fecha_expiracion' attribute with the correct type.
    """
    assert 'fecha_expiracion' in Token.__annotations__
    assert Token.__annotations__['fecha_expiracion'] == datetime

def test_token_es_valido_defaults_to_true():
    """Tests that a new token defaults to es_valido=True."""
    token = Token(
        id=uuid4(),
        usuario_id=uuid4(),
        tipo_token=TipoToken.VERIFICACION_EMAIL,
        hash_token="some_hash",
        fecha_expiracion=datetime.now(timezone.utc) + timedelta(days=1)
    )
    assert token.es_valido is True

def test_token_has_fecha_creacion_attribute():
    """
    Tests if the Token class has a 'fecha_creacion' attribute with the correct type.
    """
    assert 'fecha_creacion' in Token.__annotations__
    assert Token.__annotations__['fecha_creacion'] == datetime

def test_token_fecha_creacion_defaults_to_utcnow():
    """Tests that a new token defaults to fecha_creacion being a datetime object."""
    token = Token(
        id=uuid4(),
        usuario_id=uuid4(),
        tipo_token=TipoToken.VERIFICACION_EMAIL,
        hash_token="some_hash",
        fecha_expiracion=datetime.now(timezone.utc) + timedelta(days=1)
    )
    assert isinstance(token.fecha_creacion, datetime)
    assert token.fecha_creacion.tzinfo is not None
