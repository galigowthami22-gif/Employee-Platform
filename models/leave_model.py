"""
Leave Management Model (HRMS - Phase 14)
Comprehensive leave request and leave balance tracking system.
"""

from datetime import datetime, date
from sqlalchemy import Column, String, Date, DateTime, Enum, ForeignKey, Text, Integer, JSON, Index
from sqlalchemy.orm import relationship
from core.base_model import BaseModel
import enum


class LeaveType(str, enum.Enum):
    """Leave type enumeration."""
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


class LeaveStatus(str, enum.Enum):
    """Leave request status enumeration."""
    DRAFT = "draft"
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    CANCELLED = "cancelled"
    REVOKED = "revoked"


class LeaveRequest(BaseModel):
    """
    Leave Request model for managing employee leave requests.
    
    Attributes:
        leave_request_id: Primary key (UUID)
        company_id: Foreign key to Company (multi-tenancy)
        employee_id: Foreign key to Employee requesting leave
        leave_type: Type of leave (casual, sick, earned, etc.)
        start_date: Leave start date (inclusive)
        end_date: Leave end date (inclusive)
        days_requested: Total number of leave days
        reason: Reason for leave request
        status: Request status (pending, approved, rejected, etc.)
        
        --- Approvals ---
        approved_by: Manager/HR who approved the request
        approved_at: Timestamp of approval
        rejection_reason: Reason for rejection (if applicable)
        rejected_at: Timestamp of rejection
        
        --- Tracking ---
        created_by: User who created the request
        updated_by: User who last updated the request
    """
    __tablename__ = "leave_requests"

    # Primary & Foreign Keys
    leave_request_id = Column(String(36), primary_key=True)
    company_id = Column(String(36), ForeignKey("companies.company_id"), nullable=False)
    employee_id = Column(String(36), ForeignKey("employees.employee_id", ondelete="CASCADE"), nullable=False)
    
    # Leave Details
    leave_type = Column(Enum(LeaveType), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    days_requested = Column(Integer, nullable=False)
    reason = Column(Text, nullable=True)
    
    # Status & Approval
    status = Column(Enum(LeaveStatus), nullable=False, default=LeaveStatus.PENDING)
    approved_by = Column(String(36), nullable=True)  # User ID of approver
    approved_at = Column(DateTime, nullable=True)
    rejection_reason = Column(Text, nullable=True)
    rejected_at = Column(DateTime, nullable=True)
    
    # Additional Info
    attachments = Column(JSON, nullable=True)  # List of attachment URLs
    notes = Column(Text, nullable=True)
    
    # Audit Fields (inherited from BaseModel)
    # is_deleted, deleted_at, created_at, updated_at
    created_by = Column(String(36), nullable=True)
    updated_by = Column(String(36), nullable=True)
    
    # Relationships
    employee = relationship("Employee", foreign_keys=[employee_id])
    company = relationship("Company", foreign_keys=[company_id])
    
    # Indexes
    __table_args__ = (
        Index('idx_leave_company_employee', 'company_id', 'employee_id'),
        Index('idx_leave_company_status', 'company_id', 'status'),
        Index('idx_leave_employee_dates', 'employee_id', 'start_date', 'end_date'),
        Index('idx_leave_type', 'leave_type'),
        Index('idx_leave_is_deleted', 'is_deleted'),
    )


class LeaveBalance(BaseModel):
    """
    Leave Balance model for tracking employee's leave balances.
    
    Attributes:
        balance_id: Primary key (UUID)
        company_id: Foreign key to Company
        employee_id: Foreign key to Employee
        leave_type: Type of leave
        financial_year: Financial year (e.g., 2025-2026)
        total_allocated: Total leave days allocated for the year
        used: Leave days used
        pending: Days pending approval
        balance: Remaining balance (allocated - used)
        last_updated: Last update timestamp
    """
    __tablename__ = "leave_balances"

    # Primary & Foreign Keys
    balance_id = Column(String(36), primary_key=True)
    company_id = Column(String(36), ForeignKey("companies.company_id"), nullable=False)
    employee_id = Column(String(36), ForeignKey("employees.employee_id", ondelete="CASCADE"), nullable=False)
    
    # Leave Type & Period
    leave_type = Column(Enum(LeaveType), nullable=False)
    financial_year = Column(String(9), nullable=False)  # e.g., "2025-2026"
    
    # Balance Details
    total_allocated = Column(Integer, nullable=False, default=0)
    used = Column(Integer, nullable=False, default=0)
    pending = Column(Integer, nullable=False, default=0)
    balance = Column(Integer, nullable=False, default=0)
    carried_forward = Column(Integer, nullable=False, default=0)  # From previous year
    
    # Tracking
    last_updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    employee = relationship("Employee", foreign_keys=[employee_id])
    company = relationship("Company", foreign_keys=[company_id])
    
    # Indexes
    __table_args__ = (
        Index('idx_leave_balance_company_employee', 'company_id', 'employee_id'),
        Index('idx_leave_balance_year', 'financial_year'),
    )