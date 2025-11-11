from fastapi import HTTPException, status

class CuotaException(HTTPException):
    def __init__(self, status_code: int, detail: str):
        super().__init__(status_code=status_code, detail=detail)

class UnauthorizedException(CuotaException):
    def __init__(self, detail: str = "apiErrors.unauthorized"):
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail=detail)

class TemporadaNoEncontrada(CuotaException):
    def __init__(self, detail: str = "apiErrors.seasonNotFound"):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)

class TipoCuotaNoEncontrado(CuotaException):
    def __init__(self, detail: str = "apiErrors.feeTypeNotFound"):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)

class CuotaNoEncontrada(CuotaException):
    def __init__(self, detail: str = "apiErrors.feeNotFound"):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)

class IntentoDePagoFallido(CuotaException):
    def __init__(self, detail: str = "apiErrors.paymentAttemptFailed"):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)

class EstadoDePagoNoValido(CuotaException):
    def __init__(self, detail: str = "apiErrors.invalidPaymentState"):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)

class CuotaYaPagadaException(CuotaException):
    def __init__(self, detail: str = "apiErrors.feeAlreadyPaid"):
        super().__init__(status_code=status.HTTP_409_CONFLICT, detail=detail)