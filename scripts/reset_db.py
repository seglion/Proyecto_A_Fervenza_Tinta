'''
This script completely resets the public schema in the PostgreSQL database.
WARNING: This is a destructive operation and will delete all data.
'''
import asyncio
import sqlalchemy as sa
from sqlalchemy.ext.asyncio import create_async_engine


from src.app.core.config import settings


RESET_SCHEMA_SQL = """
DROP SCHEMA public CASCADE;
CREATE SCHEMA public;
GRANT ALL ON SCHEMA public TO CURRENT_USER;
GRANT ALL ON SCHEMA public TO public;
COMMENT ON SCHEMA public IS 'standard public schema';
"""

async def main():
    '''
    Connects to the database and completely resets the 'public' schema.
    '''
    print(f"Connecting to database to reset it...")

    db_url = str(settings.DATABASE_URL)
    if db_url.startswith("postgresql://"):
        db_url = db_url.replace("postgresql://", "postgresql+asyncpg://", 1)

    engine = create_async_engine(db_url, isolation_level="AUTOCOMMIT")

    async with engine.connect() as conn:
        print("Executing schema reset commands one by one...")
        sql_commands = [cmd.strip() for cmd in RESET_SCHEMA_SQL.split(';') if cmd.strip()]
        for command in sql_commands:
            print(f"  - Executing: {command};")
            await conn.execute(sa.text(command))
        print("Database schema 'public' has been reset successfully.")

    await engine.dispose()
    print("Connection closed.")

if __name__ == "__main__":
    print("--- Starting Database Reset Script ---")
    print("WARNING: This is a destructive operation and will delete all data in the public schema.")
    asyncio.run(main())
    print("--- Database Reset Script Finished ---")
