from sqlalchemy import Column, Boolean, DateTime
from datetime import datetime
from core.base import Base

class BaseModel(Base):

    __abstract__ = True

    is_deleted = Column(Boolean, default=False)
    deleted_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)