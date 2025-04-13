from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.table import Table, TableCreate
from app.services.table_service import create_table, get_tables, delete_table
from app.core.database import get_db

router = APIRouter(prefix="/tables", tags=["tables"])

@router.post("/", response_model=Table)
async def create_new_table(table: TableCreate, db: AsyncSession = Depends(get_db)):
    return await create_table(db, table.dict())

@router.get("/", response_model=list[Table])
async def read_tables(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    tables = await get_tables(db, skip=skip, limit=limit)
    return tables

@router.delete("/{table_id}")
async def remove_table(table_id: int, db: AsyncSession = Depends(get_db)):
    success = await delete_table(db, table_id)
    if not success:
        raise HTTPException(status_code=404, detail="Table not found")
    return {"message": "Table deleted successfully"}