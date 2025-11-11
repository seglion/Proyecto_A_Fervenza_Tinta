from fastapi import HTTPException, status

class PedidoException(HTTPException):
    def __init__(self, status_code: int, detail: str):
        super().__init__(status_code=status_code, detail=detail)

class TemporadaPedidoNoActivaException(PedidoException):
    def __init__(self, detail: str = "apiErrors.orderSeasonNotActive"):
        super().__init__(status_code=status.HTTP_409_CONFLICT, detail=detail)

class PedidoNoEncontradoException(PedidoException):
    def __init__(self, detail: str = "apiErrors.orderNotFound"):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)

class LineaDePedidoNoEncontradaException(PedidoException):
    def __init__(self, detail: str = "apiErrors.orderLineNotFound"):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)

class PedidoNoModificableException(PedidoException):
    def __init__(self, detail: str = "apiErrors.orderNotModifiable"):
        super().__init__(status_code=status.HTTP_409_CONFLICT, detail=detail)

class VariantePrendaNoEncontradaException(PedidoException):
    def __init__(self, detail: str = "apiErrors.garmentVariantNotFound"):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)

class CantidadInvalidaException(PedidoException):
    def __init__(self, detail: str = "apiErrors.invalidQuantity"):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)

class PedidoVacioException(PedidoException):
    def __init__(self, detail: str = "apiErrors.emptyOrder"):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)

class MetodoPagoInvalidoException(PedidoException):
    def __init__(self, detail: str = "apiErrors.invalidPaymentMethod"):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)

class AccesoDenegadoException(PedidoException):
    def __init__(self, detail: str = "apiErrors.accessDenied"):
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail=detail)

class TemporadaCerradaException(PedidoException):
    def __init__(self, detail: str = "apiErrors.orderSeasonClosed"):
        super().__init__(status_code=status.HTTP_409_CONFLICT, detail=detail)
        
class TemporadaPedidoNoEncontradaException(PedidoException):
    def __init__(self, detail: str = "apiErrors.orderSeasonNotFound"):
        super().__init__(status_code=status.HTTP_4G04_NOT_FOUND, detail=detail)