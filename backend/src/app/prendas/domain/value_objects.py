from enum import Enum

class GeneroPrenda(str, Enum):
    HOMBRE = "HOMBRE"
    MUJER = "MUJER"
    UNISEX = "UNISEX"

class TallaPrenda(str, Enum):
    XS = "XS"
    S = "S"
    M = "M"
    L = "L"
    XL = "XL"
    UNICA = "UNICA"