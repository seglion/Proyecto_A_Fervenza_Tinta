from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID
from typing import List

from src.app.prendas.domain.value_objects import GeneroPrenda, TallaPrenda

@dataclass
class Prenda:
    id: UUID
    nombre: str
    descripcion: str
    precio: float
    imagen_url: str
    fecha_creacion: datetime
    variantes: List["VariantePrenda"] = field(default_factory=list)

@dataclass
class VariantePrenda:
    id: UUID
    prenda_id: UUID
    genero: GeneroPrenda
    talla: TallaPrenda
    fecha_creacion: datetime