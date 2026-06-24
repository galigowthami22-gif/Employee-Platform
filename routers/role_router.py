from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.database import get_db
from core.permission import require_roles
from models.role_model import Role
from schemas.role_schema import RoleCreate

router = APIRouter(prefix="/roles", tags=["Roles"], dependencies=[Depends(require_roles("SUPER_ADMIN"))])

@router.post("/")
def create_role(payload: RoleCreate, db: Session = Depends(get_db)):
    existing_role = db.query(Role).filter(Role.name == payload.name).first()
    if existing_role:
        raise HTTPException(status_code=400, detail="Role already exists")

    role = Role(**payload.dict())
    db.add(role)
    db.commit()
    db.refresh(role)
    return role

@router.get("/")
def get_roles(db: Session = Depends(get_db)):
    return db.query(Role).all()

@router.get("/{role_id}")
def get_role(role_id: int, db: Session = Depends(get_db)):
    role = db.query(Role).filter(Role.id == role_id).first()
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    return role

@router.delete("/{role_id}")
def delete_role(role_id: int, db: Session = Depends(get_db)):
    role = db.query(Role).filter(Role.id == role_id).first()
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    db.delete(role)
    db.commit()
    return {"detail": "Role deleted"}
