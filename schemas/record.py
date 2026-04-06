from pydantic import BaseModel, Field
from typing import Optional
from datetime import date
from models.record import RecordTypeEnum

class RecordBase(BaseModel):
    amount: float = Field(..., gt=0)
    type: RecordTypeEnum
    category: str
    date: date
    notes: Optional[str] = None

class RecordCreate(RecordBase):
    pass

class RecordUpdate(BaseModel):
    amount: Optional[float] = Field(None, gt=0)
    type: Optional[RecordTypeEnum] = None
    category: Optional[str] = None
    date: Optional[date] = None
    notes: Optional[str] = None

class RecordOut(RecordBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True
