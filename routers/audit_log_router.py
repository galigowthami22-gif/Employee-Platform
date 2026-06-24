from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from core.database import get_db
from services.audit_log_service import get_audit_logs, user_audit_logs

router = APIRouter(prefix="/audit", tags=["Audit"])

@router.get("/")
def get_logs(db: Session = Depends(get_db)):
    return get_audit_logs(db)

@router.get("/user/{user_id}")
def get_user_logs(user_id: int, db: Session = Depends(get_db)):
    return user_audit_logs(db, user_id)