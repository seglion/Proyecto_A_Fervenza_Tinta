from enum import Enum

class EstadoPago(Enum):
    PENDIENTE = "pendiente"
    COMPLETADO = "completado"
    FALLIDO = "fallido"

class MetodoPago(Enum):
    STRIPE = "stripe"
    EFECTIVO = "efectivo"
