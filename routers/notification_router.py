from fastapi import APIRouter, Depends, HTTPException
from services.email_service import send_email
from sqlalchemy.orm import Session
from core.database import get_db
from models.notification_model import Notification

router = APIRouter(prefix="/notifications", tags=["Notifications"])


@router.post("/send-email")
async def test_email(email: str):
    try:
        await send_email(email, "Test Mail", "<h1>Email Working</h1>")
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Failed to send email: {exc}")
    return {"Info": "Email Sent"}


@router.get("/{user_id}")
def get_notifications(user_id: int, db: Session = Depends(get_db)):
    return db.query(Notification).filter(Notification.user_id == user_id).all()


@router.put("/{notification_id}/read")
def mark_read(notification_id: int, db: Session = Depends(get_db)):
    notification = db.query(Notification).filter(Notification.id == notification_id).first()
    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    notification.is_read = True
    db.commit()
    return {"Info": "Marked Read"}