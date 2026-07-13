"""
Leave Management Schema (HRMS - Phase 14)
Pydantic schemas for leave request and balance management.
"""

from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import date, datetime
from enum import Enum


class LeaveTypeEnum(str, Enum):
    """Leave type values."""
    CASUAL_LEAVE = "casual_leave"
    SICK_LEAVE = "sick_leave"
    EARNED_LEAVE = "earned_leave"
    MEDICAL_LEAVE = "medical_leave"
    MATERNITY_LEAVE = "maternity_leave"
    PATERNITY_LEAVE = "paternity_leave"
    BEREAVEMENT_LEAVE = "bereavement_leave"
    COMPENSATORY_OFF = "compensatory_off"
    UNPAID_LEAVE = "unpaid_leave"
    OTHER = "other"


class LeaveStatusEnum(str, Enum):
    """Leave status values."""
    DRAFT = "draft"
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    CANCELLED = "cancelled"
    REVOKED = "revoked"


# ============================================================================
# LEAVE REQUEST SCHEMAS
# ============================================================================

class LeaveRequestCreateRequest(BaseModel):
    """Schema for creating a leave request."""
    employee_id: str = Field(..., description="Employee ID")
    leave_type: LeaveTypeEnum = Field(..., description="Type of leave")
    start_date: date = Field(..., description="Leave start date")
    end_date: date = Field(..., description="Leave end date")
    reason: Optional[str] = Field(None, description="Reason for leave")
    attachments: Optional[List[str]] = Field(None, description="Attachment URLs")

    class Config:
        json_schema_extra = {
            "example": {
                "employee_id": "emp-001",
                "leave_type": "casual_leave",
                "start_date": "2026-07-15",
                "end_date": "2026-07-17",
                "reason": "Personal work"
            }
        }


class LeaveRequestApproveRequest(BaseModel):
    """Schema for approving/rejecting a leave request."""
    is_approved: bool = Field(..., description="Approval decision")
    rejection_reason: Optional[str] = Field(None, description="Reason for rejection (if applicable)")
    notes: Optional[str] = Field(None, description="Additional notes")

    class Config:
        json_schema_extra = {
            "example": {
                "is_approved": True,
                "notes": "Approved by manager"
            }
        }


# ============================================================================
# LEAVE REQUEST RESPONSE SCHEMAS
# ============================================================================

class LeaveRequestResponse(BaseModel):
    """Response schema for leave request."""
    leave_request_id: str
    company_id: str
    employee_id: str
    leave_type: str
    start_date: date
    end_date: date
    days_requested: int
    reason: Optional[str]
    status: str
    approved_by: Optional[str]
    approved_at: Optional[datetime]
    rejection_reason: Optional[str]
    rejected_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime
    created_by: Optional[str]
    is_deleted: bool

    class Config:
        from_attributes = True


class LeaveRequestListResponse(BaseModel):
    """Response schema for leave request list."""
    total: int
    page: int
    limit: int
    records: List[LeaveRequestResponse]


# ============================================================================
# LEAVE BALANCE SCHEMAS
# ============================================================================

class LeaveBalanceResponse(BaseModel):
    """Response schema for leave balance."""
    balance_id: str
    company_id: str
    employee_id: str
    leave_type: str
    financial_year: str
    total_allocated: int
    used: int
    pending: int
    balance: int
    carried_forward: int
    last_updated: datetime

    class Config:
        from_attributes = True


class EmployeeLeaveBalanceResponse(BaseModel):
    """Response schema for employee's all leave balances."""
    employee_id: str
    financial_year: str
    leave_balances: List[LeaveBalanceResponse]


# ============================================================================
# LEAVE ANALYTICS SCHEMAS
# ============================================================================

class LeaveAnalyticsResponse(BaseModel):
    """Leave analytics for period."""
    period: str
    total_leave_requests: int
    approved: int
    pending: int
    rejected: int
    average_leave_per_employee: float
    most_used_leave_type: str

    class Config:
        json_schema_extra = {
            "example": {
                "period": "2026-07",
                "total_leave_requests": 25,
                "approved": 20,
                "pending": 3,
                "rejected": 2,
                "average_leave_per_employee": 2.5,
                "most_used_leave_type": "casual_leave"
            }
        }