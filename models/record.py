import enum
from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey, Enum
from sqlalchemy.orm import relationship
from core.database import Base

class RecordTypeEnum(str, enum.Enum):
    income = "income"
    expense = "expense"

class Record(Base):
    __tablename__ = "records"

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float, nullable=False)
    type = Column(Enum(RecordTypeEnum), nullable=False)
    category = Column(String, index=True, nullable=False)
    date = Column(Date, nullable=False)
    notes = Column(String, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User")
