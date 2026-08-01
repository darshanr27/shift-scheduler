from sqlalchemy import Column, Integer, String, TIMESTAMP
from database import Base

class User(Base):
    __tablename__ = "users"
    __allow_unmapped__ = True

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    created_at = Column(TIMESTAMP, nullable=False)
