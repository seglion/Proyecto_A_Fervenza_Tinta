from fastapi import HTTPException, status

class PrendaException(HTTPException):
    def __init__(self, status_code: int, detail: str):
        super().__init__(status_code=status_code, detail=detail)

class NotAuthorizedError(PrendaException):
    def __init__(self, detail: str = "apiErrors.notAuthorized"):
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail=detail)

class PrendaNotFoundError(PrendaException):
    def __init__(self, detail: str = "apiErrors.garmentNotFound"):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)
        
class UnauthorizedException(PrendaException):
    def __init__(self, detail: str = "apiErrors.notAuthorized"):
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail=detail)