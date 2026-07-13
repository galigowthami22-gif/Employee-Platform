"""
Employee Model (HRMS - Phase 12)
Comprehensive employee management entity with all HR-related fields.
"""

from datetime import datetime
from sqlalchemy import Column, String, Text, DateTime, Enum, ForeignKey, Boolean, Date, DECIMAL, Integer, JSON, Index
from sqlalchemy.orm import relationship
from core.base_model import BaseModel
import enum


class EmploymentStatus(str, enum.Enum):
    """Employment status enumeration."""
    ACTIVE = "active"
    INACTIVE = "inactive"
    ON_LEAVE = "on_leave"
    SUSPENDED = "suspended"
    TERMINATED = "terminated"


class EmploymentType(str, enum.Enum):
    """Employment type enumeration."""
    FULL_TIME = "full_time"
    PART_TIME = "part_time"
    CONTRACT = "contract"
    TEMPORARY = "temporary"
    INTERN = "intern"
    CONSULTANT = "consultant"


class Gender(str, enum.Enum):
    """Gender enumeration."""
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"
    PREFER_NOT_TO_SAY = "prefer_not_to_say"


class MaritalStatus(str, enum.Enum):
    """Marital status enumeration."""
    SINGLE = "single"
    MARRIED = "married"
    DIVORCED = "divorced"
    WIDOWED = "widowed"
    PREFER_NOT_TO_SAY = "prefer_not_to_say"


