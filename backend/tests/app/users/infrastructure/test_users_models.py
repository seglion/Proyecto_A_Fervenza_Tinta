import pytest
from app.users.infrastructure.models import UsuarioModel

# 1. Test para asegurar que el módulo de modelos existe
def test_models_module_exists():
    from app.users.infrastructure import models
    assert models is not None

# 2. Test para asegurar que la clase UsuarioModel existe
def test_usuario_model_class_exists():
    assert UsuarioModel is not None

# 3. Test para verificar que el tablename se genera correctamente
def test_usuario_model_has_correct_tablename():
    assert UsuarioModel.__tablename__ == "usuarios"

# 4. Test para verificar que la columna 'id' es la clave primaria
def test_usuario_model_has_id_primary_key():
    assert 'id' in UsuarioModel.__table__.c
    assert UsuarioModel.__table__.c.id.primary_key is True
