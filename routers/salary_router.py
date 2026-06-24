from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi.responses import FileResponse
from datetime import date
from core.database import get_db
from dependencies.dependency import get_current_user
from core.permission import require_roles
from models.salary_structure_model import SalaryStructure
from models.payroll_model import Payroll
from schemas.salary_schema import SalaryStructureCreate
from utils.pdf_generator import generate_payslip
from services.notification_service import create_notification

router = APIRouter(prefix="/payroll", tags=["Payroll"], dependencies=[Depends(get_current_user)])

@router.post("/salary-structure")
def create_salary_structure(payload: SalaryStructureCreate, db: Session = Depends(get_db)):
    salary = SalaryStructure(**payload.model_dump())
    db.add(salary)
    db.commit()
    return {"Info": "Salary Structure Created"}

@router.get("/salary-structure/{employee_id}")
def get_salary_structure(employee_id: int, db: Session = Depends(get_db)):
    return db.query(SalaryStructure).filter(SalaryStructure.employee_id == employee_id).first()

@router.post("/generate/{employee_id}")
def generate_payroll(employee_id: int, db: Session = Depends(get_db)):
    salary = db.query(SalaryStructure).filter(SalaryStructure.employee_id == employee_id).first()
    if not salary:
        return {"Info": "Salary structure not found"}
    gross_salary = (salary.basic_salary + salary.hra + salary.allowances)
    net_salary = (gross_salary - salary.deductions)
    payroll = Payroll(employee_id=employee_id, payroll_month=date.today(), gross_salary=gross_salary, total_deductions=salary.deductions, net_salary=net_salary)
    db.add(payroll)
    db.commit()
    create_notification(db, employee_id, "Payroll Generated", f"Payroll for employee {employee_id} generated")
    return {"gross_salary": gross_salary, "deductions": salary.deductions, "net_salary": net_salary}

@router.get("/history/{employee_id}")
def payroll_history(employee_id: int, db: Session = Depends(get_db)):
    return db.query(Payroll).filter(Payroll.employee_id == employee_id).all()

@router.get("/payslip/{payroll_id}")
def download_payslip(payroll_id: int, db: Session = Depends(get_db)):
    payroll = db.query(Payroll).filter(Payroll.id == payroll_id).first()
    file_path = (f"payslip_{payroll_id}.pdf")
    generate_payslip(file_path, payroll)
    return FileResponse(path=file_path, filename=file_path, media_type="application/pdf")