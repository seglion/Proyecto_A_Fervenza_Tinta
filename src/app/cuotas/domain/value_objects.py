from enum import Enum

class EstadoPago(Enum):
    PENDIENTE = "pendiente"
    COMPLETADO = "completado"
    FALLIDO = "fallido"

class MetodoPago(Enum):
    STRIPE = "STRIPE"
    EFECTIVO = "EFECTIVO"
    TRANSFERENCIA_MANUAL = "TRANSFERENCIA_MANUAL"

# The class `NombreTipoCuota` is a Python enumeration that extends `str` and represents a specific
# type of fee.
class NombreTipoCuota(str, Enum):
    ALTA = "ALTA"
    SOCIO = "SOCIO"
