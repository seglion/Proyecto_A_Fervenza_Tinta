from fastapi import HTTPException, status

class PedidoException(HTTPException):
    def __init__(self, status_code: int, detail: str):
        super().__init__(status_code=status_code, detail=detail)

class TemporadaPedidoNoActivaException(PedidoException):
    def __init__(self, detail: str = "No hay temporada de pedidos activa en este momento."):
        super().__init__(status_code=status.HTTP_409_CONFLICT, detail=detail)

class PedidoNoEncontradoException(PedidoException):
    def __init__(self, detail: str = "Pedido no encontrado."):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)

class LineaDePedidoNoEncontradaException(PedidoException):
    def __init__(self, detail: str = "Línea de pedido no encontrada."):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)

class PedidoNoModificableException(PedidoException):
    def __init__(self, detail: str = "El pedido no se puede modificar en su estado actual."):
        super().__init__(status_code=status.HTTP_409_CONFLICT, detail=detail)

class VariantePrendaNoEncontradaException(PedidoException):
    def __init__(self, detail: str = "Variante de prenda no encontrada."):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)

class CantidadInvalidaException(PedidoException):
    def __init__(self, detail: str = "La cantidad de la prenda debe ser mayor que cero."):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)

class PedidoVacioException(PedidoException):
    def __init__(self, detail: str = "El pedido no puede estar vacío para confirmar."):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)

class MetodoPagoInvalidoException(PedidoException):
    def __init__(self, detail: str = "Método de pago inválido para esta operación."):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)

class AccesoDenegadoException(PedidoException):
    def __init__(self, detail: str = "Acceso denegado. No tiene permisos para realizar esta acción."):
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail=detail)

class TemporadaCerradaException(PedidoException):
    def __init__(self, detail: str = "La temporada de pedidos está cerrada."):
        super().__init__(status_code=status.HTTP_409_CONFLICT, detail=detail)
class TemporadaPedidoNoEncontradaException(PedidoException):
    def __init__(self, detail: str = "La temporada de pedidos no encontrada."):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)