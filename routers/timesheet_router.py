from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from core.database import get_db
from dependencies.dependency import get_current_user
from models.timesheet_model import Timesheet
from schemas.timesheet_schema import TimesheetCreate

router = APIRouter(prefix="/timesheets", tags=["Timesheets"], dependencies=[Depends(get_current_user)])

@router.post("/")
def create_timesheet(payload: TimesheetCreate, db: Session = Depends(get_db)):
    timesheet = Timesheet(**payload.model_dump())
    db.add(timesheet)
    db.commit()
    return {"Info": "Timesheet Submitted"}

@router.get("/")
def get_timesheets(db: Session = Depends(get_db)):
    return db.query(Timesheet).all()

@router.get("/employee/{employee_id}")
def employee_timesheets(employee_id: int, db: Session = Depends(get_db)):
    return db.query(Timesheet).filter(Timesheet.employee_id == employee_id).all()