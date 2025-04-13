from sqlalchemy.ext.asyncio import AsyncSession
from app.models.table import Table

async def create_table(db: AsyncSession, table_data: dict):
    table = Table(**table_data)
    db.add(table)
    await db.commit()
    await db.refresh(table)
    return table

async def get_tables(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(select(Table).offset(skip).limit(limit))
    return result.scalars().all()

async def delete_table(db: AsyncSession, table_id: int):
    table = await db.get(Table, table_id)
    if table:
        await db.delete(table)
        await db.commit()
        return True
    return False