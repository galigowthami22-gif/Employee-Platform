from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime, date
from core.database import get_db
from models.attendance_model import Attendance
from schemas.attendance_schema import AttendanceCheckIn, AttendanceCheckOut

router = APIRouter(prefix="/attendance", tags=["Attendance"])

@router.post("/check-in")
def check_in(payload: AttendanceCheckIn, db: Session = Depends(get_db)):
    attendance = Attendance(employee_id=payload.employee_id, attendance_date=date.today(), check_in=datetime.now(), status="PRESENT")
    db.add(attendance)
    db.commit()
    return {"Info": "Checked In"}

@router.post("/check-out")
def check_out(payload: AttendanceCheckOut, db: Session = Depends(get_db)):
    attendance = db.query(Attendance).filter(Attendance.employee_id == payload.employee_id, Attendance.attendance_date == date.today()).first()
    attendance.check_out = datetime.now()
    db.commit()
    return {"Info": "Checked Out"}

@router.get("/daily-report")
def daily_report(db: Session = Depends(get_db)):
    return db.query(Attendance).filter(Attendance.attendance_date == date.today()).all()

@router.get("/employee-report/{employee_id}")
def employee_report(employee_id: int, db: Session = Depends(get_db)):
    return db.query(Attendance).filter(Attendance.employee_id == employee_id).all()