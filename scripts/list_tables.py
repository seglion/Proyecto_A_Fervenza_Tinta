import asyncio
import asyncpg
from src.app.core.config import settings

async def list_tables():
    conn = None
    try:
        conn = await asyncpg.connect(settings.DATABASE_URL)
        tables = await conn.fetch("SELECT tablename FROM pg_tables WHERE schemaname = 'public';")
        print("Tables in public schema:")
        for table in tables:
            print(f"- {table['tablename']}")
    except Exception as e:
        print(f"Error connecting to database or listing tables: {e}")
    finally:
        if conn:
            await conn.close()

if __name__ == "__main__":
    asyncio.run(list_tables())
