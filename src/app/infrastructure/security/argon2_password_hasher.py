from app.core.security.i_password_hasher import IPasswordHasher
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

ph = PasswordHasher()

class Argon2PasswordHasher(IPasswordHasher):
    def hash(self, password: str) -> str:
        return ph.hash(password)

    def verify(self, password: str, hashed_password: str) -> bool:
        try:
            ph.verify(hashed_password, password)
            return True
        except VerifyMismatchError:
            return False
