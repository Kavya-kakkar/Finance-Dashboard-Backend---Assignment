from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from core.database import get_db
from core.dependencies import require_admin
from schemas.user import UserOut, UserCreate, UserUpdate
from services import user as user_service
from models.user import User

router = APIRouter()

@router.post("/", response_model=UserOut, status_code=201)
def create_user(user: UserCreate, db: Session = Depends(get_db), current_user: User = Depends(require_admin)):
    """Admin only: Create a new user."""
    return user_service.create_user(db=db, user=user)

@router.get("/", response_model=List[UserOut])
def list_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: User = Depends(require_admin)):
    """Admin only: Get all users."""
    return user_service.get_users(db, skip=skip, limit=limit)

@router.get("/{user_id}", response_model=UserOut)
def get_user(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(require_admin)):
    """Admin only: Get user details."""
    db_user = user_service.get_user(db, user_id=user_id)
    if not db_user:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.put("/{user_id}", response_model=UserOut)
def update_user(user_id: int, user_update: UserUpdate, db: Session = Depends(get_db), current_user: User = Depends(require_admin)):
    """Admin only: Update a user's role, status or details."""
    return user_service.update_user(db, user_id=user_id, user_update=user_update)