class Designation(BaseModel):
    """Designation master for employees."""
    __tablename__ = "designations"
    __table_args__ = {'extend_existing': True}

    designation_id = Column(String(36), primary_key=True)
    company_id = Column(String(36), ForeignKey("companies.company_id"), nullable=False, index=True)
    code = Column(String(50), nullable=False, unique=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)
    level = Column(Integer, nullable=True, default=1)
    is_active = Column(Boolean, default=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    created_by = Column(String(36), nullable=True)
    updated_by = Column(String(36), nullable=True)

    company = relationship("Company")

    __table_args__ = (
        Index('idx_designation_company_active', 'company_id', 'is_active'),
        Index('idx_designation_company_level', 'company_id', 'level'),
    )

    def __repr__(self):
        return f"<Designation(designation_id={self.designation_id}, code={self.code}, name={self.name})>"


class Employee(BaseModel):
    """
    Employee model representing an employee in the company.
    Central HRMS entity with comprehensive HR data.
    
    Attributes:
        employee_id: Primary key (UUID)
        company_id: Foreign key to Company (for multi-tenancy)
        user_id: Reference to user account (for authentication)
        department_id: Foreign key to Department
        designation_id: Foreign key to Designation
        manager_id: Manager's employee ID (self-reference)
        cost_center_id: Cost center for accounting
        
        --- Basic Information ---
        first_name: Employee first name
        middle_name: Employee middle name
        last_name: Employee last name
        email: Work email (unique per company)
        personal_email: Personal email
        phone: Work phone
        mobile: Mobile number
        
        --- Identification ---
        employee_code: Unique employee code/badge number
        id_type: ID document type (Passport, SSN, Aadhar, etc.)
        id_number: ID document number
        tax_id: Tax identification number (SSN, PAN, etc.)
        
        --- Personal Information ---
        date_of_birth: Date of birth
        gender: Gender
        marital_status: Marital status
        nationality: Nationality
        blood_group: Blood group
        
        --- Employment Details ---
        employment_type: Type of employment (full-time, part-time, contract, etc.)
        employment_status: Current employment status (active, inactive, terminated)
        date_of_joining: Joining date
        date_of_confirmation: Confirmation date (probation end)
        date_of_separation: Separation/termination date
        
        --- Address Information ---
        current_address: Current residential address
        permanent_address: Permanent address
        city: City
        state: State/Province
        country: Country
        postal_code: Postal code
        
        --- Employment Terms ---
        ctc: Cost To Company (annual)
        salary: Current salary
        salary_frequency: Salary payment frequency (monthly, bi-weekly, etc.)
        currency: Salary currency (ISO 4217)
        
        --- Additional Information ---
        reporting_manager_id: Reporting manager (employee_id)
        emergency_contact: Emergency contact name
        emergency_phone: Emergency contact phone
        work_location: Primary work location
        
        --- Status & Tracking ---
        is_active: Whether employee is actively working
        is_verified: Email verification status
        probation_end_date: Probation period end date
        
        --- File References ---
        profile_photo_url: Profile photo URL
        resume_url: Resume file URL
        
        --- Additional Data ---
        metadata: Additional JSON metadata
        notes: Internal notes
        
        --- Audit Fields ---
        created_at: Record creation timestamp
        updated_at: Last update timestamp
        created_by: User ID who created the record
        updated_by: User ID who last updated the record
    """
    __tablename__ = "employees"

    # Primary Key & Foreign Keys
    employee_id = Column(String(36), primary_key=True)
    company_id = Column(String(36), ForeignKey("companies.company_id"), nullable=False, index=True)
    user_id = Column(String(36), nullable=True, unique=True, index=True)
    department_id = Column(String(36), ForeignKey("departments.department_id"), nullable=True, index=True)
    designation_id = Column(String(36), nullable=True, index=True)
    manager_id = Column(String(36), ForeignKey("employees.employee_id"), nullable=True, index=True)
    cost_center_id = Column(String(36), ForeignKey("cost_centers.cost_center_id"), nullable=True)

    # Basic Information
    employee_code = Column(String(50), nullable=False, unique=True, index=True)
    first_name = Column(String(100), nullable=False, index=True)
    middle_name = Column(String(100), nullable=True)
    last_name = Column(String(100), nullable=False, index=True)
    
    # Contact Information
    email = Column(String(255), nullable=False, index=True)
    personal_email = Column(String(255), nullable=True)
    phone = Column(String(20), nullable=True)
    mobile = Column(String(20), nullable=True)
    
    # Identification
    id_type = Column(String(50), nullable=True)
    id_number = Column(String(100), nullable=True, unique=True)
    tax_id = Column(String(50), nullable=True, unique=True)
    
    # Personal Information
    date_of_birth = Column(Date, nullable=True)
    gender = Column(Enum(Gender), nullable=True)
    marital_status = Column(Enum(MaritalStatus), nullable=True)
    nationality = Column(String(100), nullable=True)
    blood_group = Column(String(10), nullable=True)
    
    # Employment Details
    employment_type = Column(Enum(EmploymentType), default=EmploymentType.FULL_TIME, nullable=False)
    employment_status = Column(Enum(EmploymentStatus), default=EmploymentStatus.ACTIVE, nullable=False, index=True)
    date_of_joining = Column(Date, nullable=False, index=True)
    date_of_confirmation = Column(Date, nullable=True)
    date_of_separation = Column(Date, nullable=True)
    
    # Address Information
    current_address = Column(Text, nullable=True)
    permanent_address = Column(Text, nullable=True)
    city = Column(String(100), nullable=True)
    state = Column(String(100), nullable=True)
    country = Column(String(100), nullable=True)
    postal_code = Column(String(20), nullable=True)
    
    # Employment Terms
    ctc = Column(DECIMAL(15, 2), nullable=True)
    salary = Column(DECIMAL(15, 2), nullable=True)
    salary_frequency = Column(String(50), default="monthly")
    currency = Column(String(3), default="USD")
    
    # Additional Information
    reporting_manager_id = Column(String(36), nullable=True, index=True)
    emergency_contact = Column(String(255), nullable=True)
    emergency_phone = Column(String(20), nullable=True)
    work_location = Column(String(255), nullable=True)
    
    # Status & Tracking
    is_active = Column(Boolean, default=True, index=True)
    is_verified = Column(Boolean, default=False)
    probation_end_date = Column(Date, nullable=True)
    
    # File References
    profile_photo_url = Column(String(500), nullable=True)
    resume_url = Column(String(500), nullable=True)
    
    # Additional Data
    attributes = Column(JSON, nullable=True)
    notes = Column(Text, nullable=True)
    
    # Audit Fields
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    created_by = Column(String(36), nullable=True)
    updated_by = Column(String(36), nullable=True)
    
    # Relationships
    company = relationship("Company")
    department = relationship("Department")
    manager = relationship("Employee", remote_side=[employee_id], backref="subordinates")
    cost_center = relationship("CostCenter")
    
    # Composite Indexes
    __table_args__ = (
        Index('idx_employee_company_status', 'company_id', 'employment_status'),
        Index('idx_employee_company_department', 'company_id', 'department_id'),
        Index('idx_employee_company_active', 'company_id', 'is_active'),
        Index('idx_employee_department_status', 'department_id', 'employment_status'),
        Index('idx_employee_code', 'employee_code'),
        Index('idx_employee_joining_date', 'date_of_joining'),
        Index('idx_employee_manager', 'manager_id'),
    )
    
    def __repr__(self):
        return f"<Employee(employee_id={self.employee_id}, code={self.employee_code}, name={self.first_name} {self.last_name})>"