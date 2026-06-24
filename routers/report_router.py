from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from core.database import get_db
from dependencies.dependency import get_current_user
from core.permission import require_roles
from services.report_service import employee_report, attendance_report, leave_report, inventory_report

router = APIRouter(prefix="/reports", tags=["Reports"], dependencies=[Depends(get_current_user)])

@router.get("/employees", dependencies=[Depends(require_roles("SUPER_ADMIN"))])
def employee_report_api(db: Session = Depends(get_db)):
    return employee_report(db)

@router.get("/attendance", dependencies=[Depends(require_roles("SUPER_ADMIN"))])
def attendance_report_api(db: Session = Depends(get_db)):
    return attendance_report(db)

@router.get("/leaves", dependencies=[Depends(require_roles("SUPER_ADMIN"))])
def leave_report_api(db: Session = Depends(get_db)):
    return leave_report(db)

@router.get("/inventory", dependencies=[Depends(require_roles("SUPER_ADMIN"))])
def inventory_report_api(db: Session = Depends(get_db)):
    return inventory_report(db)