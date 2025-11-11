from app.users.application.repositories.i_token_repository import ITokenRepository
from app.users.application.repositories.i_user_repository import IUserRepository
from app.core.security.i_password_hasher import IPasswordHasher

from app.users.domain.value_objects import TipoToken, Password
from datetime import datetime, timezone
import hashlib

from app.users.application.exceptions import InvalidTokenException, UserNotFoundException
class ConfirmarNuevaContrasenaUseCase:
    def __init__(
        self,
        token_repository: ITokenRepository,
        user_repository: IUserRepository,
        password_hasher: IPasswordHasher
    ):
        self.token_repository = token_repository
        self.user_repository = user_repository
        self.password_hasher = password_hasher

    async def execute(self, token_texto_plano: str, nueva_contrasena_str: str) -> None:
        try:
            hashed_token = hashlib.sha256(token_texto_plano.encode()).hexdigest()
            token = await self.token_repository.buscar_por_hash(hashed_token)

            # 1. Validación del token (esto ya estaba bien)
            if not token or token.tipo_token != TipoToken.RESETEO_CONTRASENA or not token.es_valido or token.fecha_expiracion < datetime.now(timezone.utc):
                if token and token.es_valido:
                    token.es_valido = False
                    await self.token_repository.actualizar(token)
                raise InvalidTokenException()

            # 2. Validación del usuario (esto ya estaba bien)
            user = await self.user_repository.buscar_por_id(token.usuario_id)
            if not user:
                token.es_valido = False
                await self.token_repository.actualizar(token)
                raise UserNotFoundException()

            # 3. Validación de la contraseña (esto puede fallar si es muy corta)
            # (Si Password.create lanza un ValueError, el 'except Exception' de abajo lo atrapará)
            password_vo = Password.create(nueva_contrasena_str)

            # 4. Hashing de la nueva contraseña (Argon2)
            hashed_new_password = self.password_hasher.hash(password_vo.value)

            # 5. Actualización en BBDD
            await self.user_repository.actualizar_contrasena(user.id, hashed_new_password)

            # 6. Invalidación del token
            token.es_valido = False
            await self.token_repository.actualizar(token)

        # --- ¡AQUÍ ESTÁ LA CORRECCIÓN! ---

        # 7. Relanza las excepciones conocidas que tu router espera (400, 404)
        except (InvalidTokenException, UserNotFoundException) as e:
            raise e
        
        # 8. Atrapa CUALQUIER OTRO error (ValueError de Password.create, error de BBDD, etc.)
        except Exception as e:
            # Imprime el error real en tu log de backend para depurar
            print(f"Error inesperado en reseteo: {e}") 
            
            # Lanza una excepción que tu router SÍ entienda
            # Esto devolverá un error 400 con el mensaje genérico traducible
            raise InvalidTokenException(detail="apiErrors.genericError")
