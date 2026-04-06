from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date
from core.database import get_db
from core.dependencies import get_current_user, require_admin, require_role, RoleEnum
from schemas.record import RecordOut, RecordCreate, RecordUpdate
from services import record as record_service
from models.record import RecordTypeEnum
from models.user import User

router = APIRouter()

@router.post("/", response_model=RecordOut, status_code=201)
def create_new_record(
    record: RecordCreate, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(require_role([RoleEnum.Admin, RoleEnum.Analyst]))
):
    """Admin and Analyst can create records."""
    return record_service.create_record(db=db, record=record, user_id=current_user.id)

@router.get("/", response_model=List[RecordOut])
def get_all_records(
    skip: int = Query(0, ge=0), 
    limit: int = Query(100, le=1000), 
    type: Optional[RecordTypeEnum] = None,
    category: Optional[str] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    """Get records based on role (Admin sees all, others see their own) and filters."""
    is_admin = current_user.role == RoleEnum.Admin
    return record_service.get_records(
        db=db, user_id=current_user.id, is_admin=is_admin, skip=skip, limit=limit,
        type=type, category=category, start_date=start_date, end_date=end_date
    )

@router.get("/{record_id}", response_model=RecordOut)
def get_single_record(
    record_id: int, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    """Retrieve a specific record."""
    is_admin = current_user.role == RoleEnum.Admin
    return record_service.get_record(db, record_id=record_id, user_id=current_user.id, is_admin=is_admin)

@router.put("/{record_id}", response_model=RecordOut)
def update_existing_record(
    record_id: int, 
    record_update: RecordUpdate, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(require_role([RoleEnum.Admin, RoleEnum.Analyst]))
):
    """Update a specific record."""
    is_admin = current_user.role == RoleEnum.Admin
    return record_service.update_record(
        db, record_id=record_id, record_update=record_update, 
        user_id=current_user.id, is_admin=is_admin
    )

@router.delete("/{record_id}", status_code=204)
def delete_record_endpoint(
    record_id: int, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(require_admin)
):
    """Only Admins can delete records."""
    record_service.delete_record(db, record_id=record_id, user_id=current_user.id, is_admin=True)
    return None
