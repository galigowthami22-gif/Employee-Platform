"""
Payroll & Salary Schema (HRMS - Phase 15)
Pydantic schemas for salary structure and payroll management.
"""

from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import date, datetime
from decimal import Decimal
from enum import Enum


class SalaryFrequencyEnum(str, Enum):
    """Salary payment frequency."""
    MONTHLY = "monthly"
    QUARTERLY = "quarterly"
    HALF_YEARLY = "half_yearly"
    ANNUALLY = "annually"
    WEEKLY = "weekly"


class PaymentModeEnum(str, Enum):
    """Payment methods."""
    BANK_TRANSFER = "bank_transfer"
    CHEQUE = "cheque"
    CASH = "cash"
    CREDIT_CARD = "credit_card"
    DIGITAL_WALLET = "digital_wallet"


class PayrollStatusEnum(str, Enum):
    """Payroll status."""
    DRAFT = "draft"
    PROCESSED = "processed"
    APPROVED = "approved"
    REJECTED = "rejected"
    PAID = "paid"
    VOIDED = "voided"


# ============================================================================
# SALARY STRUCTURE SCHEMAS
# ============================================================================

class SalaryStructureCreateRequest(BaseModel):
    """Schema for creating salary structure."""
    employee_id: str = Field(..., description="Employee ID")
    effective_from: date = Field(..., description="Effective from date")
    effective_to: Optional[date] = Field(None, description="Effective to date")
    
    # Compensation
    ctc: Decimal = Field(..., description="Cost to Company")
    basic_salary: Decimal = Field(..., description="Basic salary")
    hra: Optional[Decimal] = Field(0, description="House Rent Allowance")
    conveyance: Optional[Decimal] = Field(0, description="Conveyance allowance")
    medical_allowance: Optional[Decimal] = Field(0, description="Medical allowance")
    other_allowances: Optional[Decimal] = Field(0, description="Other allowances")
    
    # Deductions
    professional_tax: Optional[Decimal] = Field(0, description="Professional tax")
    provident_fund: Optional[Decimal] = Field(0, description="Provident fund")
    insurance: Optional[Decimal] = Field(0, description="Insurance")
    other_deductions: Optional[Decimal] = Field(0, description="Other deductions")
    
    # Configuration
    frequency: SalaryFrequencyEnum = Field(default=SalaryFrequencyEnum.MONTHLY)
    currency: str = Field(default="USD")
    notes: Optional[str] = Field(None)

    class Config:
        json_schema_extra = {
            "example": {
                "employee_id": "emp-001",
                "effective_from": "2026-07-01",
                "ctc": 600000,
                "basic_salary": 300000,
                "hra": 90000,
                "conveyance": 15000,
                "medical_allowance": 5000,
                "professional_tax": 2500,
                "provident_fund": 18000
            }
        }


class SalaryStructureResponse(BaseModel):
    """Response schema for salary structure."""
    structure_id: str
    company_id: str
    employee_id: str
    effective_from: date
    effective_to: Optional[date]
    ctc: Decimal
    basic_salary: Decimal
    hra: Decimal
    conveyance: Decimal
    medical_allowance: Decimal
    other_allowances: Decimal
    gross_salary: Decimal
    professional_tax: Decimal
    provident_fund: Decimal
    insurance: Decimal
    other_deductions: Decimal
    net_salary: Decimal
    frequency: str
    currency: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# ============================================================================
# PAYROLL SCHEMAS
# ============================================================================

class PayrollCreateRequest(BaseModel):
    """Schema for creating payroll entry."""
    employee_id: str = Field(..., description="Employee ID")
    payroll_month: date = Field(..., description="Payroll month (1st of month)")
    
    # Attendance
    working_days: Decimal = Field(..., description="Total working days")
    days_present: Decimal = Field(0, description="Days present")
    days_absent: Decimal = Field(0, description="Days absent")
    days_leave: Decimal = Field(0, description="Days on leave")
    
    # Salary Components
    basic_salary: Decimal = Field(..., description="Basic salary")
    hra: Optional[Decimal] = Field(0)
    conveyance: Optional[Decimal] = Field(0)
    medical_allowance: Optional[Decimal] = Field(0)
    other_allowances: Optional[Decimal] = Field(0)
    bonus: Optional[Decimal] = Field(0)
    incentive: Optional[Decimal] = Field(0)
    
    # Deductions
    professional_tax: Optional[Decimal] = Field(0)
    provident_fund: Optional[Decimal] = Field(0)
    insurance: Optional[Decimal] = Field(0)
    loan_deduction: Optional[Decimal] = Field(0)
    other_deductions: Optional[Decimal] = Field(0)
    
    # Payment
    advance_payment: Optional[Decimal] = Field(0)
    notes: Optional[str] = Field(None)

    class Config:
        json_schema_extra = {
            "example": {
                "employee_id": "emp-001",
                "payroll_month": "2026-07-01",
                "working_days": 22,
                "days_present": 20,
                "basic_salary": 300000,
                "hra": 90000,
                "professional_tax": 2500
            }
        }


class PayrollApproveRequest(BaseModel):
    """Schema for approving payroll."""
    is_approved: bool = Field(..., description="Approval decision")
    notes: Optional[str] = Field(None, description="Notes")


class PayrollPaymentRequest(BaseModel):
    """Schema for marking payroll as paid."""
    payment_mode: PaymentModeEnum = Field(..., description="Payment method")
    paid_date: date = Field(..., description="Date of payment")
    notes: Optional[str] = Field(None)


class PayrollResponse(BaseModel):
    """Response schema for payroll entry."""
    payroll_id: str
    company_id: str
    employee_id: str
    payroll_month: date
    working_days: Decimal
    days_present: Decimal
    days_absent: Decimal
    days_leave: Decimal
    basic_salary: Decimal
    hra: Decimal
    conveyance: Decimal
    medical_allowance: Decimal
    other_allowances: Decimal
    bonus: Decimal
    incentive: Decimal
    gross_salary: Decimal
    professional_tax: Decimal
    provident_fund: Decimal
    insurance: Decimal
    loan_deduction: Decimal
    other_deductions: Decimal
    total_deductions: Decimal
    net_salary: Decimal
    advance_payment: Decimal
    final_amount: Decimal
    status: str
    approved_by: Optional[str]
    approved_at: Optional[datetime]
    paid_date: Optional[date]
    payment_mode: Optional[str]
    reconciled: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class PayrollListResponse(BaseModel):
    """Response for payroll list."""
    total: int
    page: int
    limit: int
    records: List[PayrollResponse]


class PayrollSummaryResponse(BaseModel):
    """Summary of payroll processing."""
    period: date
    total_employees: int
    total_salary: Decimal
    total_deductions: Decimal
    total_net_salary: Decimal
    processed_count: int
    approved_count: int
    paid_count: int
    pending_count: int

    class Config:
        json_schema_extra = {
            "example": {
                "period": "2026-07-01",
                "total_employees": 100,
                "total_salary": 60000000,
                "total_deductions": 8000000,
                "total_net_salary": 52000000,
                "processed_count": 95,
                "approved_count": 90,
                "paid_count": 85,
                "pending_count": 10
            }
        }