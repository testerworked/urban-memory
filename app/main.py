from fastapi import FastAPI
from app.models.base import Base
from app.core.database import engine
import asyncio


app = FastAPI()

async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.on_event("startup")
async def startup_event():
    await create_tables()


from app.routers import tables, reservations

app.include_router(tables.router)
app.include_router(reservations.router)