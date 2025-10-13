from fastapi import FastAPI
from app.core.database import Database

app = FastAPI()

@app.on_event("startup")
async def startup():
    await Database.get_pool()

@app.on_event("shutdown")
async def shutdown():
    await Database.close_pool()
