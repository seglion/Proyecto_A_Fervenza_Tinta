from fastapi import HTTPException, status

class PedidoException(HTTPException):
    def __init__(self, status_code: int, detail: str):
        super().__init__(status_code=status_code, detail=detail)

class TemporadaCerradaException(PedidoException):
    def __init__(self, detail: str = "No hay temporada de pedidos activa o está cerrada."):
        super().__init__(status_code=status.HTTP_409_CONFLICT, detail=detail)

class PedidoNoEncontradoException(PedidoException):
    def __init__(self, detail: str = "Pedido no encontrado."):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)

class PedidoNoValidoException(PedidoException):
    def __init__(self, detail: str = "El pedido no es válido para esta operación."):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)

class AccesoDenegadoException(PedidoException):
    def __init__(self, detail: str = "Acceso denegado."):
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail=detail)
