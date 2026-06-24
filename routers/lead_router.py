from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from core.database import get_db
from models.lead_model import Lead
from models.client_model import Client
from schemas.lead_schema import LeadCreate

router = APIRouter(prefix="/leads", tags=["CRM"])

@router.post("/")
def create_lead(payload: LeadCreate, db: Session = Depends(get_db)):
    lead = Lead(**payload.model_dump())
    db.add(lead)
    db.commit()
    return {"Info": "Lead Created"}

@router.get("/")
def get_leads(db: Session = Depends(get_db)):
    return db.query(Lead).all()

@router.put("/{lead_id}/status")
def update_lead_status(lead_id: int, status: str, db: Session = Depends(get_db)):
    lead = db.query(Lead).filter(Lead.id == lead_id).first()
    lead.status = status
    db.commit()
    return {"Info": "Lead Updated"}

@router.post("/{lead_id}/convert")
def convert_lead(lead_id: int, db: Session = Depends(get_db)):
    lead = db.query(Lead).filter(Lead.id == lead_id).first()
    client = Client(company_name=lead.client_name, contact_person=lead.client_name, email=lead.email, phone=lead.phone)
    db.add(client)
    lead.status = "WON"
    db.commit()
    return {"Info": "Lead Converted"}