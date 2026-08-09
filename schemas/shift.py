from pydantic import BaseModel
from datetime import date, time
from typing import Optional

class ShiftCreate(BaseModel):
    facility_name: str
    shift_date: date
    start_time: time
    end_time: time


class ShiftResponse(BaseModel):
    id: int
    facility_name: str
    shift_date: date
    start_time: time
    end_time: time

    class Config:
        from_attributes = True

class ShiftUpdate(BaseModel):
    facility_name: Optional[str] = None
    shift_date: Optional[date] = None
    start_time: Optional[time] = None
    end_time: Optional[time] = None
