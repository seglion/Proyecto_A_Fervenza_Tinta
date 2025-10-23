from fastapi import HTTPException, status

class CuotaException(HTTPException):
    def __init__(self, status_code: int, detail: str):
        super().__init__(status_code=status_code, detail=detail)

class TemporadaNoEncontrada(CuotaException):
    def __init__(self, detail: str = "Season not found."):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)

class CuotaNoEncontrada(CuotaException):
    def __init__(self, detail: str = "Fee not found."):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)

class IntentoDePagoFallido(CuotaException):
    def __init__(self, detail: str = "Payment attempt failed."):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)

class EstadoDePagoNoValido(CuotaException):
    def __init__(self, detail: str = "Invalid payment state."):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)
