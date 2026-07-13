"""
Attendance Schema (HRMS - Phase 13)
Pydantic schemas for attendance management.
"""

from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import datetime, date
from enum import Enum


class AttendanceStatusEnum(str, Enum):
    """Attendance status values."""
    PRESENT = "present"
    ABSENT = "absent"
    LEAVE = "leave"
    HALF_DAY = "half_day"
    WORK_FROM_HOME = "work_from_home"
    HOLIDAY = "holiday"
    SICK_LEAVE = "sick_leave"
    MEDICAL_LEAVE = "medical_leave"
    COMPENSATORY_OFF = "compensatory_off"
    EMERGENCY_LEAVE = "emergency_leave"


class CheckInOutTypeEnum(str, Enum):
    """Check-in/out type values."""
    BIOMETRIC = "biometric"
    WEB = "web"
    MOBILE = "mobile"
    MANUAL = "manual"
    API = "api"


# ============================================================================
# REQUEST SCHEMAS
# ============================================================================

class AttendanceCheckInRequest(BaseModel):
    """Schema for employee check-in."""
    employee_id: str = Field(..., description="Employee ID")
    check_in_location: Optional[str] = Field(None, description="Location/device info")
    check_in_type: CheckInOutTypeEnum = Field(default=CheckInOutTypeEnum.WEB, description="Check-in method")
    metadata: Optional[dict] = Field(None, description="Additional metadata")

    class Config:
        schema_extra = {
            "example": {
                "employee_id": "emp-001",
                "check_in_location": "Office Main Gate",
                "check_in_type": "biometric",
                "metadata": {"device_id": "bio-001"}
            }
        }


class AttendanceCheckOutRequest(BaseModel):
    """Schema for employee check-out."""
    employee_id: str = Field(..., description="Employee ID")
    check_out_location: Optional[str] = Field(None, description="Location/device info")
    check_out_type: CheckInOutTypeEnum = Field(default=CheckInOutTypeEnum.WEB, description="Check-out method")
    metadata: Optional[dict] = Field(None, description="Additional metadata")

    class Config:
        schema_extra = {
            "example": {
                "employee_id": "emp-001",
                "check_out_location": "Office Main Gate",
                "check_out_type": "biometric",
                "metadata": {"device_id": "bio-001"}
            }
        }


class AttendanceMarkRequest(BaseModel):
    """Schema for manually marking attendance."""
    employee_id: str = Field(..., description="Employee ID")
    attendance_date: date = Field(..., description="Date of attendance")
    status: AttendanceStatusEnum = Field(..., description="Attendance status")
    check_in_time: Optional[datetime] = Field(None, description="Check-in time")
    check_out_time: Optional[datetime] = Field(None, description="Check-out time")
    reason: Optional[str] = Field(None, description="Reason for status")
    notes: Optional[str] = Field(None, description="Additional notes")

    class Config:
        schema_extra = {
            "example": {
                "employee_id": "emp-001",
                "attendance_date": "2026-07-08",
                "status": "present",
                "check_in_time": "2026-07-08T09:00:00",
                "check_out_time": "2026-07-08T17:30:00",
                "reason": "Regular attendance"
            }
        }


class AttendanceApproveRequest(BaseModel):
    """Schema for approving/verifying attendance."""
    attendance_id: str = Field(..., description="Attendance ID")
    is_approved: bool = Field(..., description="Approval status")
    notes: Optional[str] = Field(None, description="Approval notes")

    class Config:
        schema_extra = {
            "example": {
                "attendance_id": "att-001",
                "is_approved": True,
                "notes": "Approved by manager"
            }
        }


# ============================================================================
# RESPONSE SCHEMAS
# ============================================================================

class AttendanceResponse(BaseModel):
    """Response schema for single attendance record."""
    attendance_id: str
    company_id: str
    employee_id: str
    attendance_date: date
    
    check_in_time: Optional[datetime]
    check_in_location: Optional[str]
    check_in_type: Optional[str]
    
    check_out_time: Optional[datetime]
    check_out_location: Optional[str]
    check_out_type: Optional[str]
    
    status: str
    working_hours: Optional[str]
    is_early_checkout: Optional[str]
    
    is_approved: str
    approved_by: Optional[str]
    approved_at: Optional[datetime]
    
    reason: Optional[str]
    notes: Optional[str]
    
    created_at: datetime
    updated_at: datetime
    created_by: Optional[str]
    updated_by: Optional[str]
    is_deleted: bool

    class Config:
        from_attributes = True
        schema_extra = {
            "example": {
                "attendance_id": "att-001",
                "company_id": "comp-001",
                "employee_id": "emp-001",
                "attendance_date": "2026-07-08",
                "check_in_time": "2026-07-08T09:15:00",
                "check_in_location": "Office Main Gate",
                "check_in_type": "biometric",
                "check_out_time": "2026-07-08T17:30:00",
                "check_out_location": "Office Main Gate",
                "check_out_type": "biometric",
                "status": "present",
                "working_hours": "8.25",
                "is_early_checkout": "N",
                "is_approved": "Y",
                "approved_by": "mgr-001",
                "approved_at": "2026-07-08T18:00:00",
                "created_at": "2026-07-08T09:16:00",
                "updated_at": "2026-07-08T17:31:00"
            }
        }


class AttendanceListResponse(BaseModel):
    """Response schema for attendance list."""
    total: int
    page: int
    limit: int
    records: List[AttendanceResponse]

    class Config:
        schema_extra = {
            "example": {
                "total": 100,
                "page": 1,
                "limit": 10,
                "records": []
            }
        }


class DailyAttendanceReportResponse(BaseModel):
    """Response schema for daily attendance report."""
    report_date: date
    total_employees: int
    present: int
    absent: int
    half_day: int
    work_from_home: int
    leave: int
    sick_leave: int
    holiday: int
    on_time_count: int
    late_count: int
    created_at: datetime

    class Config:
        schema_extra = {
            "example": {
                "report_date": "2026-07-08",
                "total_employees": 50,
                "present": 45,
                "absent": 3,
                "half_day": 1,
                "work_from_home": 1,
                "leave": 0,
                "sick_leave": 0,
                "holiday": 0,
                "on_time_count": 40,
                "late_count": 5,
                "created_at": "2026-07-08T23:59:00"
            }
        }


class EmployeeAttendanceStatsResponse(BaseModel):
    """Response schema for employee attendance statistics."""
    employee_id: str
    employee_name: str
    attendance_date: date
    total_days: int
    present_days: int
    absent_days: int
    half_days: int
    leave_days: int
    work_from_home_days: int
    average_working_hours: str
    attendance_percentage: float

    class Config:
        schema_extra = {
            "example": {
                "employee_id": "emp-001",
                "employee_name": "John Doe",
                "attendance_date": "2026-07-08",
                "total_days": 20,
                "present_days": 18,
                "absent_days": 1,
                "half_days": 1,
                "leave_days": 0,
                "work_from_home_days": 0,
                "average_working_hours": "8.5",
                "attendance_percentage": 90.0
            }
        }