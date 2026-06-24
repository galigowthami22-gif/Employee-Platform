from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.orm import Session
from core.database import get_db
from dependencies.dependency import get_current_user
from core.permission import require_roles
from models.leave_model import LeaveRequest
from schemas.leave_schema import LeaveCreate
from services.notification_service import create_notification

router = APIRouter(prefix="/leaves", tags=["Leave"], dependencies=[Depends(get_current_user)])

@router.post("/")
def apply_leave(payload: LeaveCreate, db: Session = Depends(get_db)):
    leave = LeaveRequest(**payload.model_dump())
    db.add(leave)
    db.commit()
    return {"Info": "Leave Applied"}

@router.get("/")
def get_all_leaves(db: Session = Depends(get_db)):
    return db.query(LeaveRequest).all()

@router.put("/approve/{leave_id}", dependencies=[Depends(require_roles("SUPER_ADMIN"))])
def approve_leave(leave_id: int, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    leave = db.query(LeaveRequest).filter(LeaveRequest.id == leave_id).first()
    leave.status = "APPROVED"
    db.commit()
    background_tasks.add_task(create_notification, db, leave.employee_id, "Leave Approved", "Your leave request was approved")
    return {"Info": "Leave Approved"}

@router.put("/reject/{leave_id}", dependencies=[Depends(require_roles("SUPER_ADMIN"))])
def reject_leave(leave_id: int, db: Session = Depends(get_db)):
    leave = db.query(LeaveRequest).filter(LeaveRequest.id == leave_id).first()
    leave.status = "REJECTED"
    db.commit()
    return {"Info": "Leave Rejected"}