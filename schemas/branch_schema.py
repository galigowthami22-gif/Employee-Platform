"""
Branch Schema
Pydantic schemas for branch-related requests and responses.
"""

from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional, List
from datetime import datetime
from enum import Enum


class BranchStatus(str, Enum):
    """Branch status."""
    ACTIVE = "active"
    INACTIVE = "inactive"
    CLOSED = "closed"


class BranchType(str, Enum):
    """Branch type."""
    HEADQUARTERS = "headquarters"
    REGIONAL = "regional"
    SATELLITE = "satellite"
    WAREHOUSE = "warehouse"
    SERVICE_CENTER = "service_center"


# Request Schemas
class BranchContactCreateRequest(BaseModel):
    """Request schema for creating a branch contact."""
    name: str = Field(..., min_length=1, max_length=255, description="Contact person name")
    title: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    department: Optional[str] = None
    is_primary: bool = False
    
    class Config:
        schema_extra = {
            "example": {
                "name": "John Doe",
                "title": "Branch Manager",
                "phone": "+1234567890",
                "email": "john.doe@acme.com",
                "is_primary": True
            }
        }


class BranchCreateRequest(BaseModel):
    """Request schema for creating a branch."""
    company_id: str = Field(..., description="Company ID")
    name: str = Field(..., min_length=1, max_length=255, description="Branch name")
    code: str = Field(..., min_length=1, max_length=20, description="Branch code")
    type: BranchType = Field(default=BranchType.REGIONAL, description="Branch type")
    description: Optional[str] = None
    manager_id: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    website: Optional[str] = None
    country: Optional[str] = None
    state: Optional[str] = None
    city: Optional[str] = None
    address: Optional[str] = None
    postal_code: Optional[str] = None
    latitude: Optional[str] = None
    longitude: Optional[str] = None
    capacity: Optional[str] = None
    timezone: Optional[str] = None
    
    class Config:
        schema_extra = {
            "example": {
                "company_id": "comp_123456",
                "name": "New York Office",
                "code": "NYK",
                "type": "regional",
                "city": "New York",
                "country": "US",
                "capacity": "100"
            }
        }


class BranchUpdateRequest(BaseModel):
    """Request schema for updating a branch."""
    name: Optional[str] = None
    description: Optional[str] = None
    manager_id: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    website: Optional[str] = None
    country: Optional[str] = None
    state: Optional[str] = None
    city: Optional[str] = None
    address: Optional[str] = None
    postal_code: Optional[str] = None
    capacity: Optional[str] = None
    status: Optional[BranchStatus] = None
    timezone: Optional[str] = None
    
    class Config:
        schema_extra = {
            "example": {
                "name": "New York Office - Updated",
                "phone": "+1234567890",
                "status": "active"
            }
        }


# Response Schemas
class BranchContactResponse(BaseModel):
    """Response schema for branch contact."""
    contact_id: str
    branch_id: str
    name: str
    title: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    department: Optional[str] = None
    is_primary: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
        schema_extra = {
            "example": {
                "contact_id": "cont_123456",
                "branch_id": "branch_123456",
                "name": "John Doe",
                "title": "Branch Manager",
                "email": "john.doe@acme.com",
                "is_primary": True,
                "created_at": "2026-01-15T10:30:00Z",
                "updated_at": "2026-01-15T10:30:00Z"
            }
        }


class BranchResponse(BaseModel):
    """Response schema for branch (detailed)."""
    branch_id: str
    company_id: str
    name: str
    code: str
    type: BranchType
    status: BranchStatus
    description: Optional[str] = None
    manager_id: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    website: Optional[str] = None
    country: Optional[str] = None
    state: Optional[str] = None
    city: Optional[str] = None
    address: Optional[str] = None
    postal_code: Optional[str] = None
    latitude: Optional[str] = None
    longitude: Optional[str] = None
    capacity: Optional[str] = None
    established_date: Optional[datetime] = None
    timezone: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    contacts: Optional[List[BranchContactResponse]] = None
    
    class Config:
        from_attributes = True
        schema_extra = {
            "example": {
                "branch_id": "branch_123456",
                "company_id": "comp_123456",
                "name": "New York Office",
                "code": "NYK",
                "type": "regional",
                "status": "active",
                "city": "New York",
                "country": "US",
                "created_at": "2026-01-15T10:30:00Z"
            }
        }


class BranchListResponse(BaseModel):
    """Response schema for branch list (summary)."""
    branch_id: str
    company_id: str
    name: str
    code: str
    type: BranchType
    status: BranchStatus
    city: Optional[str] = None
    country: Optional[str] = None
    created_at: datetime
    
    class Config:
        from_attributes = True
        schema_extra = {
            "example": {
                "branch_id": "branch_123456",
                "company_id": "comp_123456",
                "name": "New York Office",
                "code": "NYK",
                "type": "regional",
                "status": "active",
                "city": "New York",
                "country": "US",
                "created_at": "2026-01-15T10:30:00Z"
            }
        }


class BranchStatsResponse(BaseModel):
    """Response schema for branch statistics."""
    branch_id: str
    name: str
    code: str
    total_employees: int = 0
    total_departments: int = 0
    total_teams: int = 0
    status: BranchStatus
    
    class Config:
        from_attributes = True


class BulkBranchResponse(BaseModel):
    """Response for bulk operations."""
    total: int
    successful: int
    failed: int
    branches: List[BranchListResponse]
    
    class Config:
        schema_extra = {
            "example": {
                "total": 5,
                "successful": 5,
                "failed": 0,
                "branches": []
            }
        }
