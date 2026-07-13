"""
Attendance Model (HRMS - Phase 13)
Comprehensive attendance tracking with check-in/check-out, status, and reporting.
"""

from datetime import datetime, date
from sqlalchemy import Column, String, DateTime, Enum, ForeignKey, Date, Time, Text, Index, JSON
from sqlalchemy.orm import relationship
from core.base_model import BaseModel
import enum


class AttendanceStatus(str, enum.Enum):
    """Attendance status enumeration."""
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


class CheckInOutType(str, enum.Enum):
    """Type of check-in/check-out (biometric, web, mobile, manual)."""
    BIOMETRIC = "biometric"
    WEB = "web"
    MOBILE = "mobile"
    MANUAL = "manual"
    API = "api"


class Attendance(BaseModel):
    """
    Attendance model for tracking daily employee attendance.
    Supports check-in/check-out with timestamps, status marking, and reporting.
    
    Attributes:
        attendance_id: Primary key (UUID)
        company_id: Foreign key to Company (multi-tenancy)
        employee_id: Foreign key to Employee
        attendance_date: Date of attendance
        
        --- Check-in/Check-out Details ---
        check_in_time: Time when employee checked in
        check_in_location: Location/device where employee checked in
        check_in_type: Method of check-in (biometric, web, mobile, manual)
        
        check_out_time: Time when employee checked out
        check_out_location: Location/device where employee checked out
        check_out_type: Method of check-out
        
        --- Status & Duration ---
        status: Attendance status (present, absent, leave, half_day, etc.)
        working_hours: Total working hours (calculated as check_out_time - check_in_time)
        is_early_checkout: Boolean for early checkout
        
        --- Notes & Metadata ---
        notes: Notes or remarks for the attendance record
        reason: Reason for absence, leave, or half-day
        metadata: Additional metadata as JSON (device info, IP, etc.)
        
        --- Approval & Auditing ---
        approved_by: Manager who approved/verified the attendance
        approved_at: Timestamp of approval
        is_approved: Whether attendance is verified/approved
    """
    __tablename__ = "attendance"

    # Primary & Foreign Keys
    attendance_id = Column(String(36), primary_key=True)
    company_id = Column(String(36), ForeignKey("companies.company_id"), nullable=False)
    employee_id = Column(String(36), ForeignKey("employees.employee_id", ondelete="CASCADE"), nullable=False)
    
    # Date Information
    attendance_date = Column(Date, nullable=False)
    
    # Check-in Details
    check_in_time = Column(DateTime, nullable=True)
    check_in_location = Column(String(255), nullable=True)
    check_in_type = Column(Enum(CheckInOutType), nullable=True)
    
    # Check-out Details
    check_out_time = Column(DateTime, nullable=True)
    check_out_location = Column(String(255), nullable=True)
    check_out_type = Column(Enum(CheckInOutType), nullable=True)
    
    # Status Information
    status = Column(Enum(AttendanceStatus), nullable=False, default=AttendanceStatus.ABSENT)
    working_hours = Column(String(10), nullable=True)  # e.g., "8.5" for 8 hours 30 minutes
    is_early_checkout = Column(String(1), default='N')  # 'Y' or 'N'
    
    # Notes & Metadata
    notes = Column(Text, nullable=True)
    reason = Column(String(255), nullable=True)
    attributes = Column(JSON, nullable=True)
    
    # Approval Information
    approved_by = Column(String(36), nullable=True)  # User ID of approver
    approved_at = Column(DateTime, nullable=True)
    is_approved = Column(String(1), default='N')  # 'Y' or 'N'
    
    # Audit Fields (inherited from BaseModel)
    # is_deleted, deleted_at, created_at, updated_at
    
    # Standard audit fields for this table
    created_by = Column(String(36), nullable=True)
    updated_by = Column(String(36), nullable=True)
    
    # Relationships
    employee = relationship("Employee", foreign_keys=[employee_id])
    company = relationship("Company", foreign_keys=[company_id])
    
    # Indexes for performance
    __table_args__ = (
        Index('idx_attendance_company_employee', 'company_id', 'employee_id'),
        Index('idx_attendance_company_date', 'company_id', 'attendance_date'),
        Index('idx_attendance_employee_date', 'employee_id', 'attendance_date'),
        Index('idx_attendance_status', 'status'),
        Index('idx_attendance_is_deleted', 'is_deleted'),
    )