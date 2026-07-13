"""
Employee Schema (HRMS - Phase 12)
Pydantic schemas for employee-related requests and responses.
"""

from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional, List
from datetime import datetime, date
from enum import Enum


class EmploymentStatus(str, Enum):
    """Employment status."""
    ACTIVE = "active"
    INACTIVE = "inactive"
    ON_LEAVE = "on_leave"
    SUSPENDED = "suspended"
    TERMINATED = "terminated"


class EmploymentType(str, Enum):
    """Employment type."""
    FULL_TIME = "full_time"
    PART_TIME = "part_time"
    CONTRACT = "contract"
    TEMPORARY = "temporary"
    INTERN = "intern"
    CONSULTANT = "consultant"


class Gender(str, Enum):
    """Gender."""
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"
    PREFER_NOT_TO_SAY = "prefer_not_to_say"


class MaritalStatus(str, Enum):
    """Marital status."""
    SINGLE = "single"
    MARRIED = "married"
    DIVORCED = "divorced"
    WIDOWED = "widowed"
    PREFER_NOT_TO_SAY = "prefer_not_to_say"


# Request Schemas
class EmployeeCreateRequest(BaseModel):
    """Request schema for creating an employee."""
    company_id: str = Field(..., description="Company ID")
    employee_code: str = Field(..., min_length=1, max_length=50, description="Unique employee code")
    first_name: str = Field(..., min_length=1, max_length=100, description="First name")
    middle_name: Optional[str] = None
    last_name: str = Field(..., min_length=1, max_length=100, description="Last name")
    email: EmailStr = Field(..., description="Work email")
    personal_email: Optional[EmailStr] = None
    phone: Optional[str] = None
    mobile: Optional[str] = None
    
    # Identification
    id_type: Optional[str] = None
    id_number: Optional[str] = None
    tax_id: Optional[str] = None
    
    # Personal Information
    date_of_birth: Optional[date] = None
    gender: Optional[Gender] = None
    marital_status: Optional[MaritalStatus] = None
    nationality: Optional[str] = None
    blood_group: Optional[str] = None
    
    # Employment Details
    employment_type: EmploymentType = Field(default=EmploymentType.FULL_TIME)
    employment_status: EmploymentStatus = Field(default=EmploymentStatus.ACTIVE)
    date_of_joining: date = Field(..., description="Joining date")
    date_of_confirmation: Optional[date] = None
    department_id: Optional[str] = None
    designation_id: Optional[str] = None
    manager_id: Optional[str] = None
    cost_center_id: Optional[str] = None
    
    # Address Information
    current_address: Optional[str] = None
    permanent_address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    postal_code: Optional[str] = None
    
    # Compensation
    ctc: Optional[float] = None
    salary: Optional[float] = None
    salary_frequency: str = Field(default="monthly")
    currency: str = Field(default="USD")
    
    # Additional
    reporting_manager_id: Optional[str] = None
    emergency_contact: Optional[str] = None
    emergency_phone: Optional[str] = None
    work_location: Optional[str] = None
    
    class Config:
        schema_extra = {
            "example": {
                "company_id": "comp_123456",
                "employee_code": "EMP001",
                "first_name": "John",
                "last_name": "Doe",
                "email": "john.doe@acme.com",
                "date_of_joining": "2026-01-15",
                "employment_type": "full_time",
                "department_id": "dept_123456"
            }
        }


class EmployeeUpdateRequest(BaseModel):
    """Request schema for updating an employee."""
    first_name: Optional[str] = None
    middle_name: Optional[str] = None
    last_name: Optional[str] = None
    personal_email: Optional[EmailStr] = None
    phone: Optional[str] = None
    mobile: Optional[str] = None
    gender: Optional[Gender] = None
    marital_status: Optional[MaritalStatus] = None
    department_id: Optional[str] = None
    designation_id: Optional[str] = None
    manager_id: Optional[str] = None
    employment_status: Optional[EmploymentStatus] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    postal_code: Optional[str] = None
    salary: Optional[float] = None
    work_location: Optional[str] = None
    emergency_contact: Optional[str] = None
    emergency_phone: Optional[str] = None
    
    class Config:
        schema_extra = {
            "example": {
                "first_name": "John",
                "department_id": "dept_123456",
                "salary": 75000,
                "employment_status": "active"
            }
        }


