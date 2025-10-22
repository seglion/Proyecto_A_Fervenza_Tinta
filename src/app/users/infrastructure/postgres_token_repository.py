from typing import Optional
import asyncpg

from app.users.application.repositories.i_token_repository import ITokenRepository
from app.users.domain.entities import Token
from app.users.domain.value_objects import TipoToken


class PostgresTokenRepository(ITokenRepository):
    def __init__(self, db_connection: asyncpg.Connection):
        self.db_connection = db_connection

    async def crear(self, token: Token) -> Token:
        query = """
        INSERT INTO tokens (id, usuario_id, hash_token, tipo_token, fecha_expiracion, es_valido, fecha_creacion)
        VALUES ($1, $2, $3, $4::tipotoken, $5, $6, $7)
        """
        await self.db_connection.execute(
            query,
            token.id,
            token.usuario_id,
            token.hash_token,
            token.tipo_token.value,
            token.fecha_expiracion,
            token.es_valido,
            token.fecha_creacion
        )
        return token

    async def buscar_por_hash(self, hash_token: str) -> Optional[Token]:
        query = "SELECT * FROM tokens WHERE hash_token = $1"
        row = await self.db_connection.fetchrow(query, hash_token)
        if row:
            return Token(
                id=row['id'],
                usuario_id=row['usuario_id'],
                hash_token=row['hash_token'],
                tipo_token=TipoToken(row['tipo_token']),
                fecha_expiracion=row['fecha_expiracion'],
                es_valido=row['es_valido'],
                fecha_creacion=row['fecha_creacion']
            )
        return None

    async def actualizar(self, token: Token) -> Token:
        query = """
        UPDATE tokens
        SET es_valido = $2
        WHERE id = $1
        """
        await self.db_connection.execute(query, token.id, token.es_valido)
        return token

    async def invalidar_token(self, refresh_token_hash: str) -> None:
        query = """
        UPDATE tokens
        SET es_valido = FALSE
        WHERE hash_token = $1
        """
        await self.db_connection.execute(query, refresh_token_hash)
