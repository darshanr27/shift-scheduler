from fastapi import HTTPException
from sqlalchemy.orm import Session
from models.shift import Shift
from schemas.shift import ShiftCreate, ShiftUpdate

def create_shift(db: Session, shift_in: ShiftCreate, user_id: int):
    shift = Shift(
        facility_name = shift_in.facility_name,
        shift_date = shift_in.shift_date,
        start_time = shift_in.start_time,
        end_time = shift_in.end_time,
        created_by = user_id
    )

    db.add(shift)
    db.commit()
    db.refresh(shift)
    return shift

def get_all_shifts(db: Session):
    return db.query(Shift).all()

def get_shift_by_id(db: Session, id: int):
    shift = db.query(Shift).filter(Shift.id == id).first()
    if not shift:
        raise HTTPException(status_code=404, detail="Shift not found")

    return shift

def update_shift(db: Session, id: int, shift_update: ShiftUpdate):
    shift = db.query(Shift).filter(Shift.id == id).first()
    if not shift:
        raise HTTPException(status_code=404, detail="Id not found")

    if shift_update.facility_name is not None:
        shift.facility_name = shift_update.facility_name
    if shift_update.shift_date is not None:
        shift.shift_date = shift_update.shift_date
    if shift_update.start_time is not None:
        shift.start_time = shift_update.start_time
    if shift_update.end_time is not None:
        shift.end_time = shift_update.end_time

    db.commit()
    db.refresh(shift)

    return shift

def delete_shift(db: Session, id: int):
    shift = db.query(Shift).filter(Shift.id == id).first()
    if not shift:
        raise HTTPException(status_code=404, detail="Id not found")

    db.delete(shift)
    db.commit()

    return "Successfully deleted"