class DesignationCreateRequest(BaseModel):
    """Request schema for creating a designation."""
    company_id: str = Field(..., description="Company ID")
    code: str = Field(..., min_length=1, max_length=50, description="Designation code")
    name: str = Field(..., min_length=1, max_length=255, description="Designation name")
    description: Optional[str] = None
    level: Optional[int] = None
    ctc_range_min: Optional[float] = None
    ctc_range_max: Optional[float] = None
    
    class Config:
        schema_extra = {
            "example": {
                "company_id": "comp_123456",
                "code": "SE-2",
                "name": "Senior Engineer",
                "level": 3,
                "ctc_range_min": 1000000,
                "ctc_range_max": 1500000
            }
        }


class DesignationUpdateRequest(BaseModel):
    """Request schema for updating a designation."""
    name: Optional[str] = None
    description: Optional[str] = None
    level: Optional[int] = None
    ctc_range_min: Optional[float] = None
    ctc_range_max: Optional[float] = None
    is_active: Optional[bool] = None
    
    class Config:
        schema_extra = {
            "example": {
                "name": "Senior Engineer - Updated",
                "level": 4,
                "ctc_range_max": 2000000
            }
        }


# Response Schemas
class DesignationResponse(BaseModel):
    """Response schema for designation."""
    designation_id: str
    company_id: str
    code: str
    name: str
    description: Optional[str] = None
    level: Optional[int] = None
    ctc_range_min: Optional[float] = None
    ctc_range_max: Optional[float] = None
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
        schema_extra = {
            "example": {
                "designation_id": "des_123456",
                "company_id": "comp_123456",
                "code": "SE-2",
                "name": "Senior Engineer",
                "level": 3,
                "is_active": True,
                "created_at": "2026-01-15T10:30:00Z"
            }
        }


class EmployeeResponse(BaseModel):
    """Response schema for employee (detailed)."""
    employee_id: str
    company_id: str
    employee_code: str
    first_name: str
    middle_name: Optional[str] = None
    last_name: str
    email: str
    personal_email: Optional[str] = None
    phone: Optional[str] = None
    mobile: Optional[str] = None
    date_of_birth: Optional[date] = None
    gender: Optional[Gender] = None
    marital_status: Optional[MaritalStatus] = None
    nationality: Optional[str] = None
    employment_type: EmploymentType
    employment_status: EmploymentStatus
    date_of_joining: date
    date_of_confirmation: Optional[date] = None
    department_id: Optional[str] = None
    designation_id: Optional[str] = None
    manager_id: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    postal_code: Optional[str] = None
    ctc: Optional[float] = None
    salary: Optional[float] = None
    salary_frequency: str
    currency: str
    work_location: Optional[str] = None
    emergency_contact: Optional[str] = None
    emergency_phone: Optional[str] = None
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
        schema_extra = {
            "example": {
                "employee_id": "emp_123456",
                "company_id": "comp_123456",
                "employee_code": "EMP001",
                "first_name": "John",
                "last_name": "Doe",
                "email": "john.doe@acme.com",
                "employment_status": "active",
                "employment_type": "full_time",
                "date_of_joining": "2026-01-15",
                "salary": 75000,
                "is_active": True,
                "created_at": "2026-01-15T10:30:00Z"
            }
        }


class EmployeeListResponse(BaseModel):
    """Response schema for employee list (summary)."""
    employee_id: str
    employee_code: str
    first_name: str
    last_name: str
    email: str
    employment_status: EmploymentStatus
    employment_type: EmploymentType
    department_id: Optional[str] = None
    designation_id: Optional[str] = None
    date_of_joining: date
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True
        schema_extra = {
            "example": {
                "employee_id": "emp_123456",
                "employee_code": "EMP001",
                "first_name": "John",
                "last_name": "Doe",
                "email": "john.doe@acme.com",
                "employment_status": "active",
                "employment_type": "full_time",
                "date_of_joining": "2026-01-15",
                "is_active": True,
                "created_at": "2026-01-15T10:30:00Z"
            }
        }


class EmployeeStatsResponse(BaseModel):
    """Response schema for employee statistics."""
    employee_id: str
    name: str
    email: str
    employment_status: EmploymentStatus
    department: Optional[str] = None
    designation: Optional[str] = None
    years_of_service: Optional[float] = None
    
    class Config:
        from_attributes = True


class BulkEmployeeResponse(BaseModel):
    """Response for bulk operations."""
    total: int
    successful: int
    failed: int
    employees: List[EmployeeListResponse]
    
    class Config:
        schema_extra = {
            "example": {
                "total": 50,
                "successful": 50,
                "failed": 0,
                "employees": []
            }
        }


class BulkDesignationResponse(BaseModel):
    """Response for bulk designation operations."""
    total: int
    successful: int
    failed: int
    designations: List[DesignationResponse]
    
    class Config:
        schema_extra = {
            "example": {
                "total": 10,
                "successful": 10,
                "failed": 0,
                "designations": []
            }
        }