from dotenv import load_dotenv; load_dotenv()

from fastapi import FastAPI, Depends
from app.core.database import Database, get_db
import asyncpg
import typing # Import typing
from app.users.presentation.router import router as users_router
from app.users.presentation.admin_router import router as admin_router
from app.cuotas.presentation.router import router as cuotas_router
app = FastAPI()

app.include_router(users_router)
app.include_router(admin_router)
app.include_router(cuotas_router)
@app.on_event("startup")
async def startup():
    await Database.get_pool()

@app.on_event("shutdown")
async def shutdown():
    await Database.close_pool()

@app.get("/health")
async def health_check(db: typing.Any = Depends(get_db)): # Changed type hint to typing.Any
    try:
        result = await db.fetchval("SELECT 1")
        if result == 1:
            return {"status": "ok", "database": "ok"}
        else:
            # This case is unlikely but good to have
            return {"status": "error", "database": "unexpected result"}
    except Exception:
        return {"status": "error", "database": "unavailable"}
