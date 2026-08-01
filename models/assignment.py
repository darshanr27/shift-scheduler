from sqlalchemy import Column, Integer, Boolean, ForeignKey
from database import Base

class Assignment(Base):
    __tablename__ = "assignments"
    __allow_unmapped__ = True

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    shift_id = Column(Integer, ForeignKey("shifts.id"), nullable=False)
    is_active = Column(Boolean, default=True)