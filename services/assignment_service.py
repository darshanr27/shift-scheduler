from fastapi import HTTPException
from sqlalchemy.orm import Session
from models.assignment import Assignment
from models.shift import Shift
from models.user import User

def assign(db: Session, shift_id: int, user_id: int):
    shift = db.query(Shift).filter(Shift.id == shift_id).first()
    user = db.query(User).filter(User.id == user_id).first()
    if not shift:
        raise HTTPException(status_code=400, detail="Invalid shift")
    if not user:
        raise HTTPException(status_code=400, detail="Invlid user")

    assignment = Assignment(
        user_id = user_id,
        shift_id = shift_id
    )

    db.add(assignment)
    db.commit()
    db.refresh(assignment)

    return assignment

def unassign(db: Session, shift_id: int, user_id: int):
    existing_assignment = db.query(Assignment).filter(Assignment.shift_id == shift_id, Assignment.user_id == user_id).first()

    if not existing_assignment:
        raise HTTPException(status_code=404, detail="Assignments not found")

    db.delete(existing_assignment)
    db.commit()

    return "Unassignment successful"

def get_assignments_by_shift(db: Session, shift_id: int):
    return db.query(Assignment).filter(Assignment.shift_id == shift_id).all()

def get_assignments_by_user(db: Session, user_id: int):
    return db.query(Assignment).filter(Assignment.user_id == user_id).all()
