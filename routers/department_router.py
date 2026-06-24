from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from core.database import get_db
from dependencies.dependency import get_current_user
from core.permission import require_roles
from models.department_model import Department
from schemas.department_schema import DepartmentCreate

router = APIRouter(prefix="/departments", tags=["Departments"], dependencies=[Depends(get_current_user)])

@router.post("/", dependencies=[Depends(require_roles("SUPER_ADMIN"))])
def create_department(payload: DepartmentCreate, db: Session = Depends(get_db)):
    department = Department(name=payload.name, description=payload.description)
    db.add(department)
    db.commit()
    return {"Info": "Department Created"}

@router.get("/")
def get_departments(db: Session = Depends(get_db)):
    return db.query(Department).all()

@router.get("/{department_id}")
def get_department(department_id: int, db: Session = Depends(get_db)):
    return db.query(Department).filter(Department.id == department_id).first()

@router.delete("/{department_id}")
def delete_department(department_id: int, db: Session = Depends(get_db)):
    department = db.query(Department).filter(Department.id == department_id).first()
    db.delete(department)
    db.commit()
    return {"Info": "Department Deleted"}