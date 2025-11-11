from fastapi import HTTPException, status

class UserException(HTTPException):
    def __init__(self, status_code: int, detail: str):
        super().__init__(status_code=status_code, detail=detail)

class UnauthorizedException(UserException):
    def __init__(self, detail: str = "apiErrors.unauthorized"):
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail=detail)

class UserNotFoundException(UserException):
    def __init__(self, detail: str = "apiErrors.userNotFound"):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)

class EmailAlreadyVerifiedException(UserException):
    def __init__(self, detail: str = "apiErrors.emailAlreadyVerified"):
        super().__init__(status_code=status.HTTP_409_CONFLICT, detail=detail)

class InvalidCredentialsException(UserException):
    def __init__(self, detail: str = "apiErrors.invalidCredentials"):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail)

class AccountInactiveException(UserException):
    def __init__(self, detail: str = "apiErrors.accountInactive"):
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail=detail)

class EmailNotVerifiedException(UserException):
    def __init__(self, detail: str = "apiErrors.emailNotVerified"):
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail=detail)

class UserAlreadyExistsException(UserException):
    def __init__(self, detail: str = "apiErrors.userAlreadyExists"):
        super().__init__(status_code=status.HTTP_409_CONFLICT, detail=detail)

class InvalidOldPasswordException(UserException):
    def __init__(self, detail: str = "apiErrors.invalidOldPassword"):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)

class InvalidTokenException(UserException):
    def __init__(self, detail: str = "apiErrors.invalidToken"):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)

class UserAlreadyApprovedException(UserException):
    def __init__(self, detail: str = "apiErrors.userAlreadyApproved"):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)