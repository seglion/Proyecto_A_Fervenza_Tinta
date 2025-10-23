from fastapi import HTTPException, status

class UserException(HTTPException):
    def __init__(self, status_code: int, detail: str):
        super().__init__(status_code=status_code, detail=detail)

class UnauthorizedException(UserException):
    def __init__(self, detail: str = "Not authorized."):
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail=detail)

class UserNotFoundException(UserException):
    def __init__(self, detail: str = "User not found."):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)

class EmailAlreadyVerifiedException(UserException):
    def __init__(self, detail: str = "Email already verified."):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)

class InvalidCredentialsException(UserException):
    def __init__(self, detail: str = "Invalid credentials."):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail)

class AccountInactiveException(UserException):
    def __init__(self, detail: str = "Account is inactive."):
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail=detail)

class EmailNotVerifiedException(UserException):
    def __init__(self, detail: str = "Email not verified."):
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail=detail)

class UserAlreadyExistsException(UserException):
    def __init__(self, detail: str = "User with this email already exists."):
        super().__init__(status_code=status.HTTP_409_CONFLICT, detail=detail)

class InvalidOldPasswordException(UserException):
    def __init__(self, detail: str = "Invalid old password."):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)

class InvalidTokenException(UserException):
    def __init__(self, detail: str = "Invalid or expired token."):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)

class UserAlreadyApprovedException(UserException):
    def __init__(self, detail: str = "User is already approved."):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)
