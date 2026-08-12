from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session
from database import get_db

from schemas.assignment import AssignmentResponse
from services import assignment_service
from services.auth_service import get_current_user

router = APIRouter()

@router.post("/shifts/{shift_id}/assign/{user_id}", response_model=AssignmentResponse)
def assign_shift(shift_id: int, user_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    if current_user.role != 'admin':
        raise HTTPException(status_code=403, detail="Unauthorized")
    return assignment_service.assign(db, shift_id, user_id)

@router.delete("/shifts/{shift_id}/unassign/{user_id}")
def unassign_shift(shift_id: int, user_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    if current_user.role != 'admin':
        raise HTTPException(status_code=403, detail="Unauthorized")
    return assignment_service.unassign(db, shift_id, user_id)

@router.get("/shifts/{shift_id}/assignments", response_model=list[AssignmentResponse])
def get_assignments_by_shifts(shift_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return assignment_service.get_assignments_by_shift(db, shift_id)

@router.get("/users/{user_id}/shifts", response_model=list[AssignmentResponse])
def get_assignments_by_user(user_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return assignment_service.get_assignments_by_user(db, user_id)
