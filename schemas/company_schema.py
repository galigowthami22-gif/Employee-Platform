"""
Company Schema
Pydantic schemas for company-related requests and responses.
"""

from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional, List
from datetime import datetime
from enum import Enum


class CompanyStatus(str, Enum):
    """Company status."""
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"
    ARCHIVED = "archived"


class CompanyPlan(str, Enum):
    """Company subscription plan."""
    STARTER = "starter"
    PROFESSIONAL = "professional"
    ENTERPRISE = "enterprise"
    CUSTOM = "custom"


# Request Schemas
class CompanyCreateRequest(BaseModel):
    """Request schema for creating a company."""
    name: str = Field(..., min_length=1, max_length=255, description="Company legal name")
    short_name: Optional[str] = Field(None, max_length=50, description="Short/trading name")
    description: Optional[str] = None
    legal_entity: Optional[str] = None
    registration_number: Optional[str] = None
    tax_id: Optional[str] = None
    industry: Optional[str] = None
    website: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    country: Optional[str] = None
    state: Optional[str] = None
    city: Optional[str] = None
    address: Optional[str] = None
    postal_code: Optional[str] = None
    currency: str = Field(default="USD", description="ISO 4217 currency code")
    timezone: str = Field(default="UTC", description="Company timezone")
    language: str = Field(default="en", description="Default language")
    plan: CompanyPlan = Field(default=CompanyPlan.STARTER, description="Subscription plan")
    
    class Config:
        schema_extra = {
            "example": {
                "name": "Acme Corporation",
                "short_name": "ACME",
                "industry": "Technology",
                "country": "US",
                "currency": "USD"
            }
        }


class CompanyUpdateRequest(BaseModel):
    """Request schema for updating a company."""
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    short_name: Optional[str] = None
    description: Optional[str] = None
    industry: Optional[str] = None
    website: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    country: Optional[str] = None
    state: Optional[str] = None
    city: Optional[str] = None
    address: Optional[str] = None
    postal_code: Optional[str] = None
    currency: Optional[str] = None
    timezone: Optional[str] = None
    language: Optional[str] = None
    status: Optional[CompanyStatus] = None
    
    class Config:
        schema_extra = {
            "example": {
                "name": "Acme Corporation",
                "industry": "Technology",
                "status": "active"
            }
        }


class CompanySettingsSchema(BaseModel):
    """Schema for company settings."""
    setting_id: str
    company_id: str
    max_employees: int = 100
    max_departments: int = 20
    max_projects: int = 50
    enable_mfa: bool = False
    enable_audit_logs: bool = True
    session_timeout_minutes: int = 30
    api_rate_limit: int = 1000
    backup_frequency: str = "daily"
    retention_days: int = 365
    
    class Config:
        from_attributes = True


# Response Schemas
class CompanyResponse(BaseModel):
    """Response schema for company (detailed)."""
    company_id: str
    name: str
    short_name: Optional[str] = None
    description: Optional[str] = None
    legal_entity: Optional[str] = None
    registration_number: Optional[str] = None
    tax_id: Optional[str] = None
    industry: Optional[str] = None
    website: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    logo_url: Optional[str] = None
    country: Optional[str] = None
    state: Optional[str] = None
    city: Optional[str] = None
    address: Optional[str] = None
    postal_code: Optional[str] = None
    currency: str
    timezone: str
    language: str
    status: CompanyStatus
    plan: CompanyPlan
    employee_count: Optional[int] = None
    founded_date: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    created_by: Optional[str] = None
    settings: Optional[CompanySettingsSchema] = None
    
    class Config:
        from_attributes = True
        schema_extra = {
            "example": {
                "company_id": "comp_123456",
                "name": "Acme Corporation",
                "short_name": "ACME",
                "status": "active",
                "plan": "professional",
                "currency": "USD",
                "timezone": "UTC",
                "industry": "Technology",
                "country": "US"
            }
        }


class CompanyListResponse(BaseModel):
    """Response schema for company list (summary)."""
    company_id: str
    name: str
    short_name: Optional[str] = None
    status: CompanyStatus
    plan: CompanyPlan
    industry: Optional[str] = None
    country: Optional[str] = None
    created_at: datetime
    
    class Config:
        from_attributes = True
        schema_extra = {
            "example": {
                "company_id": "comp_123456",
                "name": "Acme Corporation",
                "short_name": "ACME",
                "status": "active",
                "plan": "professional",
                "industry": "Technology",
                "country": "US",
                "created_at": "2026-01-15T10:30:00Z"
            }
        }


class CompanyStatsResponse(BaseModel):
    """Response schema for company statistics."""
    company_id: str
    name: str
    total_employees: int = 0
    total_departments: int = 0
    total_branches: int = 0
    total_teams: int = 0
    status: CompanyStatus
    plan: CompanyPlan
    
    class Config:
        from_attributes = True


class BulkCompanyResponse(BaseModel):
    """Response for bulk operations."""
    total: int
    successful: int
    failed: int
    companies: List[CompanyListResponse]
    
    class Config:
        schema_extra = {
            "example": {
                "total": 10,
                "successful": 10,
                "failed": 0,
                "companies": []
            }
        }
