"""
Department & Team Schema
Pydantic schemas for department and team-related requests and responses.
"""

from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum


class DepartmentStatus(str, Enum):
    """Department status."""
    ACTIVE = "active"
    INACTIVE = "inactive"
    ARCHIVED = "archived"


# Request Schemas
class DepartmentCreateRequest(BaseModel):
    """Request schema for creating a department."""
    company_id: str = Field(..., description="Company ID")
    branch_id: Optional[str] = None
    parent_department_id: Optional[str] = None
    code: str = Field(..., min_length=1, max_length=50, description="Department code")
    name: str = Field(..., min_length=1, max_length=255, description="Department name")
    description: Optional[str] = None
    head_id: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    location: Optional[str] = None
    budget: Optional[float] = None
    
    class Config:
        schema_extra = {
            "example": {
                "company_id": "comp_123456",
                "code": "HR",
                "name": "Human Resources",
                "head_id": "emp_123456",
                "budget": 500000
            }
        }


class DepartmentUpdateRequest(BaseModel):
    """Request schema for updating a department."""
    name: Optional[str] = None
    description: Optional[str] = None
    head_id: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    location: Optional[str] = None
    budget: Optional[float] = None
    status: Optional[DepartmentStatus] = None
    
    class Config:
        schema_extra = {
            "example": {
                "name": "Human Resources - Updated",
                "budget": 600000,
                "status": "active"
            }
        }


class TeamCreateRequest(BaseModel):
    """Request schema for creating a team."""
    company_id: str = Field(..., description="Company ID")
    department_id: str = Field(..., description="Department ID")
    branch_id: Optional[str] = None
    code: str = Field(..., min_length=1, max_length=50, description="Team code")
    name: str = Field(..., min_length=1, max_length=255, description="Team name")
    description: Optional[str] = None
    lead_id: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    location: Optional[str] = None
    capacity: Optional[str] = None
    
    class Config:
        schema_extra = {
            "example": {
                "company_id": "comp_123456",
                "department_id": "dept_123456",
                "code": "TEAM_A",
                "name": "Development Team A",
                "lead_id": "emp_123456"
            }
        }


class TeamUpdateRequest(BaseModel):
    """Request schema for updating a team."""
    name: Optional[str] = None
    description: Optional[str] = None
    lead_id: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    location: Optional[str] = None
    capacity: Optional[str] = None
    status: Optional[DepartmentStatus] = None
    
    class Config:
        schema_extra = {
            "example": {
                "name": "Development Team A - Updated",
                "lead_id": "emp_654321",
                "status": "active"
            }
        }


class TeamMemberCreateRequest(BaseModel):
    """Request schema for adding a team member."""
    employee_id: str = Field(..., description="Employee ID")
    role: Optional[str] = None
    allocation_percentage: int = Field(default=100, ge=0, le=100, description="Work allocation 0-100%")
    is_lead: bool = False
    joining_date: Optional[datetime] = None
    
    class Config:
        schema_extra = {
            "example": {
                "employee_id": "emp_123456",
                "role": "Senior Developer",
                "allocation_percentage": 100,
                "is_lead": False
            }
        }


class TeamMemberUpdateRequest(BaseModel):
    """Request schema for updating a team member."""
    role: Optional[str] = None
    allocation_percentage: Optional[int] = Field(None, ge=0, le=100)
    is_lead: Optional[bool] = None
    
    class Config:
        schema_extra = {
            "example": {
                "role": "Tech Lead",
                "allocation_percentage": 80,
                "is_lead": True
            }
        }


# Response Schemas
class TeamMemberResponse(BaseModel):
    """Response schema for team member."""
    member_id: str
    team_id: str
    employee_id: str
    role: Optional[str] = None
    allocation_percentage: int
    is_lead: bool
    joining_date: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
        schema_extra = {
            "example": {
                "member_id": "tmem_123456",
                "team_id": "team_123456",
                "employee_id": "emp_123456",
                "role": "Senior Developer",
                "allocation_percentage": 100,
                "is_lead": False,
                "created_at": "2026-01-15T10:30:00Z"
            }
        }


class DepartmentResponse(BaseModel):
    """Response schema for department (detailed)."""
    department_id: str
    company_id: str
    branch_id: Optional[str] = None
    parent_department_id: Optional[str] = None
    code: str
    name: str
    description: Optional[str] = None
    head_id: Optional[str] = None
    status: DepartmentStatus
    email: Optional[str] = None
    phone: Optional[str] = None
    location: Optional[str] = None
    budget: Optional[float] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
        schema_extra = {
            "example": {
                "department_id": "dept_123456",
                "company_id": "comp_123456",
                "code": "HR",
                "name": "Human Resources",
                "head_id": "emp_123456",
                "status": "active",
                "budget": 500000,
                "created_at": "2026-01-15T10:30:00Z"
            }
        }


class DepartmentListResponse(BaseModel):
    """Response schema for department list (summary)."""
    department_id: str
    company_id: str
    code: str
    name: str
    status: DepartmentStatus
    head_id: Optional[str] = None
    created_at: datetime
    
    class Config:
        from_attributes = True
        schema_extra = {
            "example": {
                "department_id": "dept_123456",
                "company_id": "comp_123456",
                "code": "HR",
                "name": "Human Resources",
                "status": "active",
                "created_at": "2026-01-15T10:30:00Z"
            }
        }


class TeamResponse(BaseModel):
    """Response schema for team (detailed)."""
    team_id: str
    company_id: str
    department_id: str
    branch_id: Optional[str] = None
    code: str
    name: str
    description: Optional[str] = None
    lead_id: Optional[str] = None
    status: DepartmentStatus
    email: Optional[str] = None
    phone: Optional[str] = None
    location: Optional[str] = None
    capacity: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    members: Optional[List[TeamMemberResponse]] = None
    
    class Config:
        from_attributes = True
        schema_extra = {
            "example": {
                "team_id": "team_123456",
                "company_id": "comp_123456",
                "department_id": "dept_123456",
                "code": "TEAM_A",
                "name": "Development Team A",
                "lead_id": "emp_123456",
                "status": "active",
                "created_at": "2026-01-15T10:30:00Z"
            }
        }


class TeamListResponse(BaseModel):
    """Response schema for team list (summary)."""
    team_id: str
    company_id: str
    department_id: str
    code: str
    name: str
    status: DepartmentStatus
    lead_id: Optional[str] = None
    created_at: datetime
    
    class Config:
        from_attributes = True
        schema_extra = {
            "example": {
                "team_id": "team_123456",
                "company_id": "comp_123456",
                "department_id": "dept_123456",
                "code": "TEAM_A",
                "name": "Development Team A",
                "status": "active",
                "created_at": "2026-01-15T10:30:00Z"
            }
        }


class DepartmentStatsResponse(BaseModel):
    """Response schema for department statistics."""
    department_id: str
    name: str
    code: str
    total_employees: int = 0
    total_teams: int = 0
    status: DepartmentStatus
    
    class Config:
        from_attributes = True


class BulkDepartmentResponse(BaseModel):
    """Response for bulk operations on departments."""
    total: int
    successful: int
    failed: int
    departments: List[DepartmentListResponse]
    
    class Config:
        schema_extra = {
            "example": {
                "total": 3,
                "successful": 3,
                "failed": 0,
                "departments": []
            }
        }


class BulkTeamResponse(BaseModel):
    """Response for bulk operations on teams."""
    total: int
    successful: int
    failed: int
    teams: List[TeamListResponse]
    
    class Config:
        schema_extra = {
            "example": {
                "total": 5,
                "successful": 5,
                "failed": 0,
                "teams": []
            }
        }
