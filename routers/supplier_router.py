from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from core.database import get_db
from dependencies.dependency import get_current_user
from core.permission import require_roles
from models.supplier_model import Supplier
from schemas.supplier_schema import SupplierCreate

router = APIRouter(prefix="/suppliers", tags=["Suppliers"], dependencies=[Depends(get_current_user)])

@router.post("/", dependencies=[Depends(require_roles("SUPER_ADMIN"))])
def create_supplier(payload: SupplierCreate, db: Session = Depends(get_db)):
    supplier = Supplier(**payload.model_dump())
    db.add(supplier)
    db.commit()
    return {"Info": "Supplier Created"}

@router.get("/")
def get_suppliers(db: Session = Depends(get_db)):
    return db.query(Supplier).all()