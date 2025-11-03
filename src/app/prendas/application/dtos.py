from datetime import datetime
from uuid import UUID
from pydantic import BaseModel
from src.app.prendas.domain.value_objects import GeneroPrenda, TallaPrenda


class VariantePrendaDTO(BaseModel):
    id: UUID
    prenda_id: UUID
    genero: GeneroPrenda
    talla: TallaPrenda
    fecha_creacion: datetime


class PrendaDTO(BaseModel):
    id: UUID
    nombre: str
    descripcion: str
    precio: float
    imagen_url: str
    fecha_creacion: datetime
    variantes: list[VariantePrendaDTO]