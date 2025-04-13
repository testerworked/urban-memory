from datetime import datetime
from pydantic import BaseModel
from pydantic import BaseModel, validator

class ReservationBase(BaseModel):
    customer_name: str
    table_id: int
    reservation_time: datetime  # Теперь принимает datetime объект
    duration_minutes: int

    @validator('reservation_time', pre=True)
    def parse_reservation_time(cls, value):
        if isinstance(value, str):
            try:
                return datetime.fromisoformat(value)
            except ValueError:
                raise ValueError("Invalid datetime format. Use ISO format (YYYY-MM-DDTHH:MM:SS)")
        return value

class ReservationCreate(ReservationBase):
    pass

class Reservation(ReservationBase):
    id: int
    
    class Config:
        orm_mode = True


