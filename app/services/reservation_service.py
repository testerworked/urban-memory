from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from fastapi import HTTPException, status
from app.models.reservation import Reservation
from app.models.table import Table
from sqlalchemy import func

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, cast, Integer
from sqlalchemy.sql.expression import text
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, bindparam
from fastapi import HTTPException, status
from app.models.reservation import Reservation

async def create_reservation(db: AsyncSession, reservation_data: dict):
    """
    Создает новое бронирование с проверкой:
    1. Существования столика
    2. Корректности времени
    3. Отсутствия временных конфликтов
    """
    # 1. Проверка существования столика
    table = await db.get(Table, reservation_data['table_id'])
    if not table:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Столик с id {reservation_data['table_id']} не найден"
        )

    # 2. Парсинг времени бронирования
    try:
        reservation_time = (
            datetime.fromisoformat(reservation_data['reservation_time'])
            if isinstance(reservation_data['reservation_time'], str)
            else reservation_data['reservation_time']
        )
    except (ValueError, TypeError):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Неверный формат времени. Используйте ISO формат: YYYY-MM-DDTHH:MM:SS"
        )

    # 3. Проверка что время не в прошлом
    if reservation_time < datetime.now():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Нельзя забронировать столик на прошедшее время"
        )

    # 4. Проверка конфликтов бронирования
    duration = reservation_data['duration_minutes']
    start_time = reservation_time
    end_time = start_time + timedelta(minutes=duration)
    
    # Создаем параметризованный запрос
    stmt = """
    SELECT id FROM reservations 
    WHERE table_id = :table_id 
    AND reservation_time < :end_time
    AND (reservation_time + (duration_minutes * INTERVAL '1 minute')) > :start_time
    """
    
    params = {
        'table_id': reservation_data['table_id'],
        'end_time': end_time,
        'start_time': start_time
    }
    
    conflicting = await db.execute(text(stmt), params)
    
    if conflicting.scalars().first():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Столик уже забронирован на указанное время"
        )

    # 5. Создание брони
    new_reservation = Reservation(
        customer_name=reservation_data['customer_name'],
        table_id=reservation_data['table_id'],
        reservation_time=reservation_time,
        duration_minutes=duration
    )
    
    db.add(new_reservation)
    await db.commit()
    await db.refresh(new_reservation)
    return new_reservation

async def get_reservations(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(
        select(Reservation)
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()

async def delete_reservation(db: AsyncSession, reservation_id: int):
    reservation = await db.get(Reservation, reservation_id)
    if reservation:
        await db.delete(reservation)
        await db.commit()
        return True
    return False