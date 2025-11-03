from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, ConfigDict
from src.app.prendas.domain.value_objects import GeneroPrenda, TallaPrenda
from src.app.users.domain.value_objects import Rol


class UsuarioPolicyDTO(BaseModel):
    rol: Rol
    esta_activo: bool

    model_config = ConfigDict(from_attributes=True)


class CrearPrendaDTO(BaseModel):
    nombre: str
    descripcion: str
    precio: float
    imagen_url: str


class PrendaCreadaDTO(BaseModel):
    id: UUID


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