import os
import pytest
from pydantic import BaseModel
from uuid import UUID, uuid4
from datetime import datetime

import src.app.prendas.application.dtos as dtos_module
from src.app.prendas.domain.value_objects import GeneroPrenda, TallaPrenda

def test_dtos_file_exists():
    file_path = "src/app/prendas/application/dtos.py"
    assert os.path.exists(file_path)
    assert os.path.isfile(file_path)

def test_prenda_dto_exists():
    assert hasattr(dtos_module, "PrendaDTO"), "La clase PrendaDTO no existe en el módulo"
    assert issubclass(dtos_module.PrendaDTO, BaseModel), "PrendaDTO no hereda de BaseModel"

def test_prenda_dto_attributes():
    prenda_dto = dtos_module.PrendaDTO(
        id=uuid4(),
        nombre="Camiseta",
        descripcion="Camiseta de algodón",
        precio=19.99,
        imagen_url="http://example.com/camiseta.jpg",
        fecha_creacion=datetime.now(),
        variantes=[]
    )
    assert hasattr(prenda_dto, "id")
    assert hasattr(prenda_dto, "nombre")
    assert hasattr(prenda_dto, "descripcion")
    assert hasattr(prenda_dto, "precio")
    assert hasattr(prenda_dto, "imagen_url")
    assert hasattr(prenda_dto, "fecha_creacion")
    assert hasattr(prenda_dto, "variantes")

def test_variante_prenda_dto_exists():
    assert hasattr(dtos_module, "VariantePrendaDTO"), "La clase VariantePrendaDTO no existe en el módulo"
    assert issubclass(dtos_module.VariantePrendaDTO, BaseModel), "VariantePrendaDTO no hereda de BaseModel"

def test_variante_prenda_dto_attributes():
    variante_dto = dtos_module.VariantePrendaDTO(
        id=uuid4(),
        prenda_id=uuid4(),
        genero=GeneroPrenda.HOMBRE,
        talla=TallaPrenda.M,
        fecha_creacion=datetime.now()
    )
    assert hasattr(variante_dto, "id")
    assert hasattr(variante_dto, "prenda_id")
    assert hasattr(variante_dto, "genero")
    assert hasattr(variante_dto, "talla")
    assert hasattr(variante_dto, "fecha_creacion")