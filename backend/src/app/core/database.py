import asyncpg
from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.declarative import declared_attr

from app.core.config import settings

class CustomBase:
    @declared_attr
    def __tablename__(cls) -> str:
        # Quita el sufijo 'Model' del nombre de la clase
        name = cls.__name__.removesuffix('Model')
        # Convierte a minúsculas
        name = name.lower()
        # Pluraliza (de forma simple)
        if not name.endswith('s'):
            name += 's'
        return name

# Crea la base declarativa usando nuestra clase personalizada
Base = declarative_base(cls=CustomBase)


class Database:
    _pool = None

    @classmethod
    async def get_pool(cls):
        if cls._pool is None:
            cls._pool = await asyncpg.create_pool(settings.DATABASE_URL)
        return cls._pool

    @classmethod
    async def close_pool(cls):
        if cls._pool:
            await cls._pool.close()
            cls._pool = None

async def get_db() -> asyncpg.Connection:
    pool = await Database.get_pool()
    async with pool.acquire() as connection:
        yield connection
