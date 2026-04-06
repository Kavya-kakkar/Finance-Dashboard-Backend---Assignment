import enum
from sqlalchemy import Column, Integer, String, Boolean, Enum
from core.database import Base

class RoleEnum(str, enum.Enum):
    Viewer = "Viewer"
    Analyst = "Analyst"
    Admin = "Admin"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(Enum(RoleEnum), default=RoleEnum.Viewer, nullable=False)
    is_active = Column(Boolean, default=True)
