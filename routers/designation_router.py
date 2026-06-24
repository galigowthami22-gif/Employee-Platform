from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from core.database import get_db
from dependencies.dependency import get_current_user
from core.permission import require_roles
from models.designation_model import Designation
from schemas.designation_schema import DesignationCreate

router = APIRouter(prefix="/designations", tags=["Designations"], dependencies=[Depends(get_current_user)])

@router.post("/", dependencies=[Depends(require_roles("SUPER_ADMIN"))])
def create_designation(payload: DesignationCreate, db: Session = Depends(get_db)):
    designation = Designation(title=payload.title, description=payload.description)
    db.add(designation)
    db.commit()
    return {"Info": "Designation Created"}

@router.get("/")
def get_dsignations(db: Session = Depends(get_db)):
    return db.query(Designation).all()

@router.get("/{designation_id}")
def get_designation(designation_id: int, db: Session = Depends(get_db)):
    return db.query(Designation).filter(Designation.id == designation_id).first()

@router.delete("/{designation_id}")
def delete_designation(designation_id: int, db: Session = Depends(get_db)):
    designation = db.query(Designation).filter(Designation.id == designation_id).first()
    db.delete(designation)
    db.commit()
    return {"Info": "Designation Deleted"}