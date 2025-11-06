from enum import Enum

class EstadoPago(Enum):
    PENDIENTE = "pendiente"
    COMPLETADO = "completado"
    FALLIDO = "fallido"

class MetodoPago(Enum):
    STRIPE = "STRIPE"
    EFECTIVO = "EFECTIVO"
    TRANSFERENCIA_MANUAL = "TRANSFERENCIA_MANUAL"


class NombreTipoCuota(str, Enum):
    ALTA = "ALTA"
    SOCIO = "SOCIO"
