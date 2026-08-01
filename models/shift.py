from sqlalchemy import Column, Integer, String, Date, Time, ForeignKey
from database import Base

class Shift(Base):
    __tablename__ = "shifts"
    __allow_unmapped__ = True

    id = Column(Integer, primary_key=True)
    facility_name = Column(String, nullable=False)
    shift_date = Column(Date, nullable=False)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    created_by = Column(Integer, ForeignKey("users.id"))