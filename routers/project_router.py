from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from core.database import get_db
from dependencies.dependency import get_current_user
from core.permission import require_roles
from models.project_model import Project
from schemas.project_schema import ProjectCreate

router = APIRouter(prefix="/projects", tags=["Projects"], dependencies=[Depends(get_current_user)])

@router.post("/", dependencies=[Depends(require_roles("SUPER_ADMIN"))])
def create_project(payload: ProjectCreate, db: Session = Depends(get_db)):
    project = Project(**payload.model_dump())
    db.add(project)
    db.commit()
    return {"Info": "Project Created"}

@router.get("/")
def get_projects(db: Session = Depends(get_db)):
    return db.query(Project).all()