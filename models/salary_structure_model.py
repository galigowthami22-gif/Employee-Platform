"""
Salary Structure Model (HRMS - Phase 15)
Employee salary structure and compensation details.
"""

from datetime import datetime, date
from sqlalchemy import Column, String, Date, DateTime, Enum, ForeignKey, DECIMAL, Text, JSON, Index
from sqlalchemy.orm import relationship
from core.base_model import BaseModel
import enum


class SalaryFrequency(str, enum.Enum):
    """Salary payment frequency."""
    MONTHLY = "monthly"
    QUARTERLY = "quarterly"
    HALF_YEARLY = "half_yearly"
    ANNUALLY = "annually"
    WEEKLY = "weekly"


class SalaryStructure(BaseModel):
    """
    Salary Structure model defining employee compensation breakdown.
    
    Attributes:
        structure_id: Primary key (UUID)
        company_id: Foreign key to Company (multi-tenancy)
        employee_id: Foreign key to Employee
        effective_from: Date structure becomes effective
        effective_to: Date structure ends (null = ongoing)
        
        --- Compensation Components ---
        ctc: Cost to Company (total compensation)
        basic_salary: Basic salary
        hra: House Rent Allowance
        conveyance: Conveyance/Travel allowance
        medical_allowance: Medical allowance
        other_allowances: Other allowances
        gross_salary: Total salary before deductions
        
        --- Deductions ---
        professional_tax: Professional tax
        provident_fund: EPF/Provident fund
        insurance: Insurance deductions
        other_deductions: Other deductions
        
        --- Net Salary ---
        net_salary: Salary after deductions
        
        --- Details ---
        frequency: Payment frequency
        currency: Salary currency (USD, INR, etc.)
    """
    __tablename__ = "salary_structures"

    # Primary & Foreign Keys
    structure_id = Column(String(36), primary_key=True)
    company_id = Column(String(36), ForeignKey("companies.company_id"), nullable=False)
    employee_id = Column(String(36), ForeignKey("employees.employee_id", ondelete="CASCADE"), nullable=False)
    
    # Effective Dates
    effective_from = Column(Date, nullable=False)
    effective_to = Column(Date, nullable=True)
    
    # Primary Compensation
    ctc = Column(DECIMAL(15, 2), nullable=False)
    basic_salary = Column(DECIMAL(15, 2), nullable=False)
    
    # Allowances
    hra = Column(DECIMAL(15, 2), nullable=True, default=0)
    conveyance = Column(DECIMAL(15, 2), nullable=True, default=0)
    medical_allowance = Column(DECIMAL(15, 2), nullable=True, default=0)
    other_allowances = Column(DECIMAL(15, 2), nullable=True, default=0)
    
    # Total Before Deductions
    gross_salary = Column(DECIMAL(15, 2), nullable=False)
    
    # Deductions
    professional_tax = Column(DECIMAL(15, 2), nullable=True, default=0)
    provident_fund = Column(DECIMAL(15, 2), nullable=True, default=0)
    insurance = Column(DECIMAL(15, 2), nullable=True, default=0)
    other_deductions = Column(DECIMAL(15, 2), nullable=True, default=0)
    
    # Net Salary
    net_salary = Column(DECIMAL(15, 2), nullable=False)
    
    # Configuration
    frequency = Column(Enum(SalaryFrequency), nullable=False, default=SalaryFrequency.MONTHLY)
    currency = Column(String(3), nullable=False, default='USD')
    
    # Additional Details
    notes = Column(Text, nullable=True)
    additional_details = Column(JSON, nullable=True)
    
    # Audit Fields (inherited from BaseModel)
    created_by = Column(String(36), nullable=True)
    updated_by = Column(String(36), nullable=True)
    
    # Relationships
    employee = relationship("Employee", foreign_keys=[employee_id])
    company = relationship("Company", foreign_keys=[company_id])
    
    # Indexes
    __table_args__ = (
        Index('idx_salary_structure_employee', 'employee_id'),
        Index('idx_salary_structure_company_active', 'company_id', 'effective_to'),
    )