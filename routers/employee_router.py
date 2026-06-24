from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from core.database import get_db
from dependencies.dependency import get_current_user
from core.permission import require_roles
from models.employee_model import Employee
from schemas.employee_schema import EmployeeCreate

router = APIRouter(prefix="/employees", tags=["Employees"], dependencies=[Depends(get_current_user)])

@router.post("/", dependencies=[Depends(require_roles("SUPER_ADMIN"))])
def create_employee(payload: EmployeeCreate, db: Session = Depends(get_db)):
    employee = Employee(**payload.dict())
    db.add(employee)
    db.commit()
    return {"Info": "Employee Created"}

@router.get("/")
def get_employees(db: Session = Depends(get_db)):
    return db.query(Employee).all()

@router.get("/search/")
def search_employee(keyword: str, db: Session = Depends(get_db)):
    return db.query(Employee).filter(Employee.first_name.contains(keyword)).all()

@router.get("/paginated/")
def get_paginated_employees(page: int = 1, limit: int = 10, db: Session = Depends(get_db)):
    skip = (page - 1) * limit
    employees = (db.query(Employee).offset(skip).limit(limit).all())
    return employees

@router.get("/filter/")
def filter_employee(department_id: int, db: Session = Depends(get_db)):
    return db.query(Employee).filter(Employee.department_id == department_id).all()