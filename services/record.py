from sqlalchemy.orm import Session
from models.record import Record, RecordTypeEnum
from schemas.record import RecordCreate, RecordUpdate
from fastapi import HTTPException
from typing import Optional
from datetime import date

def get_record(db: Session, record_id: int, user_id: int, is_admin: bool = False):
    query = db.query(Record).filter(Record.id == record_id)
    if not is_admin:
        query = query.filter(Record.user_id == user_id)
    record = query.first()
    if not record:
        raise HTTPException(status_code=404, detail="Record not found")
    return record

def get_records(db: Session, user_id: int, is_admin: bool = False, skip: int = 0, limit: int = 100, 
                type: Optional[RecordTypeEnum] = None, category: Optional[str] = None, 
                start_date: Optional[date] = None, end_date: Optional[date] = None):
    query = db.query(Record)
    if not is_admin:
        query = query.filter(Record.user_id == user_id)
        
    if type:
        query = query.filter(Record.type == type)
    if category:
        query = query.filter(Record.category == category)
    if start_date:
        query = query.filter(Record.date >= start_date)
    if end_date:
        query = query.filter(Record.date <= end_date)
        
    return query.order_by(Record.date.desc()).offset(skip).limit(limit).all()

def create_record(db: Session, record: RecordCreate, user_id: int):
    db_record = Record(**record.dict(), user_id=user_id)
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    return db_record

def update_record(db: Session, record_id: int, record_update: RecordUpdate, user_id: int, is_admin: bool = False):
    db_record = get_record(db, record_id, user_id, is_admin)
    
    update_data = record_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_record, key, value)
        
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    return db_record

def delete_record(db: Session, record_id: int, user_id: int, is_admin: bool = False):
    db_record = get_record(db, record_id, user_id, is_admin)
    db.delete(db_record)
    db.commit()
    return {"detail": "Record successfully deleted"}
