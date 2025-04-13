from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.reservation import Reservation, ReservationCreate
from app.services.reservation_service import create_reservation, get_reservations, delete_reservation
from app.core.database import get_db

router = APIRouter(prefix="/reservations", tags=["reservations"])

@router.post("/", response_model=Reservation)
async def create_new_reservation(reservation: ReservationCreate, db: AsyncSession = Depends(get_db)):
    return await create_reservation(db, reservation.dict())

@router.get("/", response_model=list[Reservation])
async def read_reservations(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    reservations = await get_reservations(db, skip=skip, limit=limit)
    return reservations

@router.delete("/{reservation_id}")
async def remove_reservation(reservation_id: int, db: AsyncSession = Depends(get_db)):
    success = await delete_reservation(db, reservation_id)
    if not success:
        raise HTTPException(status_code=404, detail="Reservation not found")
    return {"message": "Reservation deleted successfully"}