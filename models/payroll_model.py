"""
Payroll Model (HRMS - Phase 15)
Monthly/periodic payroll processing and salary payment tracking.
"""

from datetime import datetime, date
from sqlalchemy import Column, String, Date, DateTime, Enum, ForeignKey, DECIMAL, Text, JSON, Index
from sqlalchemy.orm import relationship
from core.base_model import BaseModel
import enum


class PayrollStatus(str, enum.Enum):
    """Payroll processing status."""
    DRAFT = "draft"
    PROCESSED = "processed"
    APPROVED = "approved"
    REJECTED = "rejected"
    PAID = "paid"
    VOIDED = "voided"


class PaymentMode(str, enum.Enum):
    """Payment method."""
    BANK_TRANSFER = "bank_transfer"
    CHEQUE = "cheque"
    CASH = "cash"
    CREDIT_CARD = "credit_card"
    DIGITAL_WALLET = "digital_wallet"


class Payroll(BaseModel):
    """
    Payroll model for processing and tracking monthly salary payments.
    
    Attributes:
        payroll_id: Primary key (UUID)
        company_id: Foreign key to Company (multi-tenancy)
        employee_id: Foreign key to Employee
        payroll_month: Year and month for payroll (e.g., 2026-07-01)
        
        --- Attendance & Adjustments ---
        working_days: Total working days in the month
        days_present: Days employee was present
        days_absent: Days employee was absent
        days_leave: Days on approved leave
        attendance_based_salary: Salary calculated on attendance
        
        --- Salary Components ---
        basic_salary: Basic salary for the period
        hra: House Rent Allowance
        conveyance: Conveyance allowance
        medical_allowance: Medical allowance
        other_allowances: Other allowances
        gross_salary: Total salary before deductions
        
        --- Deductions ---
        professional_tax: Professional tax
        provident_fund: EPF/Provident fund
        insurance: Insurance deductions
        other_deductions: Other deductions
        total_deductions: Total deductions
        
        --- Final Amount ---
        net_salary: Net salary (gross - deductions)
        advance_payment: Advance salary paid
        final_amount: Final payment amount
        
        --- Status & Tracking ---
        status: Payroll status (draft, processed, approved, paid)
        approved_by: Person who approved payroll
        approved_at: Approval timestamp
        paid_date: Date salary was paid
        payment_mode: Payment method used
        
        --- Reconciliation ---
        reconciled: Whether payroll has been reconciled
        reconciliation_date: Date of reconciliation
    """
    __tablename__ = "payroll"

    # Primary & Foreign Keys
    payroll_id = Column(String(36), primary_key=True)
    company_id = Column(String(36), ForeignKey("companies.company_id"), nullable=False)
    employee_id = Column(String(36), ForeignKey("employees.employee_id", ondelete="CASCADE"), nullable=False)
    salary_structure_id = Column(String(36), nullable=True)  # Reference to salary structure used
    
    # Period
    payroll_month = Column(Date, nullable=False)  # First day of the month
    
    # Attendance & Days
    working_days = Column(DECIMAL(5, 2), nullable=False)
    days_present = Column(DECIMAL(5, 2), nullable=False, default=0)
    days_absent = Column(DECIMAL(5, 2), nullable=False, default=0)
    days_leave = Column(DECIMAL(5, 2), nullable=False, default=0)
    attendance_based_salary = Column(DECIMAL(15, 2), nullable=True)
    
    # Salary Components (Earnings)
    basic_salary = Column(DECIMAL(15, 2), nullable=False)
    hra = Column(DECIMAL(15, 2), nullable=True, default=0)
    conveyance = Column(DECIMAL(15, 2), nullable=True, default=0)
    medical_allowance = Column(DECIMAL(15, 2), nullable=True, default=0)
    other_allowances = Column(DECIMAL(15, 2), nullable=True, default=0)
    bonus = Column(DECIMAL(15, 2), nullable=True, default=0)
    incentive = Column(DECIMAL(15, 2), nullable=True, default=0)
    
    # Gross Salary
    gross_salary = Column(DECIMAL(15, 2), nullable=False)
    
    # Deductions
    professional_tax = Column(DECIMAL(15, 2), nullable=True, default=0)
    provident_fund = Column(DECIMAL(15, 2), nullable=True, default=0)
    insurance = Column(DECIMAL(15, 2), nullable=True, default=0)
    loan_deduction = Column(DECIMAL(15, 2), nullable=True, default=0)
    other_deductions = Column(DECIMAL(15, 2), nullable=True, default=0)
    total_deductions = Column(DECIMAL(15, 2), nullable=False)
    
    # Final Salary
    net_salary = Column(DECIMAL(15, 2), nullable=False)
    advance_payment = Column(DECIMAL(15, 2), nullable=True, default=0)
    final_amount = Column(DECIMAL(15, 2), nullable=False)
    
    # Status & Approvals
    status = Column(Enum(PayrollStatus), nullable=False, default=PayrollStatus.DRAFT)
    approved_by = Column(String(36), nullable=True)
    approved_at = Column(DateTime, nullable=True)
    paid_date = Column(Date, nullable=True)
    payment_mode = Column(Enum(PaymentMode), nullable=True)
    
    # Reconciliation
    reconciled = Column(String(1), default='N')  # Y/N
    reconciliation_date = Column(DateTime, nullable=True)
    
    # Additional Information
    notes = Column(Text, nullable=True)
    payslip_url = Column(String(500), nullable=True)
    additional_data = Column(JSON, nullable=True)
    
    # Audit Fields (inherited from BaseModel)
    # is_deleted, deleted_at, created_at, updated_at
    created_by = Column(String(36), nullable=True)
    updated_by = Column(String(36), nullable=True)
    
    # Relationships
    employee = relationship("Employee", foreign_keys=[employee_id])
    company = relationship("Company", foreign_keys=[company_id])
    
    # Indexes
    __table_args__ = (
        Index('idx_payroll_company_month', 'company_id', 'payroll_month'),
        Index('idx_payroll_employee_month', 'employee_id', 'payroll_month'),
        Index('idx_payroll_status', 'status'),
        Index('idx_payroll_is_deleted', 'is_deleted'),
    )