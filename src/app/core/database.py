import asyncpg
from app.core.config import settings

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
