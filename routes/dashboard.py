from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from core.database import get_db
from core.dependencies import get_current_user, require_role, RoleEnum
from services import dashboard as dashboard_service
from models.user import User
from typing import Dict, Any

router = APIRouter()

@router.get("/summary", response_model=Dict[str, Any])
def get_dashboard_data(
    db: Session = Depends(get_db), 
    current_user: User = Depends(require_role([RoleEnum.Admin, RoleEnum.Analyst]))
):
    """
    Dashboard summary available to Admins and Analysts.
    Admins see global summary, Analysts see their own summary.
    """
    is_admin = current_user.role == RoleEnum.Admin
    return dashboard_service.get_dashboard_summary(db=db, user_id=current_user.id, is_admin=is_admin)
