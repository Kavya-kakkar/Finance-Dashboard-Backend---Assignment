from sqlalchemy.orm import Session
from sqlalchemy import func
from models.record import Record, RecordTypeEnum
from datetime import date, timedelta
from typing import Optional

def get_dashboard_summary(db: Session, user_id: int, is_admin: bool = False):
    query = db.query(Record)
    if not is_admin:
        query = query.filter(Record.user_id == user_id)
        
    # Totals
    income = db.query(func.sum(Record.amount)).filter(Record.type == RecordTypeEnum.income)
    expense = db.query(func.sum(Record.amount)).filter(Record.type == RecordTypeEnum.expense)
    
    if not is_admin:
        income = income.filter(Record.user_id == user_id)
        expense = expense.filter(Record.user_id == user_id)
        
    total_income = income.scalar() or 0.0
    total_expense = expense.scalar() or 0.0
    net_balance = total_income - total_expense
    
    # Recent 5 transactions
    recent = query.order_by(Record.date.desc()).limit(5).all()
    recent_records = [{"id": r.id, "amount": r.amount, "type": r.type, "date": r.date, "category": r.category} for r in recent]
    
    # Category totals
    category_query = db.query(Record.category, func.sum(Record.amount).label("total"))
    if not is_admin:
        category_query = category_query.filter(Record.user_id == user_id)
    category_totals = category_query.group_by(Record.category).all()
    categories = [{"category": c.category, "total": c.total} for c in category_totals]
    
    return {
        "total_income": total_income,
        "total_expense": total_expense,
        "net_balance": net_balance,
        "recent_transactions": recent_records,
        "category_totals": categories
    }
