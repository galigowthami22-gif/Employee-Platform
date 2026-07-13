"""
Company Model
Represents a company/organization/tenant in the multi-tenant system.
All other entities are scoped to a company via company_id.
"""

from datetime import datetime
from sqlalchemy import Column, String, Text, Boolean, DateTime, Enum, Integer, DECIMAL, JSON, Index, ForeignKey
from sqlalchemy.orm import relationship
from core.base_model import BaseModel
import enum


class CompanyStatus(str, enum.Enum):
    """Company status enumeration."""
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"
    ARCHIVED = "archived"


class CompanyPlan(str, enum.Enum):
    """Company subscription plan types."""
    STARTER = "starter"
    PROFESSIONAL = "professional"
    ENTERPRISE = "enterprise"
    CUSTOM = "custom"


class Company(BaseModel):
    """
    Company model representing a tenant/organization in the system.
    
    Attributes:
        company_id: Primary key (UUID)
        name: Company legal name (required)
        short_name: Short/trading name
        description: Company description
        legal_entity: Legal entity type (Pvt Ltd, Ltd, LLC, etc.)
        registration_number: Company registration number
        tax_id: Tax identification number (e.g., GST, VAT, TIN)
        fiscal_year_start: Fiscal year start month (1-12)
        status: Company status (active, inactive, suspended, archived)
        plan: Subscription plan tier
        industry: Industry classification
        website: Company website URL
        phone: Primary contact phone
        email: Primary contact email
        logo_url: Company logo URL
        founded_date: Company founding date
        employee_count: Approximate employee count
        currency: Default currency code (USD, EUR, INR, etc.)
        timezone: Default timezone (e.g., UTC, IST, EST)
        language: Default language code (en, es, fr, etc.)
        country: Country code
        state: State/Province
        city: City
        address: Street address
        postal_code: ZIP/Postal code
        metadata: Additional JSON metadata
        created_at: Record creation timestamp
        updated_at: Last update timestamp
        created_by: User ID who created the company
        updated_by: User ID who last updated the company
    """
    __tablename__ = "companies"

    # Basic Information
    company_id = Column(String(36), primary_key=True)
    name = Column(String(255), nullable=False, unique=True, index=True)
    short_name = Column(String(50), nullable=True, index=True)
    description = Column(Text, nullable=True)
    
    # Legal Information
    legal_entity = Column(String(100), nullable=True)
    registration_number = Column(String(100), nullable=True, unique=True)
    tax_id = Column(String(50), nullable=True, unique=True)
    
    # Operational Settings
    fiscal_year_start = Column(Integer, default=1, nullable=False)  # 1-12 (January-December)
    status = Column(Enum(CompanyStatus), default=CompanyStatus.ACTIVE, nullable=False, index=True)
    plan = Column(Enum(CompanyPlan), default=CompanyPlan.STARTER, nullable=False)
    
    # Classification
    industry = Column(String(100), nullable=True, index=True)
    
    # Contact Information
    website = Column(String(255), nullable=True)
    phone = Column(String(20), nullable=True)
    email = Column(String(255), nullable=True)
    
    # Branding
    logo_url = Column(String(500), nullable=True)
    
    # Timeline
    founded_date = Column(DateTime, nullable=True)
    employee_count = Column(Integer, nullable=True)
    
    # Localization
    currency = Column(String(3), default="USD", nullable=False)  # ISO 4217 code
    timezone = Column(String(50), default="UTC", nullable=False)
    language = Column(String(10), default="en", nullable=False)
    
    # Location
    country = Column(String(100), nullable=True, index=True)
    state = Column(String(100), nullable=True)
    city = Column(String(100), nullable=True)
    address = Column(Text, nullable=True)
    postal_code = Column(String(20), nullable=True)
    
    # Additional Data
    attributes = Column(JSON, nullable=True)
    
    # Audit Fields
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    created_by = Column(String(36), nullable=True, index=True)
    updated_by = Column(String(36), nullable=True)
    
    # Relationships
    settings = relationship("CompanySettings", back_populates="company", uselist=False, cascade="all, delete-orphan")
    branches = relationship("Branch", back_populates="company", cascade="all, delete-orphan")
    departments = relationship("Department", back_populates="company", cascade="all, delete-orphan")
    teams = relationship("Team", back_populates="company", cascade="all, delete-orphan")
    cost_centers = relationship("CostCenter", back_populates="company", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Company(company_id={self.company_id}, name={self.name}, status={self.status})>"


class CompanySettings(BaseModel):
    """
    Company Settings model for storing configuration and preferences.
    
    Attributes:
        setting_id: Primary key (UUID)
        company_id: Foreign key to Company
        attendance_policy: Attendance policy JSON
        leave_policy: Leave policy JSON
        payroll_frequency: Payroll frequency (monthly, bi-weekly, weekly)
        salary_structure: Default salary structure
        max_employees: Maximum employees allowed under current plan
        max_departments: Maximum departments allowed
        max_projects: Maximum projects allowed
        max_users: Maximum concurrent users
        enable_mfa: Enable MFA requirement
        enable_audit_logs: Enable audit logging
        enable_two_factor: Enable two-factor authentication
        max_failed_login_attempts: Max failed login attempts before lockout
        session_timeout_minutes: Session timeout in minutes
        password_policy: Password policy JSON
        api_rate_limit: API rate limit per hour
        allow_bulk_operations: Allow bulk operations
        allow_api_access: Allow API access
        max_file_upload_size_mb: Max file upload size in MB
        backup_frequency: Backup frequency (daily, weekly, monthly)
        retention_days: Data retention in days
        created_at: Record creation timestamp
        updated_at: Last update timestamp
    """
    __tablename__ = "company_settings"

    setting_id = Column(String(36), primary_key=True)
    company_id = Column(String(36), ForeignKey("companies.company_id"), nullable=False, index=True, unique=True)
    
    # Policies
    attendance_policy = Column(JSON, nullable=True)
    leave_policy = Column(JSON, nullable=True)
    payroll_frequency = Column(String(50), default="monthly")
    salary_structure = Column(String(100), nullable=True)
    
    # Limits
    max_employees = Column(Integer, default=100)
    max_departments = Column(Integer, default=20)
    max_projects = Column(Integer, default=50)
    max_users = Column(Integer, default=50)
    
    # Security Settings
    enable_mfa = Column(Boolean, default=False)
    enable_audit_logs = Column(Boolean, default=True)
    enable_two_factor = Column(Boolean, default=False)
    max_failed_login_attempts = Column(Integer, default=5)
    session_timeout_minutes = Column(Integer, default=30)
    password_policy = Column(JSON, nullable=True)
    
    # API & Operations
    api_rate_limit = Column(Integer, default=1000)  # per hour
    allow_bulk_operations = Column(Boolean, default=True)
    allow_api_access = Column(Boolean, default=True)
    
    # File Management
    max_file_upload_size_mb = Column(Integer, default=100)
    
    # Backup & Retention
    backup_frequency = Column(String(50), default="daily")
    retention_days = Column(Integer, default=365)
    
    # Audit Fields
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Foreign Key
    __table_args__ = (
        Index('idx_company_settings_company_id', 'company_id'),
    )
    
    # Relationship
    company = relationship("Company", back_populates="settings")
    
    def __repr__(self):
        return f"<CompanySettings(setting_id={self.setting_id}, company_id={self.company_id})>"
