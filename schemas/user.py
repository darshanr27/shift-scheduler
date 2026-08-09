from pydantic import BaseModel

class UserCreate(BaseModel):
    email: str
    password: str
    role: str
    first_name: str
    last_name: str

class UserResponse(BaseModel):
    id: int
    email: str
    role: str
    first_name: str
    last_name: str

    class Config:
        from_attributes = True

class LoginSchema(BaseModel):
    email: str
    password: str