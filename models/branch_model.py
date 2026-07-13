"""
Branch Model
Represents a branch/office location of a company.
"""

from datetime import datetime
from sqlalchemy import Column, String, Text, DateTime, Enum, ForeignKey, Boolean, Index
from sqlalchemy.orm import relationship
from core.base_model import BaseModel
import enum

class BranchStatus(str, enum.Enum):
    """Branch status enumeration."""
    ACTIVE = "active"
    INACTIVE = "inactive"
    CLOSED = "closed"

class BranchType(str, enum.Enum):
    """Branch type enumeration."""
    HEADQUARTERS = "headquarters"
    REGIONAL = "regional"
    SATELLITE = "satellite"
    WAREHOUSE = "warehouse"
    SERVICE_CENTER = "service_center"

class Branch(BaseModel):
    """
    Branch model representing a physical office/location of a company.
    
    Attributes:
        branch_id: Primary key (UUID)
        company_id: Foreign key to Company (for multi-tenancy)
        name: Branch name
        code: Unique branch code (e.g., HQ, BLR, NYK)
        type: Branch type (headquarters, regional, satellite, warehouse, service_center)
        status: Branch status (active, inactive, closed)
        description: Branch description
        manager_id: Manager/Head of branch (User ID)
        phone: Contact phone
        email: Contact email
        website: Branch website
        country: Country code
        state: State/Province
        city: City
        address: Street address
        postal_code: ZIP/Postal code
        latitude: GPS latitude
        longitude: GPS longitude
        capacity: Employee capacity at this branch
        established_date: Date branch was established
        timezone: Branch timezone
        created_at: Record creation timestamp
        updated_at: Last update timestamp
        created_by: User ID who created the branch
        updated_by: User ID who last updated the branch
    """
    __tablename__ = "branches"

    branch_id = Column(String(36), primary_key=True)
    company_id = Column(String(36), ForeignKey("companies.company_id"), nullable=False, index=True)
    
    # Basic Information
    name = Column(String(255), nullable=False, index=True)
    code = Column(String(20), nullable=False, index=True)
    type = Column(Enum(BranchType), default=BranchType.REGIONAL, nullable=False)
    status = Column(Enum(BranchStatus), default=BranchStatus.ACTIVE, nullable=False, index=True)
    description = Column(Text, nullable=True)
    
    # Management
    manager_id = Column(String(36), nullable=True, index=True)
    
    # Contact Information
    phone = Column(String(20), nullable=True)
    email = Column(String(255), nullable=True)
    website = Column(String(255), nullable=True)
    
    # Location
    country = Column(String(100), nullable=True, index=True)
    state = Column(String(100), nullable=True)
    city = Column(String(100), nullable=True)
    address = Column(Text, nullable=True)
    postal_code = Column(String(20), nullable=True)
    
    # Geolocation
    latitude = Column(String(20), nullable=True)
    longitude = Column(String(20), nullable=True)
    
    # Operational
    capacity = Column(String(50), nullable=True)  # Employee capacity
    established_date = Column(DateTime, nullable=True)
    timezone = Column(String(50), nullable=True)
    
    # Audit Fields
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    created_by = Column(String(36), nullable=True)
    updated_by = Column(String(36), nullable=True)
    
    # Relationships
    company = relationship("Company", back_populates="branches")
    contacts = relationship("BranchContact", back_populates="branch", cascade="all, delete-orphan")
    
    # Index for company and active status
    __table_args__ = (
        Index('idx_branch_company_status', 'company_id', 'status'),
        Index('idx_branch_company_code', 'company_id', 'code'),
    )
    
    def __repr__(self):
        return f"<Branch(branch_id={self.branch_id}, name={self.name}, code={self.code})>"

class BranchContact(BaseModel):
    """
    Branch Contact model for storing contact persons at a branch.
    
    Attributes:
        contact_id: Primary key (UUID)
        branch_id: Foreign key to Branch
        company_id: Foreign key to Company (for multi-tenancy)
        name: Contact person name
        title: Job title
        phone: Contact phone
        email: Contact email
        department: Department (optional)
        is_primary: Is this the primary contact
        created_at: Record creation timestamp
        updated_at: Last update timestamp
    """
    __tablename__ = "branch_contacts"

    contact_id = Column(String(36), primary_key=True)
    branch_id = Column(String(36), ForeignKey("branches.branch_id"), nullable=False, index=True)
    company_id = Column(String(36), ForeignKey("companies.company_id"), nullable=False, index=True)
    
    # Contact Information
    name = Column(String(255), nullable=False)
    title = Column(String(100), nullable=True)
    phone = Column(String(20), nullable=True)
    email = Column(String(255), nullable=True)
    department = Column(String(100), nullable=True)
    
    # Settings
    is_primary = Column(Boolean, default=False)
    
    # Audit Fields
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    branch = relationship("Branch", back_populates="contacts")
    
    # Indexes
    __table_args__ = (
        Index('idx_branch_contact_branch_primary', 'branch_id', 'is_primary'),
        Index('idx_branch_contact_company', 'company_id'),
    )
    
    def __repr__(self):
        return f"<BranchContact(contact_id={self.contact_id}, name={self.name})>"
