from fastapi import FastAPI, Depends
from app.core.database import Database, get_db
import asyncpg

app = FastAPI()

@app.on_event("startup")
async def startup():
    await Database.get_pool()

@app.on_event("shutdown")
async def shutdown():
    await Database.close_pool()

@app.get("/health")
async def health_check(db: asyncpg.Connection = Depends(get_db)):
    try:
        result = await db.fetchval("SELECT 1")
        if result == 1:
            return {"status": "ok", "database": "ok"}
        else:
            # This case is unlikely but good to have
            return {"status": "error", "database": "unexpected result"}
    except Exception:
        return {"status": "error", "database": "unavailable"}
