"""
Cost Center Model
Represents cost centers for financial tracking and allocation.
"""

from datetime import datetime
from sqlalchemy import Column, String, Text, DateTime, ForeignKey, DECIMAL, Boolean, Index
from sqlalchemy.orm import relationship
from core.base_model import BaseModel


class CostCenter(BaseModel):
    """
    Cost Center model for financial tracking and budget allocation.
    
    Attributes:
        cost_center_id: Primary key (UUID)
        company_id: Foreign key to Company (for multi-tenancy)
        code: Unique cost center code
        name: Cost center name
        description: Cost center description
        manager_id: Cost center manager (User ID)
        budget: Annual budget allocation
        spent: Amount already spent
        is_active: Whether cost center is active
        created_at: Record creation timestamp
        updated_at: Last update timestamp
        created_by: User ID who created the cost center
        updated_by: User ID who last updated the cost center
    """
    __tablename__ = "cost_centers"

    cost_center_id = Column(String(36), primary_key=True)
    company_id = Column(String(36), ForeignKey("companies.company_id"), nullable=False, index=True)
    
    # Basic Information
    code = Column(String(50), nullable=False, index=True)
    name = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)
    
    # Management
    manager_id = Column(String(36), nullable=True, index=True)
    
    # Budget
    budget = Column(DECIMAL(15, 2), nullable=True)
    spent = Column(DECIMAL(15, 2), default=0)
    
    # Status
    is_active = Column(Boolean, default=True, index=True)
    
    # Audit Fields
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    created_by = Column(String(36), nullable=True)
    updated_by = Column(String(36), nullable=True)
    
    # Relationships
    company = relationship("Company", back_populates="cost_centers")
    
    # Composite Index
    __table_args__ = (
        Index('idx_cost_center_company_active', 'company_id', 'is_active'),
        Index('idx_cost_center_company_code', 'company_id', 'code'),
    )
    
    def __repr__(self):
        return f"<CostCenter(cost_center_id={self.cost_center_id}, code={self.code}, name={self.name})>"
