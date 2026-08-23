from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timezone
from database import get_db
from schemas.user import UserCreate, UserResponse, LoginSchema
from models.user import User
from services.auth_service import hash_password, verify_password, create_access_token, get_user_by_email, get_current_user

router = APIRouter()

@router.get("/auth/me", response_model = UserResponse)
def get_me(current_user = Depends(get_current_user)):
    return current_user

@router.post("/auth/signup", response_model=UserResponse)
def sign_up(user: UserCreate, db: Session = Depends(get_db)):
    existing = get_user_by_email(db, user.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_pwd = hash_password(user.password)
    userModel = User(
        email = user.email,
        hashed_password = hashed_pwd,
        role = user.role,
        first_name = user.first_name,
        last_name = user.last_name,
        created_at = datetime.now(timezone.utc)
        )

    db.add(userModel)
    db.commit()
    db.refresh(userModel)
    return userModel

@router.post("/auth/login")
def login(user: LoginSchema, db: Session = Depends(get_db)):
    existing = get_user_by_email(db, user.email)
    if not existing:
        raise HTTPException(status_code=400, detail="User not found")
    password_verification = verify_password(user.password, existing.hashed_password)

    if password_verification:
        token = create_access_token({"sub": user.email})
        return {"access_token": token, "token_type": "bearer"}

    raise HTTPException(status_code=401, detail="Invalid password")