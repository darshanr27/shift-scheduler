from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db

from schemas.shift import ShiftCreate, ShiftUpdate, ShiftResponse
from services import shift_services
from services.auth_service import get_current_user

router = APIRouter()

@router.post("/shifts", response_model=ShiftResponse)
def create_shift(shift_in: ShiftCreate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=401, detail="Unauthorized")
    return shift_services.create_shift(db, shift_in, current_user.id)

@router.get("/shifts", response_model=list[ShiftResponse])
def get_all_shifts(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return shift_services.get_all_shifts(db)

@router.get("/shifts/{id}", response_model=ShiftResponse)
def get_shifts_by_id(id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return shift_services.get_shift_by_id(db, id)

@router.put("/shifts/{id}", response_model=ShiftResponse)
def update_shift(id: int, shift_update: ShiftUpdate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=401, detail="Unauthorized")
    return shift_services.update_shift(db, id, shift_update)

@router.delete("/shifts/{id}")
def delete_shift(id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=401, detail="Unauthorized")
    return shift_services.delete_shift(db, id)