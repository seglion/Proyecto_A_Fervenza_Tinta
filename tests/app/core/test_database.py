import pytest
from sqlalchemy.orm import declarative_base

# Suponemos que nuestra CustomBase estará en app.core.database
# Esta importación fallará al principio
from app.core.database import Base


# 1. Test para verificar que la base personalizada genera bien el nombre de la tabla
def test_custom_base_generates_tablename():
    # Arrange: Creamos una clase de modelo de prueba que hereda de nuestra Base
    class ProductoModel(Base):
        # No definimos __tablename__ a propósito
        __abstract__ = True # Para que SQLAlchemy no intente mapearla realmente
        pass

    # Act: Accedemos al nombre de la tabla generado
    table_name = ProductoModel.__tablename__

    # Assert: Comprobamos que el nombre es el esperado
    assert table_name == "productos"
