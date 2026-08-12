from pydantic import BaseModel

class AssignmentResponse(BaseModel):
    id: int
    shift_id: int
    user_id: int
    is_active: bool

    class Config:
        from_attributes = True